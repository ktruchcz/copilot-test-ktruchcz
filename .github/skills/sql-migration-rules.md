# PostgreSQL SQL Migration Rules

Comprehensive rules for migrating SQL/DDL/DML and PL/SQL to PostgreSQL. Source examples (Oracle syntax) are shown as "before" context; PostgreSQL is always the output.

## Table of Contents

1. [General Rules](#1-general-rules)
2. [Constraints](#2-constraints)
3. [DML Table Name Checklist](#3-dml-table-name-checklist)
4. [DELETE Statement](#4-delete-statement)
5. [Dual Table](#5-dual-table)
6. [Empty Strings and NULL](#6-empty-strings-and-null)
7. [Hierarchical Queries](#7-hierarchical-queries)
8. [Joins](#8-joins)
9. [Packages](#9-packages)
10. [PL/SQL to PL/pgSQL](#10-plsql-to-plpgsql)
11. [Sequences](#11-sequences)
12. [Synonyms / search_path](#12-synonyms--search_path)
13. [Date Functions](#13-date-functions)
14. [Transactions](#14-transactions)
15. [Temporary Tables and Materialized Views](#15-temporary-tables-and-materialized-views)
16. [Foreign Keys](#16-foreign-keys)
17. [Indexes](#17-indexes)
18. [Partitioned Tables](#18-partitioned-tables)
19. [Advanced Data Types and Collections](#19-advanced-data-types-and-collections)
20. [Generated Columns and Invisible Columns](#20-generated-columns-and-invisible-columns)
21. [Advanced PL/pgSQL Function Patterns](#21-advanced-plpgsql-function-patterns)
22. [REF CURSOR Functions](#22-ref-cursor-functions)
23. [CHECK Constraints with CASE](#23-check-constraints-with-case)

---

## 1. General Rules

- Exclude schema qualifiers from all object definitions: `"MYSCHEMA"."TABLE_NAME"` → `TABLE_NAME`
- Do not add a duplicate `PRIMARY KEY` if one already exists.
- No trailing comma after the last column in `CREATE TABLE`.
- Move comments inside `CREATE TABLE` parentheses to outside the table definition.
- All identifiers are case-insensitive unless explicitly quoted.
- Preserve all comments from the source in the migrated output.
- Test the final PostgreSQL SQL for successful execution.
- Auto-increment with Oracle `SEQUENCE` + trigger → PostgreSQL `SERIAL` or `GENERATED ALWAYS AS IDENTITY`.

---

## 2. Constraints

### Deferrable Constraints

- `FOREIGN KEY`, `UNIQUE`, and `EXCLUDE` constraints can be `DEFERRABLE`.
- `CHECK` constraints **cannot** be marked `DEFERRABLE` in PostgreSQL — remove the `DEFERRABLE` clause from any CHECK constraint.

```sql
-- To defer FK checks during bulk operations:
ALTER TABLE orders ADD CONSTRAINT fk_customer
  FOREIGN KEY (customer_id) REFERENCES customers(id)
  DEFERRABLE INITIALLY DEFERRED;

BEGIN;
SET CONSTRAINTS ALL DEFERRED;
-- DML here
COMMIT;
```

### NOT NULL

- `attnotnull` in `pg_attribute` tracks NOT NULL state. Apply `NOT NULL` as column constraints in `CREATE TABLE`.

---

## 3. DML Table Name Checklist

- Every table in INSERT statements must have a matching `CREATE TABLE`.
- Column names in INSERT statements must exactly match column definitions.
- Errors like `relation "<table_name>" does not exist` → check for missing CREATE TABLE or typos.
- Column names must not be changed during migration.

---

## 4. DELETE Statement

```sql
-- Source: DELETE mytable WHERE ...
-- PostgreSQL: FROM is mandatory
DELETE FROM mytable WHERE column_name = 'value';
```

---

## 5. Dual Table

```sql
-- Source: SELECT SYSDATE FROM DUAL;
-- PostgreSQL:
SELECT NOW();

-- If DUAL is required for compatibility, create a view:
CREATE VIEW dual AS SELECT 1 AS dummy;
```

---

## 6. Empty Strings and NULL

PostgreSQL empty strings (`''`) are NOT NULL. Source databases may treat empty as NULL.

```sql
-- To check for both:
WHERE mycol IS NULL OR mycol = ''
```

---

## 7. Hierarchical Queries

Source `CONNECT BY` → PostgreSQL recursive CTE:

```sql
-- Source: SELECT ... CONNECT BY PRIOR emp_id = manager_id START WITH manager_id IS NULL
WITH RECURSIVE emp_tree AS (
    SELECT emp_id, manager_id FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.emp_id, e.manager_id
    FROM employees e
    JOIN emp_tree t ON e.manager_id = t.emp_id
)
SELECT * FROM emp_tree;
```

Manually rewrite logic for LEVEL, SYS_CONNECT_BY_PATH, CONNECT_BY_ROOT, CONNECT_BY_ISLEAF.

### Recursive CTE Type Mismatch Fix

If you emulate `SYS_CONNECT_BY_PATH` with arrays or strings, cast the non-recursive term explicitly:

```sql
-- Array path:
ARRAY[last_name]::character varying[] AS hierarchy_path

-- String path:
last_name::character varying AS hierarchy_path
```

---

## 8. Joins

```sql
-- Source outer join syntax (+):
-- SELECT * FROM t1, t2 WHERE t1.id = t2.fk(+);
-- PostgreSQL:
SELECT * FROM t1 LEFT OUTER JOIN t2 ON t1.id = t2.fk;
```

---

## 9. Packages

PostgreSQL has no packages. Use schemas and grouped functions:

```sql
CREATE SCHEMA my_pkg;
CREATE OR REPLACE FUNCTION my_pkg.do_something() RETURNS void AS $$
BEGIN
  -- logic
END;
$$ LANGUAGE plpgsql;
```

Consider creating a config table for package-level constants.

---

## 10. PL/SQL to PL/pgSQL

### Basic Function

```sql
-- Source (Oracle): PROCEDURE / FUNCTION ... IS BEGIN ... END; /
-- PostgreSQL:
CREATE OR REPLACE FUNCTION hello_proc()
RETURNS void AS $$
BEGIN
  RAISE NOTICE 'Hello from PostgreSQL!';
END;
$$ LANGUAGE plpgsql;
```

Key conversions:
- `DBMS_OUTPUT.PUT_LINE(msg)` → `RAISE NOTICE '%', msg;`
- `:=` for assignment → same in PL/pgSQL (`:=` is valid)
- `%TYPE`, `%ROWTYPE` → same syntax in PL/pgSQL
- `SYSDATE` → `CURRENT_DATE` or `NOW()`
- `NVL(x, y)` → `COALESCE(x, y)`
- `DECODE(col, v1, r1, v2, r2, ...)` → `CASE WHEN ... END`
- `MONTHS_BETWEEN(d1, d2)` → `EXTRACT(MONTH FROM AGE(d1, d2))` or compute via integer arithmetic
- `EXECUTE IMMEDIATE sql USING :bind` → `EXECUTE format($f$...%L...$f$, val)` or `EXECUTE sql USING val`
- `FORALL` bulk operations → `FOREACH` loop or `unnest()` with INSERT
- `DBMS_OUTPUT.PUT_LINE` → `RAISE NOTICE`
- Custom exception variables (not predefined PG conditions) → use `RAISE EXCEPTION` + `WHEN OTHERS`

### `RAISE EXCEPTION` Percent Sign

In `RAISE EXCEPTION` messages, `%` is a format placeholder. Use `%%` for a literal percent:

```sql
RAISE EXCEPTION 'Cannot reduce salary by more than 10%%';
-- With a placeholder:
RAISE EXCEPTION 'Reduction exceeds % percent', 10;
```

### FOR-IN-SELECT Loop Variable

- Selecting one column → use a scalar variable.
- Selecting multiple columns → declare the variable as `RECORD`:

```sql
DECLARE dept_rec RECORD;
FOR dept_rec IN SELECT dept_name, dept_id FROM departments LOOP
  -- use dept_rec.dept_name, dept_rec.dept_id
END LOOP;
```

Error `loop variable of loop over rows must be a record variable` → switch to `RECORD`.

### PL/SQL Procedures vs Functions

- PostgreSQL 11+: procedures are `CREATE PROCEDURE name(...) LANGUAGE plpgsql AS $$ ... $$` — no `RETURNS` clause.
- Functions must always have a `RETURNS` clause.
- All functions/procedures end with `LANGUAGE plpgsql`.

### Exception Handling

Use PostgreSQL exception names (e.g., `unique_violation`, `division_by_zero`, `no_data_found`).  
Use `WHEN OTHERS` sparingly with meaningful error messages.

---

## 11. Sequences

```sql
-- Source: mysequence.NEXTVAL
-- PostgreSQL:
nextval('mysequence');

-- Source: CREATE SEQUENCE ... ORDER;
CREATE SEQUENCE advanced_seq
    START 1000
    INCREMENT 5
    MAXVALUE 999999999
    MINVALUE 1
    CYCLE
    CACHE 50;
-- ORDER option is not supported — omit it
```

Column default using sequence:
```sql
id INTEGER DEFAULT nextval('my_sequence') NOT NULL
-- or:
id SERIAL PRIMARY KEY
-- or:
id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
```

---

## 12. Synonyms / search_path

```sql
-- Source: CREATE SYNONYM abc.mytable FOR xyz.mytable;
-- PostgreSQL: use a view or set search_path:
SET search_path TO abc, xyz;
-- Or create a view:
CREATE VIEW mytable AS SELECT * FROM xyz.mytable;
```

---

## 13. Date Functions

| Source | PostgreSQL |
|--------|-----------|
| `SYSDATE` | `CURRENT_DATE` or `NOW()` |
| `SYSTIMESTAMP` | `CURRENT_TIMESTAMP` |
| `TO_DATE('20180314','yyyymmdd')` | `TO_DATE('20180314','yyyymmdd')` ✓ |
| `TO_DATE('string','yyyymmddhh24miss')` | `TO_TIMESTAMP('string','yyyymmddhh24miss')::TIMESTAMP(0)` |
| `MONTHS_BETWEEN(d1,d2)` | `EXTRACT(MONTH FROM AGE(d1, d2))` |
| `ADD_MONTHS(d, n)` | `d + INTERVAL 'n months'` or `d + (n || ' months')::interval` |
| `TRUNC(date,'MM')` | `DATE_TRUNC('month', date)` |

---

## 14. Transactions

PostgreSQL requires explicit `BEGIN` for multi-statement transactions:

```sql
BEGIN;
-- statements
COMMIT;
-- or ROLLBACK;
```

Default isolation level is `READ COMMITTED` in both Oracle and PostgreSQL.

---

## 15. Temporary Tables and Materialized Views

### Temporary Tables

```sql
-- Source: CREATE GLOBAL TEMPORARY TABLE ... ON COMMIT DELETE ROWS
CREATE TEMP TABLE temp_data (id INTEGER) ON COMMIT DELETE ROWS;
-- PostgreSQL temp tables are session-specific, not global
```

### Materialized Views

```sql
-- Source: CREATE MATERIALIZED VIEW mv BUILD IMMEDIATE REFRESH COMPLETE ON DEMAND AS ...
CREATE MATERIALIZED VIEW mv AS
SELECT ... FROM ...
WITH DATA;               -- populate immediately

-- To refresh manually:
REFRESH MATERIALIZED VIEW mv;

-- Without initial data:
CREATE MATERIALIZED VIEW mv AS SELECT ... WITH NO DATA;
```

---

## 16. Foreign Keys

Syntax is identical for simple and composite foreign keys:

```sql
ALTER TABLE order_items
  ADD CONSTRAINT fk_order_items
  FOREIGN KEY (order_id, product_id)
  REFERENCES orders(order_id, product_id);
```

---

## 17. Indexes

| Source Index Type | PostgreSQL |
|------------------|-----------|
| Standard B-tree | `CREATE INDEX idx ON table(col)` — identical |
| Unique | `CREATE UNIQUE INDEX idx ON table(col)` — identical |
| Bitmap | Not supported → use standard B-tree; use GIN/GiST for arrays/JSONB |
| Reverse Key | Not needed → use standard B-tree |
| Function-based | `CREATE INDEX idx ON table(UPPER(col))` — supported natively |
| IOT (Index Organized) | Use regular table + `CLUSTER` |

---

## 18. Partitioned Tables

### Partitioning Types Support

| Type | PostgreSQL Support |
|------|-------------------|
| Range | ✓ |
| List | ✓ |
| Hash | ✓ (PG 11+) |
| Interval | ✗ — create partitions manually |
| Reference | ✗ — manage independently |
| Composite/Subpartition | ✗ — use single-level only |

### Critical: Primary Keys on Partitioned Tables

- Do NOT add a primary key to a partitioned table unless the source had one.
- Any primary key or unique constraint on a partitioned table **must include all partition key columns**.

```sql
-- Range partition example:
CREATE TABLE sales (
    sale_id BIGINT,       -- no PRIMARY KEY here if source had none
    sale_date DATE NOT NULL
) PARTITION BY RANGE (sale_date);

CREATE TABLE sales_2022 PARTITION OF sales
    FOR VALUES FROM ('2022-01-01') TO ('2023-01-01');
```

### List Partition

```sql
CREATE TABLE customers (
    customer_id BIGINT,
    region VARCHAR(20)
) PARTITION BY LIST (region);

CREATE TABLE customers_east PARTITION OF customers FOR VALUES IN ('EAST');
```

### Hash Partition

```sql
CREATE TABLE orders (
    order_id BIGINT,
    order_date DATE
) PARTITION BY HASH (order_id);

CREATE TABLE orders_p0 PARTITION OF orders FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE orders_p1 PARTITION OF orders FOR VALUES WITH (MODULUS 4, REMAINDER 1);
-- etc.
```

---

## 19. Advanced Data Types and Collections

### Data Type Mapping

| Source Type | PostgreSQL Type |
|------------|----------------|
| XMLTYPE | XML |
| CLOB / LONG | TEXT |
| BLOB / LONG RAW / BFILE | BYTEA |
| RAW | BYTEA or UUID |
| ROWID / UROWID | TEXT |
| BINARY_FLOAT | REAL |
| BINARY_DOUBLE / FLOAT | DOUBLE PRECISION |
| INTERVAL YEAR TO MONTH | INTERVAL |
| INTERVAL DAY TO SECOND | INTERVAL |

### Object Types / VARRAY

Composite types are supported, but array-of-composite is not:

```sql
CREATE TYPE phone_type AS (
    phone_kind VARCHAR(20),
    phone_number VARCHAR(20)
);
-- Do NOT do: CREATE TYPE phone_list AS phone_type[];  -- invalid in PG
```

Use a separate normalized table for VARRAY/nested table collections:

```sql
CREATE TABLE customer_phones (
    phone_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT REFERENCES customers(customer_id),
    phone_kind VARCHAR(20),
    phone_number VARCHAR(20)
);
```

---

## 20. Generated Columns and Invisible Columns

```sql
-- Generated (virtual) column:
ALTER TABLE employees
ADD COLUMN annual_salary NUMERIC GENERATED ALWAYS AS (salary * 12) STORED;
-- Note: PostgreSQL only supports STORED (not VIRTUAL) generated columns.

-- Invisible column → migrate as regular column:
ALTER TABLE employees
ADD COLUMN internal_id BIGINT DEFAULT nextval('employees_seq');
-- Create a VIEW exposing only the visible columns if needed.
```

---

## 21. Advanced PL/pgSQL Function Patterns

### Replace Oracle-Specific Constructs

| Oracle | PostgreSQL |
|--------|-----------|
| Package constant | Config table or function parameter |
| `EXECUTE IMMEDIATE sql USING :v` | `EXECUTE format(...) USING v` or `EXECUTE sql USING v` |
| Explicit cursor loop | `FOR rec IN SELECT ... LOOP` |
| `DBMS_OUTPUT.PUT_LINE` | `RAISE NOTICE '%', val` |
| `MONTHS_BETWEEN(SYSDATE, hire_date)` | `FLOOR(EXTRACT(MONTH FROM AGE(CURRENT_DATE, hire_date)))` |
| Nested `DECLARE ... BEGIN ... END` | Flatten where possible; retain if complex exception handling is needed |
| `FORALL i IN ... INSERT VALUES arr(i)` | `FOREACH val IN ARRAY arr LOOP INSERT ... END LOOP` |

### Complex Function Example

```sql
CREATE OR REPLACE FUNCTION calculate_bonus(
    p_employee_id INTEGER,
    p_bonus_pct NUMERIC DEFAULT 0.1
) RETURNS NUMERIC AS $$
DECLARE
    v_salary        NUMERIC;
    v_hire_date     DATE;
    v_years_service INTEGER;
    v_bonus         NUMERIC := 0;
    v_multiplier    NUMERIC := 1.0;
    v_project_count INTEGER := 0;
BEGIN
    SELECT salary, hire_date
    INTO v_salary, v_hire_date
    FROM employees WHERE employee_id = p_employee_id;

    v_years_service := FLOOR(EXTRACT(YEAR FROM AGE(CURRENT_DATE, v_hire_date)));

    IF v_years_service > 10 THEN
        v_multiplier := 1.5;
    ELSIF v_years_service > 5 THEN
        v_multiplier := 1.2;
    END IF;

    v_bonus := v_salary * p_bonus_pct * v_multiplier;

    SELECT COUNT(*) INTO v_project_count
    FROM employee_projects WHERE employee_id = p_employee_id;
    v_bonus := v_bonus + (v_project_count * 100);

    RAISE NOTICE 'Bonus for employee %: %', p_employee_id, v_bonus;
    RETURN v_bonus;

EXCEPTION
    WHEN NO_DATA_FOUND THEN RETURN 0;
    WHEN OTHERS THEN RETURN NULL;
END;
$$ LANGUAGE plpgsql;
```

---

## 22. REF CURSOR Functions

```sql
-- Source: RETURN SYS_REFCURSOR
CREATE OR REPLACE FUNCTION get_employee_cursor()
RETURNS refcursor AS $$
DECLARE
    emp_cursor refcursor;
BEGIN
    OPEN emp_cursor FOR
        SELECT employee_id, first_name, last_name FROM employees;
    RETURN emp_cursor;
END;
$$ LANGUAGE plpgsql;
```

---

## 23. CHECK Constraints with CASE

PostgreSQL CHECK constraints cannot use `CASE` expressions directly. Rewrite as boolean logic:

```sql
-- Source: CHECK (CASE WHEN job_id='MANAGER' THEN salary>=5000 ... END = TRUE)
ALTER TABLE employees ADD CONSTRAINT chk_salary
CHECK (
    (job_id = 'MANAGER' AND salary >= 5000) OR
    (job_id = 'CLERK' AND salary >= 2000) OR
    (job_id NOT IN ('MANAGER', 'CLERK') AND salary >= 1000)
);
```
