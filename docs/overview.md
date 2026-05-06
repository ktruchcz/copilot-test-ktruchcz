# Overview

`copilot-test-ktruchcz` is a minimal Java 21 console application that prints a time-aware greeting to stdout. It serves as a baseline environment validator and a sandbox for GitHub Copilot experiments.

## Purpose

The application demonstrates several modern Java language features in a single, self-contained source file. Running it confirms that the Java 21 toolchain is correctly configured.

## Key Features

| Feature | Java Version | Description |
|---------|-------------|-------------|
| Records | Java 16+ | Immutable `Greeting` value object with compact constructor validation |
| Sealed interfaces | Java 17+ | `TimeOfDay` hierarchy with `Morning`, `Afternoon`, and `Evening` subtypes |
| Pattern matching in switch | Java 21 | Maps `TimeOfDay` instances to salutation strings |
| Text blocks | Java 15+ | Multi-line string for the greeting banner |
| `var` type inference | Java 10+ | Used throughout `main` for local variables |
| Guarded patterns | Java 21 | `case Integer h when h < 12` in `TimeOfDay.of` |

## Output

When executed, the application prints a greeting banner followed by runtime metadata:

```
╔══════════════════════════════╗
║  Good morning, World!  ║
╚══════════════════════════════╝
Java version : 21.0.x
Today's date : 2026-05-06 (Spring)
```

The salutation (`Good morning` / `Good afternoon` / `Good evening`) is derived from the current day-of-month modulo 24, mapped to a `TimeOfDay` value. The season is derived from the current month.

## Design Decisions

- **Single-class design** — all logic lives in `HelloWorld.java` to keep the example self-contained.
- **No external dependencies** — only the standard Java library (`java.time`) is used.
- **Validation in constructors** — `Greeting`'s compact constructor guards against blank inputs, illustrating idiomatic record design.
- **Sealed types for exhaustive switches** — using a sealed interface ensures the compiler enforces handling of all `TimeOfDay` variants.

*Last updated: 2026-05-06*
