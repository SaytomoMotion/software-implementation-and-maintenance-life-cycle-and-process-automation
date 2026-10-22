# Git practical

[Open the practice files](https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation/tree/git-practice/main) · [View the commits](https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation/commits/git-practice/main/)

## Tasks 1–5: commits and local changes

1. Created a local repository named `git-practice` and added `README.md`. Checked
   `git status` before staging, after `git add`, and after the first commit.
2. Created `src/main.py` with `Hello world`, committed it, then changed the greeting.
   Compared `git diff` with `git diff --staged` to see which changes the next commit would include.
3. Split the work into two commits: README and program changes first, then `config.txt` and `notes.txt`.
4. Replaced the program with `BROKEN FILE` and restored the committed version using `git restore`.
   Also staged and unstaged a temporary README edit; the edit remained in the working tree.
5. Added `.gitignore` rules for `.env`, log files and `build/`. Checked that these files were ignored
   and that only `.gitignore` entered that commit.

## Tasks 6–9: branches, merging and GitHub

6. Created `feature/greeting`, added a personalized greeting, and switched between branches
   to compare their file contents.
7. Merged the greeting branch and inspected the history with
   `git log --oneline --graph --decorate --all`.
8. Changed the same greeting on two branches, triggered a merge conflict, inspected the markers,
   and committed a resolution. The final program prints `Hello from Git course`.
9. Published the practice to GitHub using `git push -u`, then ran `git fetch`, `git branch -vv`,
   and `git pull --ff-only` to check synchronization and upstream tracking.

The local main branch is published as `git-practice/main` to keep the exercise separate from the
motion design project on the repository's default branch. Related remote branches use `git-practice/` too.

## Task 10: two working copies

Two separate clones represented roles A and B. One added `header.txt`; the other added `footer.txt`.
Both branches were pushed and merged. The two copies then changed the same README title,
which produced a conflict. The resolution kept both roles in the title.

This demonstrates the Git operations using two working copies. It was a simulation, without a second student.

## Three conflicts

| Conflict | File | Resolution commit | Saved conflict markers |
| --- | --- | --- | --- |
| 1 | `src/main.py` | [ddabf2d](https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation/commit/ddabf2d4584e96833d6be73aa28c069eb54a664c) | [conflict-1-before-resolution.txt](conflict-1-before-resolution.txt) |
| 2 | `README.md` | [6269a28](https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation/commit/6269a28507a000bab2ea1810e0133d71769ff2ff) | [conflict-2-before-resolution.txt](conflict-2-before-resolution.txt) |
| 3 | `config.txt` | [9a13e4f](https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation/commit/9a13e4ff0f157c55941ecaaa1001840717de1837) | [conflict-3-before-resolution.txt](conflict-3-before-resolution.txt) |

- **Greeting:** `Hello from MAIN` and `Hello from FEATURE` became `Hello from Git course`.
- **README:** the competing role A and role B titles became `Git practice by roles A and B`.
- **Configuration:** `mode=production` and `mode=test` resolved to `mode=dev` for the practice environment.

The first two conflicts belong to Tasks 8 and 10. The configuration conflict brings the total to three.
Each came from a real merge of diverged branches. Git reported an unmerged file, and each resolution
created a two-parent merge commit. The final working tree was clean and the program's output was checked.

## Evidence and verification

- [Command output](terminal-transcript.md)
- [Conflict commit records](conflicts.json)
- [Git history bundle](git-practice.bundle)

The transcript includes an unsuccessful local-transport attempt followed by successful GitHub pushes.
`git fsck --full` and bundle verification passed. A fresh clone from GitHub was also checked.

To inspect the final program:

```text
git clone --branch git-practice/main https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation.git git-practice
cd git-practice
python src/main.py
```

Expected output: `Hello from Git course`.
