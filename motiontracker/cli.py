"""Command-line project management and explicit migration commands."""
import argparse
import json
import sqlite3
import sys

from motiontracker.migration import migrate_database
from motiontracker.model import FORMATS, STATUSES
from motiontracker.service import ProjectService, read_legacy_tasks
from motiontracker.storage import ProjectStore


def add_fields(command, editing=False):
    if editing:
        command.add_argument("--title")
    command.add_argument("--client", **({} if editing else {"required": True}))
    command.add_argument("--brief")
    command.add_argument("--deadline", help="YYYY-MM-DD; use 'none' to clear when editing")
    command.add_argument("--revision-limit", type=int)
    command.add_argument("--format", choices=FORMATS, action="append", dest="delivery_formats")


def parser():
    result = argparse.ArgumentParser(description="Manage motion design projects, revisions and deliveries")
    result.add_argument("--db", default="data/motion-projects.sqlite3", help="SQLite project database")
    commands = result.add_subparsers(dest="command", required=True)
    create = commands.add_parser("add", help="Create a client project")
    create.add_argument("title")
    add_fields(create)
    edit = commands.add_parser("edit", help="Update a project brief or delivery requirements")
    edit.add_argument("id")
    add_fields(edit, editing=True)
    listing = commands.add_parser("list", help="List projects in deadline order")
    listing.add_argument("--status", choices=STATUSES)
    listing.add_argument("--client")
    listing.add_argument("--overdue", action="store_true")
    listing.add_argument("--json", action="store_true")
    show = commands.add_parser("show", help="Show all project details")
    show.add_argument("id")
    status = commands.add_parser("status", help="Change project status")
    status.add_argument("id")
    status.add_argument("value", choices=STATUSES)
    revision = commands.add_parser("revise", help="Record one revision round")
    revision.add_argument("id")
    revision.add_argument("--allow-extra", action="store_true")
    commands.add_parser("stats", help="Summarize workload and overdue projects")
    migration = commands.add_parser("migrate", help="Apply database schema migrations")
    migration.add_argument("--dry-run", action="store_true")
    importing = commands.add_parser("import-tasks", help="Import old version-1 task JSON without editing it")
    importing.add_argument("path")
    importing.add_argument("--dry-run", action="store_true")
    return result


def main(argv=None):
    arguments = parser().parse_args(argv)
    try:
        if arguments.command == "migrate":
            print(json.dumps(migrate_database(arguments.db, arguments.dry_run), indent=2))
            return 0
        imported_projects = None
        if arguments.command == "import-tasks":
            # Validate the full input before opening or creating the destination database.
            imported_projects = read_legacy_tasks(arguments.path)
            if arguments.dry_run:
                print(json.dumps({"eligible": len(imported_projects), "dry_run": True,
                                  "database_changed": False}, indent=2))
                return 0
        with ProjectStore(arguments.db) as store:
            if store.migration["backup"]:
                print("Database upgraded; backup: " + store.migration["backup"], file=sys.stderr)
            service = ProjectService(store)
            if arguments.command == "import-tasks":
                print(json.dumps(store.import_projects(imported_projects)))
            elif arguments.command in {"add", "edit"}:
                fields = {name: getattr(arguments, name) for name in
                          ("client", "brief", "deadline", "revision_limit", "delivery_formats")
                          if getattr(arguments, name) is not None}
                if fields.get("deadline") == "none":
                    fields["deadline"] = None
                if arguments.command == "add":
                    project = service.add(arguments.title, **fields)
                    print(f"Added {project.id}: {project.title}")
                else:
                    if arguments.title is not None:
                        fields["title"] = arguments.title
                    project = service.edit(arguments.id, **fields)
                    print(f"Updated {project.id}: {project.title}")
            elif arguments.command == "list":
                projects = service.list(arguments.status, arguments.client, arguments.overdue)
                if arguments.json:
                    print(json.dumps([project.to_record() for project in projects], ensure_ascii=False))
                elif not projects:
                    print("No projects found.")
                else:
                    for project in projects:
                        print(f"{project.id} | {project.status} | {project.client} | {project.title} | "
                              f"due {project.deadline or '-'} | revisions {project.revision_count}/{project.revision_limit}")
            elif arguments.command == "show":
                print(json.dumps(service.get(arguments.id).to_record(), ensure_ascii=False, indent=2))
            elif arguments.command == "status":
                project = service.edit(arguments.id, status=arguments.value)
                print(f"{project.title}: {project.status}")
            elif arguments.command == "revise":
                project = service.revise(arguments.id, arguments.allow_extra)
                print(f"{project.title}: revision {project.revision_count}/{project.revision_limit}")
            else:
                print(json.dumps(service.stats(), indent=2))
    except sqlite3.Error:
        print("Error: Cannot read or update the project database; check access and schema.", file=sys.stderr)
        return 1
    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0
