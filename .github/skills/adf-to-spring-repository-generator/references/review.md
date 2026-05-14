# Review Checklist

- Verify every repository method returns DTOs or the correct entity type for standard CRUD inherited methods.
- Verify every custom query is JPQL and uses entity field names.
- Verify `@Param` names match query placeholders exactly.
- Verify unused parameters were not generated from source literals.
- Verify complex queries still align DTO field order with constructor order.
- Verify repository generic type uses the entity class, not the repository class.
