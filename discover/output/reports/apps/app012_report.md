# IoTSensorApp-012 (app012)

## Application Overview
- Status: Production
- Solution type: Custom made
- Criticality: High
- Deployment: AWS
- Users: 85
- Architecture: 2-Tier
- Containerized: Yes
- CI/CD: Yes

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | Windows Server 2022 | CURRENT_VERSION | 2031-10-14 | Windows Server 2022 is within Microsoft's current support lifecycle. |
| programming_language | Rust 1.70 | OUTDATED | n/a | Rust 1.70 is behind current stable releases and should be refreshed. |
| application_server | Microsoft IIS 10.0 | CURRENT_VERSION | n/a | IIS 10.0 remains current when hosted on supported Windows Server releases. |
| database | PostgreSQL 14 | OUTDATED | 2026-11-12 | PostgreSQL 14 is still supported but not the preferred current version. |

## Complexity Assessment
- Complexity score: **6 / 10**
- Complexity label: **Medium**
- Cost multiplier: **1.2x**

- **Business Criticality** (high): Criticality is High and raises migration risk tolerance requirements.
- **Technology Debt** (medium): Technology debt includes 0 EOL and 2 outdated component(s).
- **Integration Surface** (high): The application exposes 20 API endpoints and 8 external interfaces.
- **Data Volume** (medium): Database size is 800GB, increasing cutover and data migration effort.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | NOT_APPLICABLE | - | - | Operating system Windows Server 2022 is already on a current supported release. |
| Switch to standard Linux Operating System | APPLICABLE | $360 | $400 | Windows Server 2022 is not a standard Linux platform and can be standardized onto enterprise Linux. |
| Switch to ARM-based CPU | APPLICABLE | $6,000 | $1,000 | The application has cloud or container portability characteristics that make ARM migration feasible. |
| Applications Server replacement | NOT_APPLICABLE | - | - | Application server Microsoft IIS 10.0 is current. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | FULFILLED | - | - | The application is already fully deployed in AWS. |
| Application Containerization | FULFILLED | - | - | The application is already containerized. |
| Application Refactoring and De-coupling | APPLICABLE | $300,000 | $150,000 | The recorded architecture (2-Tier) suggests a layered or monolithic design suitable for decoupling. |
| Upgrade Legacy Databases | APPLICABLE | $12,000 | $10,000 | Database engine PostgreSQL 14 is OUTDATED and should be upgraded. |
| Switch to Managed Database | APPLICABLE | $6,000 | $10,000 | PostgreSQL 14 is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $6,000 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | NOT_APPLICABLE | - | - | PostgreSQL 14 is already PostgreSQL-based. |

## Business Case
- Applicable scenarios: switch_to_standard_linux_os, switch_to_arm_cpu, app_refactor_decoupling, upgrade_legacy_databases, switch_to_managed_db, managed_arm_db
- Migration cost: $330,360
- Yearly savings: $176,400
- Three-year ROI: 60.2%
- Payback period: 1.87 years
