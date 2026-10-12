# Lecture 1: Git version control

Source: the supplied `1_git_version_control_2026_EN_stundents.pdf` and its study guide.

The working tree holds edited files. The index selects the next snapshot. The local repository
holds commits. The remote exchanges history. Saving, staging, committing and pushing are different actions.

A commit records a snapshot, author metadata, purpose and parent history. A hash identifies the
commit; it does not itself prove authorization. Keep one logical change per commit and explain intent.
Use `git status`, `git diff` and `git diff --staged` to inspect the different states.

Short branches reduce divergence. A pull request records the problem, solution, verification and risk.
Automation checks repeatable questions; reviewers assess requirements, architecture and operational impact.
Protected main is a recommended team policy, not something this project has enabled automatically.

GitHub Flow fits short changes and frequent integration. Git Flow has extra release and hotfix
branches and may suit several supported versions; choose it for a concrete delivery need.

For a conflict, understand both intended changes, produce a coherent result, remove markers and run tests.
Git accepting the merge does not establish that behavior is correct.

`restore` changes uncommitted file state. `restore --staged` removes staging while retaining edits.
`revert` records a reversal of published work. `reflog` tracks recent local reference movements.
`bisect` helps locate a regression by testing history.

Tags identify release points. With a defined public API, SemVer uses MAJOR for incompatibility,
MINOR for compatible functionality and PATCH for compatible fixes.

Keep credentials outside Git. Ignoring a file does not untrack it or rotate a leaked credential.

## Lecture exercise, still separate from the commit-count task

Slide 20 asks for a small feature on a branch with 2-3 logical commits, a PR describing problem,
solution, tests and risk, and one intentional conflict followed by tests. Publishing 30 commits
alone does not complete that exercise or the later three-conflict assignment.
