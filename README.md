# copilot-test-ktruchcz

A simple Hello World Java application modernized with Maven and JUnit 5.

## Requirements

- Java 17+
- Maven 3.8+

## Build

```bash
mvn compile
```

## Run

```bash
mvn exec:java -Dexec.mainClass="com.example.HelloWorld"
```

Or build and run the JAR:

```bash
mvn package
java -jar target/hello-world-1.0.0.jar
```

## Test

```bash
mvn test
```