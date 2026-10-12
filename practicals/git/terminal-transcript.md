
## Task 1 — repository, staging and first commit

```text
$ git init -b main
Initialized empty Git repository in C:/Users/mmrkr/Documents/Codex/2026-10-08/i-x20/outputs/git-practice/.git/
[exit 0]
```

```text
$ git config user.name SaytomoMotion
[exit 0]
```

```text
$ git config user.email 155469523+SaytomoMotion@users.noreply.github.com
[exit 0]
```

```text
$ git config commit.gpgsign false
[exit 0]
```

```text
$ git config core.autocrlf false
[exit 0]
```

```text
$ git status --short
?? README.md
[exit 0]
```

```text
$ git add README.md
[exit 0]
```

```text
$ git status --short
A  README.md
[exit 0]
```

```text
$ git commit -m Initial commit
[main (root-commit) 746885e] Initial commit
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
[exit 0]
```

```text
$ git status --short
[exit 0]
```

```text
$ git log --oneline
746885e Initial commit
[exit 0]
```


## Task 2 — unstaged and staged diffs

```text
$ git add src/main.py
[exit 0]
```

```text
$ git commit -m Add main program
[main 08c716b] Add main program
 1 file changed, 1 insertion(+)
 create mode 100644 src/main.py
[exit 0]
```

```text
$ git rev-parse HEAD
08c716be542fe1b644fd87402a41c27c4e28e59c
[exit 0]
```

```text
$ git diff
diff --git a/src/main.py b/src/main.py
index 44159b3..a69a1db 100644
--- a/src/main.py
+++ b/src/main.py
@@ -1 +1,2 @@
-print("Hello world")
+print("Hello Git")
+print("Version 2")
[exit 0]
```

```text
$ git diff --staged
[exit 0]
```

```text
$ git add src/main.py
[exit 0]
```

```text
$ git diff
[exit 0]
```

```text
$ git diff --staged
diff --git a/src/main.py b/src/main.py
index 44159b3..a69a1db 100644
--- a/src/main.py
+++ b/src/main.py
@@ -1 +1,2 @@
-print("Hello world")
+print("Hello Git")
+print("Version 2")
[exit 0]
```

```text
$ git commit -m Update greeting
[main 7be85bd] Update greeting
 1 file changed, 2 insertions(+), 1 deletion(-)
[exit 0]
```

```text
$ python src/main.py
Hello Git
Version 2
[exit 0]
```


## Task 3 — selective staging into two commits

```text
$ git status --short
 M README.md
 M src/main.py
?? config.txt
?? notes.txt
[exit 0]
```

```text
$ git add README.md src/main.py
[exit 0]
```

```text
$ git commit -m Update app and documentation
[main d9fdf5a] Update app and documentation
 2 files changed, 4 insertions(+)
[exit 0]
```

```text
$ git rev-parse HEAD
d9fdf5a5701248b7dab199ca48372f06be892340
[exit 0]
```

```text
$ git diff-tree --no-commit-id --name-only -r HEAD
README.md
src/main.py
[exit 0]
```

```text
$ git status --short
?? config.txt
?? notes.txt
[exit 0]
```

```text
$ git add config.txt notes.txt
[exit 0]
```

```text
$ git commit -m Add config and notes
[main 01e679b] Add config and notes
 2 files changed, 2 insertions(+)
 create mode 100644 config.txt
 create mode 100644 notes.txt
[exit 0]
```

```text
$ git rev-parse HEAD
01e679ba8461102abb06c2edd189d19107fbeb42
[exit 0]
```

```text
$ git log --oneline
01e679b Add config and notes
d9fdf5a Update app and documentation
7be85bd Update greeting
08c716b Add main program
746885e Initial commit
[exit 0]
```


## Task 4 — restore and unstage without losing an edit

```text
$ git status --short
 M src/main.py
[exit 0]
```

```text
$ git diff
diff --git a/src/main.py b/src/main.py
index 1b8b283..cd7451e 100644
--- a/src/main.py
+++ b/src/main.py
@@ -1,3 +1 @@
-print("Hello Git")
-print("Version 2")
-print("Practice session")
+BROKEN FILE
[exit 0]
```

