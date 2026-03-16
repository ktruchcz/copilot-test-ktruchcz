# arc42 Architecture Documentation

**Project:** copilot-test-ktruchcz — Code Migration Orchestration Framework  
**Version:** 1.0  
**Date:** 2026-03-16

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

### 1.1 Purpose

The **Code Migration Orchestration Framework** automates technology migrations between programming languages and frameworks. It coordinates a pipeline of specialized AI agents — Analysis, Migration, and Validation — to migrate an entire application codebase from one technology stack to another with minimal human intervention.

### 1.2 Goals

| Priority | Goal |
|----------|------|
| 1 | Automate source-code analysis and produce a structured migration plan |
| 2 | Migrate all source files to the target technology without manual intervention |
| 3 | Validate and fix the migrated codebase until it compiles and starts |
| 4 | Produce traceable handoff documents at every pipeline stage |
| 5 | Contain all output within a dedicated `output/` directory |

### 1.3 Stakeholders

| Stakeholder | Expectation |
|-------------|-------------|
| Developer / User | Provide source and target technologies; receive a working migrated codebase |
| Orchestrator Agent | Drive the pipeline; delegate all technical work to subagents |
| Analysis Agent | Produce `output/analysis-report.md` within 15 minutes |
| Migration Agent | Produce migrated code and `output/migration-report.md` at maximum speed |
| Validation Agent | Make the migrated code build and start within 20 minutes |

---

## 2. Constraints

### 2.1 Technical Constraints

| Constraint | Rationale |
|------------|-----------|
| All output must be written to `output/` only | Prevents accidental modification of source files |
| Source files are read-only | Ensures the original codebase is never altered |
| No access to parent directories (`../`) | Enforces workspace isolation |
| Each agent is time-boxed (Analysis ≤15 min, Validation ≤20 min) | Prevents indefinite blocking of the pipeline |
| Migration Agent does not fix errors | Separation of concerns; fixing is delegated to Validation Agent |

### 2.2 Organisational Constraints

| Constraint | Rationale |
|------------|-----------|
| Agent communication is file-based only | Enables asynchronous execution and traceable handoffs |
| Validation error retries are limited to 3 per error | Prevents infinite fix loops |
| Orchestrator does not implement any migration logic | Single-responsibility principle for coordination |

---

## 3. Context and Scope

### 3.1 System Context

```
┌─────────────────────────────────────────────────────────┐
│                      User / CI System                   │
│  provides: SOURCE_TECH, TARGET_TECH, source codebase    │
└──────────────────────────┬──────────────────────────────┘
                           │ trigger
                           ▼
            ┌──────────────────────────┐
            │   Migration Orchestrator  │
            │   (orchestrator.agent.md) │
            └──────────────────────────┘
                           │ delegates to
          ┌────────────────┼───────────────────┐
          ▼                ▼                   ▼
  ┌───────────────┐ ┌────────────────┐ ┌──────────────────┐
  │ Analysis Agent│ │ Migration Agent│ │ Validation Agent │
  └───────────────┘ └────────────────┘ └──────────────────┘
          │                │                   │
          └────────────────┴───────────────────┘
                           │ writes to
                    ┌──────────────┐
                    │  output/     │
                    │  directory   │
                    └──────────────┘
```

### 3.2 External Interfaces

| Interface | Direction | Description |
|-----------|-----------|-------------|
| User input | → System | `SOURCE_TECH` and `TARGET_TECH` parameters, source codebase |
| `output/analysis-report.md` | Analysis → Migration | Structured analysis: dependencies, architecture, file catalog, migration order, risks |
| `output/migration-report.md` | Migration → Validation | List of migrated files, target project location, known issues |
| `output/validation-report.md` | Validation → User | Build status, errors fixed, remaining issues |
| `output/{target-app-name}/` | Migration → Validation | Fully migrated target codebase |

---

## 4. Solution Strategy

### 4.1 Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Architecture style | Sequential agent pipeline | Each stage has a clearly scoped responsibility; output of one feeds into the next |
| Agent communication | File-based handoffs (markdown) | Stateless, traceable, and easy to inspect manually |
| Error handling strategy | Time-boxed retries (3 tries / 20 min) | Prevents infinite fix loops while maximising automatic recovery |
| Output isolation | Dedicated `output/` directory | Prevents corruption of the original source |
| Speed vs. quality trade-off | Speed first (migrate all, fix second) | Maximises throughput; validation is a separate concern |

### 4.2 Reusable Skills

Sixteen reusable skills (`R1`–`R6`, `E1`–`E7`, `O1`–`O2`) encapsulate common procedures used by agents, enabling consistent behaviour and reducing duplication across the pipeline.

