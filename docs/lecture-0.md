# Lecture 0: course introduction

Source: the supplied `0_course_introduction_2026_EN_stundents.pdf` and its study guide.

Software readiness extends beyond running on one workstation. We need to repeatedly build,
verify, deliver, observe and recover the system. The feedback loop is plan, code, verify, deliver,
operate and learn. An incident should inform the next change.

Quality includes correctness, security, maintainability, reliability and observability. A working
feature can still fail these other requirements. Fast checks reduce the delay before detecting defects.
DevOps means shared responsibility for the service outcome, with clear ownership across roles.

Automation is useful for a process with understood inputs, outputs and measurable success.
Choose work that repeats, estimate manual effort and failure cost, and include automation maintenance.
See [the completed planning exercise](automation-exercise.md).

AI suggestions still require review and checks. The person submitting work must understand it and
be able to explain the decisions. Confidence in generated text is not evidence of correctness.

The course calls for a personal Git account, a development workstation, a Linux account on
studenti.uso.lv and a separate course repository. The Linux account's setup is not completed by
creating a GitHub repository. No grading percentages or next meeting date are specified here.

## Questions to explain aloud

1. Why is local success insufficient? Undeclared versions and configuration can hide dependencies.
2. What should be automated first? A repeated process whose success and failure are understood.
3. What closes the lifecycle loop? Evidence from operation and incidents informs planning.
