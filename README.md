# copilot-test-ktruchcz

A Java 21 Hello World application demonstrating modern language features: records, sealed interfaces, pattern-matching switch, text blocks, and `var`.

## Build and Test

Requires **JDK 21** and **Maven 3.6+**.

```bash
# Compile the project
mvn compile

# Run the tests
mvn test

# Compile and test in one step (clean build)
mvn clean test

# Run the application after compiling
java -cp target/classes HelloWorld
```

## Features Demonstrated

- **Records** (`Greeting`, `Morning`, `Afternoon`, `Evening`) — immutable value objects
- **Sealed interfaces** (`TimeOfDay`) — exhaustive type hierarchy
- **Pattern-matching switch** — time-of-day determination
- **Text blocks** — formatted Unicode greeting output
- **`var`** — local-variable type inference

## Project Structure

```
src/
  main/java/HelloWorld.java   # Production source (canonical)
  test/java/HelloWorldTest.java
pom.xml
arc42-documentation.md       # Architecture documentation
.github/workflows/build.yml  # CI: runs mvn test on push/PR
```