```text
$ git restore src/main.py
[exit 0]
```

```text
$ git add README.md
[exit 0]
```

```text
$ git status --short
M  README.md
[exit 0]
```

```text
$ git restore --staged README.md
[exit 0]
```

```text
$ git diff --staged
[exit 0]
```

```text
$ git diff README.md
diff --git a/README.md b/README.md
index 0257453..cae4c17 100644
--- a/README.md
+++ b/README.md
@@ -2,3 +2,5 @@
 
 ## Usage
 Run python src/main.py.
+
+Temporary README change
[exit 0]
```

```text
$ git status --short
 M README.md
[exit 0]
```

```text
$ git restore README.md
[exit 0]
```


## Task 5 — ignore unwanted files

```text
$ git add .gitignore
[exit 0]
```

```text
$ git commit -m Add gitignore rules
[main a4e9552] Add gitignore rules
 1 file changed, 4 insertions(+)
 create mode 100644 .gitignore
[exit 0]
```

```text
$ git rev-parse HEAD
a4e95521e06b4f88ab16ffc997d9ce5f19807f67
[exit 0]
```

```text
$ git diff-tree --no-commit-id --name-only -r HEAD
.gitignore
[exit 0]
```

```text
$ git check-ignore .env debug.log build/output.txt
.env
debug.log
build/output.txt
[exit 0]
```

```text
$ git status --short
[exit 0]
```


## Task 6 — branches and changing working-tree contents

```text
$ git switch -c feature/greeting
Switched to a new branch 'feature/greeting'
[exit 0]
```

```text
$ git add src/main.py
[exit 0]
```

```text
$ git commit -m Add personalized greeting
[feature/greeting c671a74] Add personalized greeting
 1 file changed, 2 insertions(+), 3 deletions(-)
[exit 0]
```

```text
$ git rev-parse HEAD
c671a746820bc659a0d43529b5825d0697e3449a
[exit 0]
```

```text
$ git branch
* feature/greeting
  main
[exit 0]
```

```text
$ python src/main.py
Name: Hello Ada
[exit 0]
```

```text
$ git switch main
Switched to branch 'main'
[exit 0]
```

```text
$ git switch feature/greeting
Switched to branch 'feature/greeting'
[exit 0]
```


## Task 7 — merge and inspect the graph

```text
$ git switch main
Switched to branch 'main'
[exit 0]
```

```text
$ git merge feature/greeting
Updating a4e9552..c671a74
Fast-forward
 src/main.py | 5 ++---
 1 file changed, 2 insertions(+), 3 deletions(-)
[exit 0]
```

```text
$ git log --oneline --graph --decorate --all
* c671a74 (HEAD -> main, feature/greeting) Add personalized greeting
* a4e9552 Add gitignore rules
* 01e679b Add config and notes
* d9fdf5a Update app and documentation
* 7be85bd Update greeting
* 08c716b Add main program
* 746885e Initial commit
[exit 0]
```

```text
$ git branch
  feature/greeting
* main
[exit 0]
```

```text
$ python src/main.py
Name: Hello Ada
[exit 0]
```


## Task 8 — real code conflict, conflict 1 of 3

```text
$ git switch -c feature/message
Switched to a new branch 'feature/message'
[exit 0]
```

```text
$ git add src/main.py
[exit 0]
```

```text
$ git commit -m Change message in feature
[feature/message ceb7798] Change message in feature
 1 file changed, 1 insertion(+), 2 deletions(-)
[exit 0]
```

```text
$ git rev-parse HEAD
ceb77980e4097b89613c046e50ce42362c434c3b
[exit 0]
```

```text
$ git switch main
Switched to branch 'main'
[exit 0]
```

```text
$ git add src/main.py
[exit 0]
```

```text
$ git commit -m Change message in main
[main 94ae425] Change message in main
 1 file changed, 1 insertion(+), 2 deletions(-)
[exit 0]
```

```text
$ git rev-parse HEAD
94ae4257089b2a86137fd05c3556bed2bdfb771e
[exit 0]
```

