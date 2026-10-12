"""Application use cases; the CLI supplies the concrete store."""
from tasktracker.model import Task
from tasktracker.validation import validate_id


class TaskNotFoundError(Exception):
    pass


class TaskService:
    def __init__(self, store):
        self.store = store

    def add(self, title):
        task = Task.create(title)
        tasks = self.store.load()
        tasks.append(task)
        self.store.save(tasks)
        return task

    def list(self, status="all"):
        if status not in {"all", "open", "done"}:
            raise ValueError("Status must be all, open or done")
        tasks = self.store.load()
        if status == "all":
            return tasks
        return [task for task in tasks if task.completed == (status == "done")]

    def complete(self, task_id):
        validate_id(task_id)
        tasks = self.store.load()
        for index, task in enumerate(tasks):
            if task.id == task_id:
                result = task.complete()
                tasks[index] = result
                self.store.save(tasks)
                return result
        raise TaskNotFoundError("No task matches that ID")
