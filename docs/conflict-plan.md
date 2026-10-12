# Later conflict practical: plan only

The user reserved three conflicts for a later task. This file plans them; none is claimed completed.
Create each from a clean shared base, commit different edits to the same lines on two branches,
then merge to trigger a real Git conflict. Conflict markers typed into a file are not sufficient evidence.

1. Documentation: competing startup wording in README. Keep accurate commands and both useful clarifications.
2. Validation: competing title-limit changes. Agree on the final requirement and update boundary tests with it.
3. Output: competing empty-list messages in the CLI. Choose one consistent contract and update its tests.

For each conflict record the branch tips, failed merge output, unmerged status, marker-bearing file,
reason for the combined result, passing tests and resolution commit. Publish the relevant branches and
resolved history when the user starts that task. Do not leave markers on main as a substitute for resolution.

The supplied practical has code and pair-work conflicts; coordinate with a real classmate if the lecturer
requires actual pair work. Simulating two branches is not evidence that two people participated.
