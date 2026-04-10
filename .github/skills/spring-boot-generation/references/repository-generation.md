# Spring Data Repository Generation

Generate a Spring Data JPA repository interface for the target Spring Boot application.

## Rules

### Interface Structure

- Define repositories as interfaces annotated with `@Repository`.
- Extend `JpaRepository<EntityClass, IDType>` where the type parameters are the **entity class** and its **primary key type** (or `@IdClass` type for composite keys).
- Name the interface by appending `Repository` to the entity name (e.g., `CountryEO` → `CountryEORepository`).
- If multiple ViewObjects reference the same entity, merge their methods into a single repository.

### Method Implementation

- Implement every query method as a `@Query`-annotated method using **JPQL** (not native SQL).
- Keep method names exactly as provided in the source — do not rename them.
- Use the `@Param` annotation for every method parameter.
- Only include a method parameter when the corresponding variable actually appears in the JPQL query. If the query value is a literal (hardcoded), do not create a parameter for it.

### JPQL Rules

- Reference entity field names (camelCase), not database column names, in JPQL.
- When the query returns a DTO, use the `SELECT new com.<package>.dtos.MyDTO(...)` JPQL constructor syntax.
- The DTO package in the JPQL string must match the actual DTO package (change `repositories` to `dtos` in the package path).
- Use `like %:param%` for wildcard searches; do not quote the `%` symbols.
- Reproduce `WHERE` clause conditions from the source view object exactly.

### Simple Query Pattern

Use this when the query selects all fields from a single entity with no joins:

```java
@Repository
public interface CountryEORepository extends JpaRepository<CountryEO, Integer> {

    @Query("SELECT new com.example.dtos.CountryDTO(c.id, c.country, c.regionEO.id, c.countryCode) " +
           "FROM CountryEO c")
    List<CountryDTO> findAllCountries();
}
```

### Complex Query Pattern (joins / conditions)

Use this for queries with joins, conditions, or aggregations:

```java
@Repository
public interface InventoryEORepository extends JpaRepository<InventoryEO, InventoryEOId> {

    @Query("SELECT new com.example.dtos.LowStockDTO(" +
           "i.productId, w.id, i.amountInStock, i.reorderPoint, " +
           "p.name, p.id) " +
           "FROM InventoryEO i JOIN i.warehouseEO w JOIN i.productEO p " +
           "WHERE i.amountInStock <= i.reorderPoint")
    List<LowStockDTO> findLowStockItems();

    List<CustomerDTO> searchCustomersByNameAndCity(
        @Param("name") String name,
        @Param("city") String city);
}
```

### DTO Rules

- use Lombok: `@Builder`, `@AllArgsConstructor`, `@NoArgsConstructor`, `@Data` (in that order).
- Match attribute types to the **entity** types, not the raw SQL types (e.g., use `LocalDate` not `Date`).
- Use `Long` instead of `BigInteger`.
- Make sure the number and order of constructor arguments in JPQL match the DTO's `@AllArgsConstructor`.

### Oracle ADD_MONTHS Translation

If the source SQL uses `ADD_MONTHS(TRUNC(SYSDATE,'MM'), ...)`, translate to JPQL as:
```sql
ADD_MONTHS(CAST(DATE_TRUNC(SYSDATE,'MM') AS DATE), ...)
```

### Validation Checklist

- [ ] `JpaRepository<EntityClass, IDType>` — uses entity name, not repository name, as `T`
- [ ] All method parameters have `@Param`
- [ ] Only parameters that appear in JPQL are declared as method arguments
- [ ] Literal values in source view criteria are inlined in JPQL (not turned into parameters)
- [ ] DTO constructor arguments match the `@AllArgsConstructor` order
- [ ] `LocalDate`/`LocalDateTime` in DTOs, not `Timestamp` or `Date`
- [ ] `Long` not `BigInteger`

---

## ADF Source Notes (skip if not migrating from ADF)

When the source is an ADF ViewObject (`.vo.xml`):

- The repository method names come from `ViewCriteria` names in the VO XML — use them verbatim.
- Method parameters correspond to `ViewCriteriaItem` bind variables (those whose `Value` starts with `:`).
- When a `ViewCriteriaItem` has a literal `Value` (not starting with `:`), inline it in the JPQL rather than making a parameter.
- `ViewAttribute` tags define the columns selected — map them to entity fields by name (use the entity field type, not the VO attribute type).
- `SelectList`, `FromList`, and `Where` XML nodes describe the underlying SQL structure.
- `ViewLinkAccessor` elements indicate inter-entity joins.
- At minimum, every repository must have one method based on the VO's query returning a DTO.
