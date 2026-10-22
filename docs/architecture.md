# Architecture

The CLI parses commands and formats output. ProjectService provides project operations and filters.
The immutable Project model validates text, calendar dates, status, formats and revision values.
ProjectStore persists values through parameterized SQLite queries.

Numbered SQL migrations run in one explicit transaction. SQLite's user_version records the schema.
Existing databases are backed up first. Scripts are read through package resources, so they also
work inside the packaged .pyz application.

Revision recording uses a conditional SQL update that checks the current budget in the database.
An explicit extra-round option can exceed the budget. Both revision count and status update together.

Legacy import validates the entire input before opening the database, then inserts in a transaction.
Existing IDs are skipped. The original tasktracker package supplies legacy validation and remains
runnable for old JSON files.

The build packages Python and SQL resources with source revision metadata and a checksum.
Local databases and credentials are excluded. Everything uses Python's standard library.
