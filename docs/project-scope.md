# Project scope

This course project demonstrates a small, repeatable change process using a local task tracker.
It uses Python's standard library so startup does not depend on third-party packages.

## Requirements

- Add a title, rejecting blank titles, control characters and titles above 200 characters.
- Give every task an independent UUID.
- List all, open or completed tasks, with optional JSON output.
- Complete a task without changing its identity or title.
- Persist tasks across separate program invocations.
- Report invalid data without overwriting it or displaying its contents.

## Acceptance evidence

Run `python -m unittest discover -s tests -v`. Then add, list and complete a task in separate processes.
The data file must retain the completed state. A rejected command must return a nonzero exit status.

## Boundaries

This is a single-user, single-writer learning application. It is not a network service and does not
provide authentication, concurrent writers, production deployment or production observability.
Those would require additional requirements and verification.
