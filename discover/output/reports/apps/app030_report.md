# APIGatewayApp-030 (app030)

## Application Overview
- Status: Production
- Solution type: Open Source
- Criticality: High
- Deployment: AWS
- Users: 1800
- Architecture: 3-Tier
- Containerized: Yes
- CI/CD: Yes

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | RHEL 8 | CURRENT_VERSION | 2029-05-31 | RHEL 8 is still within its active support window. |
| programming_language | Go 1.19 | OUTDATED | n/a | Go 1.19 is behind the actively supported Go release train. |
| application_server | Glassfish 3.0 | EOL | n/a | Glassfish 3.0 is end-of-life. |
| database | MySQL 5.7 | EOL | 2023-10-31 | MySQL 5.7 is end-of-life. |

## Complexity Assessment
- Complexity score: **6 / 10**
- Complexity label: **Medium**
- Cost multiplier: **1.2x**

- **Business Criticality** (high): Criticality is High and raises migration risk tolerance requirements.
- **Technology Debt** (high): Technology debt includes 2 EOL and 1 outdated component(s).
- **Integration Surface** (high): The application exposes 50 API endpoints and 30 external interfaces.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | NOT_APPLICABLE | - | - | Operating system RHEL 8 is already on a current supported release. |
| Switch to standard Linux Operating System | NOT_APPLICABLE | - | - | RHEL 8 is already a Linux-based operating system. |
| Switch to ARM-based CPU | APPLICABLE | $6,000 | $1,000 | The application has cloud or container portability characteristics that make ARM migration feasible. |
| Applications Server replacement | APPLICABLE | $12,000 | $12,000 | Application server Glassfish 3.0 is EOL and should be replaced or upgraded. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | FULFILLED | - | - | The application is already fully deployed in AWS. |
| Application Containerization | FULFILLED | - | - | The application is already containerized. |
| Application Refactoring and De-coupling | APPLICABLE | $300,000 | $150,000 | The recorded architecture (3-Tier) suggests a layered or monolithic design suitable for decoupling. |
| Upgrade Legacy Databases | APPLICABLE | $12,000 | $10,000 | Database engine MySQL 5.7 is EOL and should be upgraded. |
| Switch to Managed Database | APPLICABLE | $6,000 | $10,000 | MySQL 5.7 is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $6,000 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | APPLICABLE | $6,000 | $15,000 | Database size is 80GB and the application has cloud deployment characteristics suitable for serverless database options. |
| Switch Database Engine to PostgreSQL | APPLICABLE | $30,000 | $15,000 | MySQL 5.7 is a candidate for PostgreSQL standardization to reduce license and platform cost. |

## Business Case
- Applicable scenarios: switch_to_arm_cpu, application_server_replacement, app_refactor_decoupling, upgrade_legacy_databases, switch_to_managed_db, managed_arm_db, serverless_db_migration, switch_db_engine_postgresql
- Migration cost: $378,000
- Yearly savings: $218,000
- Three-year ROI: 73.0%
- Payback period: 1.73 years
