# SecurityApp-013 (app013)

## Application Overview
- Status: Production
- Solution type: Custom made
- Criticality: Critical
- Deployment: On-Premise
- Users: 520
- Architecture: 3-Tier
- Containerized: No
- CI/CD: Yes

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | Debian 7 | EOL | 2016-04-26 | Debian 7 is long past end-of-life. |
| programming_language | Java 17 | CURRENT_VERSION | 2029-09-30 | Java 17 is a current LTS release with active support. |
| application_server | Websphere 8.0 | EOL | n/a | Websphere 8.0 is end-of-life. |
| database | SQL Server 2022 | CURRENT_VERSION | 2033-01-11 | SQL Server 2022 is current and fully supported. |

## Complexity Assessment
- Complexity score: **7 / 10**
- Complexity label: **High**
- Cost multiplier: **1.5x**

- **Technology Debt** (high): Technology debt includes 2 EOL and 0 outdated component(s).
- **Integration Surface** (high): The application exposes 8 API endpoints and 15 external interfaces.
- **Deployment Model** (high): Deployment includes on-premise infrastructure, increasing migration and network dependency complexity.
- **Data Volume** (medium): Database size is 600GB, increasing cutover and data migration effort.
- **Runtime Portability** (medium): The workload is not containerized, reducing portability and slowing platform transitions.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | APPLICABLE | $1,500 | $500 | Operating system Debian 7 is EOL and should be moved to a supported baseline. |
| Switch to standard Linux Operating System | NOT_APPLICABLE | - | - | Debian 7 is already a Linux-based operating system. |
| Switch to ARM-based CPU | NOT_APPLICABLE | - | - | The application is on-premise only and not containerized, so ARM migration is not currently a fit. |
| Applications Server replacement | APPLICABLE | $15,000 | $12,000 | Application server Websphere 8.0 is EOL and should be replaced or upgraded. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | APPLICABLE | $7,500 | $3,000 | The deployment model includes on-premise infrastructure, so additional cloud migration remains available. |
| Application Containerization | APPLICABLE | $150,000 | $100,000 | The application is not containerized and could gain portability and operational consistency from container adoption. |
| Application Refactoring and De-coupling | APPLICABLE | $375,000 | $150,000 | The recorded architecture (3-Tier) suggests a layered or monolithic design suitable for decoupling. |
| Upgrade Legacy Databases | NOT_APPLICABLE | - | - | Database engine SQL Server 2022 is current. |
| Switch to Managed Database | APPLICABLE | $7,500 | $10,000 | SQL Server 2022 is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $7,500 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | APPLICABLE | $37,500 | $15,000 | SQL Server 2022 is a candidate for PostgreSQL standardization to reduce license and platform cost. |

## Business Case
- Applicable scenarios: os_update_security_patch, application_server_replacement, app_deployment_to_cloud, app_containerization, app_refactor_decoupling, switch_to_managed_db, managed_arm_db, switch_db_engine_postgresql
- Migration cost: $601,500
- Yearly savings: $295,500
- Three-year ROI: 47.4%
- Payback period: 2.04 years
