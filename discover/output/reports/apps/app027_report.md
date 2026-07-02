# DataWarehouseApp-027 (app027)

## Application Overview
- Status: Production
- Solution type: Custom made
- Criticality: High
- Deployment: AWS, On-premise
- Users: 320
- Architecture: 3-Tier
- Containerized: No
- CI/CD: Yes

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | RHEL 7 | EOL | 2024-06-30 | RHEL 7 reached end of maintenance support in June 2024. |
| programming_language | Java 11 | OUTDATED | n/a | Java 11 is still used but has been superseded by newer LTS releases such as Java 17 and 21. |
| application_server | Websphere 8.5 | OUTDATED | n/a | Websphere 8.5 remains available only with extended support and is outdated. |
| database | SQL Server 2022 | CURRENT_VERSION | 2033-01-11 | SQL Server 2022 is current and fully supported. |

## Complexity Assessment
- Complexity score: **8 / 10**
- Complexity label: **High**
- Cost multiplier: **1.5x**

- **Business Criticality** (high): Criticality is High and raises migration risk tolerance requirements.
- **Technology Debt** (high): Technology debt includes 1 EOL and 2 outdated component(s).
- **Integration Surface** (high): The application exposes 5 API endpoints and 20 external interfaces.
- **Deployment Model** (medium): Deployment includes on-premise infrastructure, increasing migration and network dependency complexity.
- **Data Volume** (high): Database size is 5000GB, increasing cutover and data migration effort.
- **Runtime Portability** (medium): The workload is not containerized, reducing portability and slowing platform transitions.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | APPLICABLE | $1,500 | $500 | Operating system RHEL 7 is EOL and should be moved to a supported baseline. |
| Switch to standard Linux Operating System | NOT_APPLICABLE | - | - | RHEL 7 is already a Linux-based operating system. |
| Switch to ARM-based CPU | APPLICABLE | $7,500 | $1,000 | The application has cloud or container portability characteristics that make ARM migration feasible. |
| Applications Server replacement | APPLICABLE | $15,000 | $12,000 | Application server Websphere 8.5 is OUTDATED and should be replaced or upgraded. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | APPLICABLE | $7,500 | $3,000 | The deployment model includes on-premise infrastructure, so additional cloud migration remains available. |
| Application Containerization | APPLICABLE | $150,000 | $100,000 | The application is not containerized and could gain portability and operational consistency from container adoption. |
| Application Refactoring and De-coupling | APPLICABLE | $375,000 | $150,000 | The recorded architecture (3-Tier) suggests a layered or monolithic design suitable for decoupling. |
| Upgrade Legacy Databases | NOT_APPLICABLE | - | - | Database engine SQL Server 2022 is current. |
| Switch to Managed Database | APPLICABLE | $7,500 | $10,000 | SQL Server 2022 is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $7,500 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | APPLICABLE | $37,500 | $15,000 | SQL Server 2022 is a candidate for PostgreSQL standardization to reduce license and platform cost. |

## Business Case
- Applicable scenarios: os_update_security_patch, switch_to_arm_cpu, application_server_replacement, app_deployment_to_cloud, app_containerization, app_refactor_decoupling, switch_to_managed_db, managed_arm_db, switch_db_engine_postgresql
- Migration cost: $609,000
- Yearly savings: $296,500
- Three-year ROI: 46.1%
- Payback period: 2.05 years
