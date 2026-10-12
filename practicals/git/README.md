# Git practical session: results

Completed on 12 October 2026 from the supplied `git_practical_session_v2_english_stundents.pdf`.
This is the one dedicated practical-session guide in the supplied course archive, with ten tasks.

## Where to inspect the work

- [Working practice project](https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation/tree/git-practice/main)
- [Actual practice commit history](https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation/commits/git-practice/main/)
- [Terminal transcript](terminal-transcript.md), including checks and one failed local-transport attempt
- [Conflict records](conflicts.json) and marker-bearing snapshots linked below
- [Portable Git history](git-practice.bundle)

The practice lives on `git-practice/main` in the existing course repository. Its root is the requested
git-practice project with README.md, src/main.py, config.txt, notes.txt, .gitignore, header.txt and footer.txt.
The earlier task-tracker project remains on the course repository's main branch.
Remote practice branches use the git-practice/ prefix to keep their independent history identifiable.
Local exercise branch names follow the guide. No shared history was force-pushed.

## Task-by-task evidence

| Task | Result | Verification |
| --- | --- | --- |
| 1 | Complete | Fresh local repository named git-practice; README untracked, staged, then clean after first commit |
| 2 | Complete | Committed Hello world, changed to Hello Git plus Version 2; compared regular and staged diffs |
| 3 | Complete | First commit contains exactly README.md and src/main.py; config.txt and notes.txt enter a separate commit |
| 4 | Complete | Restored BROKEN FILE to the committed program; unstaged a README edit and verified the edit remained |
| 5 | Complete | .env, debug.log and build/output.txt ignored; commit includes only .gitignore |
| 6 | Complete | feature/greeting has personalized input; switching branches changes working-tree contents |
| 7 | Complete | Greeting merged into main; branch remains and graph inspected |
| 8 | Complete | Actual code merge conflict, marker inspection, deliberate resolution and program verification |
| 9 | Complete | Actual GitHub push with upstream tracking, fetch, branch -vv and pull --ff-only |
| 10 | Git mechanics complete; human pairing not performed | Two independent clones push header/footer branches, merge both files and resolve a real overlapping README conflict |

Task 10 was executed as roles A and B by one assistant. It does not demonstrate participation by a second
student. If the lecturer requires real pair work, repeat that part with a classmate and preserve their contribution.
No second human identity was invented.

## Three real conflicts

Each conflict was produced by merging diverged commits that edit the same lines. The failed merge returned
exit status 1 and Git reported UU. The saved snapshots contain Git-generated conflict markers. Each resolution
is a two-parent merge commit, not a file containing manually inserted markers.

| Conflict | File | Resolution commit | Before-resolution snapshot |
| --- | --- | --- | --- |
| 1 | `src/main.py` | [ddabf2d](https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation/commit/ddabf2d4584e96833d6be73aa28c069eb54a664c) | [conflict-1-before-resolution.txt](conflict-1-before-resolution.txt) |
| 2 | `README.md` | [6269a28](https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation/commit/6269a28507a000bab2ea1810e0133d71769ff2ff) | [conflict-2-before-resolution.txt](conflict-2-before-resolution.txt) |
| 3 | `config.txt` | [9a13e4f](https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation/commit/9a13e4ff0f157c55941ecaaa1001840717de1837) | [conflict-3-before-resolution.txt](conflict-3-before-resolution.txt) |

1. The greeting resolved to `Hello from Git course`, matching the practical's answer.
2. The README title retained both simulated roles.
3. The configuration resolved to `mode=dev`, suitable for this learning environment.

The three-conflict total includes the two conflicts required by Tasks 8 and 10, plus one additional
configuration conflict. These are three total conflicts, not three additional conflicts after the practical.
After each resolution, the working tree was clean, conflict markers were absent, and the program produced
the expected greeting. The configuration resolution was checked separately for its intended value.

## Transport and integrity

The initial local bare-remote rehearsal failed because the Windows sandbox could not launch Git's shell
transport. That failure remains in the transcript. Task 9 subsequently used authenticated HTTPS GitHub
transport successfully. Tasks 10 and the third conflict also pushed to the actual GitHub repository.
The sign-in credentials are outside the repository and are excluded from these files.

All resolution commits and feature tips were published. `git fsck --full` and bundle verification succeeded.
The bundle includes the recorded branch/ref history and can be inspected without a GitHub login:

```text
git clone git-practice.bundle recovered-practice
cd recovered-practice
git log --oneline --graph --decorate --all
python src/main.py
```

For the hosted practice branch:

```text
git clone --branch git-practice/main https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation.git git-practice
cd git-practice
python src/main.py
```

Expected output: `Hello from Git course`.

The lecture exercises, course exam, Linux-account setup and actual human pair participation are outside this
completed technical practical. This report does not claim they were completed.
