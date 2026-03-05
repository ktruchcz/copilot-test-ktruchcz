# arc42 Architecture Documentation

## HelloWorld Application

**Version:** 1.0  
**Date:** 2026-03-05

---

## Table of Contents

1. [Introduction and Goals](#1-introduction-and-goals)
2. [Constraints](#2-constraints)
3. [Context and Scope](#3-context-and-scope)
4. [Solution Strategy](#4-solution-strategy)
5. [Building Block View](#5-building-block-view)
6. [Runtime View](#6-runtime-view)
7. [Deployment View](#7-deployment-view)
8. [Crosscutting Concepts](#8-crosscutting-concepts)
9. [Architecture Decisions](#9-architecture-decisions)
10. [Quality Requirements](#10-quality-requirements)
11. [Risks and Technical Debt](#11-risks-and-technical-debt)
12. [Glossary](#12-glossary)

---

## 1. Introduction and Goals

### 1.1 Requirements Overview

The HelloWorld application is a minimal Java program that demonstrates the basic structure of a Java application. Its sole purpose is to print the text "Hello World" to the standard output when executed.

**Key features:**
- Outputs "Hello World" to the console
- Serves as a baseline reference for the project repository structure

### 1.2 Quality Goals

| Priority | Quality Goal     | Motivation                                           |
|----------|------------------|------------------------------------------------------|
| 1        | Simplicity       | The application should be as simple as possible      |
| 2        | Understandability| Code should be easy to read and understand           |
| 3        | Executability    | The application must compile and run without errors  |

### 1.3 Stakeholders

| Role        | Name/Contact  | Expectations                                     |
|-------------|---------------|--------------------------------------------------|
| Developer   | ktruchcz      | Working, compilable Java application             |
| Repository  | GitHub        | Properly structured and versioned source code    |

---

## 2. Constraints

### 2.1 Technical Constraints

| Constraint  | Description                                              |
|-------------|----------------------------------------------------------|
| Language    | The application is implemented in Java                   |
| JDK version | Requires Java Development Kit (JDK) to compile and run  |
| No framework| No external frameworks or libraries are used             |

### 2.2 Organizational Constraints

| Constraint       | Description                                         |
|------------------|-----------------------------------------------------|
| Repository       | Source code is hosted on GitHub                     |
| Version Control  | Git is used for version control                     |

---

## 3. Context and Scope

### 3.1 Business Context

The HelloWorld application operates entirely standalone. It reads no external inputs and produces a single line of output to the user's console.

```
User/System
    |
    v
+------------------+
|  HelloWorld App  |  --> "Hello World" (stdout)
+------------------+
```

### 3.2 Technical Context

| Channel      | Description                                         |
|--------------|-----------------------------------------------------|
| Standard Out | The application writes its output to `System.out`  |
| JVM          | The application runs on the Java Virtual Machine    |

---

## 4. Solution Strategy

The application follows the simplest possible Java program structure:

- A single public class (`HelloWorld`) with a `main` method serves as the entry point
- The Java standard library's `System.out.println` is used to produce output
- No design patterns, frameworks, or dependencies are needed for this use case

---

## 5. Building Block View

### 5.1 Level 1 – Overall System

```
+-------------------------------------------+
|              HelloWorld System             |
|                                           |
|  +--------------------------------------+ |
|  |         HelloWorld (Class)           | |
|  |  + main(String[] args): void         | |
|  +--------------------------------------+ |
+-------------------------------------------+
```

### 5.2 HelloWorld Class

**Responsibility:** Entry point of the application. Prints "Hello World" to standard output.

| Method                        | Description                                      |
|-------------------------------|--------------------------------------------------|
| `main(String[] args): void`   | Application entry point; prints "Hello World"   |

---

## 6. Runtime View

### 6.1 Application Startup and Execution

```
User/OS
  |
  |--> java HelloWorld
          |
          v
     [JVM loads HelloWorld class]
          |
          v
     [main() is invoked]
          |
          v
     [System.out.println("Hello World")]
          |
          v
     "Hello World" printed to console
          |
          v
     [Application exits]
```

---

## 7. Deployment View

### 7.1 Infrastructure

The application can be deployed on any system with a compatible Java Runtime Environment (JRE).

**Compilation:**
```bash
javac HelloWorld.java
```

**Execution:**
```bash
java HelloWorld
```

### 7.2 Deployment Diagram

```
+----------------------------+
|   Developer Machine / CI  |
|                            |
|  HelloWorld.java           |
|       |                    |
|   javac                    |
|       |                    |
|  HelloWorld.class          |
|       |                    |
|   java HelloWorld          |
|       |                    |
|  stdout: "Hello World"     |
+----------------------------+
```

---

## 8. Crosscutting Concepts

### 8.1 Logging / Output

The application uses `System.out.println` for its sole output. No logging framework is required at this scale.

### 8.2 Error Handling

The application has no external inputs or resources, so no error handling is needed beyond what the JVM provides by default.

---

## 9. Architecture Decisions

### ADR-001: Use of Plain Java (No Framework)

**Status:** Accepted

**Context:**  
The application's only requirement is to print a message to the console. No web server, database, or business logic is needed.

**Decision:**  
Use plain Java with the standard library only. No third-party frameworks or build tools are required.

**Consequences:**  
- Minimal dependencies
- Fast startup time
- Easy to understand and maintain

---

## 10. Quality Requirements

### 10.1 Quality Tree

| Quality        | Scenario                                            | Priority |
|----------------|-----------------------------------------------------|----------|
| Correctness    | Running `java HelloWorld` prints "Hello World"      | High     |
| Simplicity     | Any developer can understand the code in < 1 minute | High     |
| Portability    | Runs on any OS with a compatible JRE                | Medium   |

---

## 11. Risks and Technical Debt

| Risk / Debt        | Description                                          | Mitigation                                      |
|--------------------|------------------------------------------------------|-------------------------------------------------|
| JDK Version        | Application may behave differently on older JDKs    | Target a specific, well-supported JDK version   |
| No build tool      | Manual compilation required; not easily automated   | Consider adding Maven or Gradle in the future   |
| No automated tests | There are no unit tests verifying the output        | Add JUnit tests if the application grows        |

---

## 12. Glossary

| Term   | Definition                                                                 |
|--------|----------------------------------------------------------------------------|
| Arc42  | A template for documenting software architectures, structured in 12 sections |
| JDK    | Java Development Kit – tools required to compile and run Java applications |
| JRE    | Java Runtime Environment – required to run compiled Java applications      |
| JVM    | Java Virtual Machine – the runtime environment that executes Java bytecode |
| stdout | Standard output stream – the default output channel for console applications |