---

## 5. Building Block View

### 5.1 Level 1 — System Overview

```
┌─────────────────────────────────────────────────────────┐
│             Migration Orchestration Framework           │
│                                                         │
│  ┌────────────────────────────────────────────────┐     │
│  │               Orchestrator Agent               │     │
│  └────────────────────────────────────────────────┘     │
│            │              │              │              │
│  ┌─────────▼────┐  ┌──────▼──────┐  ┌───▼──────────┐  │
│  │ Analysis     │  │  Migration  │  │  Validation  │  │
│  │ Agent        │  │  Agent      │  │  Agent       │  │
│  └──────────────┘  └─────────────┘  └──────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │                   Skills Library                  │   │
│  │  R1 R2 R3 R4 R5 R6   E1 E2 E3 E4 E5 E6 E7   O1 O2  │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 5.2 Level 2 — Agent Responsibilities

#### Orchestrator Agent (`orchestrator.agent.md`)
- **Responsibility:** Coordinate the pipeline; no implementation
- **Tools:** `read`, `edit`
- **Inputs:** `SOURCE_TECH`, `TARGET_TECH` from user
- **Outputs:** Final migration summary

#### Analysis Agent (`analysis.agent.md`)
- **Responsibility:** Analyse source codebase and produce a migration plan
- **Tools:** `read`, `search`, `edit`
- **Inputs:** `SOURCE_TECH`, `TARGET_TECH`, workspace source files
- **Outputs:** `output/analysis-report.md`
- **Time budget:** ≤15 minutes

#### Migration Agent (`migration.agent.md`)
- **Responsibility:** Set up target project and migrate all source files
- **Tools:** `read`, `search`, `edit`, `execute`
- **Inputs:** `output/analysis-report.md`
- **Outputs:** `output/{target-app-name}/`, `output/migration-report.md`
- **Policy:** Migrate all files first; do not fix errors

#### Validation Agent (`validation.agent.md`)
- **Responsibility:** Build, fix, and validate the migrated project
- **Tools:** `read`, `search`, `edit`, `execute`
- **Inputs:** `output/migration-report.md`, `output/{target-app-name}/`
- **Outputs:** `output/validation-report.md`
- **Time budget:** ≤20 minutes; ≤3 fix attempts per error

### 5.3 Skills Library

| Category | Skill | Purpose |
|----------|-------|---------|
| Repetitive Ops | R1 – Parse Source File | Extract structured info from source files |
| Repetitive Ops | R2 – Map Data Types | Translate types between languages |
| Repetitive Ops | R3 – Transform Class | Convert full class/component files |
| Repetitive Ops | R4 – Convert Function Logic | Convert function/method bodies |
| Repetitive Ops | R5 – Fix Import Paths | Update import paths after restructuring |
| Repetitive Ops | R6 – Generate Config | Create build/framework configuration files |
| Error Recovery | E1 – Resolve Missing Import | Fix missing dependencies and imports |
| Error Recovery | E2 – Fix Type Mismatch | Resolve type compatibility issues |
| Error Recovery | E3 – Fix Undefined Property | Fix missing properties/methods |
| Error Recovery | E4 – Resolve Build Config | Fix build system configuration issues |
| Error Recovery | E5 – Fix Dependency Conflict | Resolve dependency tree conflicts |
| Error Recovery | E6 – Handle Missing Feature | Find/implement missing equivalents |
| Error Recovery | E7 – Systematic Batch Fix | Handle many errors by grouping and prioritising |
| Orchestration | O1 – Create Handoff Document | Create structured handoff files |
| Orchestration | O2 – Read Migration Context | Validate and parse upstream handoff documents |

---

## 6. Runtime View

### 6.1 Happy-Path Migration Flow

```
User
 │
 │  "Migrate <SOURCE_TECH> to <TARGET_TECH>"
 ▼
Orchestrator
 │
 │  invoke Analysis Agent
 ▼
Analysis Agent
 │  reads source files, catalogs dependencies & architecture
 │  produces output/analysis-report.md  (status: COMPLETE)
 ▼
Orchestrator
 │  verifies output/analysis-report.md exists
 │  invoke Migration Agent
 ▼
Migration Agent
 │  reads output/analysis-report.md
 │  scaffolds target project
 │  migrates all source files → output/{target-app-name}/
 │  produces output/migration-report.md  (status: COMPLETE)
 ▼
Orchestrator
 │  verifies output/migration-report.md exists
 │  invoke Validation Agent
 ▼
