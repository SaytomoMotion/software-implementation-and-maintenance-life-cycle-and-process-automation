import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tasktracker.model import Task
from tasktracker.storage import JsonStore, StorageError


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "nested" / "tasks.json"
        self.store = JsonStore(self.path)

    def test_missing_and_roundtrip(self):
        self.assertEqual(self.store.load(), [])
        tasks = [Task.create("Read ā"), Task.create("Test").complete()]
        self.store.save(tasks)
        self.assertEqual(self.store.load(), tasks)

    def test_corruption_preserved(self):
        self.path.parent.mkdir()
        self.path.write_text("broken", encoding="utf-8")
        with self.assertRaises(StorageError):
            self.store.load()
        self.assertEqual(self.path.read_text(), "broken")

    def test_unsupported_schema_and_duplicate_ids(self):
        self.path.parent.mkdir()
        task = Task.create("Read").to_record()
        for document in ({"schema_version": 2, "tasks": []},
                         {"schema_version": True, "tasks": []},
                         {"schema_version": 1, "tasks": [task, task]}):
            self.path.write_text(json.dumps(document), encoding="utf-8")
            with self.assertRaises(StorageError):
                self.store.load()

    def test_replace_failure_keeps_previous_data(self):
        first = [Task.create("Original")]
        self.store.save(first)
        with patch("tasktracker.storage.os.replace", side_effect=OSError("disk failure")):
            with self.assertRaises(StorageError):
                self.store.save([Task.create("Replacement")])
        self.assertEqual(self.store.load(), first)
        self.assertEqual(list(self.path.parent.glob(".tasks-*.tmp")), [])

    def test_invalid_encoding_is_reported(self):
        self.path.parent.mkdir()
        self.path.write_bytes(b"\xff\xfe")
        with self.assertRaises(StorageError):
            self.store.load()
