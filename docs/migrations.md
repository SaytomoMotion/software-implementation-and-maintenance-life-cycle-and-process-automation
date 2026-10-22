# Database migration and legacy import

001_projects.sql creates ID, title, client, brief, deadline and status.
002_revisions_and_formats.sql adds revision_limit, revision_count and delivery_formats and a
deadline index. Defaults are 2 rounds, 0 used and ["mp4"]. Existing project fields remain intact.
SQLite user_version advances with the successful migration transaction.

## Rehearse the upgrade

```text
python -m examples.create_v1_database --db data/migration-demo.sqlite3
python -m motiontracker --db data/migration-demo.sqlite3 migrate --dry-run
python -m motiontracker --db data/migration-demo.sqlite3 migrate
python -m motiontracker --db data/migration-demo.sqlite3 show 12345678-1234-4234-8234-123456789abc
```

The example refuses to overwrite an existing file. The preview changes nothing. A real upgrade
uses SQLite's backup API to create a timestamped .bak beside the database. The backup remains
version 1 with the original record; the working database becomes version 2.
Repeating the upgrade performs no steps and creates no additional backup.

Normal commands also upgrade version-1 files before use and report the backup path to stderr.
A new database applies both scripts without a backup because it contains no existing data.
The version-1 fixture demonstrates an actual SQL schema change; it is not a previous public app release.

## Failure and recovery

SQL statements and the version update run in one transaction. Tests deliberately fail after an
ALTER TABLE and verify that the column and version changes roll back and the original row remains.
The pre-upgrade backup stays available. Unknown future versions and unversioned databases with
tables are rejected rather than guessed at.

Stop writers before manual recovery. Preserve the current database and restore a backup to a
separate path. Use migrate --dry-run to inspect it without alteration, then compare the records.
Opening a restored version-1 backup with a normal command will upgrade it again.

## Import old task JSON

```text
python -m motiontracker import-tasks examples/legacy-tasks.json --dry-run
python -m motiontracker import-tasks examples/legacy-tasks.json
```

Use data/tasks.json for an actual old task file. The source is read without modification.
All records are validated before opening the database; inserts use a transaction. Malformed data
imports nothing, and a failed insert rolls back earlier inserts from that import. Existing IDs
are skipped, preserving later project edits.

The preview counts valid input without creating or modifying the database. It does not predict
skipped IDs in an existing database. Fill in client details, deadlines and formats after import.
