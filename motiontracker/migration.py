"""Ordered SQL upgrades, with dry runs, backups and transactional schema changes."""
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from importlib.resources import files
from pathlib import Path
from uuid import uuid4

LATEST_VERSION = 2
SCRIPTS = {1: "001_projects.sql", 2: "002_revisions_and_formats.sql"}


def script_for(version):
    return files("motiontracker").joinpath("migrations", SCRIPTS[version]).read_text(encoding="utf-8")


def inspect_schema(connection):
    version = connection.execute("PRAGMA user_version").fetchone()[0]
    if version > LATEST_VERSION:
        raise ValueError("Database was created by a newer application; no changes made")
    tables = connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall()
    if version == 0 and tables:
        raise ValueError("Unversioned database contains tables; refusing to change it")
    if version and not any(row[0] == "projects" for row in tables):
        raise ValueError("Project database schema is incomplete")
    if version:
        expected = {"id", "title", "client", "brief", "deadline", "status"}
        if version >= 2:
            expected |= {"revision_limit", "revision_count", "delivery_formats"}
        columns = {row[1] for row in connection.execute("PRAGMA table_info(projects)")}
        if columns != expected:
            raise ValueError("Project database columns do not match its schema version")
    return version


def apply_script(connection, script):
    # executescript() commits an existing transaction, so execute complete statements individually.
    statement = ""
    for line in script.splitlines(keepends=True):
        statement += line
        if sqlite3.complete_statement(statement):
            connection.execute(statement)
            statement = ""
    if statement.strip():
        raise ValueError("Incomplete SQL migration")


def migrate_database(path, dry_run=False):
    path = Path(path)
    if path.exists():
        with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as reader:
            version = inspect_schema(reader)
    else:
        version = 0
    plan = {"from_version": version, "to_version": LATEST_VERSION,
            "steps": [SCRIPTS[number] for number in range(version + 1, LATEST_VERSION + 1)],
            "backup": None, "dry_run": dry_run}
    if dry_run or version == LATEST_VERSION:
        return plan
    path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(path)) as connection:
        if version:
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            backup = path.with_name(path.name + f".pre-v{LATEST_VERSION}-{stamp}-{uuid4().hex[:8]}.bak")
            with backup.open("xb"):
                pass
            with closing(sqlite3.connect(backup)) as target:
                connection.backup(target)
            plan["backup"] = str(backup)
        try:
            connection.execute("BEGIN IMMEDIATE")
            current = inspect_schema(connection)
            for number in range(current + 1, LATEST_VERSION + 1):
                apply_script(connection, script_for(number))
                connection.execute(f"PRAGMA user_version = {number}")
            connection.commit()
        except Exception:
            connection.rollback()
            raise
    return plan
