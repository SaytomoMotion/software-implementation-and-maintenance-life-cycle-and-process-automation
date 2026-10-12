# Architecture

The CLI parses arguments and prints results. TaskService implements add, list and complete use cases.
Task owns validated immutable values. JsonStore converts validated records into a versioned JSON file.
Validation rules are shared instead of repeated at each boundary.

Data flows from CLI arguments to service methods, into the model and store, then back as task values.
The service accepts a store object with load/save operations. Tests use an in-memory substitute;
the application uses JsonStore. Business behavior therefore does not depend on terminal formatting.

Completion returns a replacement Task, retaining its ID and title. No operation mutates an existing
Task. Storage validation rejects unknown fields and duplicate IDs so invalid files do not look valid.

The layers are intentionally small. A network API, database and dependency-injection framework would
add complexity without serving the present single-user requirements.
