---
name: oracle-to-postgres-logic-and-data-convert
description: Convert Oracle SQL logic, DDL, and seed data into PostgreSQL-compatible SQL with preserved constraints, comments, and object intent. Use this whenever the user is migrating Oracle tables, DML, triggers, sequences, PL/SQL fragments, or mixed schema-plus-data scripts to PostgreSQL, even if they only say "make this run on Postgres".
---

# Oracle to Postgres Logic and Data Convert

Generate PostgreSQL output that is executable, not merely syntactically similar to Oracle.

## Required inputs

- Oracle SQL or PL/SQL source files
- Schema definitions and seed data if they are split across files
- Execution errors, when the task is a repair pass

## Workflow

1. Read [references/sql-rules.md](references/sql-rules.md) before converting anything.
2. If the task is a review or fix pass, also read [references/review.md](references/review.md).
3. Remove Oracle-only syntax, convert types and functions, and preserve constraints and comments.
4. Check DDL and DML together so table names, column names, and execution order remain consistent.
5. If the prompt includes runtime errors, resolve them using the same migration rules instead of ad hoc workarounds.

## Output contract

- Output PostgreSQL-compatible SQL.
- Preserve comments and database intent.
- Avoid introducing new objects unless the source semantics require them.

## Reference files

- [references/sql-rules.md](references/sql-rules.md): migration rules for DDL, DML, functions, sequences, and Oracle syntax replacement.
- [references/review.md](references/review.md): validation and troubleshooting checklist.
