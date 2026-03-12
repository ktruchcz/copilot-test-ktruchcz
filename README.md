# Hello World

A simple Hello World Java application modernized with Maven, Java 17, and JUnit 5.

## Prerequisites

- Java 17+
- Maven 3.6+

## Build

```bash
mvn clean package
```

## Run

```bash
java -jar target/hello-world-1.0.0.jar
```

Or directly with Maven:

```bash
mvn exec:java -Dexec.mainClass="com.example.HelloWorld"
```

## Test

```bash
mvn test
```

## Project Structure

```
src/
├── main/java/com/example/
│   └── HelloWorld.java       # Main application class
└── test/java/com/example/
    └── HelloWorldTest.java   # JUnit 5 unit tests
```