```text
$ git rev-parse HEAD
94ae4257089b2a86137fd05c3556bed2bdfb771e
[exit 0]
```

```text
$ git rev-parse feature/message
ceb77980e4097b89613c046e50ce42362c434c3b
[exit 0]
```

```text
$ git merge feature/message
Auto-merging src/main.py
CONFLICT (content): Merge conflict in src/main.py
Automatic merge failed; fix conflicts and then commit the result.
[exit 1]
```

```text
$ git status --short
UU src/main.py
[exit 0]
```

```text
$ git diff --cc
diff --cc src/main.py
index de9dd6f,cd3ff12..0000000
--- a/src/main.py
+++ b/src/main.py
@@@ -1,1 -1,1 +1,5 @@@
++<<<<<<< HEAD
 +print("Hello from MAIN")
++=======
+ print("Hello from FEATURE")
++>>>>>>> feature/message
[exit 0]
```

```text
$ git add src/main.py
[exit 0]
```

```text
$ git commit -m Resolve conflict 1: combine the greeting into the course message
[main ddabf2d] Resolve conflict 1: combine the greeting into the course message
[exit 0]
```

```text
$ git rev-parse HEAD
ddabf2d4584e96833d6be73aa28c069eb54a664c
[exit 0]
```

```text
$ git rev-list --parents -n 1 HEAD
ddabf2d4584e96833d6be73aa28c069eb54a664c 94ae4257089b2a86137fd05c3556bed2bdfb771e ceb77980e4097b89613c046e50ce42362c434c3b
[exit 0]
```

```text
$ git status --short
[exit 0]
```

```text
$ python src/main.py
Hello from Git course
[exit 0]
```

```text
$ git log --oneline --graph --decorate --all
*   ddabf2d (HEAD -> main) Resolve conflict 1: combine the greeting into the course message
|\  
| * ceb7798 (feature/message) Change message in feature
* | 94ae425 Change message in main
|/  
* c671a74 (feature/greeting) Add personalized greeting
* a4e9552 Add gitignore rules
* 01e679b Add config and notes
* d9fdf5a Update app and documentation
* 7be85bd Update greeting
* 08c716b Add main program
* 746885e Initial commit
[exit 0]
```


## Task 9 — transport rehearsal; actual GitHub push still requires authenticated access

This bare remote is a local transport rehearsal, not GitHub. Publication to GitHub is tracked separately.

```text
$ git init --bare -b main C:\Users\mmrkr\Documents\Codex\2026-10-08\i-x20\work\git-practice-origin.git
Initialized empty Git repository in C:/Users/mmrkr/Documents/Codex/2026-10-08/i-x20/work/git-practice-origin.git/
[exit 0]
```

```text
$ git remote add origin C:\Users\mmrkr\Documents\Codex\2026-10-08\i-x20\work\git-practice-origin.git
[exit 0]
```

```text
$ git remote -v
origin	C:\Users\mmrkr\Documents\Codex\2026-10-08\i-x20\work\git-practice-origin.git (fetch)
origin	C:\Users\mmrkr\Documents\Codex\2026-10-08\i-x20\work\git-practice-origin.git (push)
[exit 0]
```

```text
$ git push -u origin main
      0 [main] sh (14320) C:\Users\mmrkr\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\usr\bin\sh.exe: *** fatal error - NtCreateDirectoryObject(\BaseNamedObjects\msys-2.0S5-b2518d5437aab8ba): 0xC0000022
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
[exit 128]
```

```text
$ git rev-list --parents -n 1 HEAD
error: missing config value GIT_CONFIG_VALUE_0
fatal: unable to parse command-line config
[exit 128]
```

```text
$ git rev-list --parents -n 1 HEAD
ddabf2d4584e96833d6be73aa28c069eb54a664c 94ae4257089b2a86137fd05c3556bed2bdfb771e ceb77980e4097b89613c046e50ce42362c434c3b
[exit 0]
```


## Task 9 — actual GitHub push, fetch and pull

```text
$ git remote set-url origin https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation.git
[exit 0]
```

