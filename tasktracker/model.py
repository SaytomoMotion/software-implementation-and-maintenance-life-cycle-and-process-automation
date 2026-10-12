"""Task values are independent of storage and the user interface."""
from dataclasses import asdict, dataclass, replace
from uuid import uuid4
from tasktracker.validation import validate_id, validate_title


@dataclass(frozen=True)
class Task:
    id: str
    title: str
    completed: bool = False

    def __post_init__(self):
        validate_id(self.id)
        object.__setattr__(self, "title", validate_title(self.title))
        if type(self.completed) is not bool:
            raise ValueError("Completed must be a boolean")

    @classmethod
    def create(cls, title):
        return cls(str(uuid4()), title)

    @classmethod
    def from_record(cls, record):
        if not isinstance(record, dict) or set(record) != {"id", "title", "completed"}:
            raise ValueError("Invalid task record fields")
        return cls(**record)

    def to_record(self):
        return asdict(self)

    def complete(self):
        return replace(self, completed=True)
