---
name: obligatory_java_current_version_update
description: Keep Java source/target/toolchain, CI setup, and all documentation aligned to the repository's current approved Java version. Always apply when touching pom.xml, build.yml, arc42 docs, README, or any file that mentions a Java version. The current approved version for this project is Java 25.
---

# Obligatory Java Current Version Update

The current approved Java version for this project is **Java 25**.

## Mandatory update checklist

### 1. Maven build (`pom.xml`)
- `<java.version>` property → `25`
- `<maven.compiler.source>` → `${java.version}` (or `25`)
- `<maven.compiler.target>` → `${java.version}` (or `25`)
- `<maven.compiler.release>` → `${java.version}` (or `25`)
- `<release>` inside `maven-compiler-plugin` configuration → `${java.version}`

### 2. CI pipeline (`.github/workflows/build.yml`)
- `java-version` field in `actions/setup-java@v4` step → `'25'`
- Distribution must be `temurin` (Eclipse Temurin is the canonical distribution for Java 25 EA/GA)

### 3. Architecture and API documentation (`arc42-documentation.md`, `README.md`)
- Replace all version-specific references (e.g. "JRE 1.0", "Java 8") with **Java 25**
- Update the minimum system requirements table: Java Runtime → **JDK 25 (Temurin)**
- Update Technical Constraints section: remove outdated "no build tool / no tests / no CI" statements
- Reflect actual project state: Maven (`pom.xml`), JUnit 5 tests, GitHub Actions CI
- Remove or supersede any ADRs that are no longer accurate (e.g. "ADR-002 No Build Tool", "ADR-004 No Unit Tests")
- Update code metrics (LOC, class count, method count) to match the actual modernized source
- Update risk register: remove already-resolved risks (R-02 No build automation, R-03 No CI)
- Update technical debt backlog: close already-completed items (TD-01 Add JUnit 5, TD-02 pom.xml, TD-03 GitHub Actions)

### 4. Java source files — use Java 25 idioms
Ensure source code demonstrates and leverages the following features available in Java 25:
- **Records** (GA since Java 16) — use for immutable value objects
- **Sealed interfaces / classes** (GA since Java 17) — use for closed type hierarchies
- **Text blocks** (GA since Java 15) — use for multi-line string literals
- **`var` local-variable type inference** (GA since Java 10)
- **Switch expressions** (GA since Java 14) — use arrow-label `->` form
- **Pattern matching for `switch`** (GA since Java 21) — use guarded patterns (`when`)
- **Pattern matching for `instanceof`** (GA since Java 16)

### 5. Test suite
- Ensure all existing tests compile and pass with `mvn -B test` on Java 25
- Tests must cover all records, sealed hierarchy branches, and utility methods

## Files to verify / update in this project

| File | What to check |
|------|---------------|
| `pom.xml` | `java.version` property = `25`; plugin versions current |
| `.github/workflows/build.yml` | `java-version: '25'`, distribution `temurin` |
| `arc42-documentation.md` | Reflects actual modernized project state |
| `src/main/java/HelloWorld.java` | Uses Java 25 features; AI comment present |
| `src/test/java/HelloWorldTest.java` | Covers all new inner types; AI comment present |
| `HelloWorld.java` (root) | Keep in sync with `src/main/java/HelloWorld.java` or remove as duplicate |
