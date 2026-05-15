# Portfolio Modernization Report

**Generated:** 2026-05-15
**Input Source:** `discover/input/apps_db_complete.xlsx`
**Applications Analyzed:** 30

## Executive Summary

The portfolio analysis was executed using the Excel inventory located in `discover/input/apps_db_complete.xlsx`. Out of 30 applications, 24 are in scope and 6 are out of scope. The technology landscape shows significant lifecycle risk with 46 end-of-life component instances across the in-scope estate. Complexity is primarily medium-to-high, indicating meaningful transformation effort. Financially, the identified modernization opportunities indicate a break-even period of approximately 1.7 years.

## Scope

- **Total applications:** 30
- **In scope:** 24
- **Out of scope:** 6 (`app003`, `app005`, `app007`, `app009`, `app029`, `app030`)

## Technology Lifecycle Summary

| Status | Count |
|--------|-------|
| CURRENT_VERSION | 45 |
| OUTDATED | 13 |
| EOL | 46 |
| NO_KNOWLEDGE | 16 |

## Complexity Summary

| Level | Count |
|-------|-------|
| HIGH | 11 |
| MEDIUM | 19 |
| LOW | 0 |

## Scenario Outcome Summary (In-Scope Apps)

| Outcome | Count |
|---------|-------|
| APPLICABLE | 79 |
| FULFILLED | 76 |
| BLOCKED | 32 |
| PARTIALLY_FULFILLED | 10 |
| NOT_APPLICABLE | 21 |
| LACK_OF_DATA | 22 |

Top applicable scenarios:

1. `update_outdated_components` (17)
2. `os_update_security_patch` (14)
3. `application_server_replacement` (13)
4. `switch_db_engine_open_source` (9)
5. `app_deployment_to_cloud` (8)

## Financial Summary

| Metric | Value |
|--------|-------|
| Applications assessed | 24 |
| Applications with opportunities | 21 |
| Total applicable scenarios | 79 |
| Total one-time investment | €2,165,896 |
| Total annual savings | €1,275,300 |
| Portfolio break-even | 1.7 years |

Missing finance configuration was detected for:

- `switch_db_engine_open_source`
- `update_outdated_components`
