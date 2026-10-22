# Project data

Default file: data/motion-projects.sqlite3. Schema version: SQLite PRAGMA user_version.

| Field | Meaning |
| --- | --- |
| id | Canonical UUID, retained on legacy import |
| title | 1–200 characters |
| client | 1–120 characters; imported tasks use Unassigned |
| brief | Optional, up to 4,000 characters; newlines allowed |
| deadline | Optional valid YYYY-MM-DD date |
| status | briefing, in_progress, review, delivered or on_hold |
| revision_limit | Agreed rounds, default 2 |
| revision_count | Used rounds, default 0 |
| delivery_formats | JSON array stored as text, default MP4 |

Formats: mp4, mov, gif, webm and png-sequence. Duplicate selections are removed.
Revision values are integers from 0 to 1,000,000. Extra rounds require --allow-extra.
Overdue comparisons use the computer's local calendar date. Delivered projects are not overdue.

The old JSON format has schema_version 1 and tasks with exactly id, title and completed.
Import keeps IDs and titles and maps completed to delivered, otherwise briefing. No real client
or deadline is inferred. The original JSON is unchanged.
The JSON version and SQLite schema version are separate versioning systems.
