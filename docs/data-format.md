# Data format

The file is UTF-8 JSON containing exactly schema_version and tasks. Version 1 is an integer.
Each task has exactly id, title and completed. IDs are unique canonical lowercase UUID strings,
titles are trimmed text of 1-200 characters without control characters, and completed is boolean.

```json
{
  "schema_version": 1,
  "tasks": [
    {
      "id": "12345678-1234-4234-8234-123456789abc",
      "title": "Read lecture 0",
      "completed": false
    }
  ]
}
```

A missing file means an empty list. Malformed data or an unsupported version produces an error.
The program must not replace it with an empty list. Preserve the original before investigating.

Saving writes and flushes a temporary file beside the destination, then replaces the destination.
This prevents a partial destination write. It is not a multi-process lock or a complete guarantee
against all hardware failures. Only one writer should use a data file at a time.

For a future schema change, design an explicit migration, backup first, test old records and
verify the result before switching readers. Do not infer a migration just from the version number.
