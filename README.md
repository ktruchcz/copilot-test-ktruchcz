# Hello World — Java 21

A modern Java 21 application that demonstrates key language features introduced
since Java 9, including **records**, **text blocks**, **enhanced switch expressions**,
and **local variable type inference** (`var`).

---

## Prerequisites

| Tool | Minimum version |
|------|----------------|
| Java | 21 (LTS) |
| Maven | 3.9+ |

Verify your installation:

```bash
java --version   # should report 21.x
mvn  --version   # should report 3.9.x
```

---

## Project structure

```
.
├── pom.xml
└── src
    ├── main
    │   └── java
    │       └── com/example/helloworld
    │           ├── HelloWorld.java   # entry point
    │           └── Greeting.java     # record demonstrating Java 16+ records
    └── test
        └── java
            └── com/example/helloworld
                ├── HelloWorldTest.java
                └── GreetingTest.java
```

---

## Build

```bash
mvn package
```

The compiled JAR is placed in `target/helloworld-1.0.0-SNAPSHOT.jar`.

---

## Run

```bash
# Using Maven:
mvn exec:java -Dexec.mainClass="com.example.helloworld.HelloWorld"

# Using the packaged JAR directly:
java -jar target/helloworld-1.0.0-SNAPSHOT.jar
```

---

## Test

```bash
mvn test
```

Test reports are written to `target/surefire-reports/`.

---

## Modern Java features used

| Feature | Java version introduced | Where used |
|---------|------------------------|------------|
| `var` (local-variable type inference) | 10 | `HelloWorld.java` |
| Text blocks | 15 (standard) | `Greeting.java`, `HelloWorld.java` |
| Records | 16 (standard) | `Greeting.java` |
| Enhanced switch expressions | 14 (standard) | `HelloWorld.java` |
| `List.of` / Stream API | 9 / 8 | `HelloWorld.java` |
