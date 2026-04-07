# TestApp2

A modernized Java 21 application demonstrating current language features and best practices.

## Java 21 Features Showcased

| Feature | JEP | Since |
|---|---|---|
| Records | JEP 395 | Java 16 |
| Sealed interfaces | JEP 409 | Java 17 |
| Text blocks | JEP 378 | Java 15 |
| Pattern-matching switch | JEP 441 | Java 21 |
| `var` type inference | JEP 286 | Java 10 |
| Enhanced `instanceof` | JEP 394 | Java 16 |
| Stream API improvements | — | Java 8+ |
| Sequenced collections | JEP 431 | Java 21 |

## Prerequisites

- **Java 21** (LTS)
- **Maven 3.9+**

## Build & Run

```bash
# Compile
mvn compile

# Run all tests
mvn test

# Build executable JAR
mvn package

# Run the application
java --enable-preview -jar target/testapp2-1.0.0.jar
```

## Project Structure

```
.
├── pom.xml
├── src
│   ├── main
│   │   └── java
│   │       └── com/testapp2
│   │           └── HelloWorld.java   # Main application
│   └── test
│       └── java
│           └── com/testapp2
│               └── HelloWorldTest.java  # JUnit 5 tests
└── README.md
```
