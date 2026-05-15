# Review Checklist

- Verify the class uses `@DataJpaTest`.
- Verify base test class extension is present only if the project provides one.
- Verify `@DirtiesContext` is used when test data isolation requires it.
- Verify assertions reflect the SQL fixture data, including expected row counts.
- Verify repository methods under test match the declared query behavior.
- Verify the class compiles and runs without unnecessary test setup annotations.
