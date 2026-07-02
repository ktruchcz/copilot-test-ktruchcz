# ComplianceApp-022 (app022)

## Application Overview
- Status: Production
- Solution type: Custom made
- Criticality: Critical
- Deployment: AWS, On-premise
- Users: 310
- Architecture: 3-Tier
- Containerized: Yes
- CI/CD: Yes

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | RHEL 7 | EOL | 2024-06-30 | RHEL 7 reached end of maintenance support in June 2024. |
| programming_language | Scala 2.13 | OUTDATED | n/a | Scala 2.13 is still usable but Scala 3 is the current strategic direction. |
| application_server | Payara 6.0 | CURRENT_VERSION | n/a | Payara 6 is the current supported major line. |
| database | PostgreSQL 14 | OUTDATED | 2026-11-12 | PostgreSQL 14 is still supported but not the preferred current version. |

## Complexity Assessment
- Complexity score: **6 / 10**
- Complexity label: **Medium**
- Cost multiplier: **1.2x**

- **Technology Debt** (high): Technology debt includes 1 EOL and 2 outdated component(s).
- **Integration Surface** (high): The application exposes 16 API endpoints and 12 external interfaces.
- **Deployment Model** (medium): Deployment includes on-premise infrastructure, increasing migration and network dependency complexity.
- **Data Volume** (medium): Database size is 500GB, increasing cutover and data migration effort.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | APPLICABLE | $1,200 | $500 | Operating system RHEL 7 is EOL and should be moved to a supported baseline. |
| Switch to standard Linux Operating System | NOT_APPLICABLE | - | - | RHEL 7 is already a Linux-based operating system. |
| Switch to ARM-based CPU | APPLICABLE | $6,000 | $1,000 | The application has cloud or container portability characteristics that make ARM migration feasible. |
| Applications Server replacement | NOT_APPLICABLE | - | - | Application server Payara 6.0 is current. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | APPLICABLE | $6,000 | $3,000 | The deployment model includes on-premise infrastructure, so additional cloud migration remains available. |
| Application Containerization | FULFILLED | - | - | The application is already containerized. |
| Application Refactoring and De-coupling | APPLICABLE | $300,000 | $150,000 | The recorded architecture (3-Tier) suggests a layered or monolithic design suitable for decoupling. |
| Upgrade Legacy Databases | APPLICABLE | $12,000 | $10,000 | Database engine PostgreSQL 14 is OUTDATED and should be upgraded. |
| Switch to Managed Database | APPLICABLE | $6,000 | $10,000 | PostgreSQL 14 is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $6,000 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | NOT_APPLICABLE | - | - | PostgreSQL 14 is already PostgreSQL-based. |

## Business Case
- Applicable scenarios: os_update_security_patch, switch_to_arm_cpu, app_deployment_to_cloud, app_refactor_decoupling, upgrade_legacy_databases, switch_to_managed_db, managed_arm_db
- Migration cost: $337,200
- Yearly savings: $179,500
- Three-year ROI: 59.7%
- Payback period: 1.88 years
