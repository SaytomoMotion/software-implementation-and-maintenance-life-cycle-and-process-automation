import unittest
from tasktracker.service import TaskNotFoundError, TaskService


class MemoryStore:
    def __init__(self):
        self.tasks = []

    def load(self):
        return list(self.tasks)

    def save(self, tasks):
        self.tasks = list(tasks)


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = TaskService(MemoryStore())

    def test_add_list_and_filter(self):
        first = self.service.add("Study")
        second = self.service.add("Practice")
        self.service.complete(first.id)
        self.assertEqual(self.service.list("open"), [second])
        self.assertEqual(self.service.list("done")[0].id, first.id)
        self.assertEqual(len(self.service.list()), 2)

    def test_completion_is_idempotent(self):
        task = self.service.add("Read")
        first = self.service.complete(task.id)
        self.assertEqual(self.service.complete(task.id), first)

    def test_missing_id(self):
        with self.assertRaises(TaskNotFoundError):
            self.service.complete("12345678-1234-4234-8234-123456789abc")

    def test_invalid_input_does_not_create_tasks(self):
        with self.assertRaises(ValueError):
            self.service.add(" ")
        self.assertEqual(self.service.list(), [])
        with self.assertRaises(ValueError):
            self.service.list("unknown")
