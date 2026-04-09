---
name: postgresql-migration
description: "Migrate SQL and PL/SQL code to PostgreSQL. Use whenever the TARGET database is PostgreSQL—regardless of the source (Oracle, MySQL, SQL Server, etc.). Invoke for DDL migration (tables, sequences, triggers, views, indexes), DML conversion, PL/pgSQL function and procedure generation, or when the user mentions migrating stored procedures, database schemas, or SQL scripts to PostgreSQL. Also includes a review checklist for validating migrated PostgreSQL scripts."
---

# PostgreSQL Migration Skill

This skill guides migration of any relational database code to **PostgreSQL**. All core rules focus on correct PostgreSQL output. References to Oracle syntax appear only as "before" examples — the rules themselves apply to any source producing PostgreSQL-compatible output.

## Core Rules (apply to all migrations)

- Exclude schema name qualifiers from all object definitions. `CREATE TABLE "MYSCHEMA"."DEPARTMENTS"` → `CREATE TABLE DEPARTMENTS`.
- Do not add a duplicate `PRIMARY KEY` constraint if one already exists on the table.
- Ensure no trailing comma after the last column in a `CREATE TABLE` statement.
- Move inline comments inside `CREATE TABLE` parentheses to outside the definition.
- Treat all identifiers as case-insensitive unless they were explicitly quoted in the source.
- Preserve all comments from the original SQL in the migrated file.
- Test each migrated file for successful execution and correct object creation.

## Quick Reference: Data Type Mapping

| Source Type | PostgreSQL Type |
|------------|----------------|
| NUMBER(p, 0) / INTEGER | `INTEGER` or `BIGINT` |
| NUMBER(p, s) | `NUMERIC(p, s)` |
| VARCHAR2(n) / NVARCHAR2(n) | `VARCHAR(n)` |
| DATE | `DATE` or `TIMESTAMP` (context-dependent) |
| TIMESTAMP | `TIMESTAMP` |
| TIMESTAMP WITH TIME ZONE | `TIMESTAMPTZ` |
| CLOB / LONG | `TEXT` |
| BLOB / LONG RAW / BFILE | `BYTEA` |
| RAW | `BYTEA` or `UUID` |
| ROWID / UROWID | `TEXT` |
| FLOAT / BINARY_DOUBLE | `DOUBLE PRECISION` |
| BINARY_FLOAT | `REAL` |
| CHAR(n) | `CHAR(n)` |
| XMLTYPE | `XML` |
| INTERVAL YEAR TO MONTH | `INTERVAL` |
| INTERVAL DAY TO SECOND | `INTERVAL` |

## Reference Files

| Task | Reference |
|------|-----------|
| Full migration rules (DDL, DML, PL/pgSQL, sequences, triggers, etc.) | [references/sql-migration-rules.md](references/sql-migration-rules.md) |
| Review checklist (post-migration validation) | [references/review-checklist.md](references/review-checklist.md) |
| DevOps error handling (resolving execution errors) | [references/devops-error-handling.md](references/devops-error-handling.md) |

When generating or reviewing PostgreSQL output, **always** read `references/sql-migration-rules.md` first. For review tasks, also read `references/review-checklist.md`.
