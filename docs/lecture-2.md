# Lecture 2: software development fundamentals

Source: the supplied `2_software_development_fundamentals_2026_EN_stundents.pdf` and its study guide.

Six foundations support maintenance: environment, code, configuration, data, dependencies and telemetry.
A new colleague should be able to run, change and diagnose the project using the repository.

Declare important runtime and package versions and verify startup in a clean environment. Match
relevant external-service behavior rather than every hardware detail. Use synthetic development data.
A VM has its own guest kernel; a container shares a host kernel. A Dev Container declares a development
environment. A remote workstation describes where work occurs and may itself use a VM or container.

Readable code uses domain names, focused responsibilities and explicit dependencies. Formatters and
linters handle repeated style checks. Tests explain behavior. Comments preserve reasons, constraints
and trade-offs rather than restating the next line.

Code defines shared behavior. Configuration supplies environment-specific values. Secrets grant access.
Feature flags temporarily control activation and need an owner, removal condition and tests for both states.
Validate configuration early and avoid printing secret values in errors.

Schema changes must preserve compatibility while old and new versions overlap. Expand introduces the
new structure, migrate moves and verifies usage, and contract removes the old structure after active
consumers have moved. Test at realistic scale and test backup restoration against recovery requirements.

Declare dependencies, lock their resolutions, inventory components, scan and make small verified updates.
A lockfile records resolved versions. An SBOM describes components. Provenance describes build inputs
and origin. A signature supports verification of origin and integrity; these artifacts answer different questions.

Structured events use stable fields, a timezone and request/trace context. Do not log credentials or
unnecessary personal data. Severity differs from alert routing. Plan retention, access and log volume.

## Application to this repository

The motion design tracker uses SQLite with numbered migrations. Schema 2 adds revision budgets
and delivery formats to existing project records, with an automatic backup and transactional rollback.
The app validates input and uses parameterized SQL. Its build contains the SQL resources and source
revision metadata. The legacy task JSON can be imported without changing the original file.
See [migration examples](migrations.md) and [automation](automation.md).
