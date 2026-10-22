# Motion Design Project Manager

A local command-line app for client animation projects: briefs, deadlines, production status,
revision budgets and delivery formats. Course project for Software Implementation and Maintenance
Life Cycle and Process Automation.

Requires Python 3.12.14, declared in `.python-version`. SQLite is included in Python's standard
library. No extra packages or server are required. This version has no browser interface.

## Start a client project

From the repository folder:

```text
python -m motiontracker add "Brand logo intro" --client "Demo Studio" --brief "15-second animation with an end card" --deadline 2026-11-15 --revision-limit 2 --format mp4 --format mov
python -m motiontracker list
```

The first command creates `data/motion-projects.sqlite3` and prints a project ID.
Replace `PROJECT_ID` below with that full ID:

```text
python -m motiontracker show PROJECT_ID
python -m motiontracker status PROJECT_ID in_progress
python -m motiontracker revise PROJECT_ID
python -m motiontracker status PROJECT_ID delivered
python -m motiontracker stats
```

Statuses: `briefing`, `in_progress`, `review`, `delivered`, `on_hold`.
Formats: `mp4`, `mov`, `gif`, `webm`, `png-sequence`.
Recording a revision moves the project to review. After the agreed limit, `revise` stops;
use `--allow-extra` only to record an explicitly agreed extra round.

## Find and edit work

```text
python -m motiontracker list --client "Demo Studio"
python -m motiontracker list --status review
python -m motiontracker list --overdue
python -m motiontracker list --json
python -m motiontracker edit PROJECT_ID --brief "Approved storyboard" --deadline 2026-11-20
python -m motiontracker edit PROJECT_ID --revision-limit 3 --format mov
```

Repeating `--format` selects several formats; editing formats replaces the previous selection.
Use `--deadline none` to clear a deadline. Overdue means the deadline has passed and the project
is not delivered. Listings sort by deadline, with undated work last.

For another database, put `--db` before the command:
`python -m motiontracker --db data/demo.sqlite3 list`.
Use `python -m motiontracker --help` for all commands. On Windows, `py -3.12` can replace
`python` when that interpreter is available through the launcher.

## Demonstrate a real database migration

Schema 1 stores ID, title, client, brief, deadline and status.
Schema 2 adds revision limit, revision count, delivery formats and a deadline index.

```text
python -m examples.create_v1_database --db data/migration-demo.sqlite3
python -m motiontracker --db data/migration-demo.sqlite3 migrate --dry-run
python -m motiontracker --db data/migration-demo.sqlite3 migrate
python -m motiontracker --db data/migration-demo.sqlite3 show 12345678-1234-4234-8234-123456789abc
```

The fixture uses synthetic project data and refuses to overwrite an existing file. The dry run
changes nothing. A real upgrade creates a backup, preserves the project and adds defaults of two
revisions, zero used rounds and MP4 delivery. Repeating the migration does nothing.
Existing schema-1 databases also upgrade automatically before normal commands.
See [migrations and recovery](docs/migrations.md).

### Import the previous tracker data

```text
python -m motiontracker import-tasks examples/legacy-tasks.json --dry-run
python -m motiontracker import-tasks examples/legacy-tasks.json
```

Use `data/tasks.json` instead of the example to import your previous tasks. The input file stays
unchanged. IDs and titles are retained; completed tasks become delivered projects. Imported
projects use Unassigned as the client, no deadline, two revisions and MP4. Edit these details
afterwards. Repeat imports skip existing IDs without overwriting later edits.

## Automation and packaged app

```text
python -m compileall -q motiontracker tasktracker scripts examples tests
python -m unittest discover -s tests -v
python -m scripts.build
python dist/motiondesk.pyz --help
```

GitHub Actions runs compilation, tests, a database upgrade rehearsal and a packaged-app check on
pushes and pull requests. It uploads `motiondesk.pyz` and its SHA-256 checksum as a build artifact.
The package still requires Python; it is not a standalone Windows executable.
There is no production deployment. Databases, backups and generated files are ignored by Git.

## Project documentation

- [Requirements](docs/project-scope.md) and [architecture](docs/architecture.md)
- [Data format](docs/data-format.md) and [migrations](docs/migrations.md)
- [Automation](docs/automation.md), [tests](docs/test-plan.md) and [maintenance](docs/maintenance.md)

## Git practical

The original practical and three conflict resolutions are preserved:
[practice project](https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation/tree/git-practice/main),
[lab report](practicals/git/README.md). Task 10 used two working copies to simulate pair-work operations.
The old `python -m tasktracker` commands remain available for legacy JSON task files.
