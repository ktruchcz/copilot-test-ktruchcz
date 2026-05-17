# Review Checklist

- Verify every non-null database column has either `nullable = false`, `@NotNull`, or both where appropriate.
- Verify every date and timestamp field uses Java time types, not legacy SQL date classes.
- Verify composite keys create a separate IdClass instead of inlining custom logic.
- Verify the IdClass mirrors entity id field names and types exactly and does not contain relationship fields.
- Verify shared PK/FK columns are not mapped twice as writable fields and writable relationships.
- Verify `generator`, `name`, and `sequenceName` are identical on `@SequenceGenerator`.
- Verify `mappedBy` values and collection names follow the same camelCase naming used on the owning side.
- Verify imports come from `jakarta.*`.
- Verify relationship fields do not invent entities or comments that were not provided in the source.
