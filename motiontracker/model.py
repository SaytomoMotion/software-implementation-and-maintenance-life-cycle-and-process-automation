"""Validated project values shared by storage and application commands."""
from dataclasses import asdict, dataclass
from datetime import date
from uuid import uuid4

from tasktracker.validation import validate_id

STATUSES = ("briefing", "in_progress", "review", "delivered", "on_hold")
FORMATS = ("mp4", "mov", "gif", "webm", "png-sequence")


def validate_project_id(value):
    try:
        return validate_id(value)
    except ValueError as error:
        raise ValueError(str(error).replace("Task ID", "Project ID")) from error


def text_field(value, name, limit, allow_empty=False, multiline=False):
    if not isinstance(value, str):
        raise ValueError(f"{name} must be text")
    allowed = {"\n", "\t"} if multiline else set()
    if any((ord(char) < 32 and char not in allowed) or ord(char) == 127 for char in value):
        raise ValueError(f"{name} contains unsupported control characters")
    value = value.strip()
    if not value and not allow_empty:
        raise ValueError(f"{name} cannot be blank")
    if len(value) > limit:
        raise ValueError(f"{name} must be at most {limit} characters")
    return value


@dataclass(frozen=True)
class Project:
    id: str
    title: str
    client: str = "Unassigned"
    brief: str = ""
    deadline: str | None = None
    status: str = "briefing"
    revision_limit: int = 2
    revision_count: int = 0
    delivery_formats: tuple[str, ...] = ("mp4",)

    def __post_init__(self):
        validate_project_id(self.id)
        for name, maximum in (("title", 200), ("client", 120), ("brief", 4000)):
            value = text_field(getattr(self, name), name.capitalize(), maximum,
                               allow_empty=name == "brief", multiline=name == "brief")
            object.__setattr__(self, name, value)
        if self.deadline is not None:
            if not isinstance(self.deadline, str):
                raise ValueError("Deadline must be YYYY-MM-DD or omitted")
            try:
                parsed = date.fromisoformat(self.deadline)
            except ValueError as error:
                raise ValueError("Deadline must be a valid YYYY-MM-DD date") from error
            if parsed.isoformat() != self.deadline:
                raise ValueError("Deadline must use YYYY-MM-DD")
        if self.status not in STATUSES:
            raise ValueError("Unsupported project status")
        for name in ("revision_limit", "revision_count"):
            value = getattr(self, name)
            if type(value) is not int or not 0 <= value <= 1_000_000:
                raise ValueError(f"{name} must be an integer between 0 and 1000000")
        if not isinstance(self.delivery_formats, (list, tuple)) or not self.delivery_formats:
            raise ValueError("At least one delivery format is required")
        if any(not isinstance(value, str) or value not in FORMATS for value in self.delivery_formats):
            raise ValueError("Unsupported delivery format")
        object.__setattr__(self, "delivery_formats", tuple(dict.fromkeys(self.delivery_formats)))

    @classmethod
    def create(cls, title, **fields):
        return cls(id=str(uuid4()), title=title, **fields)

    def to_record(self):
        record = asdict(self)
        record["delivery_formats"] = list(self.delivery_formats)
        return record

    def is_overdue(self, today=None):
        today = today or date.today()
        return bool(self.deadline and self.deadline < today.isoformat() and self.status != "delivered")