Validation Agent
 │  reads output/migration-report.md
 │  runs build → fixes errors (≤3 tries/error, ≤20 min)
 │  runs start → smoke test
 │  produces output/validation-report.md  (status: COMPLETE)
 ▼
Orchestrator
 │  compiles final summary
 ▼
User  ←  Final migration report
```

### 6.2 Failure Scenarios

| Scenario | Detection | Response |
|----------|-----------|----------|
| `output/analysis-report.md` missing | Migration Agent checks at startup | Stop; report missing file to Orchestrator |
| `output/migration-report.md` missing | Validation Agent checks at startup | Stop; report missing file to Orchestrator |
| Analysis times out (>15 min) | Analysis Agent self-monitors | Finalise partial report; mark incomplete sections |
| Validation cannot fix error in 3 tries | Validation Agent counts retries | Document error; move on |
| Validation time budget exhausted (20 min) | Validation Agent self-monitors | Write final report with remaining issues |

---

## 7. Deployment View

### 7.1 Repository Layout

```
copilot-test-ktruchcz/
├── .github/
│   ├── agents/                    # Agent definition files
│   │   ├── orchestrator.agent.md
│   │   ├── analysis.agent.md
│   │   ├── migration.agent.md
│   │   ├── validation.agent.md
│   │   └── all-in-one-migration.agent.md
│   ├── skills/                    # Reusable skill procedures
│   │   ├── R1-parse-source-file.md
│   │   ├── R2-map-data-types.md
│   │   ├── ...
│   │   ├── E1-resolve-missing-import.md
│   │   ├── ...
│   │   ├── O1-create-handoff-document.md
│   │   └── O2-read-migration-context.md
│   └── hooks/                     # Git hooks (reserved)
├── docs/
│   └── arc42.md                   # This document
├── HelloWorld.java                # Example source file
└── README.md
```

### 7.2 Runtime Output Layout

```
output/                            # Created at runtime; git-ignored
├── analysis-report.md             # Produced by Analysis Agent
├── migration-report.md            # Produced by Migration Agent
├── validation-report.md           # Produced by Validation Agent
└── {target-app-name}/             # Migrated application code
    └── ...
