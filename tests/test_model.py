import unittest
from tasktracker.model import Task


class ModelTests(unittest.TestCase):
    def test_new_task_and_roundtrip(self):
        first = Task.create("Read Git")
        self.assertFalse(first.completed)
        self.assertNotEqual(first.id, Task.create("Read Git").id)
        self.assertEqual(Task.from_record(first.to_record()), first)

    def test_completion_preserves_original_and_is_idempotent(self):
        task = Task.create("Practice")
        done = task.complete()
        self.assertFalse(task.completed)
        self.assertTrue(done.completed)
        self.assertEqual(done.complete(), done)
        self.assertEqual(done.id, task.id)

    def test_invalid_records(self):
        valid = Task.create("Task").to_record()
        for record in (None, [], {}, {**valid, "extra": 1}, {**valid, "completed": "false"}):
            with self.subTest(record=record), self.assertRaises(ValueError):
                Task.from_record(record)