```text
$ git remote -v
origin	https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation.git (fetch)
origin	https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation.git (push)
[exit 0]
```

```text
$ git push -u origin main:refs/heads/git-practice/main
branch 'main' set up to track 'origin/git-practice/main'.
remote: 
remote: Create a pull request for 'git-practice/main' on GitHub by visiting:        
remote:      https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation/pull/new/git-practice/main        
remote: 
To https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation.git
 * [new branch]      main -> git-practice/main
[exit 0]
```

```text
$ git fetch origin
From https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation
 * [new branch]      main       -> origin/main
[exit 0]
```

```text
$ git branch -vv
  feature/greeting c671a74 Add personalized greeting
  feature/message  ceb7798 Change message in feature
* main             ddabf2d [origin/git-practice/main] Resolve conflict 1: combine the greeting into the course message
[exit 0]
```

```text
$ git pull --ff-only
Already up to date.
[exit 0]
```

```text
$ git status --short
[exit 0]
```


## Task 10 — two working copies, one remote; simulated roles, not two human students

```text
$ git clone -b git-practice/main https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation.git C:\Users\mmrkr\Documents\Codex\2026-10-08\i-x20\work\git-practice-copy-a
Cloning into 'C:\Users\mmrkr\Documents\Codex\2026-10-08\i-x20\work\git-practice-copy-a'...
[exit 0]
```

```text
$ git clone -b git-practice/main https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation.git C:\Users\mmrkr\Documents\Codex\2026-10-08\i-x20\work\git-practice-copy-b
Cloning into 'C:\Users\mmrkr\Documents\Codex\2026-10-08\i-x20\work\git-practice-copy-b'...
[exit 0]
```

```text
$ git config user.name SaytomoMotion
[exit 0]
```

```text
$ git config user.email 155469523+SaytomoMotion@users.noreply.github.com
[exit 0]
```

```text
$ git config commit.gpgsign false
[exit 0]
```

```text
$ git config core.autocrlf false
[exit 0]
```

```text
$ git config user.name SaytomoMotion
[exit 0]
```

```text
$ git config user.email 155469523+SaytomoMotion@users.noreply.github.com
[exit 0]
```

```text
$ git config commit.gpgsign false
[exit 0]
```

```text
$ git config core.autocrlf false
[exit 0]
```

```text
$ git branch -m main
[exit 0]
```

```text
$ git branch -m main
[exit 0]
```

```text
$ git switch -c feature/header
Switched to a new branch 'feature/header'
[exit 0]
```

```text
$ git add header.txt
[exit 0]
```

```text
$ git commit -m Add header
[feature/header cef96c7] Add header
 1 file changed, 1 insertion(+)
 create mode 100644 header.txt
[exit 0]
```

```text
$ git rev-parse HEAD
cef96c735783cda5556ee0a7c9aa37fe009dcc92
[exit 0]
```

```text
$ git push -u origin feature/header:refs/heads/git-practice/feature/header
branch 'feature/header' set up to track 'origin/git-practice/feature/header'.
remote: 
remote: Create a pull request for 'git-practice/feature/header' on GitHub by visiting:        
remote:      https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation/pull/new/git-practice/feature/header        
remote: 
To https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation.git
 * [new branch]      feature/header -> git-practice/feature/header
[exit 0]
```

```text
$ git switch -c feature/footer
Switched to a new branch 'feature/footer'
[exit 0]
```

```text
$ git add footer.txt
[exit 0]
```

```text
$ git commit -m Add footer
[feature/footer 9c11445] Add footer
 1 file changed, 1 insertion(+)
 create mode 100644 footer.txt
[exit 0]
```

```text
$ git rev-parse HEAD
9c11445e9b55abce538c1659d77257053865919c
[exit 0]
```

```text
$ git push -u origin feature/footer:refs/heads/git-practice/feature/footer
branch 'feature/footer' set up to track 'origin/git-practice/feature/footer'.
remote: 
remote: Create a pull request for 'git-practice/feature/footer' on GitHub by visiting:        
remote:      https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation/pull/new/git-practice/feature/footer        
remote: 
To https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation.git
 * [new branch]      feature/footer -> git-practice/feature/footer
[exit 0]
```

