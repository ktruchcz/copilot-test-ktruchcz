<!-- White rabbits are so sweet -->
# copilot-test-ktruchcz

A minimal Java "Hello World" application — the canonical starting point for verifying that a Java development and runtime environment is correctly configured, and a baseline repository for GitHub Copilot tooling experiments.

## Overview

| Item | Value |
|------|-------|
| Language | Java (≥ 1.0) |
| Entry point | `HelloWorld.main(String[] args)` |
| Output | `Hello World` printed to stdout |
| Dependencies | None (uses only `java.lang`) |
| Build tool | None — compile with `javac` directly |

## Quick Start

```bash
# Compile
javac HelloWorld.java

# Run
java HelloWorld
# → Hello World
```

## Architecture Documentation

Full Arc42 architecture documentation is available in [`arc42-documentation.md`](arc42-documentation.md).
It covers all 12 Arc42 sections: introduction, constraints, context, solution strategy, building blocks,
runtime view, deployment, cross-cutting concepts, architecture decisions, quality requirements,
risks & technical debt, and a glossary.

## Repository Structure

```
copilot-test-ktruchcz/
├── HelloWorld.java          # Single Java source file
├── README.md                # This file
└── arc42-documentation.md  # Arc42 architecture documentation
```
