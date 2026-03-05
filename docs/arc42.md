# arc42 Architecture Documentation

## HelloWorld Application

**Version:** 1.0  
**Date:** 2026-03-05

---

## 1. Introduction and Goals

### 1.1 Requirements Overview

The HelloWorld application is a minimal Java program that demonstrates a basic runnable Java class. Its sole purpose is to print "Hello World" to the standard output.

### 1.2 Quality Goals

| Priority | Quality Goal | Motivation |
|----------|-------------|------------|
| 1 | Simplicity | The application is a single-class proof-of-concept with no dependencies |
| 2 | Readability | Code is self-explanatory and easy to understand |

### 1.3 Stakeholders

| Role | Name | Expectations |
|------|------|-------------|
| Developer | ktruchcz | Working, buildable Java program |

---

## 2. Architecture Constraints

| Constraint | Background |
|-----------|------------|
| Java | The application is implemented in Java |
| No external dependencies | No libraries or frameworks are used |
| Single class | The entire application fits in one `.java` file |

---

## 3. System Scope and Context

### 3.1 Business Context

The HelloWorld application has no external interfaces. It receives no input and produces a single line of text output.

```
+-------------------+          stdout
|   HelloWorld App  | -------> "Hello World"
+-------------------+
```

### 3.2 Technical Context

| Channel | Input | Output |
|---------|-------|--------|
| Standard Output (stdout) | — | "Hello World" |

---

## 4. Solution Strategy

The simplest possible Java program structure is used: a single public class with a `main` method that calls `System.out.println`.

---

## 5. Building Block View

### 5.1 Level 1 – Overall System

The application consists of a single building block:

| Class | Responsibility |
|-------|---------------|
| `HelloWorld` | Entry point; prints "Hello World" to stdout |

---

## 6. Runtime View

### 6.1 Application Start

1. JVM starts and calls `HelloWorld.main(String[] args)`
2. `System.out.println("Hello World")` writes the string to stdout
3. The JVM exits normally

---

## 7. Deployment View

The application is deployed as a single compiled `.class` file (or packaged in a `.jar`). It requires a JRE (Java Runtime Environment) to execute.

```
+-------------------------+
|  Host machine (any OS)  |
|  +-------------------+  |
|  |   JRE             |  |
|  |  HelloWorld.class |  |
|  +-------------------+  |
+-------------------------+
```

**Build and run:**
```bash
javac HelloWorld.java
java HelloWorld
```

---

## 8. Cross-cutting Concepts

| Concept | Description |
|---------|-------------|
| Logging | Application output is written directly to `System.out` |
| Error handling | No error handling is required for this application |

---

## 9. Architecture Decisions

### ADR-001: Single-class design

**Status:** Accepted  
**Context:** The application only needs to print one message.  
**Decision:** Implement the application as a single Java class with a `main` method.  
**Consequences:** Maximum simplicity; no extensibility required.

---

## 10. Quality Requirements

| Quality Attribute | Scenario | Measure |
|------------------|----------|---------|
| Correctness | Running the application produces "Hello World" on stdout | Manual / automated verification |
| Portability | Runs on any OS with a compatible JRE | Tested on standard JRE 8+ |

---

## 11. Risks and Technical Debts

| ID | Risk / Debt | Priority | Mitigation |
|----|-------------|----------|-----------|
| R1 | No automated tests | Low | Add a JUnit test if the application grows |
| R2 | No build system (Maven/Gradle) | Low | Introduce a build tool if more classes are added |

---

## 12. Glossary

| Term | Definition |
|------|-----------|
| JVM | Java Virtual Machine – runtime environment that executes Java bytecode |
| JRE | Java Runtime Environment – minimum Java installation needed to run a compiled Java program |
| arc42 | A pragmatic, lightweight template for documenting software architectures |
| stdout | Standard output stream – the default destination for text output in a command-line program |
