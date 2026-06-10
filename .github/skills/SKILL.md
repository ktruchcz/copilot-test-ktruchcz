---
name: technology-assessment
description: >
  Assesses the lifecycle status of technology components (OS, databases, frameworks,
  application servers, languages) for each application in the portfolio. Classifies
  components as CURRENT_VERSION, OUTDATED, EOL, or NO_KNOWLEDGE. Use when evaluating
  technology health, identifying EOL risks, or assessing technology currency.
---

# Technology Assessment

Evaluate the lifecycle status of every technology component for each application.

## Input

Read application records from:

- `output/applications/consolidated_schema/consolidated_schema_application_<app_id>.json`
- `output/out_of_scope_results/out_of_scope_<app_id>.json`

Only assess applications where `out_of_scope` is `false`.

## Process

For each application, assess these technology dimensions:

| Dimension | Source field | What to assess |
|-----------|-------------|----------------|
| Operating System | `Operating system` | OS version currency and vendor support status |
| Database | `db_engine` | DB engine version, EOL status, vendor support |
| Programming Language | `programming_language` | Language version, active support window |
| Framework | `framework` or parsed from language/server fields | Framework version, LTS status, security patches |
| Application Server | `Application Server type` | Server version, EOL, known vulnerabilities |

### Status classification

Assign one of these statuses to each component:

| Status | Meaning | Criteria |
|--------|---------|----------|
| `CURRENT_VERSION` | Actively supported | Within vendor's active support window, receiving patches |
| `OUTDATED` | Still supported but aging | In extended support or 1-2 major versions behind current |
| `EOL` | No longer supported | Past vendor EOL date, no security patches |
| `NO_KNOWLEDGE` | Cannot assess | Public lifecycle support information is unavailable |

### Assessment guidelines

- **Use your knowledge** of technology lifecycle dates. For common technologies (Java, .NET, PostgreSQL, MySQL, RHEL, Ubuntu, Windows Server, etc.) you have reliable knowledge of version support timelines.
- **Be conservative**: If uncertain whether something is CURRENT or OUTDATED, choose OUTDATED.
- **Version parsing**: Extract version numbers from strings like "PostgreSQL 14.2" → engine: PostgreSQL, version: 14.2.
- **Composite entries**: If a field contains multiple technologies (e.g., "MySQL 5.7, Redis 6.0"), assess each separately.
- **Provide reasoning**: Always explain why a status was assigned (e.g., "Java 8 reached premier support EOL in March 2022").

## Output format

Save one JSON file per in-scope application to `output/technology_assessment/technology_assessment_<app_id>.json`:

```json
{
  "application_identifier": "app001",
  "components_analyzed": [
    {
      "component_name": "RHEL",
      "component_family": "RHEL",
      "component_type": "os",
      "managed_service": false,
      "version": "8",
      "component_status": "CURRENT_VERSION",
      "eol_date": "2029-05-31",
      "reason": "RHEL 8 is supported until May 2029.",
      "confidence": 9
    }
  ],
  "has_eol_components": false,
  "has_outdated_components": true,
  "has_missing_version_data": false,
  "analysis_timestamp": "2026-04-22T00:00:00Z"
}
```

Use these booleans exactly:

- `has_eol_components`: true if any component has `component_status == "EOL"`
- `has_outdated_components`: true if any component has `component_status == "OUTDATED"`
- `has_missing_version_data`: true if any component has missing/unknown version-support evidence
