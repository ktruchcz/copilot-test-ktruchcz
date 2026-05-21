# Review Checklist

- Verify controller endpoints expose correct path and query parameters.
- Verify all public API return types are DTOs (not JPA entities).
- Verify service methods align with the requested business operations.
- Verify constructor injection is used in both controller and service classes.
- Verify `@DateTimeFormat` is present for LocalDate/LocalDateTime request parameters.
- Verify repository interactions match the intended business behavior.
- Verify error handling and HTTP status handling are present.
