# copilot-test-ktruchcz

A **Hello World** application modernized to **Java 21** with a full Maven build system.

## Features

- **Java 21 LTS** – latest long-term support release
- **Records** – immutable `Greeting` and `Person` data carriers
- **Sealed interfaces** – restricted `OutputTarget` hierarchy
- **Pattern-matching `switch`** – exhaustive dispatch over sealed types
- **Text blocks** – readable multi-line banner string
- **Maven** build system with JUnit 5 test support
- **GitHub Actions** CI workflow (`.github/workflows/ci.yml`)

## Project structure

```
.
├── pom.xml                          # Maven build descriptor (Java 21)
├── src/
│   ├── main/java/com/example/
│   │   └── HelloWorld.java          # Modernized application source
│   └── test/java/com/example/
│       └── HelloWorldTest.java      # JUnit 5 unit tests
└── .github/workflows/
    └── ci.yml                       # GitHub Actions CI pipeline
```

## Build & run

```bash
# Compile and run all tests
mvn clean verify

# Run the application
java --enable-preview -jar target/hello-world-1.0.0.jar
```
