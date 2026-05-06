# Review Checklist

- Verify the class uses `@ExtendWith(MockitoExtension.class)` and no broader Spring test annotations.
- Verify service dependencies are `@Mock` and the service under test is `@InjectMocks`.
- Verify `lenient()` stubbing is used only when intentionally needed for shared setup.
- Verify test method names are specific and behavior-oriented.
- Verify assertions validate actual business behavior, not only non-null results.
- Verify error paths are covered with `assertThrows` where appropriate.
