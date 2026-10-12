# Git command reference

These commands are a study reference, not a record that every practical was performed.

| Command | Purpose |
| --- | --- |
| `git status` | Inspect tracked, untracked, staged and unstaged state |
| `git diff` | Compare working tree changes against the index |
| `git diff --staged` | Compare the index against the current commit |
| `git add path` | Select current file contents for the next commit |
| `git add -p` | Select changes in smaller hunks |
| `git commit -m "purpose"` | Record the selected snapshot locally |
| `git switch -c feature/name` | Create and switch to a branch |
| `git switch main` | Switch to the main branch |
| `git restore path` | Discard unstaged edits to a specified file; inspect first |
| `git restore --staged path` | Unstage a file while keeping working edits |
| `git merge feature/name` | Integrate another branch |
| `git fetch origin` | Update remote-tracking information without integrating it |
| `git pull --ff-only` | Fetch and integrate only if a fast-forward is possible |
| `git push -u origin feature/name` | Publish a branch and set upstream tracking |
| `git log --oneline --graph --decorate --all` | Inspect branch relationships |
| `git revert COMMIT` | Record a reversal in shared history |

Inspect `git remote -v` before adding origin. A GitHub web-editor commit is already remote;
fetching it later downloads that history to a local clone.
