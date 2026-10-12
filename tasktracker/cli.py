"""Command-line boundary for local course tasks."""
import argparse
import json
import sys
from tasktracker.service import TaskNotFoundError, TaskService
from tasktracker.storage import JsonStore, StorageError


def parser():
    result = argparse.ArgumentParser(description="Track local course tasks")
    result.add_argument("--data", default="data/tasks.json", help="JSON task file")
    commands = result.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="Add one task")
    add.add_argument("title")
    listing = commands.add_parser("list", help="List tasks")
    listing.add_argument("--status", choices=("all", "open", "done"), default="all")
    listing.add_argument("--json", action="store_true", help="Print machine-readable records")
    complete = commands.add_parser("complete", help="Mark a task complete")
    complete.add_argument("id")
    return result


def main(argv=None):
    arguments = parser().parse_args(argv)
    service = TaskService(JsonStore(arguments.data))
    try:
        if arguments.command == "add":
            task = service.add(arguments.title)
            print(f"Added {task.id}: {task.title}")
        elif arguments.command == "complete":
            task = service.complete(arguments.id)
            print(f"Completed {task.id}: {task.title}")
        else:
            tasks = service.list(arguments.status)
            if arguments.json:
                print(json.dumps([task.to_record() for task in tasks], ensure_ascii=False))
            elif not tasks:
                print("No tasks found.")
            else:
                for task in tasks:
                    state = "done" if task.completed else "open"
                    print(f"{task.id} [{state}] {task.title}")
    except (ValueError, StorageError, TaskNotFoundError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0
