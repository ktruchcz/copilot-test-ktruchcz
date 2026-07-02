# RouteOptApp-011 (app011)

## Application Overview
- Status: Production
- Solution type: Custom made
- Criticality: Medium
- Deployment: AWS
- Users: 125
- Architecture: 3-Tier
- Containerized: Yes
- CI/CD: Yes

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | CentOS 7 | EOL | 2024-06-30 | CentOS 7 reached end-of-life in June 2024. |
| programming_language | Python 3.11 | CURRENT_VERSION | 2027-10-31 | Python 3.11 remains within active support. |
| application_server | Glassfish 4.0 | EOL | n/a | Glassfish 4.0 is end-of-life. |
| database | PostgreSQL 14 | OUTDATED | 2026-11-12 | PostgreSQL 14 is still supported but not the preferred current version. |

## Complexity Assessment
- Complexity score: **4 / 10**
- Complexity label: **Medium**
- Cost multiplier: **1.2x**

- **Business Criticality** (medium): Criticality is Medium and requires controlled cutover planning.
- **Technology Debt** (high): Technology debt includes 2 EOL and 1 outdated component(s).
- **Integration Surface** (medium): The application exposes 12 API endpoints and 5 external interfaces.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | APPLICABLE | $1,200 | $500 | Operating system CentOS 7 is EOL and should be moved to a supported baseline. |
| Switch to standard Linux Operating System | NOT_APPLICABLE | - | - | CentOS 7 is already a Linux-based operating system. |
| Switch to ARM-based CPU | APPLICABLE | $6,000 | $1,000 | The application has cloud or container portability characteristics that make ARM migration feasible. |
| Applications Server replacement | APPLICABLE | $12,000 | $12,000 | Application server Glassfish 4.0 is EOL and should be replaced or upgraded. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | FULFILLED | - | - | The application is already fully deployed in AWS. |
| Application Containerization | FULFILLED | - | - | The application is already containerized. |
| Application Refactoring and De-coupling | APPLICABLE | $300,000 | $150,000 | The recorded architecture (3-Tier) suggests a layered or monolithic design suitable for decoupling. |
| Upgrade Legacy Databases | APPLICABLE | $12,000 | $10,000 | Database engine PostgreSQL 14 is OUTDATED and should be upgraded. |
| Switch to Managed Database | APPLICABLE | $6,000 | $10,000 | PostgreSQL 14 is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $6,000 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | NOT_APPLICABLE | - | - | PostgreSQL 14 is already PostgreSQL-based. |

## Business Case
- Applicable scenarios: os_update_security_patch, switch_to_arm_cpu, application_server_replacement, app_refactor_decoupling, upgrade_legacy_databases, switch_to_managed_db, managed_arm_db
- Migration cost: $343,200
- Yearly savings: $188,500
- Three-year ROI: 64.8%
- Payback period: 1.82 years