```text
$ git fetch origin
From https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation
 * [new branch]      git-practice/feature/footer -> origin/git-practice/feature/footer
 * [new branch]      git-practice/feature/header -> origin/git-practice/feature/header
[exit 0]
```

```text
$ git merge origin/git-practice/feature/header
Updating ddabf2d..cef96c7
Fast-forward
 header.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 header.txt
[exit 0]
```

```text
$ git merge --no-edit origin/git-practice/feature/footer
Merge made by the 'ort' strategy.
 footer.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 footer.txt
[exit 0]
```

```text
$ git push origin main:refs/heads/git-practice/main
To https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation.git
   ddabf2d..0d77d0e  main -> git-practice/main
[exit 0]
```

```text
$ git switch main
M	.gitignore
M	README.md
M	config.txt
M	notes.txt
M	src/main.py
Your branch is up to date with 'origin/git-practice/main'.
Switched to branch 'main'
[exit 0]
```

```text
$ git pull --ff-only
Updating ddabf2d..0d77d0e
Fast-forward
 footer.txt | 1 +
 header.txt | 1 +
 2 files changed, 2 insertions(+)
 create mode 100644 footer.txt
 create mode 100644 header.txt
From https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation
   ddabf2d..0d77d0e  git-practice/main -> origin/git-practice/main
 * [new branch]      git-practice/feature/footer -> origin/git-practice/feature/footer
[exit 0]
```

```text
$ git switch main
M	.gitignore
M	README.md
M	config.txt
M	notes.txt
M	src/main.py
Your branch is up to date with 'origin/git-practice/main'.
Switched to branch 'main'
[exit 0]
```

```text
$ git pull --ff-only
Updating ddabf2d..0d77d0e
Fast-forward
 footer.txt | 1 +
 header.txt | 1 +
 2 files changed, 2 insertions(+)
 create mode 100644 footer.txt
 create mode 100644 header.txt
From https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation
   ddabf2d..0d77d0e  git-practice/main -> origin/git-practice/main
 * [new branch]      git-practice/feature/header -> origin/git-practice/feature/header
[exit 0]
```

```text
$ git switch -c feature/readme-a
Switched to a new branch 'feature/readme-a'
[exit 0]
```

```text
$ git switch -c feature/readme-b
Switched to a new branch 'feature/readme-b'
[exit 0]
```

```text
$ git add README.md
[exit 0]
```

```text
$ git commit -m Clarify README title in role A
[feature/readme-a 65bd8bc] Clarify README title in role A
 1 file changed, 1 insertion(+), 1 deletion(-)
[exit 0]
```

```text
$ git rev-parse HEAD
65bd8bc9020ed49f6b8dcd1f5dda31b845957a1f
[exit 0]
```

```text
$ git add README.md
[exit 0]
```

```text
$ git commit -m Clarify README title in role B
[feature/readme-b 2b06a31] Clarify README title in role B
 1 file changed, 1 insertion(+), 1 deletion(-)
[exit 0]
```

```text
$ git rev-parse HEAD
2b06a31bae2af48778e9551ffe1029ea539ccc16
[exit 0]
```

```text
$ git push -u origin feature/readme-a:refs/heads/git-practice/feature/readme-a
branch 'feature/readme-a' set up to track 'origin/git-practice/feature/readme-a'.
remote: 
remote: Create a pull request for 'git-practice/feature/readme-a' on GitHub by visiting:        
remote:      https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation/pull/new/git-practice/feature/readme-a        
remote: 
To https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation.git
 * [new branch]      feature/readme-a -> git-practice/feature/readme-a
[exit 0]
```

```text
$ git push -u origin feature/readme-b:refs/heads/git-practice/feature/readme-b
branch 'feature/readme-b' set up to track 'origin/git-practice/feature/readme-b'.
remote: 
remote: Create a pull request for 'git-practice/feature/readme-b' on GitHub by visiting:        
remote:      https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation/pull/new/git-practice/feature/readme-b        
remote: 
To https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation.git
 * [new branch]      feature/readme-b -> git-practice/feature/readme-b
[exit 0]
```

