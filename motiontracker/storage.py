"""SQLite persistence with parameterized queries and atomic revision updates."""
import json
import sqlite3
from pathlib import Path

from motiontracker.migration import migrate_database
from motiontracker.model import Project

FIELDS = ("id", "title", "client", "brief", "deadline", "status", "revision_limit",
          "revision_count", "delivery_formats")


class ProjectNotFoundError(ValueError):
    pass


def project_from_row(row):
    record = dict(row)
    try:
        record["delivery_formats"] = json.loads(record["delivery_formats"])
        return Project(**record)
    except (ValueError, TypeError) as error:
        raise ValueError("Stored project data is invalid; inspect a backup") from error


def values(project):
    record = project.to_record()
    record["delivery_formats"] = json.dumps(record["delivery_formats"])
    return tuple(record[name] for name in FIELDS)


class ProjectStore:
    def __init__(self, path):
        self.path = Path(path)
        self.migration = migrate_database(path)
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row

    def __enter__(self):
        return self

    def __exit__(self, *arguments):
        self.connection.close()

    def all(self):
        rows = self.connection.execute("SELECT * FROM projects ORDER BY deadline IS NULL, deadline, title, id")
        return [project_from_row(row) for row in rows]

    def get(self, project_id):
        row = self.connection.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        if row is None:
            raise ProjectNotFoundError("Project ID was not found")
        return project_from_row(row)

    def insert(self, project):
        with self.connection:
            self.connection.execute("INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", values(project))
        return project

    def update(self, project):
        with self.connection:
            result = self.connection.execute(
                "UPDATE projects SET title=?, client=?, brief=?, deadline=?, status=?, revision_limit=?, "
                "revision_count=?, delivery_formats=? WHERE id=?", values(project)[1:] + (project.id,))
            if result.rowcount != 1:
                raise ProjectNotFoundError("Project ID was not found")
        return project

    def revise(self, project_id, allow_extra=False):
        with self.connection:
            result = self.connection.execute(
                "UPDATE projects SET revision_count=revision_count+1, status='review' "
                "WHERE id=? AND revision_count < 1000000 AND (? OR revision_count < revision_limit)",
                (project_id, allow_extra))
            if result.rowcount != 1:
                self.get(project_id)
                raise ValueError("Revision limit reached; use --allow-extra to record an agreed extra round")
            project = self.get(project_id)
        return project

    def import_projects(self, projects):
        inserted = 0
        with self.connection:
            for project in projects:
                result = self.connection.execute(
                    "INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(id) DO NOTHING",
                    values(project))
                inserted += result.rowcount
        return {"imported": inserted, "skipped": len(projects) - inserted}
