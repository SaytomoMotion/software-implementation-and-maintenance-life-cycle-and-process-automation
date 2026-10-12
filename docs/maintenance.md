# Maintenance

Keep local task data under ignored data/ or provide an explicit --data path. Do not use real secrets
as task titles. The application has no secret configuration, network access or login requirement.
The --data option is ordinary configuration; source logic is code; task records are application data.

For an invalid JSON file, stop edits, preserve a copy, investigate its schema and restore a known-good
backup. For a write error, check directory access and disk availability. Errors avoid printing stored titles.
After restoring a backup, use list --json to verify records and confirm completion states.

Make backups when no writer is running. Test a restore in a separate temporary location using
--data before trusting the backup. A backup that has not been restored successfully is unverified.

For a published code regression, identify the introducing change, add a regression test and create a fix
or a reviewed revert. Run the suite before publishing. Preserve shared history rather than rewriting it.

There is no production service or defined recovery-time objective here. Set those requirements before
claiming production readiness. Keep runtime updates small and rerun the suite on the declared version.
