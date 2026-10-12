# Commit plan and review guide

These 30 new changes build a small task tracker and supporting course documentation.
The initial GitHub README commit predates them, so the finished repository has 31 commits in total.
Each listed change has its own commit; verification uses the actual Git history rather than this list alone.

1. `chore: exclude local task data and generated Python files` — `.gitignore`
2. `chore: define the task tracker package and version` — `tasktracker/__init__.py`
3. `feat: validate task titles and identifiers` — `tasktracker/validation.py`
4. `test: cover blank oversized and unsafe task inputs` — `tests/test_validation.py`
5. `feat: introduce immutable tasks with validated JSON records` — `tasktracker/model.py`
6. `test: verify task identity completion and record validation` — `tests/test_model.py`
7. `feat: persist versioned task data with atomic file replacement` — `tasktracker/storage.py`
8. `test: check persistence corruption and failed writes` — `tests/test_storage.py`
9. `feat: add list and complete tasks through a storage-independent service` — `tasktracker/service.py`
10. `test: verify service filtering and missing-task handling` — `tests/test_service.py`
11. `feat: expose task commands with explicit data paths and safe errors` — `tasktracker/cli.py`
12. `feat: support running the tracker as a Python module` — `tasktracker/__main__.py`
13. `test: cover CLI output validation filters and safe failures` — `tests/test_cli.py`
14. `test: verify persisted tasks across separate CLI processes` — `tests/test_roundtrip.py`
15. `chore: declare the tested Python runtime` — `.python-version`
16. `ci: run the same Python checks for pushes and pull requests` — `.github/workflows/checks.yml`
17. `docs: define task tracker requirements and acceptance criteria` — `docs/project-scope.md`
18. `docs: summarize lifecycle quality and shared responsibility` — `docs/lecture-0.md`
19. `docs: explain Git states coherent history and review workflows` — `docs/lecture-1.md`
20. `docs: summarize reproducible environments and maintenance fundamentals` — `docs/lecture-2.md`
21. `docs: answer the automation prioritization exercise with explicit estimates` — `docs/automation-exercise.md`
22. `docs: distinguish staging restoration and remote synchronization commands` — `docs/git-command-reference.md`
23. `docs: map the ten practical tasks and separate later conflict work` — `docs/practical-checklist.md`
24. `docs: explain domain service storage and CLI responsibilities` — `docs/architecture.md`
25. `docs: specify JSON schema compatibility and storage limits` — `docs/data-format.md`
26. `docs: document safe backups diagnosis and change recovery` — `docs/maintenance.md`
27. `docs: map behavioral risks to unit and process checks` — `docs/test-plan.md`
28. `docs: plan three later conflicts with explicit resolution evidence` — `docs/conflict-plan.md`
29. `docs: record the purpose of the thirty course-project changes` — `docs/commit-log.md`
30. `docs: provide startup commands and links to course exercises` — `README.md`

The code implements behavior, tests check failure and success paths, and the notes explain choices
from lectures 0-2. This commit-count exercise is separate from demonstrating terminal staging,
branch collaboration, a pull request and the later intentional conflicts.
