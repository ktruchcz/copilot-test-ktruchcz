# Hello World (Java 21)

Minimal Java modernization scenario (`java-update`) for a Maven-based Hello World app.

## Requirements

- JDK 21
- Maven 3.9+

## Build and test

```bash
mvn clean test
```

## Run

```bash
mvn -q -DskipTests compile exec:java -Dexec.mainClass=HelloWorld
```
