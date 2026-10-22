# Test plan

Run python -m unittest discover -s tests -v from the repository root.

| Risk | Check |
| --- | --- |
| Bad title, client, date, status or format | Model and CLI rejection tests |
| Lost briefs, formats or status | SQLite persistence and separate process tests |
| Exceeded revision budget | Conditional update, explicit override and two-connection checks |
| Wrong overdue results | Fixed dates, including delivered projects |
| Migration loses records | Version-1 fixture, preserved fields and default values |
| Unusable backup | Open backup and verify original schema and row |
| Partially applied migration | Inject failure after ALTER TABLE; verify rollback |
| Unsupported database changed | Future and unversioned databases retain original bytes |
| Dry run writes data | Filesystem and schema checks |
| Legacy import changes source or duplicates work | Byte comparison and repeated import |
| Partial import | Validation and trigger-induced rollback |
| Unstable build | Byte and checksum comparison |
| Package lacks SQL or depends on checkout | Packaged app run from an isolated directory |

Legacy task-tracker tests remain for compatibility. All test projects use synthetic clients and
temporary files. No production deployment, rendering, payment or multi-user stress test is claimed.
