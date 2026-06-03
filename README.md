# copilot-test-ktruchcz

Simple Java greeting project.

The application is a small layered CLI flow:

- `HelloWorld` (entry point)
- `GreetingController`
- `GreetingService`
- `GreetingRepository`

Tests are in `src/test/java/HelloWorldTest.java` (JUnit 5).

## Build and test

Requires Java 25.

```bash
mvn clean test
```

`HelloWorld` prints `Hello World` by default and supports overriding recipient via the first CLI argument.
