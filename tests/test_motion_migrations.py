import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from motiontracker.migration import apply_script, migrate_database, script_for

ID = "12345678-1234-4234-8234-123456789abc"


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "projects.sqlite3"

    def create_version_one(self):
        with closing(sqlite3.connect(self.path)) as connection:
            apply_script(connection, script_for(1))
            connection.execute("PRAGMA user_version=1")
            connection.execute("INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?)",
                               (ID, "Brand intro", "Demo Studio", "15 seconds", "2026-11-01", "review"))
            connection.commit()

    def read_schema(self, path=None):
        with closing(sqlite3.connect(path or self.path)) as connection:
            version = connection.execute("PRAGMA user_version").fetchone()[0]
            columns = [row[1] for row in connection.execute("PRAGMA table_info(projects)")]
            return version, columns

    def test_new_database_dry_run_has_no_filesystem_side_effect(self):
        nested = self.path.parent / "not-created" / "projects.db"
        plan = migrate_database(nested, dry_run=True)
        self.assertEqual(plan["from_version"], 0)
        self.assertEqual(len(plan["steps"]), 2)
        self.assertFalse(nested.parent.exists())

    def test_new_database_and_repeat_upgrade(self):
        first = migrate_database(self.path)
        self.assertEqual(self.read_schema()[0], 2)
        self.assertIsNone(first["backup"])
        second = migrate_database(self.path)
        self.assertEqual(second["steps"], [])
        self.assertEqual(list(self.path.parent.glob("*.bak")), [])

    def test_version_one_upgrades_preserving_records_and_original_backup(self):
        self.create_version_one()
        preview = migrate_database(self.path, dry_run=True)
        self.assertEqual(preview["steps"], ["002_revisions_and_formats.sql"])
        self.assertEqual(self.read_schema()[0], 1)
        self.assertEqual(list(self.path.parent.glob("*.bak")), [])
        plan = migrate_database(self.path)
        self.assertEqual(self.read_schema()[0], 2)
        self.assertEqual(self.read_schema(plan["backup"])[0], 1)
        with closing(sqlite3.connect(self.path)) as connection:
            row = connection.execute("SELECT id, client, status, revision_limit, revision_count, delivery_formats FROM projects").fetchone()
        self.assertEqual(row, (ID, "Demo Studio", "review", 2, 0, '["mp4"]'))
        with closing(sqlite3.connect(plan["backup"])) as connection:
            self.assertEqual(connection.execute("SELECT id FROM projects").fetchone()[0], ID)

    def test_failed_upgrade_rolls_back_ddl_data_and_version(self):
        self.create_version_one()
        bad_script = "ALTER TABLE projects ADD COLUMN temporary_value TEXT;\nSELECT * FROM missing_table;\n"
        with patch("motiontracker.migration.script_for", return_value=bad_script):
            with self.assertRaises(sqlite3.Error):
                migrate_database(self.path)
        version, columns = self.read_schema()
        self.assertEqual(version, 1)
        self.assertNotIn("temporary_value", columns)
        self.assertEqual(len(list(self.path.parent.glob("*.bak"))), 1)
        with closing(sqlite3.connect(self.path)) as connection:
            self.assertEqual(connection.execute("SELECT title FROM projects").fetchone()[0], "Brand intro")

    def test_future_or_unversioned_database_is_not_changed(self):
        for version in (0, 99):
            target = self.path.with_name(f"other-{version}.sqlite3")
            with closing(sqlite3.connect(target)) as connection:
                connection.execute("CREATE TABLE unrelated (value TEXT)")
                connection.execute(f"PRAGMA user_version={version}")
                connection.commit()
            original = target.read_bytes()
            with self.assertRaises(ValueError):
                migrate_database(target)
            self.assertEqual(target.read_bytes(), original)
