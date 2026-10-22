# Maintenance

Keep real client records in ignored data/ files. SQLite databases, generated backups and build
outputs are excluded from Git. Never put client secrets in briefs or commit real client records.

Before upgrading important data, stop other writers and use migrate --dry-run. Upgrades from
version 1 create a SQLite backup before changing the schema. Copy important backups to a separate
backup location; files on the same disk do not protect against disk failure.

Rehearse recovery at a separate path. Inspect a restored file using migrate --dry-run, then
upgrade it and compare IDs, briefs and statuses. Preserve the original during investigation.
Do not manually change user_version to bypass a schema error. Check the app version that wrote
the file. For lock or write errors, resolve competing writers or filesystem access first.

Run tests and the migration demo before publishing code changes. Record artifact checksums and
source commits. Revision budgets do not create invoices or authorize charges; billing is separate.
