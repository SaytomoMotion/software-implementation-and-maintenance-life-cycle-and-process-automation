import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from motiontracker.cli import main
from motiontracker.service import read_legacy_tasks

ID = "12345678-1234-4234-8234-123456789abc"


class MotionCliTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "projects.sqlite3"

    def invoke(self, *arguments):
        output, errors = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            code = main(["--db", str(self.path), *arguments])
        return code, output.getvalue(), errors.getvalue()

    def legacy_file(self, completed=False):
        source = Path(self.folder.name) / "old-tasks.json"
        source.write_text(json.dumps({"schema_version": 1, "tasks": [
            {"id": ID, "title": "Logo intro", "completed": completed}]}), encoding="utf-8")
        return source

    def test_full_client_project_lifecycle(self):
        code, _, errors = self.invoke("add", "Brand intro", "--client", "Demo Studio", "--brief",
                                      "15 seconds", "--deadline", "2026-11-15", "--revision-limit", "1",
                                      "--format", "mp4", "--format", "mov")
        self.assertEqual((code, errors), (0, ""))
        project = json.loads(self.invoke("list", "--json")[1])[0]
        self.assertEqual(project["delivery_formats"], ["mp4", "mov"])
        project_id = project["id"]
        self.assertEqual(self.invoke("status", project_id, "in_progress")[0], 0)
        self.assertEqual(self.invoke("revise", project_id)[0], 0)
        self.assertEqual(self.invoke("revise", project_id)[0], 1)
        self.assertEqual(self.invoke("revise", project_id, "--allow-extra")[0], 0)
        self.assertEqual(self.invoke("edit", project_id, "--deadline", "none", "--format", "gif")[0], 0)
        details = json.loads(self.invoke("show", project_id)[1])
        self.assertIsNone(details["deadline"])
        self.assertEqual(details["delivery_formats"], ["gif"])
        self.assertEqual(self.invoke("status", project_id, "delivered")[0], 0)
        stats = json.loads(self.invoke("stats")[1])
        self.assertEqual(stats["by_status"]["delivered"], 1)
        self.assertEqual(stats["over_revision_budget"], 1)

    def test_empty_list_and_filters(self):
        self.assertEqual(self.invoke("list"), (0, "No projects found.\n", ""))
        self.invoke("add", "Intro", "--client", "Demo Studio")
        self.assertEqual(len(json.loads(self.invoke("list", "--client", "demo studio", "--json")[1])), 1)
        self.assertEqual(json.loads(self.invoke("list", "--status", "review", "--json")[1]), [])

    def test_invalid_input_and_missing_project_are_reported(self):
        for command in (("add", " ", "--client", "Studio"),
                        ("add", "Intro", "--client", "Studio", "--deadline", "2026-02-30"),
                        ("show", "not-an-id"), ("show", ID)):
            with self.subTest(command=command):
                code, output, errors = self.invoke(*command)
                self.assertEqual(code, 1)
                self.assertEqual(output, "")
                self.assertIn("Error:", errors)
                self.assertNotIn("Traceback", errors)

    def test_migration_dry_run_does_not_create_database(self):
        code, output, _ = self.invoke("migrate", "--dry-run")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output)["to_version"], 2)
        self.assertFalse(self.path.exists())

    def test_import_dry_run_and_idempotent_import_preserve_original(self):
        source = self.legacy_file(completed=True)
        original = source.read_bytes()
        self.assertEqual(json.loads(self.invoke("import-tasks", str(source), "--dry-run")[1])["eligible"], 1)
        self.assertFalse(self.path.exists())
        first = self.invoke("import-tasks", str(source))
        self.assertEqual(first[0], 0)
        self.assertEqual(json.loads(first[1]), {"imported": 1, "skipped": 0})
        self.assertEqual(json.loads(self.invoke("import-tasks", str(source))[1]), {"imported": 0, "skipped": 1})
        project = json.loads(self.invoke("show", ID)[1])
        self.assertEqual(project["status"], "delivered")
        self.assertEqual(project["client"], "Unassigned")
        self.assertEqual(source.read_bytes(), original)

    def test_invalid_import_is_rejected_before_database_creation(self):
        source = self.legacy_file()
        document = json.loads(source.read_text())
        document["tasks"].append({"invalid": "record"})
        source.write_text(json.dumps(document), encoding="utf-8")
        code, output, errors = self.invoke("import-tasks", str(source))
        self.assertEqual(code, 1)
        self.assertEqual(output, "")
        self.assertIn("no tasks were imported", errors)
        self.assertFalse(self.path.exists())

    def test_argument_errors(self):
        for arguments in (("add", "Intro"), ("status", ID, "unknown"), ("add", "Intro", "--client", "Studio", "--format", "unknown")):
            with self.subTest(arguments=arguments), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as caught:
                    main(list(arguments))
                self.assertEqual(caught.exception.code, 2)

    def test_separate_processes_persist_project_state(self):
        def run(*arguments):
            return subprocess.run([sys.executable, "-m", "motiontracker", "--db", str(self.path),
                                   *arguments], capture_output=True, text=True, check=False)
        self.assertEqual(run("add", "Intro", "--client", "Studio").returncode, 0)
        listing = run("list", "--json")
        self.assertEqual(listing.returncode, 0)
        project_id = json.loads(listing.stdout)[0]["id"]
        self.assertEqual(run("status", project_id, "delivered").returncode, 0)
        self.assertEqual(json.loads(run("show", project_id).stdout)["status"], "delivered")


class LegacyImportValidationTests(unittest.TestCase):
    def test_reject_duplicate_ids_boolean_version_and_invalid_encoding(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "old.json"
            task = {"id": ID, "title": "Intro", "completed": False}
            for document in ({"schema_version": True, "tasks": [task]},
                             {"schema_version": 1, "tasks": [task, task]},
                             {"schema_version": 1, "tasks": "invalid"}):
                source.write_text(json.dumps(document), encoding="utf-8")
                with self.assertRaises(ValueError):
                    read_legacy_tasks(source)
            source.write_bytes(b"\xff\xfe")
            with self.assertRaises(ValueError):
                read_legacy_tasks(source)
