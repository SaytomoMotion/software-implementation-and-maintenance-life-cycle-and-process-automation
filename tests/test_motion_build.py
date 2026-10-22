import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.build import build


class BuildTests(unittest.TestCase):
    def test_build_is_reproducible_and_contains_schema_scripts(self):
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.pyz"
            second = Path(directory) / "second.pyz"
            digest = build(first, revision="example-commit")["sha256"]
            self.assertEqual(build(second, revision="example-commit")["sha256"], digest)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first) as archive:
                self.assertIn("motiontracker/migrations/002_revisions_and_formats.sql", archive.namelist())
                self.assertEqual(json.loads(archive.read("build-info.json"))["source_revision"], "example-commit")
                self.assertFalse(any(name.startswith(("data/", "work/", ".git/")) for name in archive.namelist()))

    def test_packaged_app_can_create_migrate_and_read_its_own_database(self):
        with tempfile.TemporaryDirectory() as directory:
            app = Path(directory) / "motiondesk.pyz"
            database = Path(directory) / "projects.sqlite3"
            build(app)
            def run(*arguments):
                return subprocess.run([sys.executable, str(app), "--db", str(database), *arguments],
                                      cwd=directory, capture_output=True, text=True, check=False)
            result = run("add", "Logo", "--client", "Demo Studio")
            self.assertEqual(result.returncode, 0, result.stderr)
            listing = run("list", "--json")
            self.assertEqual(listing.returncode, 0, listing.stderr)
            self.assertEqual(json.loads(listing.stdout)[0]["client"], "Demo Studio")
            self.assertEqual(json.loads(run("migrate", "--dry-run").stdout)["from_version"], 2)
