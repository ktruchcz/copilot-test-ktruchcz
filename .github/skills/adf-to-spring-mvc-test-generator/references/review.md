# Review Checklist

- Verify the test class uses `@WebMvcTest` and not broader Spring annotations.
- Verify `MockMvc` is used for endpoint calls.
- Verify service dependencies are mocked with `@MockBean`.
- Verify test data respects DTO types.
- Verify assertions cover response size, key fields, and status codes.
