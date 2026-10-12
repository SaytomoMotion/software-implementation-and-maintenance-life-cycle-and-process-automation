"""Input rules shared by the model and command line."""
from uuid import UUID


def validate_title(value):
    if not isinstance(value, str):
        raise ValueError("Task title must be text")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ValueError("Task title cannot contain control characters")
    title = value.strip()
    if not title:
        raise ValueError("Task title cannot be blank")
    if len(title) > 200:
        raise ValueError("Task title must be at most 200 characters")
    return title


def validate_id(value):
    if not isinstance(value, str):
        raise ValueError("Task ID must be text")
    try:
        normalized = str(UUID(value))
    except (ValueError, AttributeError) as error:
        raise ValueError("Task ID must be a UUID") from error
    if value != normalized:
        raise ValueError("Task ID must use canonical lowercase UUID format")
    return value
