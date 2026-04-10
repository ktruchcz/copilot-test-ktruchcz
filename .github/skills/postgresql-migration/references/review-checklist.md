# PostgreSQL Migration Review Checklist

Use this checklist when reviewing PostgreSQL code that was migrated from another database (e.g., Oracle, MySQL). It complements the generation rules in `sql-migration-rules.md`.

## 1. General

- All Oracle-specific constructs are properly converted to PostgreSQL equivalents.
- No hardcoded configuration or environment variables.
- Code is modular and testable.

## 2. Data Types & Table Definitions

- [ ] All source data types are mapped to correct PostgreSQL equivalents:
  - `NUMBER` → `NUMERIC`, `INTEGER`, or `BIGINT` (check precision/scale)
  - `VARCHAR2` → `VARCHAR`
  - `DATE` → `DATE` or `TIMESTAMP` (as appropriate)
  - `CLOB`/`BLOB` → `TEXT`/`BYTEA`
  - `RAW` → `BYTEA`
  - `NVARCHAR2` → `VARCHAR`
  - `LONG` → `TEXT`
  - `FLOAT` → `DOUBLE PRECISION`
  - `ROWID`/`UROWID` → `UUID` or `TEXT`
  - Oracle `OBJECT`, `TABLE`, `VARRAY` → JSONB, composite type, or separate tables
- [ ] Oracle `SEQUENCE` + trigger auto-increment → PostgreSQL `SERIAL` or `GENERATED ALWAYS AS IDENTITY`
- [ ] Default values use PostgreSQL syntax (`DEFAULT now()`, `DEFAULT CURRENT_TIMESTAMP`)
- [ ] Oracle defaults (`SYSDATE`, `SYSTIMESTAMP`) replaced with PostgreSQL equivalents
- [ ] All `NOT NULL`, `UNIQUE`, `CHECK`, `FOREIGN KEY` constraints present and correctly defined
- [ ] Composite primary keys and unique constraints migrated accurately
- [ ] Oracle-only storage parameters removed (`PCTFREE`, `INITRANS`, `MAXTRANS`)
- [ ] No trailing comma after last column in `CREATE TABLE`

## 3. Sequences, Triggers, Auto-Increment

- [ ] Oracle sequences/triggers replaced with `SERIAL` or identity columns
- [ ] Custom sequences created with `DEFAULT nextval('sequence_name')`
- [ ] `ORDER` option removed from `CREATE SEQUENCE` (not supported)
- [ ] Sequence `CACHE` value preserved if present

## 4. Procedures, Functions, and Logic

- [ ] All PL/SQL rewritten using valid PL/pgSQL syntax
- [ ] Oracle-specific constructs converted: `%TYPE`, `%ROWTYPE`, `:=`, `EXECUTE IMMEDIATE`, `FORALL`
- [ ] Every function has a correct `RETURNS` clause
- [ ] Procedures (PG 11+) defined with `CREATE PROCEDURE` — no `RETURNS` clause
- [ ] All functions/procedures end with `LANGUAGE plpgsql;`
- [ ] Parameters use PostgreSQL data types
- [ ] Control structures correct: `IF`, `CASE`, `LOOP`, `EXIT`, `FOR`

## 5. Cursors and Control Structures

- [ ] All cursors use valid PL/pgSQL syntax (`FOR`, `LOOP`, `EXIT`)
- [ ] `DBMS_OUTPUT.PUT_LINE` replaced with `RAISE NOTICE`
- [ ] No remaining Oracle-specific cursor or control structure syntax

## 6. Exception Handling

- [ ] Exception blocks use PostgreSQL exception names (`unique_violation`, `division_by_zero`)
- [ ] `RAISE NOTICE`, `RAISE WARNING`, `RAISE EXCEPTION` used correctly
- [ ] `WHEN OTHERS` used only when appropriate with meaningful messages
- [ ] All `%` in `RAISE EXCEPTION` messages are either `%%` (literal) or have matching parameters
- [ ] No Oracle exception names remaining

## 7. Packages and Synonyms

- [ ] Oracle packages refactored into PostgreSQL schemas or grouped functions
- [ ] Synonym references replaced with views or `search_path`
- [ ] Package constants replaced with config tables or function parameters

## 8. DML Validation

- [ ] Every table in INSERT statements has a matching `CREATE TABLE`
- [ ] Column names in INSERT statements match the column definitions exactly
- [ ] No `relation "<table_name>" does not exist` or `column "<col>" does not exist` errors
- [ ] `DELETE FROM` used (not bare `DELETE <table>`)

## 9. Partitioned Tables

- [ ] Partition type supported in PostgreSQL (Range, List, Hash only — no Interval, Reference, or Composite)
- [ ] Primary key includes all partition key columns (or is absent if source had none)
- [ ] Partition bounds types match the column type exactly
- [ ] Subpartitioned tables redesigned into single-level partitioning

## 10. Advanced Features

- [ ] CONNECT BY hierarchical queries converted to `WITH RECURSIVE`
- [ ] Oracle JSON functions replaced with PostgreSQL JSONB equivalents
- [ ] Nested tables / VARRAY normalized to separate tables with foreign keys
- [ ] Bitmap/reverse-key indexes replaced with B-tree indexes
- [ ] Generated columns use `STORED` (not `VIRTUAL`)
- [ ] Invisible columns migrated as regular columns
