import sqlite3
import tempfile
import unittest
from datetime import date
from pathlib import Path

from motiontracker.model import Project
from motiontracker.service import ProjectService
from motiontracker.storage import ProjectNotFoundError, ProjectStore


class ProjectStorageTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "projects.sqlite3"

    def test_persistence_edits_client_filter_and_deadline_order(self):
        with ProjectStore(self.path) as store:
            service = ProjectService(store)
            later = service.add("Later", client="Studio A", deadline="2026-11-02")
            earlier = service.add("Earlier", client="Studio A", deadline="2026-11-01")
            service.add("Undated", client="Studio B")
            self.assertEqual([p.id for p in service.list(client="studio a")], [earlier.id, later.id])
            service.edit(earlier.id, brief="Approved brief", delivery_formats=("mov", "gif"))
        with ProjectStore(self.path) as store:
            self.assertEqual(store.get(earlier.id).brief, "Approved brief")
            self.assertEqual(store.get(earlier.id).delivery_formats, ("mov", "gif"))
            self.assertIsNone(store.all()[-1].deadline)

    def test_revision_budget_requires_explicit_override(self):
        with ProjectStore(self.path) as store:
            service = ProjectService(store)
            project = service.add("Logo", client="Studio", revision_limit=1)
            self.assertEqual(service.revise(project.id).revision_count, 1)
            with self.assertRaisesRegex(ValueError, "Revision limit reached"):
                service.revise(project.id)
            self.assertEqual(service.get(project.id).revision_count, 1)
            extra = service.revise(project.id, allow_extra=True)
            self.assertEqual(extra.revision_count, 2)
            self.assertEqual(extra.status, "review")
            self.assertEqual(service.stats()["over_revision_budget"], 1)

    def test_statistics_exclude_delivered_from_overdue(self):
        with ProjectStore(self.path) as store:
            service = ProjectService(store)
            service.add("Late", client="Studio", deadline="2026-10-20")
            done = service.add("Delivered", client="Studio", deadline="2026-10-20")
            service.edit(done.id, status="delivered")
            today = date(2026, 10, 22)
            self.assertEqual(service.stats(today)["overdue"], 1)
            self.assertEqual([p.title for p in service.list(overdue=True, today=today)], ["Late"])

    def test_missing_project_and_invalid_edit(self):
        with ProjectStore(self.path) as store:
            service = ProjectService(store)
            with self.assertRaises(ProjectNotFoundError):
                service.get("12345678-1234-4234-8234-123456789abc")
            project = service.add("Logo", client="Studio")
            with self.assertRaises(ValueError):
                service.edit(project.id, deadline="not-a-date")
            self.assertIsNone(service.get(project.id).deadline)

    def test_import_is_atomic_on_database_failure(self):
        with ProjectStore(self.path) as store:
            first = Project.create("First", client="Studio")
            second = Project.create("Rejected", client="Studio")
            store.connection.execute("CREATE TRIGGER reject_project BEFORE INSERT ON projects "
                                     "WHEN NEW.title = 'Rejected' BEGIN SELECT RAISE(ABORT, 'Rejected'); END")
            with self.assertRaises(sqlite3.Error):
                store.import_projects([first, second])
            self.assertEqual(store.all(), [])

    def test_two_connections_cannot_exceed_revision_budget(self):
        with ProjectStore(self.path) as first, ProjectStore(self.path) as second:
            project = first.insert(Project.create("Intro", client="Studio", revision_limit=1))
            first.revise(project.id)
            with self.assertRaises(ValueError):
                second.revise(project.id)
            self.assertEqual(second.get(project.id).revision_count, 1)
