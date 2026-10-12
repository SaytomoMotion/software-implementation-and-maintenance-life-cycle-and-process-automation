"""Single-writer JSON persistence; invalid existing data is never silently reset."""
import json
import os
import tempfile
from pathlib import Path
from tasktracker.model import Task


class StorageError(Exception):
    """A safe message that does not include task content."""


class JsonStore:
    def __init__(self, path):
        self.path = Path(path)

    def load(self):
        try:
            raw = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return []
        except (OSError, UnicodeError) as error:
            raise StorageError("Cannot read task data") from error
        try:
            document = json.loads(raw)
            if not isinstance(document, dict) or set(document) != {"schema_version", "tasks"}:
                raise ValueError("Invalid document")
            if type(document["schema_version"]) is not int or document["schema_version"] != 1:
                raise ValueError("Unsupported schema")
            if not isinstance(document["tasks"], list):
                raise ValueError("Invalid task list")
            tasks = [Task.from_record(record) for record in document["tasks"]]
            if len({task.id for task in tasks}) != len(tasks):
                raise ValueError("Duplicate IDs")
            return tasks
        except (ValueError, TypeError, UnicodeError) as error:
            raise StorageError("Invalid task data; preserve the file and restore a known-good backup") from error

    def save(self, tasks):
        temporary = None
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=self.path.parent,
                                             prefix=".tasks-", suffix=".tmp", delete=False) as stream:
                temporary = Path(stream.name)
                json.dump({"schema_version": 1, "tasks": [task.to_record() for task in tasks]},
                          stream, ensure_ascii=False, indent=2)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            # Same-directory replacement avoids a partially written destination.
            os.replace(temporary, self.path)
        except OSError as error:
            raise StorageError("Cannot save task data") from error
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()
