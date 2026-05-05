---
name: complexity-assessment
description: >
  Scores the modernization complexity of each application on a 1-10 scale, considering
  server count, dependencies, technology age, EOL components, business criticality,
  and integration complexity. Classifies as LOW (1-3), MEDIUM (4-6), or HIGH (7-10).
  Use when scoring application complexity, estimating modernization effort, or
  prioritizing applications for transformation.
---

# Complexity Assessment

Score each application's modernization complexity on a 1-10 scale.

## Input

Read these files:
- `output/applications/consolidated_schema/consolidated_schema_application_<app_id>.json` — normalized application input
- `output/technology_assessment/technology_assessment_<app_id>.json` — per-application component lifecycle statuses
- `output/out_of_scope_results/out_of_scope_<app_id>.json` — in-scope filter

Only compute complexity for applications where `out_of_scope` is `false`.

## Scoring model

Evaluate each application across these factors. Each factor contributes to the final score.

### Factor weights

| Factor | Weight | Score range | How to assess |
|--------|--------|-------------|---------------|
| Technology age & EOL | 25% | 1-10 | More EOL/outdated components → higher score |
| Integration complexity | 20% | 1-10 | More interfaces and dependencies → higher |
| Infrastructure scale | 15% | 1-10 | More servers/environments → higher |
| Business criticality | 15% | 1-10 | Higher criticality → higher complexity (risk) |
| Code & architecture | 15% | 1-10 | Legacy patterns, monolith → higher |
| Data complexity | 10% | 1-10 | Multiple databases, large data → higher |

### Scoring guidelines per factor

**Technology age & EOL (25%)**
- 1-3: All components current, no EOL concerns
- 4-6: Some outdated components, approaching EOL
- 7-10: Multiple EOL components, critical security gaps

**Integration complexity (20%)**
- 1-3: 0-2 interfaces, loosely coupled
- 4-6: 3-5 interfaces, some tight coupling
- 7-10: 6+ interfaces, deeply integrated with other systems

**Infrastructure scale (15%)**
- 1-3: 1-2 servers, single environment
- 4-6: 3-5 servers, multiple environments
- 7-10: 6+ servers, complex multi-environment setup

**Business criticality (15%)**
- 1-3: Low criticality, few users
- 4-6: Medium criticality, moderate user base
- 7-10: Business-critical, high user count, revenue-impacting

**Code & architecture (15%)**
- 1-3: Modern stack, microservices, containerized
- 4-6: Mixed architecture, some legacy patterns
- 7-10: Monolith, legacy language, no CI/CD

**Data complexity (10%)**
- 1-3: Single database, straightforward schema
- 4-6: Multiple data stores, moderate data volume
- 7-10: Complex data landscape, legacy databases, data migration challenges

### Computing the final score

```
final_score = round(
    tech_age * 0.25 +
    integration * 0.20 +
    infrastructure * 0.15 +
    criticality * 0.15 +
    architecture * 0.15 +
    data * 0.10
)
```

Clamp the result to 1-10.

### Classification

| Range | Level | Meaning |
|-------|-------|---------|
| 1-3 | `LOW` | Straightforward modernization, limited risk |
| 4-6 | `MEDIUM` | Moderate effort, some risk factors |
| 7-10 | `HIGH` | Complex transformation, significant planning needed |

## Rules

- **Only use available data.** If a factor cannot be assessed due to missing information, use a neutral score of 5 for that factor and note it in the reasoning.
- **Provide per-factor reasoning.** Explain each factor score so the assessment is traceable.
- **Consider EOL from technology assessment.** Applications with `EOL` components get a minimum technology age score of 7.
- **Confidence must be numeric.** Use integer confidence from 1 to 10.

## Output format

Save one JSON file per in-scope application to `output/complexity_results/complexity_<app_id>.json`:

```json
{
  "application_identifier": "app001",
  "complexity_score": 7,
  "confidence": 8,
  "reasoning": "Business-critical app with multiple integrations and one outdated technology.",
  "contributing_factors": {
    "number_of_servers": 2,
    "number_of_databases": 1,
    "number_of_environments": 2,
    "number_of_interfaces": 5,
    "business_criticality": "High",
    "number_of_outdated_technologies": 1,
    "number_of_eol_technologies": 0,
    "number_of_dependencies": 0,
    "ci_cd_present": "No",
    "containerized": "No"
  }
}
```

Do not include legacy fields like `complexity_level`, `factors`, or `overall_reasoning` in the per-app output file.
