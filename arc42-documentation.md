# arc42 Architecture Documentation

## ERPApp

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
8. [Cross-cutting Concepts](#8-cross-cutting-concepts)
9. [Architecture Decisions](#9-architecture-decisions)
10. [Quality Requirements](#10-quality-requirements)
11. [Risks and Technical Debt](#11-risks-and-technical-debt)
12. [Glossary](#12-glossary)

---

## 1. Introduction and Goals

### 1.1 Requirements Overview

ERPApp is a Java-based application currently in its initial phase. The application starts with a simple "Hello World" entry point, serving as the foundation for a future ERP (Enterprise Resource Planning) system.

**Core functional requirements:**
- Provide a runnable Java entry point
- Output a greeting message to confirm the application starts correctly

### 1.2 Quality Goals

| Priority | Quality Goal      | Scenario                                          |
|----------|-------------------|---------------------------------------------------|
| 1        | Reliability       | The application starts and executes without errors |
| 2        | Maintainability   | Code is simple, readable, and easy to extend      |
| 3        | Portability       | Runs on any platform supporting a JVM             |

### 1.3 Stakeholders

| Role        | Name/Description              | Expectations                              |
|-------------|-------------------------------|-------------------------------------------|
| Developer   | ktruchcz                      | Clean, working codebase to build upon     |
| End User    | Future ERP system users       | A reliable, functional ERP application   |

---

## 2. Constraints

### 2.1 Technical Constraints

| Constraint         | Description                                     |
|--------------------|-------------------------------------------------|
| Java               | Application is implemented in Java              |
| JVM                | Requires a Java Virtual Machine to run          |
| No build tool yet  | No Maven/Gradle configuration present currently |

### 2.2 Organizational Constraints

| Constraint         | Description                                          |
|--------------------|------------------------------------------------------|
| Version Control    | Source code is managed in GitHub                     |
| Early Stage        | Project is in initial/prototype phase                |

---

## 3. Context and Scope

### 3.1 Business Context

```
┌───────────────────────────────────────────────┐
│                    ERPApp                       │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │            HelloWorld (main)              │ │
│  │    Prints "Hello World" to stdout         │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
└───────────────────────────────────────────────┘
              │
              ▼
       Standard Output (Console)
```

| Neighbour System / Actor | Description                                      |
|--------------------------|--------------------------------------------------|
| JVM (Java Virtual Machine) | Executes the compiled bytecode                 |
| Standard Output (Console)  | Receives and displays the application output   |
| Developer / User           | Invokes the application and reads the output   |

### 3.2 Technical Context

The application communicates solely through standard output (`System.out`). There are no external interfaces, databases, or network connections at this stage.

---

## 4. Solution Strategy

The application is intentionally simple at this stage. The chosen strategy is:

- **Programming Language:** Java — widely used, platform-independent via the JVM
- **Entry Point:** A single `main` method in `HelloWorld.java`
- **Incremental Development:** Starting with a minimal working application, extending it toward a full ERP system in future iterations

---

## 5. Building Block View

### 5.1 Level 1 — Whitebox: Overall System

```
┌─────────────────────────────────────┐
│              ERPApp                  │
│                                      │
│   ┌──────────────────────────────┐  │
│   │         HelloWorld           │  │
│   │  + main(String[] args): void │  │
│   └──────────────────────────────┘  │
│                                      │
└─────────────────────────────────────┘
```

| Building Block | Responsibility                                           |
|----------------|----------------------------------------------------------|
| `HelloWorld`   | Application entry point; outputs a greeting to console   |

---

## 6. Runtime View

### 6.1 Application Startup

```
User/Script           JVM                  HelloWorld
     │                  │                       │
     │── java HelloWorld ──>                    │
     │                  │── main(args) ────────>│
     │                  │                       │── System.out.println("Hello World")
     │                  │                       │
     │<── exit ─────────│<──────────────────────│
```

**Steps:**
1. The user (or script) invokes `java HelloWorld`
2. The JVM loads and executes the `main` method
3. `HelloWorld.main` prints "Hello World" to standard output
4. The JVM exits normally

---

## 7. Deployment View

### 7.1 Infrastructure

```
┌──────────────────────────────────────┐
│         Developer Machine            │
│                                      │
│   ┌──────────────────────────────┐  │
│   │     Java Runtime (JVM)       │  │
│   │                              │  │
│   │  ┌────────────────────────┐  │  │
│   │  │   HelloWorld.class     │  │  │
│   │  │  (compiled bytecode)   │  │  │
│   │  └────────────────────────┘  │  │
│   └──────────────────────────────┘  │
│                                      │
└──────────────────────────────────────┘
```

**Deployment steps:**
1. Compile: `javac HelloWorld.java`
2. Run: `java HelloWorld`

**Requirements:**
- Java Development Kit (JDK) for compilation
- Java Runtime Environment (JRE) or JDK for execution

---

## 8. Cross-cutting Concepts

### 8.1 Logging / Output

Currently, the application uses `System.out.println` for output. In future iterations, a logging framework (e.g., SLF4J, Log4j) should be introduced.

### 8.2 Error Handling

No explicit error handling is implemented at this stage. The JVM handles any unexpected runtime errors.

### 8.3 Coding Conventions

- Standard Java naming conventions apply
- Each class resides in its own `.java` file

---

## 9. Architecture Decisions

### ADR-001: Use Java as the implementation language

**Status:** Accepted  
**Context:** The project requires a widely-supported, object-oriented language for building an ERP system.  
**Decision:** Java is used as the primary programming language.  
**Consequences:**
- Platform independence via the JVM
- Large ecosystem of libraries and frameworks available for future ERP functionality
- Requires a JRE/JDK on the target machine

### ADR-002: Start with a minimal Hello World application

**Status:** Accepted  
**Context:** The project is at an early stage and needs a working foundation.  
**Decision:** Begin with a single `HelloWorld` class as the entry point.  
**Consequences:**
- Immediate working application that can be built upon
- No unnecessary complexity at the start

---

## 10. Quality Requirements

### 10.1 Quality Tree

```
Quality
├── Reliability
│   └── Application starts and runs without errors
├── Maintainability
│   └── Code is readable, well-structured, and easy to extend
├── Portability
│   └── Runs on any platform with a JVM (Windows, Linux, macOS)
└── Performance
    └── Startup time is negligible for current scope
```

### 10.2 Quality Scenarios

| ID  | Quality Attribute | Scenario                                                              | Expected Response                  |
|-----|-------------------|-----------------------------------------------------------------------|------------------------------------|
| QS1 | Reliability       | Developer runs `java HelloWorld` on a machine with JRE installed      | "Hello World" is printed; exit 0   |
| QS2 | Portability       | Application is compiled and run on Windows, Linux, and macOS          | Consistent behaviour on all platforms |
| QS3 | Maintainability   | New developer reads the codebase for the first time                   | Understands structure within minutes |

---

## 11. Risks and Technical Debt

| ID  | Risk / Technical Debt                            | Probability | Impact | Mitigation                                              |
|-----|--------------------------------------------------|-------------|--------|---------------------------------------------------------|
| R1  | No build tool (Maven/Gradle) configured          | High        | Medium | Introduce a build tool as the project grows             |
| R2  | No automated tests                               | High        | Medium | Add unit tests (e.g., JUnit) as functionality expands   |
| R3  | No package structure                             | Medium      | Low    | Introduce Java packages when adding more classes        |
| R4  | `System.out` used instead of a logging framework | Medium      | Low    | Replace with a logging framework in future iterations   |

---

## 12. Glossary

| Term  | Definition                                                                 |
|-------|----------------------------------------------------------------------------|
| ERP   | Enterprise Resource Planning — software for managing business processes    |
| JVM   | Java Virtual Machine — the runtime environment for executing Java bytecode |
| JDK   | Java Development Kit — tools for compiling and running Java applications   |
| JRE   | Java Runtime Environment — minimal environment for running Java programs   |
| arc42 | A template for documenting software and system architecture                |
| ADR   | Architecture Decision Record — a document capturing an architectural choice |
