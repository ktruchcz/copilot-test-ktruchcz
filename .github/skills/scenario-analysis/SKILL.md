---
name: scenario-analysis
description: >
  Evaluates modernization scenarios against each application in the portfolio. Uses
  scenario definitions with trigger criteria, exclusions, and fulfillment indicators.
  Classifies each scenario-application pair as FULFILLED, PARTIALLY_FULFILLED,
  APPLICABLE, BLOCKED, NOT_APPLICABLE, or LACK_OF_DATA. Use when assessing modernization options,
  identifying transformation opportunities, or evaluating scenario applicability.
---

# Scenario Analysis

Evaluate which modernization scenarios apply to each application.

## Input

Read these files:
- `output/applications/consolidated_schema/consolidated_schema_application_<app_id>.json` — normalized application JSON files
- `output/technology_assessment/technology_assessment_<app_id>.json` — per-application component lifecycle statuses
- `output/complexity_results/complexity_<app_id>.json` — per-application complexity assessments
- `references/modernization_scenarios_list.json` (bundled with this skill) — scenario definitions

First generate out-of-scope decisions for all applications, then scenario applicability
only for in-scope applications.

Out-of-scope output (all apps):
- `output/out_of_scope_results/out_of_scope_<app_id>.json`

Scenario output (in-scope apps only):
- `output/scenario_applicability_results/scenario_assessment_<app_id>.json`

## Understanding scenario definitions

Each scenario in the config has this structure:

```json
{
  "scenario_id": "os_update_security_patch",
  "scenario_name": "Operating System Update",
  "criteria": {
    "primary_triggers": ["conditions that make this scenario relevant"],
    "secondary_conditions": ["supporting signals that strengthen the case"],
    "exclusion_criteria": ["conditions that rule out this scenario"],
    "fulfilled_indicators": ["signs the scenario is already done"]
  },
  "modernization_suggestion": "What to do",
  "reasoning": "Why this matters",
  "priority": "High|Medium|Low",
  "modernization_effects": ["security", "cost", "agility", "sustainability"],
  "technical_focus": "Operating System|Application|Database|Storage|Observability",
  "cloud_adaption_level": "High|Medium|Low",
  "effort": "High|Medium|Low"
}
```

## Evaluation process

For each application:

### Step 0: Determine out-of-scope status

Always write an out-of-scope file with at least exclusions `RETIRED` and `SAP`.

If application is out-of-scope, skip scenario evaluation for that application.

Example out-of-scope file:

```json
{
  "application_identifier": "app001",
  "assessments": [
    {
      "exclusion_type": "RETIRED",
      "applies": false,
      "confidence": 9,
      "reasoning": "Application status is Production."
    },
    {
      "exclusion_type": "SAP",
      "applies": false,
      "confidence": 9,
      "reasoning": "No SAP indicators found in solution type or description."
    }
  ],
  "out_of_scope": false
}
```

For each in-scope application × scenario pair:

### Step 1: Check fulfilled indicators first

If any fulfilled indicator matches → status = `FULFILLED`.
The scenario's goal is already achieved; no action needed.

### Step 2: Check exclusion criteria

If any exclusion criterion matches:
- Use `BLOCKED` for hard constraints (vendor lock-in, unsupported platform constraints, non-refactorable 3rd party app).
- Use `NOT_APPLICABLE` for natural non-fit where the scenario simply does not apply.
The scenario cannot or should not be applied.

### Step 3: Check primary triggers

If at least one primary trigger matches → the scenario is potentially applicable.
If no primary trigger matches → status = `NOT_APPLICABLE`.

### Step 4: Assess applicability

If primary triggers match and no exclusions apply:
- If enough data exists to make a confident assessment → `APPLICABLE`
- If critical data is missing → `LACK_OF_DATA`
- If there is strong but incomplete evidence of fulfillment → `PARTIALLY_FULFILLED`

### Matching rules

- **Semantic matching, not string matching.** "Operating System Version is Outdated" matches an application with RHEL 6 (which is EOL), even if the Excel doesn't literally say "outdated".
- **Use technology assessment results.** If the technology assessment found a component is EOL, that directly triggers related scenarios.
- **Missing data.** If the data needed to evaluate a trigger is not available, skip that trigger. If ALL primary triggers require missing data → `LACK_OF_DATA`.
- **Note secondary conditions.** These strengthen the case but don't trigger on their own. Mention matching secondary conditions in reasoning.

## Output format

Save one JSON file per in-scope application to
`output/scenario_applicability_results/scenario_assessment_<app_id>.json`:

```json
{
  "application_identifier": "app001",
  "scenarios_detailed": [
    {
      "id": "os_update_security_patch",
      "status": "FULFILLED",
      "match_type": "ai",
      "reason": "Operating system AIX 7.2 is currently supported.",
      "confidence": 9,
      "source": {
        "document_id": "",
        "document_title": "",
        "section": "",
        "content_excerpt": "",
        "relevance": ""
    }
    }
  ]
}
```

Per-scenario objects must contain:

- `id`
- `status`
- `match_type`
- `reason`
- `confidence` (1-10 integer)
- `source`

Do not include `scenario_name` in scenario entries.

Allowed status values for per-scenario output are:

- `FULFILLED`
- `PARTIALLY_FULFILLED`
- `APPLICABLE`
- `BLOCKED`
- `NOT_APPLICABLE`
- `LACK_OF_DATA`

## Scenario reference

The full scenario definitions are bundled with this skill at [references/modernization_scenarios_list.json](references/modernization_scenarios_list.json).
Read that file at the start of this step. It contains all trigger criteria, exclusions, and fulfillment indicators.
