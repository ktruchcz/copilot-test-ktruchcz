# InventoryApp-008 (app008)

## Application Overview
- Status: Production
- Solution type: Custom made
- Criticality: High
- Deployment: On-Premise
- Users: 875
- Architecture: 1-Tier
- Containerized: No
- CI/CD: No

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | AIX 6 | EOL | 2017-04-30 | AIX 6 is end-of-life and no longer receives vendor support. |
| programming_language | COBOL-2014 | OUTDATED | n/a | COBOL-2014 is an older standard with limited ecosystem modernization momentum. |
| application_server | Oracle Weblogic 8.0 | EOL | n/a | Oracle Weblogic 8.0 is long out of support. |
| database | SQL Server 2019 | CURRENT_VERSION | 2030-01-08 | SQL Server 2019 remains within support. |

## Complexity Assessment
- Complexity score: **6 / 10**
- Complexity label: **Medium**
- Cost multiplier: **1.2x**

- **Business Criticality** (high): Criticality is High and raises migration risk tolerance requirements.
- **Technology Debt** (high): Technology debt includes 2 EOL and 1 outdated component(s).
- **Deployment Model** (high): Deployment includes on-premise infrastructure, increasing migration and network dependency complexity.
- **Delivery Automation** (medium): CI/CD is not present, so deployment automation and regression confidence are weaker.
- **Runtime Portability** (medium): The workload is not containerized, reducing portability and slowing platform transitions.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | APPLICABLE | $1,200 | $500 | Operating system AIX 6 is EOL and should be moved to a supported baseline. |
| Switch to standard Linux Operating System | APPLICABLE | $360 | $400 | AIX 6 is not a standard Linux platform and can be standardized onto enterprise Linux. |
| Switch to ARM-based CPU | NOT_APPLICABLE | - | - | The application is on-premise only and not containerized, so ARM migration is not currently a fit. |
| Applications Server replacement | APPLICABLE | $12,000 | $12,000 | Application server Oracle Weblogic 8.0 is EOL and should be replaced or upgraded. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | APPLICABLE | $6,000 | $3,000 | The deployment model includes on-premise infrastructure, so additional cloud migration remains available. |
| Application Containerization | APPLICABLE | $120,000 | $100,000 | The application is not containerized and could gain portability and operational consistency from container adoption. |
| Application Refactoring and De-coupling | APPLICABLE | $300,000 | $150,000 | The recorded architecture (1-Tier) suggests a layered or monolithic design suitable for decoupling. |
| Upgrade Legacy Databases | NOT_APPLICABLE | - | - | Database engine SQL Server 2019 is current. |
| Switch to Managed Database | APPLICABLE | $6,000 | $10,000 | SQL Server 2019 is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $6,000 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | APPLICABLE | $30,000 | $15,000 | SQL Server 2019 is a candidate for PostgreSQL standardization to reduce license and platform cost. |

## Business Case
- Applicable scenarios: os_update_security_patch, switch_to_standard_linux_os, application_server_replacement, app_deployment_to_cloud, app_containerization, app_refactor_decoupling, switch_to_managed_db, managed_arm_db, switch_db_engine_postgresql
- Migration cost: $481,560
- Yearly savings: $295,900
- Three-year ROI: 84.3%
- Payback period: 1.63 years
