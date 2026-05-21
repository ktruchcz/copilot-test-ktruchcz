# Analysis Summary

**Source Technology:** Java 25 / Maven / JUnit 5
**Target Technology:** Python 3 / pyproject.toml (hatchling) / pytest
**Analysis Date:** 2025-07-11
**Total Source Files Analysed:** 4
*(HelloWorld.java × 2 identical copies · HelloWorldTest.java × 1 · pom.xml × 1)*

---

## 1. Application Overview

The application is the simplest possible Java program: a single public class `HelloWorld` whose `main` method writes the string `"Hello World"` (plus a trailing OS newline supplied automatically by `println`) to standard output. There is no user input, no file I/O, no networking, no database access, and no third-party **runtime** dependency.

## 2. Source File Inventory

| # | Path | Role | Lines |
|---|------|------|-------|
| 1 | `HelloWorld.java` (repo root) | Application entry point — **duplicate, discard** | 7 |
| 2 | `src/main/java/HelloWorld.java` | Application entry point — **canonical** | 7 |
| 3 | `src/test/java/HelloWorldTest.java` | JUnit 5 unit test — stdout capture | 26 |
| 4 | `pom.xml` | Maven build / dependency descriptor | 56 |

> **Note:** The root-level `HelloWorld.java` and `src/main/java/HelloWorld.java` are byte-for-byte identical. The root copy is a leftover artefact and is not migrated as a separate file.

## 3. Source Constructs Inventory

| Java Construct | Location | Notes |
|----------------|----------|-------|
| `public class HelloWorld` | `HelloWorld.java:2` | Top-level public class |
| `public static void main(String[] args)` | `HelloWorld.java:4` | JVM entry point; `args` is **unused** |
| `System.out.println("Hello World")` | `HelloWorld.java:5` | Writes string + OS newline to stdout |
| `@Test` annotation | `HelloWorldTest.java:12` | JUnit 5 Jupiter test marker |
| `ByteArrayOutputStream` / `PrintStream` | `HelloWorldTest.java:14–18` | Manual stdout-capture boilerplate |
| `System.setOut(…)` / restore in `finally` | `HelloWorldTest.java:15–21` | Stdout swap |
| `assertEquals(expected, actual)` | `HelloWorldTest.java:24` | JUnit assertion |
| `System.lineSeparator()` | `HelloWorldTest.java:24` | Platform newline |

## 4. Dependencies

| Dependency | Scope | Version | Python Equivalent |
|------------|-------|---------|-------------------|
| `org.junit.jupiter:junit-jupiter` | test | 5.11.4 | `pytest >= 8.0` |
| Maven Compiler Plugin | build | 3.13.0 | n/a — Python is interpreted |
| Maven Surefire Plugin | build | 3.5.2 | n/a — `pytest` runs tests directly |

---

# Migration Plan

## Step 1 — Map the entry-point class to a Python module

**Java → Python mapping:**

| Java construct | Python equivalent | Rationale |
|----------------|-------------------|-----------|
| `public class HelloWorld { … }` | *removed* | Python modules are top-level; no class wrapper needed |
| `public static void main(String[] args)` | `def main() -> None:` | No class, no static keyword, no args parameter (unused in source) |
| `System.out.println("Hello World")` | `print("Hello World")` | `print()` appends `"\n"` by default — identical behaviour |
| JVM `main` entry-point convention | `if __name__ == "__main__": main()` | Idiomatic Python entry-point guard |

**Target `hello_world.py`:**
```python
# Migrated from src/main/java/HelloWorld.java
def main() -> None:
    print("Hello World")


if __name__ == "__main__":
    main()
```

## Step 2 — Map the JUnit 5 test to pytest

| Java construct | Python equivalent | Rationale |
|----------------|-------------------|-----------|
| `ByteArrayOutputStream` + `System.setOut` boilerplate | `capsys` fixture | pytest built-in; zero boilerplate, thread-safe |
| `@Test` annotation | `def test_…():` naming convention | pytest discovers `test_` prefixed functions automatically |
| `assertEquals(expected, actual)` | `assert actual == expected` | pytest rewrites plain `assert` with full diff output |
| `System.lineSeparator()` | `"\n"` (hard-coded) | Python `print()` always uses `"\n"` |
| `HelloWorld.main(new String[0])` | `main()` | Direct function call after `from hello_world import main` |

**Target `tests/test_hello_world.py`:**
```python
# Migrated from src/test/java/HelloWorldTest.java
from hello_world import main


def test_main_prints_hello_world_with_trailing_newline(capsys) -> None:
    main()
    captured = capsys.readouterr()
    assert captured.out == "Hello World\n"
```

## Step 3 — Replace pom.xml with pyproject.toml

| Maven field | Value | pyproject.toml field |
|-------------|-------|----------------------|
| `artifactId` | `hello-world` | `[project] name = "hello-world"` |
| `version` | `1.0.0` | `[project] version = "1.0.0"` |
| `description` | "A simple Hello World…" | `[project] description = "…"` |
| `junit-jupiter` (test scope) | 5.11.4 | `[project.optional-dependencies] dev = ["pytest>=8.0"]` |

**Target `pyproject.toml`:**
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "hello-world"
version = "1.0.0"
description = "A simple Hello World application"
requires-python = ">=3.11"

[project.optional-dependencies]
dev = ["pytest>=8.0"]

[project.scripts]
hello-world = "hello_world:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

## Step 4 — Target file layout

```
hello_world.py                  ← main application module
tests/
    __init__.py                 ← empty package marker (pytest import compatibility)
    test_hello_world.py         ← pytest test module
pyproject.toml                  ← replaces pom.xml
```

## Step 5 — Migration execution order

1. `pyproject.toml` — project scaffold
2. `hello_world.py` — application logic
3. `tests/__init__.py` — empty package marker
4. `tests/test_hello_world.py` — test module

---

# File Mapping

| Source File | Target File | Action | Notes |
|-------------|-------------|--------|-------|
| `src/main/java/HelloWorld.java` | `hello_world.py` | **Migrate** | Canonical source |
| `HelloWorld.java` (repo root) | *(none)* | **Discard** | Byte-for-byte duplicate of canonical source |
| `src/test/java/HelloWorldTest.java` | `tests/test_hello_world.py` | **Migrate** | Rewritten using `capsys`; semantics preserved |
| `pom.xml` | `pyproject.toml` | **Replace** | All relevant metadata preserved |
| *(new)* | `tests/__init__.py` | **Create** | Empty file — pytest package marker |

---

# Risk Assessment

| # | Risk | Severity | Recommended Approach |
|---|------|----------|----------------------|
| 1 | **Duplicate source file** — `HelloWorld.java` exists at repo root *and* under `src/main/java/` | LOW | Migrate only `src/main/java/HelloWorld.java` |
| 2 | **Platform newline divergence** — Java test uses `System.lineSeparator()` | LOW | Assert against hard-coded `"Hello World\n"` in Python |
| 3 | **`args` parameter removed** — `main(String[] args)` → `def main() -> None:` | LOW | Safe — `args` is completely unused |
| 4 | **pytest import discovery** | LOW | Create empty `tests/__init__.py` |
| 5 | **Build toolchain fully replaced** | LOW | CI pipeline change: `mvn test` → `python -m pytest` |

### Overall Migration Risk: 🟢 LOW

Estimated implementation effort: < 30 minutes, zero architectural decisions required.
