---
description: Create or update the speckit prompts based on provided principle inputs, ensuring all dependent templates stay in sync.
tools: [vscode, execute, read, edit, search, browser, todo]
handoffs: 
  - label: Build Specification 
    agent: speckit.constitution
    prompt: Build the feature specification based on the principle inputs. I want to build...
---

# Main Objective

The main objective is to migrate the entire application from source technology to another.

## Parameter Extraction

**Extract from user message:**
- `SOURCE_TECH:` (e.g., "Java Swing", "Flask", "Spring Boot")
- `TARGET_TECH:` (e.g., "React 18", "FastAPI", "Angular 17")

If unclear, ask: "What is the source technology and what should it be migrated to?"


The purpose of that is modernization and maintainability.

Your task is to complete all Spec Kit prompt files so that they can generate correct Spec Driven Development artifacts.

To do this correctly, you need to review the project structure and consider the following user instruction:

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Each .prompt.md file must include:

- The purpose of the prompt
- Instructions on what the agent should generate
- The expected output format
- Guidelines on how to interpret the source and target technologies
- How to use the user's context
- Migrated code in Angular must be functionally equivalent to the original Swing code, following Angular best practices and design patterns.
- Migrated code should be saved in main project directory in "output"


List of files to edit, in the order in which the agents using them will be invoked:

- speckit.constitution.prompt.md
- speckit.specify.prompt.md
- speckit.clarify.prompt.md
- speckit.plan.prompt.md
- speckit.checklist.prompt.md
- speckit.tasks.prompt.md
- speckit.analyze.prompt.md
- speckit.implement.prompt.md


After **ALL** prompts have been completed, orchestrator must run the speckit agent `speckit.constitution`.

