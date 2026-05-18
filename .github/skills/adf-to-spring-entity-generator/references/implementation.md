# Implementation Guide

## Goal

Convert a data model descriptor and its database schema into a Spring Boot JPA entity that compiles and preserves all database semantics.

## Entity generation rules

- Use `jakarta.persistence.*` and `jakarta.validation.constraints.*` (never `javax.*`).
- Apply Lombok annotations in this order: `@Builder`, `@AllArgsConstructor`, `@NoArgsConstructor`, `@Data`.
- Derive the Java class name from the entity name in the source descriptor.
- Convert database column names to camelCase field names.
- Use `@Entity` and `@Table(name = "...")` with the exact database table name.
- Use `@Column` for each field with the exact database column name.
- Include column constraints: `nullable`, `length`, `precision`, `scale` from DDL.
- Add validation annotations (`@NotNull`, `@Size`, etc.) when the schema or descriptor makes the constraint explicit.

## Primary key / identifier rules

- Identify the real primary key strategy from the model and SQL schema.
- For sequence-based identity, use `@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "...")` with `@SequenceGenerator`.
- Set `generator`, `name`, and `sequenceName` consistently.
- Create a separate IdClass for composite primary keys and annotate the entity with `@IdClass(...)`.
- The IdClass must implement `Serializable`, use Lombok for consistent equality, and mirror the entity's id field names and types exactly.

## Type mapping

- `VARCHAR`, `VARCHAR2` → `String`
- `NUMBER(7,0)`, `NUMBER(9,0)`, `NUMBER(10,0)` → `Integer`
- `NUMBER(11,2)` → `BigDecimal`
- `NUMBER(19,0)` → `Long`
- `DATE` → `LocalDate`
- `TIMESTAMP` → `LocalDateTime`
- Import `java.util.List` for collection relationships.

## Relationship / association mapping

- Study the model's relationship definitions and foreign key constraints together.
- Use relationship name from the model to derive the field name.
- Prefer `@ManyToOne` or `@OneToMany` with `FetchType.LAZY` unless the source clearly requires eager loading.
- For collection relationships, pluralize the entity name (e.g., `Item` → `items`).
- Use `mappedBy` on the inverse side to match the owning-side field name exactly.
- Assume related entities are already generated and reference them by their class names.

## Composite key + foreign key pattern

- When a foreign-key column is also part of the primary key, keep the scalar id field and also map the relationship.
- On the relationship side, use `@JoinColumn(insertable = false, updatable = false)` so JPA does not write the same column twice.
- The IdClass must contain only id fields (not relationship objects).
- The IdClass should provide stable equality through Lombok or explicit implementation.

### Example pattern

```java
@Id
@Column(name = "PRODUCT_ID", nullable = false)
private Integer productId;

@ManyToOne(fetch = FetchType.LAZY)
@JoinColumn(name = "PRODUCT_ID", referencedColumnName = "ID", insertable = false, updatable = false)
private Product product;
```

## Output checklist

- Entity class name matches the source descriptor entity name.
- Column mappings match the database schema exactly.
- Sequence generation settings are internally consistent.
- Foreign key relationships match the database constraints.
- No `java.sql.Date`, `java.sql.Timestamp`, or `BigInteger` in the domain model.
- All constraints and nullable settings are preserved.
