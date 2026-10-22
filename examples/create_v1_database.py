"""Create a synthetic version-1 database for rehearsing upgrades; never overwrite a file."""
import argparse
import sqlite3
from contextlib import closing
from pathlib import Path

from motiontracker.migration import apply_script, script_for


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="data/migration-demo.sqlite3")
    arguments = parser.parse_args()
    path = Path(arguments.db)
    if path.exists():
        parser.error("Destination already exists; choose a new demo database path")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb"):
        pass
    with closing(sqlite3.connect(path)) as connection:
        apply_script(connection, script_for(1))
        connection.execute("PRAGMA user_version=1")
        connection.execute("INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?)",
                           ("12345678-1234-4234-8234-123456789abc", "Brand intro", "Demo Studio",
                            "15-second animation, end card with logo", "2026-11-15", "review"))
        connection.commit()
    print(f"Created synthetic schema-version-1 project database: {path}")


if __name__ == "__main__":
    main()