```text
$ git fetch origin
From https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation
 * [new branch]      git-practice/feature/readme-a -> origin/git-practice/feature/readme-a
 * [new branch]      git-practice/feature/readme-b -> origin/git-practice/feature/readme-b
[exit 0]
```

```text
$ git merge origin/git-practice/feature/readme-a
Updating 0d77d0e..65bd8bc
Fast-forward
 README.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
[exit 0]
```

```text
$ git rev-parse HEAD
65bd8bc9020ed49f6b8dcd1f5dda31b845957a1f
[exit 0]
```

```text
$ git rev-parse origin/git-practice/feature/readme-b
2b06a31bae2af48778e9551ffe1029ea539ccc16
[exit 0]
```

```text
$ git merge origin/git-practice/feature/readme-b
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
Automatic merge failed; fix conflicts and then commit the result.
[exit 1]
```

```text
$ git status --short
UU README.md
[exit 0]
```

```text
$ git diff --cc
diff --cc README.md
index 84937df,23dd49a..0000000
--- a/README.md
+++ b/README.md
@@@ -1,4 -1,4 +1,8 @@@
++<<<<<<< HEAD
 +# Git practice by role A
++=======
+ # Git practice by role B
++>>>>>>> origin/git-practice/feature/readme-b
  
  ## Usage
  Run python src/main.py.
[exit 0]
```

```text
$ git add README.md
[exit 0]
```

```text
$ git commit -m Resolve conflict 2: retain both simulated roles in the README title
[main 6269a28] Resolve conflict 2: retain both simulated roles in the README title
[exit 0]
```

```text
$ git rev-parse HEAD
6269a28507a000bab2ea1810e0133d71769ff2ff
[exit 0]
```

```text
$ git rev-list --parents -n 1 HEAD
6269a28507a000bab2ea1810e0133d71769ff2ff 65bd8bc9020ed49f6b8dcd1f5dda31b845957a1f 2b06a31bae2af48778e9551ffe1029ea539ccc16
[exit 0]
```

```text
$ git status --short
[exit 0]
```

```text
$ python src/main.py
Hello from Git course
[exit 0]
```

```text
$ git push origin main:refs/heads/git-practice/main
To https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation.git
   0d77d0e..6269a28  main -> git-practice/main
[exit 0]
```


## Additional configuration conflict, conflict 3 of 3

```text
$ git switch -c feature/config
Switched to a new branch 'feature/config'
[exit 0]
```

```text
$ git add config.txt
[exit 0]
```

```text
$ git commit -m Set feature configuration to test mode
[feature/config ef8e292] Set feature configuration to test mode
 1 file changed, 1 insertion(+), 1 deletion(-)
[exit 0]
```

```text
$ git rev-parse HEAD
ef8e2928fc3d9d4c3fc6ea72f7f0dd7189021f67
[exit 0]
```

```text
$ git switch main
Your branch is up to date with 'origin/git-practice/main'.
Switched to branch 'main'
[exit 0]
```

```text
$ git add config.txt
[exit 0]
```

```text
$ git commit -m Set main configuration to production mode
[main e57c5b5] Set main configuration to production mode
 1 file changed, 1 insertion(+), 1 deletion(-)
[exit 0]
```

```text
$ git rev-parse HEAD
e57c5b5e024034bd3452aa5d989dc87b06e492ca
[exit 0]
```

```text
$ git rev-parse HEAD
e57c5b5e024034bd3452aa5d989dc87b06e492ca
[exit 0]
```

```text
$ git rev-parse feature/config
ef8e2928fc3d9d4c3fc6ea72f7f0dd7189021f67
[exit 0]
```

```text
$ git merge feature/config
Auto-merging config.txt
CONFLICT (content): Merge conflict in config.txt
Automatic merge failed; fix conflicts and then commit the result.
[exit 1]
```

```text
$ git status --short
UU config.txt
[exit 0]
```

