"""Project use cases and read-only import of the old task JSON format."""
import json
from dataclasses import replace
from pathlib import Path

from motiontracker.model import Project, STATUSES, validate_project_id
from tasktracker.model import Task


def read_legacy_tasks(path):
    try:
        document = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(document, dict) or set(document) != {"schema_version", "tasks"}:
            raise ValueError("Invalid document")
        if type(document["schema_version"]) is not int or document["schema_version"] != 1:
            raise ValueError("Unsupported version")
        if not isinstance(document["tasks"], list):
            raise ValueError("Invalid task list")
        tasks = [Task.from_record(record) for record in document["tasks"]]
        if len({task.id for task in tasks}) != len(tasks):
            raise ValueError("Duplicate task IDs")
        return [Project(id=task.id, title=task.title, client="Unassigned",
                        brief="Imported task; add the client and project brief.",
                        status="delivered" if task.completed else "briefing") for task in tasks]
    except (ValueError, TypeError, UnicodeError) as error:
        raise ValueError("Invalid legacy task file; no tasks were imported") from error


class ProjectService:
    def __init__(self, store):
        self.store = store

    def add(self, title, **fields):
        return self.store.insert(Project.create(title, **fields))

    def get(self, project_id):
        validate_project_id(project_id)
        return self.store.get(project_id)

    def edit(self, project_id, **changes):
        if not changes:
            raise ValueError("Provide at least one project field to update")
        return self.store.update(replace(self.get(project_id), **changes))

    def list(self, status=None, client=None, overdue=False, today=None):
        if status is not None and status not in STATUSES:
            raise ValueError("Unsupported project status")
        return [project for project in self.store.all()
                if (status is None or project.status == status)
                and (client is None or project.client.casefold() == client.casefold())
                and (not overdue or project.is_overdue(today))]

    def revise(self, project_id, allow_extra=False):
        validate_project_id(project_id)
        return self.store.revise(project_id, allow_extra)

    def stats(self, today=None):
        projects = self.store.all()
        return {"total": len(projects), "by_status": {
            status: sum(project.status == status for project in projects) for status in STATUSES},
            "overdue": sum(project.is_overdue(today) for project in projects),
            "over_revision_budget": sum(project.revision_count > project.revision_limit for project in projects)}