```

### 7.3 Execution Environment

The framework runs entirely within a GitHub Copilot agent workspace. No external services or databases are required. All state is persisted as markdown files within the `output/` directory.

---

## 8. Crosscutting Concepts

### 8.1 Workspace Isolation

Every agent enforces a strict workspace boundary:
- Reads are limited to the current workspace directory tree.
- Writes are limited to `output/`.
- Parent directory access (`../`) is explicitly prohibited.

### 8.2 File-Based State Management

All inter-agent state is stored as structured markdown files in `output/`. This ensures:
- **Traceability:** Each stage's output is inspectable by humans.
- **Resumability:** A failed pipeline can be restarted from the last successful stage.
- **Simplicity:** No shared memory or message bus is required.

### 8.3 Error Handling

| Policy | Details |
|--------|---------|
| Per-error retry limit | 3 attempts per distinct error before skipping |
| Total time budget | 20 minutes for the Validation Agent's fix loop |
| Partial completion | Agents document incomplete work explicitly rather than failing silently |
| Fail-fast on missing handoffs | Agents stop immediately if an upstream handoff file is missing |

### 8.4 Handoff Document Structure

All handoff documents follow the structure defined in skill `O1-create-handoff-document.md` and are validated by skill `O2-read-migration-context.md`. Documents carry a status footer:

- `COMPLETE` — all required sections present and agent finished normally
- `PARTIAL` — agent ran out of time; document contains whatever was completed
- `FAILED` — agent could not complete its primary task

### 8.5 Speed vs. Quality Trade-off

The Migration Agent operates under a "migrate all, fix none" policy to maximise throughput. Error fixing is entirely delegated to the Validation Agent, which has its own time-boxed budget. This separation allows the migration of large codebases without blocking on individual file errors.

---

## 9. Architecture Decisions

### ADR-001: Sequential Agent Pipeline

**Status:** Accepted  
**Context:** Multiple specialised capabilities are required (analysis, code translation, build fixing). A single large agent would be difficult to reason about and maintain.  
**Decision:** Split responsibilities across three sequential agents coordinated by an Orchestrator.  
**Consequences:** Clear separation of concerns; predictable execution order; easy to restart from a failed stage; slightly more overhead than a monolithic approach.

### ADR-002: File-Based Handoffs Over In-Memory State

**Status:** Accepted  
**Context:** Agents are stateless and may run in separate contexts.  
**Decision:** All inter-agent communication uses structured markdown files in `output/`.  
**Consequences:** Human-readable pipeline state; enables debugging; no shared memory required; slight I/O overhead.

### ADR-003: Migrate First, Fix Second

**Status:** Accepted  
**Context:** Stopping migration to fix individual errors would dramatically slow down large migrations.  
**Decision:** The Migration Agent migrates all files without fixing errors. The Validation Agent handles all error correction.  
**Consequences:** Fast migration throughput; Validation Agent may face a large backlog of errors; not suitable for zero-error-tolerance requirements.

### ADR-004: Time-Boxed Error Fixing

**Status:** Accepted  
**Context:** Automated error fixing can loop indefinitely on complex or novel errors.  
**Decision:** Apply a 3-tries-per-error limit and a 20-minute total budget for the Validation Agent.  
**Consequences:** Bounded execution time; some errors may remain unresolved and require manual intervention; known limitations are documented in `output/validation-report.md`.

### ADR-005: Reusable Skills Library

**Status:** Accepted  
**Context:** Common operations (type mapping, file parsing, import fixing) are needed across multiple agents.  
**Decision:** Extract these into 16 named skill documents (`R1`–`R6`, `E1`–`E7`, `O1`–`O2`) that agents reference explicitly.  
**Consequences:** Consistent behaviour across agents; single point of update for common logic; slight indirection.

---

## 10. Quality Requirements

### 10.1 Quality Tree

| Quality Attribute | Scenario | Measure |
|-------------------|----------|---------|
| **Correctness** | Migrated code compiles and starts | Build passes; application starts without runtime error |
| **Completeness** | All source files are migrated | Migration Agent processes 100% of source files listed in the analysis report |
| **Traceability** | Every pipeline stage is inspectable | Handoff documents exist in `output/` after each stage |
| **Reliability** | Pipeline does not hang indefinitely | All agents are time-boxed; partial results are always written |
| **Isolation** | Source files are never modified | Source files remain byte-for-byte identical after migration |
| **Transparency** | Remaining issues are visible | `output/validation-report.md` documents all unresolved errors |

---

## 11. Risks and Technical Debt

### 11.1 Known Risks

| Risk | Severity | Description | Mitigation |
|------|----------|-------------|------------|
| Complex GUI toolkit migration | HIGH | Migrating Swing → React requires significant structural changes beyond type mapping | Risk Assessment section in Analysis Agent flags this; Validation Agent is allocated the full budget |
| Missing direct equivalents | MEDIUM | Some source constructs have no 1:1 equivalent in the target technology | Skill E6 provides strategies; flagged in analysis report |
| Async pattern mismatch | MEDIUM | Thread-based concurrency vs. Promise-based models require architectural changes | Documented in risk assessment; manual review recommended |
| Build system differences | LOW–MEDIUM | Different build tools may require manual configuration | Skill R6 and E4 address common cases |
| Large codebases exceeding time budgets | MEDIUM | Analysis or Validation may not complete within their time budgets | Partial completion is explicitly handled; PARTIAL status in handoff document |

### 11.2 Technical Debt

| Item | Description |
|------|-------------|
| No automated tests for agents | Agent behaviour is defined by markdown prompts; no automated regression testing exists |
| No rollback mechanism | If the pipeline fails mid-run, partial output must be manually cleaned up |
| All-in-one migration agent overlap | `all-in-one-migration.agent.md` overlaps with the orchestrated pipeline; the relationship between the two approaches is not explicitly documented |

---

## 12. Glossary

| Term | Definition |
|------|------------|
| **Agent** | An AI-driven component with a specific, scoped responsibility in the migration pipeline |
| **Analysis Agent** | The agent responsible for analysing the source codebase and producing the migration plan |
| **Migration Agent** | The agent responsible for translating source files to the target technology |
| **Orchestrator Agent** | The coordinating agent that drives the pipeline and manages handoffs |
| **Validation Agent** | The agent responsible for building and fixing the migrated codebase |
| **Handoff Document** | A structured markdown file in `output/` used to pass state between agents |
| **Skill** | A reusable, named procedure document referenced by agents for common operations |
| **SOURCE_TECH** | The technology stack being migrated from (e.g., Java Swing, Flask) |
| **TARGET_TECH** | The technology stack being migrated to (e.g., React 18, FastAPI) |
| **Workspace** | The root directory of the repository; agents must not access anything outside it |
| **output/** | The directory where all agent-generated files and migrated code are written |
| **COMPLETE / PARTIAL / FAILED** | Status values in handoff document footers indicating the outcome of an agent's run |
| **3-tries rule** | The policy of attempting to fix a single error at most 3 times before moving on |
| **Time budget** | The maximum wall-clock time allocated to a given agent phase |
