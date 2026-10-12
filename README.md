# Software implementation and maintenance life cycle and process automation

A small Python task tracker for applying the course's Git and software-maintenance principles.
It adds tasks, lists them and marks them complete, with local JSON persistence.

## Start

Prerequisite: Python 3.12.14 (declared in .python-version). No third-party packages are required.
Clone this repository, enter its directory and run:

```text
python -m tasktracker add "Study presentations 0, 1 and 2"
python -m tasktracker list
python -m tasktracker complete UUID_FROM_LIST
python -m tasktracker list --status done
```

Replace UUID_FROM_LIST with the full ID printed by list. On Windows, `py -3.12` can replace
`python` if the interpreter is available through the Python launcher.

The default data file is data/tasks.json, created when adding the first task and excluded from Git.
Specify another location before the subcommand with `python -m tasktracker --data path/tasks.json list`.
Use `list --json` for machine-readable output and `python -m tasktracker --help` for command help.
The program supports one writer at a time. Invalid stored data causes an error and remains untouched.

## Check the project

```text
python -m compileall -q tasktracker tests
python -m unittest discover -s tests -v
```

The same checks are configured for GitHub Actions. Exit status 0 means success, 1 means an application
error, and 2 means an argument error. The [test plan](docs/test-plan.md) explains coverage and limits.

## Course materials and decisions

- [Project scope](docs/project-scope.md) and [architecture](docs/architecture.md)
- Study notes: [lecture 0](docs/lecture-0.md), [lecture 1](docs/lecture-1.md), [lecture 2](docs/lecture-2.md)
- [Automation exercise answer](docs/automation-exercise.md)
- [Git command reference](docs/git-command-reference.md) and [practical checklist](docs/practical-checklist.md)
- [Data format](docs/data-format.md) and [maintenance](docs/maintenance.md)
- [Thirty-change review guide](docs/commit-log.md)
- [Later three-conflict plan](docs/conflict-plan.md), still awaiting its own practical session

The repository contains original study notes based on the supplied course PDFs. It does not redistribute
the lecture PDFs. The 30 new commits supplement the initial README commit; the later conflict and
pair-work exercises remain separate tasks. No license has been selected.
