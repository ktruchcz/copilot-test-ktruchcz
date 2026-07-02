# BackupApp-017 (app017)

## Application Overview
- Status: Production
- Solution type: 3rd party software
- Criticality: High
- Deployment: On-Premise
- Users: 45
- Architecture: unknown
- Containerized: No
- CI/CD: No

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | RHEL 7 | EOL | 2024-06-30 | RHEL 7 reached end of maintenance support in June 2024. |
| programming_language | PowerShell | CURRENT_VERSION | n/a | PowerShell 7.x remains current; the specific version was not provided. |
| application_server | Payara 5.0 | OUTDATED | n/a | Payara 5.0 is entering extended support and is no longer the strategic current line. |
| database | Oracle 12c | EOL | 2022-07-31 | Oracle 12c is out of support. |

## Complexity Assessment
- Complexity score: **8 / 10**
- Complexity label: **High**
- Cost multiplier: **1.5x**

- **Business Criticality** (high): Criticality is High and raises migration risk tolerance requirements.
- **Technology Debt** (high): Technology debt includes 2 EOL and 1 outdated component(s).
- **Integration Surface** (medium): The application exposes 2 API endpoints and 8 external interfaces.
- **Deployment Model** (high): Deployment includes on-premise infrastructure, increasing migration and network dependency complexity.
- **Delivery Automation** (medium): CI/CD is not present, so deployment automation and regression confidence are weaker.
- **Runtime Portability** (medium): The workload is not containerized, reducing portability and slowing platform transitions.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | APPLICABLE | $1,500 | $500 | Operating system RHEL 7 is EOL and should be moved to a supported baseline. |
| Switch to standard Linux Operating System | NOT_APPLICABLE | - | - | RHEL 7 is already a Linux-based operating system. |
| Switch to ARM-based CPU | NOT_APPLICABLE | - | - | The application is on-premise only and not containerized, so ARM migration is not currently a fit. |
| Applications Server replacement | APPLICABLE | $15,000 | $12,000 | Application server Payara 5.0 is OUTDATED and should be replaced or upgraded. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | APPLICABLE | $7,500 | $3,000 | The deployment model includes on-premise infrastructure, so additional cloud migration remains available. |
| Application Containerization | APPLICABLE | $150,000 | $100,000 | The application is not containerized and could gain portability and operational consistency from container adoption. |
| Application Refactoring and De-coupling | NOT_APPLICABLE | - | - | The recorded architecture (unknown) does not clearly indicate a monolithic pattern. |
| Upgrade Legacy Databases | APPLICABLE | $15,000 | $10,000 | Database engine Oracle 12c is EOL and should be upgraded. |
| Switch to Managed Database | APPLICABLE | $7,500 | $10,000 | Oracle 12c is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $7,500 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | APPLICABLE | $37,500 | $15,000 | Oracle 12c is a candidate for PostgreSQL standardization to reduce license and platform cost. |

## Business Case
- Applicable scenarios: os_update_security_patch, application_server_replacement, app_deployment_to_cloud, app_containerization, upgrade_legacy_databases, switch_to_managed_db, managed_arm_db, switch_db_engine_postgresql
- Migration cost: $241,500
- Yearly savings: $155,500
- Three-year ROI: 93.2%
- Payback period: 1.55 years
