---
name: java-jpa-entity-generator
description: Generate Spring Boot JPA entities from data models, entity descriptors, database schemas, or entity relationship specifications. Use this to convert legacy entity definitions, data models, database table schemas, or entity descriptors into modern JPA entities with proper annotations and relationships.
---

# JPA Entity Generator (Spring Boot)

Generate JPA entities that map database tables to Java domain objects.

## Required inputs

- Entity descriptor or data model specification (from any legacy format)
- SQL DDL for the corresponding database table, including sequences and foreign keys
- Related entity names if associations/relationships exist
- Target Java package name if specified

## Workflow

1. Confirm the entity name and the exact database table it maps to.
2. Read [references/implementation.md](references/implementation.md) before generating code.
3. If reviewing or correcting an existing entity, also read [references/review.md](references/review.md).
4. Generate the main entity class first, then create a separate IdClass when the primary key is composite.
5. Use Jakarta JPA annotations, Lombok for boilerplate, and Java time types for dates/times.
6. Run the review checklist against field mappings, ID generation strategy, and associations before finalizing.

## Output contract

- Output a complete, compilable Java entity class.
- Create a separate IdClass file for composite primary keys.
- Express database constraints and relationships using JPA annotations.
- Use proper naming conventions and follow the target project's entity patterns.
- Keep assumptions minimal; if source data is missing, call out the gap briefly.

## Reference files

- [references/implementation.md](references/implementation.md): generation rules for SQL types, sequences, and associations.
- [references/review.md](references/review.md): reviewer checklist for correctness and consistency.
