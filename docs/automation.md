# Automation

GitHub Actions runs on pushes, pull requests and manual dispatch. It uses the declared Python
version, compiles source, runs all tests, rehearses a version-1-to-2 database upgrade, builds the
application, checks the packaged CLI, then uploads the .pyz and SHA-256 checksum.

External actions are pinned to specific commits. Repository permissions are read-only.
Build files contain code, SQL and source revision metadata; no client databases or credentials.

Local commands:

```text
python -m compileall -q motiontracker tasktracker scripts examples tests
python -m unittest discover -s tests -v
python -m scripts.build
python dist/motiondesk.pyz --help
```

The build fixes file ordering and ZIP metadata and normalizes line endings. Identical source
and revision values produce identical bytes. A changed source revision intentionally changes
the checksum. Tests compare two builds and run the packaged app from an isolated folder.

This is continuous integration and artifact creation, with no production deployment.
The app still needs Python 3.12. It does not render videos or contact clients.
