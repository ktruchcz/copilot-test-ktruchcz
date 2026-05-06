# Development Guide

Instructions for building, testing, and running the Hello World application.

## Prerequisites

| Requirement | Version |
|-------------|---------|
| JDK | 21 or later |
| Maven | 3.9 or later |

## Build

Compile all sources and run the full test suite:

```bash
mvn verify
```

Compile sources only (skip tests):

```bash
mvn compile
```

## Run

After compiling, run the application via Maven:

```bash
mvn exec:java -Dexec.mainClass=HelloWorld
```

Or compile and run the single source file directly with the JDK:

```bash
javac -d target/classes src/main/java/HelloWorld.java
java -cp target/classes HelloWorld
```

## Test

Run the JUnit 5 test suite:

```bash
mvn test
```

Tests cover:

- `Greeting` record — field storage, formatted output, blank-input validation
- `TimeOfDay` factory — correct subtype returned for hour ranges 0-11, 12-16, 17-23
- `seasonOf` — correct season string for all twelve months

## Project Layout

```
.
├── src/
│   ├── main/java/HelloWorld.java   # Application source
│   └── test/java/HelloWorldTest.java  # JUnit 5 tests
├── pom.xml                         # Maven build descriptor
└── docs/                           # Developer documentation
```

## Dependencies

| Dependency | Scope | Purpose |
|------------|-------|---------|
| `org.junit.jupiter:junit-jupiter` | test | JUnit 5 test framework |

No runtime dependencies are required.

*Last updated: 2026-05-06*
