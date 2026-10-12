# Automation prioritization exercise

Lecture 0, slide 6 asks for a repeated activity, its manual cost and error cost, and an automation decision.
The following numbers are planning assumptions, not measurements.

Activity: compiling source and running the complete task tracker test suite before sharing a change.
Assume 30 changes, 4 minutes of manual command selection and checking per change, and 2 minutes
with one documented workflow. Assume 30 minutes to prepare and maintain the workflow.

Manual effort: 30 x 4 = 120 minutes. Automated effort: 30 + 30 x 2 = 90 minutes.
Estimated saving: 30 minutes. Time-only break-even: 30 / (4 - 2) = 15 runs.
The application runtime and test execution time remain; automation mainly removes forgotten steps.

If a missed check produces a defect, assume 20 minutes of later debugging. Its probability is unknown,
so do not add speculative incident savings to the calculation. Repeatability is an additional benefit.

Automate compilation and tests now using the same commands locally and in CI. Postpone a deployment
pipeline and a container setup until the project actually needs them. Revisit this decision as usage changes.

Success means all checks complete successfully. A failed command should stop the CI job and identify
the failing check. A successful exit alone is insufficient if the suite tests no meaningful behavior.
