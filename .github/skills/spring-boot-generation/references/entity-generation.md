# Spring Boot JPA Entity Generation

Generate a JPA entity class for the target Spring Boot application.

## Rules

- Annotate the class with `@Entity` and `@Table(name = "TABLE_NAME")`.
- Apply Lombok in this exact order: `@Builder`, `@AllArgsConstructor`, `@NoArgsConstructor`, `@Data`.
- Use `import jakarta.persistence.*` — never `javax.persistence`.

### Primary Keys

- Annotate the PK field with `@Id`.
- For sequence-based generation, use `@GeneratedValue` + `@SequenceGenerator` where the `generator`, `name`, and `sequenceName` attributes all share the **same value** (the exact sequence name from the schema — no suffix added). Always include `allocationSize = 1`.

```java
@Id
@GeneratedValue(strategy = GenerationType.AUTO, generator = "S_COUNTRIES")
@SequenceGenerator(name = "S_COUNTRIES", sequenceName = "S_COUNTRIES", allocationSize = 1)
private Integer id;
```

- For tables with a database trigger managing the PK, use `GenerationType.SEQUENCE` and reference the trigger's sequence.

### Composite Primary Keys

- If the entity has a composite PK, create a separate `@IdClass` in its own file:
  - Include one field per PK component with the same types as in the entity.
  - Implement `Serializable`, apply `@Data`, `@Builder`, `@AllArgsConstructor`, `@NoArgsConstructor`.
- Annotate the entity class with `@IdClass(MyEntityId.class)` and mark each PK field with `@Id`.

### Fields

- Use `@Column(name = "COLUMN_NAME")` to map each field to its exact DB column name.
- Set `nullable`, `length`, `precision`, and `scale` in `@Column` to match constraints.
- Apply `@NotNull` (from `jakarta.validation.constraints`) for non-nullable columns.
- Apply `@Size(max = N)` for varchar fields where max length is defined.
- Convert column names to camelCase (e.g. `AMOUNT_IN_STOCK` → `amountInStock`).
- Import `import java.util.List;` when `List` is used.
- Import `import java.math.BigDecimal;` when `BigDecimal` is used.
- Use `Long`, not `BigInteger`.

### Associations / Relationships

- Map relationships using `@ManyToOne`, `@OneToMany`, `@ManyToMany` as appropriate.
- Use `@JoinColumn` for owning side of a `@ManyToOne`.
- For `@OneToMany` bidirectional, use `mappedBy` pointing to the owning-side field name in camelCase.
  - If the owning entity is itself (self-referencing), `mappedBy` points to the field name within the same entity.
  - Naming pattern for List fields: append `s` to the entity name (e.g. `ProductEO` → `productEOs`).
- Use `FetchType.LAZY` as the fetch strategy unless eager loading is explicitly required.
- Do not add assumptions as comments. If something is unclear, keep the code minimal rather than guessing.

### Example

```java
@Entity
@Table(name = "S_INVENTORY")
@Builder
@AllArgsConstructor
@NoArgsConstructor
@Data
@IdClass(InventoryEOId.class)
public class InventoryEO {
    @Id
    @Column(name = "PRODUCT_ID", nullable = false)
    private Integer productId;

    @Id
    @Column(name = "WAREHOUSE_ID", nullable = false)
    private Long warehouseId;

    @Column(name = "AMOUNT_IN_STOCK")
    private Integer amountInStock;

    @Column(name = "RESTOCK_DATE")
    private java.time.LocalDate restockDate;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "PRODUCT_ID", referencedColumnName = "ID",
                insertable = false, updatable = false)
    private ProductEO productEO;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "WAREHOUSE_ID", referencedColumnName = "ID",
                insertable = false, updatable = false)
    private WarehouseEO warehouseEO;
}
```

### Validation Checklist

Before finalizing, verify:
- [ ] Every class has at least one `@Id` or `@EmbeddedId`/`@IdClass` configuration
- [ ] All `jakarta` imports — no `javax`
- [ ] `allocationSize = 1` on every `@SequenceGenerator`
- [ ] `LocalDate` for dates, `LocalDateTime` for timestamps — never `Timestamp` or `java.sql.Date`
- [ ] `Long` not `BigInteger`
- [ ] `mappedBy` value uses exact field name (camelCase) from the owning entity; append `s` for collections
- [ ] Sequence generator `name`, `generator`, and `sequenceName` are identical
- [ ] Package name matches what was provided in the prompt

---

## ADF Source Notes (skip if not migrating from ADF)

When the source is an ADF XML Entity Object (`.eo.xml` + SQL DDL):

- The Java class name comes from the `Name` attribute of the `<Entity>` tag (e.g., `InventoryEO`).
- Field names come from column names in the schema, converted to camelCase.
- The sequence name comes from the `DBObjectName` attribute in the EO XML (do **not** append `_ID`).
- The `<Association>` XML tag defines relationships; `<AccessorAttribute>` and `<AssociationEnd>` clarify direction.
- The `AliasName` attribute in nested entity descriptors gives the camelCase variable name for the relationship field.
- Related entities referenced in descriptors are assumed to already exist as JPA entities.