```text
$ git diff --cc
diff --cc config.txt
index 92bae99,806ca51..0000000
--- a/config.txt
+++ b/config.txt
@@@ -1,1 -1,1 +1,5 @@@
++<<<<<<< HEAD
 +mode=production
++=======
+ mode=test
++>>>>>>> feature/config
[exit 0]
```

```text
$ git add config.txt
[exit 0]
```

```text
$ git commit -m Resolve conflict 3: keep the practice environment in development mode
[main 9a13e4f] Resolve conflict 3: keep the practice environment in development mode
[exit 0]
```

```text
$ git rev-parse HEAD
9a13e4ff0f157c55941ecaaa1001840717de1837
[exit 0]
```

```text
$ git rev-list --parents -n 1 HEAD
9a13e4ff0f157c55941ecaaa1001840717de1837 e57c5b5e024034bd3452aa5d989dc87b06e492ca ef8e2928fc3d9d4c3fc6ea72f7f0dd7189021f67
[exit 0]
```

```text
$ git status --short
[exit 0]
```

```text
$ python src/main.py
Hello from Git course
[exit 0]
```

```text
$ git push origin main:refs/heads/git-practice/main
To https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation.git
   6269a28..9a13e4f  main -> git-practice/main
[exit 0]
```

```text
$ git push origin feature/greeting:refs/heads/git-practice/feature/greeting feature/message:refs/heads/git-practice/feature/message feature/config:refs/heads/git-practice/feature/config
To https://github.com/SaytomoMotion/software-implementation-and-maintenance-life-cycle-and-process-automation.git
 * [new branch]      feature/greeting -> git-practice/feature/greeting
 * [new branch]      feature/message -> git-practice/feature/message
 * [new branch]      feature/config -> git-practice/feature/config
[exit 0]
```

```text
$ git fetch origin
[exit 0]
```

```text
$ git pull --ff-only
Already up to date.
[exit 0]
```

```text
$ git branch -vv
  feature/config   ef8e292 Set feature configuration to test mode
  feature/greeting c671a74 Add personalized greeting
  feature/message  ceb7798 Change message in feature
* main             9a13e4f [origin/git-practice/main] Resolve conflict 3: keep the practice environment in development mode
[exit 0]
```

```text
$ git log --oneline --graph --decorate --all
*   9a13e4f (HEAD -> main, origin/git-practice/main) Resolve conflict 3: keep the practice environment in development mode
|\  
| * ef8e292 (origin/git-practice/feature/config, feature/config) Set feature configuration to test mode
* | e57c5b5 Set main configuration to production mode
|/  
*   6269a28 Resolve conflict 2: retain both simulated roles in the README title
|\  
| * 2b06a31 (origin/git-practice/feature/readme-b) Clarify README title in role B
* | 65bd8bc (origin/git-practice/feature/readme-a) Clarify README title in role A
|/  
*   0d77d0e Merge remote-tracking branch 'origin/git-practice/feature/footer'
|\  
| * 9c11445 (origin/git-practice/feature/footer) Add footer
* | cef96c7 (origin/git-practice/feature/header) Add header
|/  
*   ddabf2d Resolve conflict 1: combine the greeting into the course message
|\  
| * ceb7798 (origin/git-practice/feature/message, feature/message) Change message in feature
* | 94ae425 Change message in main
|/  
* c671a74 (origin/git-practice/feature/greeting, feature/greeting) Add personalized greeting
* a4e9552 Add gitignore rules
* 01e679b Add config and notes
* d9fdf5a Update app and documentation
* 7be85bd Update greeting
* 08c716b Add main program
* 746885e Initial commit
* cd42f04 (origin/main, origin/HEAD) docs: provide startup commands and links to course exercises
* 3eaa245 docs: record the purpose of the thirty course-project changes
* fcdc665 docs: plan three later conflicts with explicit resolution evidence
* 0eb93ec docs: map behavioral risks to unit and process checks
* 163b85b docs: document safe backups diagnosis and change recovery
* 778c72c docs: specify JSON schema compatibility and storage limits
* dd47029 docs: explain domain service storage and CLI responsibilities
* dc31fb0 docs: map the ten practical tasks and separate later conflict work
* a85b3a5 docs: distinguish staging restoration and remote synchronization commands
* 32f087b docs: answer the automation prioritization exercise with explicit estimates
* 90765e8 docs: summarize reproducible environments and maintenance fundamentals
* 86b13a5 docs: explain Git states coherent history and review workflows
* 6d2c5a1 docs: summarize lifecycle quality and shared responsibility
* a037c3c docs: define task tracker requirements and acceptance criteria
* 0750175 ci: run the same Python checks for pushes and pull requests
* 05cb2da chore: declare the tested Python runtime
* c8c96ce test: verify persisted tasks across separate CLI processes
* ebff27b test: cover CLI output validation filters and safe failures
* 11d705b feat: support running the tracker as a Python module
* 243905f feat: expose task commands with explicit data paths and safe errors
* 29cd910 test: verify service filtering and missing-task handling
* 198a286 feat: add list and complete tasks through a storage-independent service
* dbf20c6 test: check persistence corruption and failed writes
* 04d1663 feat: persist versioned task data with atomic file replacement
* a5fe9ec test: verify task identity completion and record validation
* 7c32611 feat: introduce immutable tasks with validated JSON records
* 371a0ca test: cover blank oversized and unsafe task inputs
* 73e8aa9 feat: validate task titles and identifiers
* 4b1a203 chore: define the task tracker package and version
* 611d4f1 chore: exclude local task data and generated Python files
* 496ecc5 Initial commit
[exit 0]
```

