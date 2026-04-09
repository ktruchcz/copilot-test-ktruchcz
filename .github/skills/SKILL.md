---
name: spring-boot-generation
description: "Generate Spring Boot Java backend code (entities, repositories, controllers, services, and tests). Use whenever generating @Entity, @Repository, @RestController, @Service classes, or any Spring test (@WebMvcTest, @DataJpaTest, @ExtendWith). Invoke for any migration where the TARGET is Spring Boot—regardless of the source technology (ADF, Python, legacy Java, .NET, etc.). Also use when the user asks to create JPA entities from a schema, write JPQL queries, or set up constructor injection patterns."
---

# Spring Boot Generation Skill

This skill guides the generation of idiomatic Spring Boot code for the target application. All rules focus on the **target technology** — Spring Boot / Spring Data JPA / Spring MVC. Apply these regardless of the source technology you're migrating from.

## Core Conventions (apply everywhere)

- Use **constructor injection** with `@Autowired`. Never use field injection.
- Use **`jakarta.*`** for JPA and validation annotations (not legacy `javax.*`):
  - `import jakarta.persistence.*`
  - `import jakarta.validation.constraints.*`
- Use **Lombok** annotations in this order: `@Builder`, `@AllArgsConstructor`, `@NoArgsConstructor`, `@Data`
- Use **DTOs** as return types for all service and controller methods. Never expose entities directly.
- Use **`Long`** instead of `BigInteger` everywhere.
- Use **`java.time.LocalDate`** for dates and **`java.time.LocalDateTime`** for timestamps. Never use `java.sql.Date` or `java.sql.Timestamp` in domain types.

## SQL Type Mapping

| SQL / Oracle Type  | Java Type           |
|--------------------|---------------------|
| VARCHAR / VARCHAR2 | `String`            |
| DATE               | `java.time.LocalDate` |
| TIMESTAMP          | `java.time.LocalDateTime` |
| NUMBER(≤10, 0)     | `Integer`           |
| NUMBER(19, 0)      | `Long`              |
| NUMBER(p, s≥1)     | `BigDecimal`        |
| CLOB / TEXT        | `String`            |
| NUMERIC(p,s)       | use precision/scale rules above |

## Reference Files

| Task | Reference |
|------|-----------|
| Generate a JPA `@Entity` class | [references/entity-generation.md](references/entity-generation.md) |
| Generate a Spring Data `@Repository` interface with JPQL | [references/repository-generation.md](references/repository-generation.md) |
| Generate a `@RestController` + `@Service` pair | [references/controller-service-generation.md](references/controller-service-generation.md) |
| Generate unit tests with Mockito | [references/test-generation.md](references/test-generation.md#unit-tests) |
| Generate `@WebMvcTest` controller tests | [references/test-generation.md](references/test-generation.md#mvc-tests) |
| Generate `@DataJpaTest` integration tests | [references/test-generation.md](references/test-generation.md#integration-tests) |

Read the relevant reference file before generating code for that layer.
