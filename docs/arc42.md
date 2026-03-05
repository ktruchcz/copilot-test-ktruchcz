# arc42 Architecture Documentation

**About arc42**

arc42, the template for documentation of software and system architectures.

Template Version 8.2 EN. (based upon AsciiDoc version), January 2023

Created, maintained and © by Dr. Peter Hruschka, Dr. Gernot Starke and contributors. See <https://arc42.org>.

---

## Table of Contents

1. [Introduction and Goals](#1-introduction-and-goals)
2. [Architecture Constraints](#2-architecture-constraints)
3. [System Scope and Context](#3-system-scope-and-context)
4. [Solution Strategy](#4-solution-strategy)
5. [Building Block View](#5-building-block-view)
6. [Runtime View](#6-runtime-view)
7. [Deployment View](#7-deployment-view)
8. [Cross-cutting Concepts](#8-cross-cutting-concepts)
9. [Architecture Decisions](#9-architecture-decisions)
10. [Quality Requirements](#10-quality-requirements)
11. [Risks and Technical Debt](#11-risks-and-technical-debt)
12. [Glossary](#12-glossary)

---

## 1. Introduction and Goals

### Requirements Overview

The **HelloWorld** application is a minimal Java program that demonstrates the classic "Hello, World!" example. Its sole purpose is to print the text `Hello World` to the standard output when executed.

**Top-level requirements:**

| ID  | Requirement                                      |
|-----|--------------------------------------------------|
| R1  | The application shall print "Hello World" to stdout. |
| R2  | The application shall exit cleanly after printing. |

### Quality Goals

| Priority | Quality Goal    | Motivation                                             |
|----------|-----------------|--------------------------------------------------------|
| 1        | Simplicity      | The application should be as simple as possible to understand and maintain. |
| 2        | Correctness     | The output must always be exactly "Hello World".       |
| 3        | Portability     | The application should run on any JVM-capable platform. |

### Stakeholders

| Role          | Name / Contact | Expectations                                      |
|---------------|----------------|---------------------------------------------------|
| Developer     | ktruchcz       | Simple, working demonstration of a Java program.  |
| Reviewer      | Team           | Clear, readable, and well-documented source code. |

---

## 2. Architecture Constraints

| Constraint           | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| Language             | Java (any standard JDK version)                                             |
| Runtime              | Java Virtual Machine (JVM)                                                  |
| No external dependencies | The application uses only the Java standard library (no third-party libraries). |
| Single class         | The entire application fits in a single Java class (`HelloWorld.java`).     |

---

## 3. System Scope and Context

### Business Context

The HelloWorld application has no external business interfaces. It takes no input and produces a single line of output to the console.

```
+-------------------+       stdout        +-------------------+
|   HelloWorld App  | ------------------> |   Console / User  |
+-------------------+                     +-------------------+
```

### Technical Context

| Channel  | Description                                              |
|----------|----------------------------------------------------------|
| stdout   | Standard output stream — the application writes "Hello World" to it. |

There are no network connections, file I/O, or database interactions.

---

## 4. Solution Strategy

| Goal        | Strategy                                                          |
|-------------|-------------------------------------------------------------------|
| Simplicity  | Implement the entire application as a single `public static void main` method in one class. |
| Correctness | Use `System.out.println` to reliably write the expected string to stdout. |
| Portability | Use only the Java standard library — no platform-specific APIs.   |

---

## 5. Building Block View

### Level 1 — Overall System

```
+------------------------------------------+
|              HelloWorld                  |
|                                          |
|  + main(String[] args): void             |
|    - Prints "Hello World" to stdout      |
+------------------------------------------+
```

The application consists of a single building block:

| Building Block | Description                                                   |
|----------------|---------------------------------------------------------------|
| `HelloWorld`   | The only class in the system. Contains the `main` entry point. |

### Level 2 — HelloWorld Class

| Element             | Type   | Description                                   |
|---------------------|--------|-----------------------------------------------|
| `main(String[] args)` | Method | Entry point of the application. Calls `System.out.println("Hello World")`. |

---

## 6. Runtime View

### Scenario: Application Startup and Output

```
[JVM] --> main(args)
             |
             v
      System.out.println("Hello World")
             |
             v
         [Console]: Hello World
             |
             v
         [JVM exits normally]
```

**Steps:**

1. The JVM loads the `HelloWorld` class.
2. The JVM calls `HelloWorld.main(String[] args)`.
3. `System.out.println("Hello World")` writes `Hello World` followed by a newline to stdout.
4. The `main` method returns and the JVM exits with code `0`.

---

## 7. Deployment View

### Infrastructure

The application runs on any machine with a compatible Java Runtime Environment (JRE) installed.

```
+-----------------------------+
|       Developer Machine     |
|                             |
|  +-----------------------+  |
|  |   Java Runtime (JVM)  |  |
|  |                       |  |
|  |   HelloWorld.class    |  |
|  +-----------------------+  |
+-----------------------------+
```

### Deployment Steps

1. Compile: `javac HelloWorld.java`
2. Run: `java HelloWorld`

No deployment pipeline or containerization is required for this application.

---

## 8. Cross-cutting Concepts

### Logging / Output

The application uses `System.out.println` directly. There is no logging framework — the output itself is the only observable behaviour.

### Error Handling

The application contains no explicit error handling because there are no failure modes in its current scope.

### Testability

The `main` method can be tested by capturing `System.out` and asserting that it contains `Hello World`.

---

## 9. Architecture Decisions

### ADR-001: Single-class Implementation

| Field       | Content                                                          |
|-------------|------------------------------------------------------------------|
| **Status**  | Accepted                                                         |
| **Context** | The application has a single, trivial responsibility.            |
| **Decision**| Implement the entire application in one class (`HelloWorld`).    |
| **Consequences** | Maximum simplicity; no package structure or build tooling required. |

### ADR-002: No External Dependencies

| Field       | Content                                                          |
|-------------|------------------------------------------------------------------|
| **Status**  | Accepted                                                         |
| **Context** | The application only needs to print a string.                    |
| **Decision**| Use only `java.lang.System` from the standard library.           |
| **Consequences** | Zero dependency management overhead.                        |

---

## 10. Quality Requirements

### Quality Tree

```
Quality
├── Simplicity
│   └── Single class, single method
├── Correctness
│   └── Output is always exactly "Hello World"
└── Portability
    └── Runs on any JVM (Java SE)
```

### Quality Scenarios

| ID  | Quality Goal | Scenario                                          | Expected Result                      |
|-----|--------------|---------------------------------------------------|--------------------------------------|
| QS1 | Correctness  | Run `java HelloWorld` on any JVM.                 | Prints `Hello World` to stdout.      |
| QS2 | Portability  | Compile and run on Linux, macOS, or Windows JVM.  | Same output on all platforms.        |
| QS3 | Simplicity   | A new developer reads the source code.            | Understands the code within seconds. |

---

## 11. Risks and Technical Debt

| ID  | Risk / Debt        | Description                                                                           | Mitigation                                   |
|-----|--------------------|---------------------------------------------------------------------------------------|----------------------------------------------|
| R1  | No automated tests | There are currently no unit tests for the `HelloWorld` class.                         | Add a JUnit test that captures stdout output. |
| R2  | No build tool      | Compilation relies on running `javac` manually.                                       | Introduce Maven or Gradle if the project grows. |
| R3  | Single file        | As the project grows, a single-file approach will not scale.                           | Restructure into a proper Maven/Gradle project when needed. |

---

## 12. Glossary

| Term       | Definition                                                                 |
|------------|----------------------------------------------------------------------------|
| arc42      | A practical template for documenting software and system architectures.    |
| JVM        | Java Virtual Machine — the runtime environment for executing Java bytecode. |
| JDK        | Java Development Kit — includes the compiler (`javac`) and runtime (`java`). |
| JRE        | Java Runtime Environment — subset of JDK needed to run (not compile) Java programs. |
| stdout     | Standard output stream — the default output channel for console applications. |
| ADR        | Architecture Decision Record — a short document capturing an important design decision. |