```text
$ git status --short
[exit 0]
```


## Portable history archive and integrity check

```text
$ git bundle create C:\Users\mmrkr\Documents\Codex\2026-10-08\i-x20\outputs\git-practical-evidence\git-practice.bundle --all
[exit 0]
```

```text
$ git bundle verify C:\Users\mmrkr\Documents\Codex\2026-10-08\i-x20\outputs\git-practical-evidence\git-practice.bundle
The bundle contains these 15 refs:
ef8e2928fc3d9d4c3fc6ea72f7f0dd7189021f67 refs/heads/feature/config
c671a746820bc659a0d43529b5825d0697e3449a refs/heads/feature/greeting
ceb77980e4097b89613c046e50ce42362c434c3b refs/heads/feature/message
9a13e4ff0f157c55941ecaaa1001840717de1837 refs/heads/main
cd42f043601a9df68336f1c450b8a55dbc84d1a1 refs/remotes/origin/HEAD
ef8e2928fc3d9d4c3fc6ea72f7f0dd7189021f67 refs/remotes/origin/git-practice/feature/config
9c11445e9b55abce538c1659d77257053865919c refs/remotes/origin/git-practice/feature/footer
c671a746820bc659a0d43529b5825d0697e3449a refs/remotes/origin/git-practice/feature/greeting
cef96c735783cda5556ee0a7c9aa37fe009dcc92 refs/remotes/origin/git-practice/feature/header
ceb77980e4097b89613c046e50ce42362c434c3b refs/remotes/origin/git-practice/feature/message
65bd8bc9020ed49f6b8dcd1f5dda31b845957a1f refs/remotes/origin/git-practice/feature/readme-a
2b06a31bae2af48778e9551ffe1029ea539ccc16 refs/remotes/origin/git-practice/feature/readme-b
9a13e4ff0f157c55941ecaaa1001840717de1837 refs/remotes/origin/git-practice/main
cd42f043601a9df68336f1c450b8a55dbc84d1a1 refs/remotes/origin/main
9a13e4ff0f157c55941ecaaa1001840717de1837 HEAD
The bundle records a complete history.
The bundle uses this hash algorithm: sha1
C:/Users/mmrkr/Documents/Codex/2026-10-08/i-x20/outputs/git-practical-evidence/git-practice.bundle is okay
[exit 0]
```

```text
$ git fsck --full
dangling blob cae4c1704861c0026a871d416aa0d26eddfe76c4
dangling tree 093f1565d297139cd0456108d3d910c1675a6f52
dangling tree 230988a76570d1f03119acedbd057f05e079e5b3
dangling tree c7b7692e9adc1f558270d8bc8d088508af5f20c0
[exit 0]
```
