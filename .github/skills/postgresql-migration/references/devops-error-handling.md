# DevOps Error Handling: PostgreSQL Migration

When you encounter execution errors during PostgreSQL migration (missing tables, syntax errors, constraint violations, etc.):

1. Extract the **full error message** and **file path** from the error output.
2. Use a file-reading tool to read the complete content of the problematic file.
   - Note: files are under `./output`, not `/docker-entrypoint-initdb.d`.
3. If there are missing objects or unclear references, use a directory listing tool to see all available SQL files before making assumptions.
4. Read related files (e.g., other SQL scripts that might define missing tables or sequences) before creating new objects or applying fixes.
5. Do not create new objects randomly — confirm they don't already exist in other files first.

Common errors and where to look:

| Error | Likely Cause |
|-------|-------------|
| `relation "<table>" does not exist` | Table not yet created, or wrong execution order |
| `column "<col>" does not exist` | Column renamed or typo in INSERT/SELECT |
| `unique constraint ... must include all partitioning columns` | PK on partitioned table missing partition key column |
| `ERROR: loop variable ... must be a record variable` | FOR-IN-SELECT loop with multiple columns — use `RECORD` |
| `too few parameters specified for RAISE` | Literal `%` in RAISE message — use `%%` |
| `recursive query column N has type ... in non-recursive term` | Type mismatch in WITH RECURSIVE — add explicit cast |
| `CHECK constraints cannot be marked DEFERRABLE` | Remove DEFERRABLE from CHECK constraint |
