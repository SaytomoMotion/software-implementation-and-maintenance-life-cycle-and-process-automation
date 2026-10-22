import unittest
from datetime import date

from motiontracker.model import Project


class ProjectModelTests(unittest.TestCase):
    def test_project_defaults_and_format_normalization(self):
        project = Project.create(" Logo intro ", client=" Studio ", delivery_formats=["mov", "mp4", "mov"])
        self.assertEqual(project.title, "Logo intro")
        self.assertEqual(project.client, "Studio")
        self.assertEqual(project.delivery_formats, ("mov", "mp4"))
        self.assertEqual(project.to_record()["delivery_formats"], ["mov", "mp4"])
        self.assertEqual(project.status, "briefing")

    def test_invalid_fields_and_calendar_dates(self):
        invalid = [dict(title=" "), dict(client=" "), dict(title="Unsafe\nTitle"),
                   dict(brief="hidden\x1bcontent"), dict(deadline="2026-02-30"),
                   dict(deadline="20261022"), dict(deadline=2026), dict(status="random"),
                   dict(revision_limit=-1), dict(revision_count=True),
                   dict(delivery_formats=[]), dict(delivery_formats=["unknown"])]
        for fields in invalid:
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                Project.create(**{"title": "Project", **fields})

    def test_brief_supports_newlines(self):
        self.assertEqual(Project.create("Intro", brief="First frame\nEnd card").brief,
                         "First frame\nEnd card")

    def test_deadline_is_overdue_only_after_due_day_and_before_delivery(self):
        due = "2026-10-22"
        self.assertFalse(Project.create("Intro", deadline=due).is_overdue(date(2026, 10, 22)))
        self.assertTrue(Project.create("Intro", deadline=due).is_overdue(date(2026, 10, 23)))
        self.assertFalse(Project.create("Intro", deadline=due, status="delivered").is_overdue(date(2026, 10, 23)))
        self.assertFalse(Project.create("Intro").is_overdue(date(2026, 10, 23)))
