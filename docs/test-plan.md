# Test plan

Run from the repository root:

```text
python -m compileall -q tasktracker tests
python -m unittest discover -s tests -v
```

| Risk | Verification |
| --- | --- |
| Blank, oversized or terminal-control title | Validation boundary and rejection tests |
| Invalid task fields or completion type | Model record validation tests |
| State lost between commands | Separate-process lifecycle test |
| Corrupt data silently overwritten | Storage corruption-preservation test |
| Unsupported schema or duplicate IDs accepted | Storage schema tests |
| Failed replacement destroys previous data | Mocked replacement failure and cleanup test |
| Completion changes identity or creates duplicates | Model and service idempotence tests |
| Filtering returns the wrong tasks | Service and CLI status tests |
| CLI failure looks successful | Nonzero status and safe stderr tests |

The suite does not prove concurrent writes, hardware crash durability or every operating-system
permission failure. These remain outside the scope. CI repeats the same commands on Linux;
local checks also exercise the code on the development platform.
