# ERPApp-001 (app001)

## Application Overview
- Status: Production
- Solution type: Custom made
- Criticality: High
- Deployment: On-Premise
- Users: 350
- Architecture: 1-Tier
- Containerized: No
- CI/CD: No

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | AIX 7.2 | CURRENT_VERSION | 2028-04-30 | AIX 7.2 remains under IBM support through approximately 2028. |
| programming_language | COBOL-2014 | OUTDATED | n/a | COBOL-2014 is an older standard with limited ecosystem modernization momentum. |
| application_server | None | NO_KNOWLEDGE | n/a | No application server is recorded for this application. |
| database | Oracle 19c | CURRENT_VERSION | 2027-04-30 | Oracle 19c remains a supported long-term release. |

## Complexity Assessment
- Complexity score: **6 / 10**
- Complexity label: **Medium**
- Cost multiplier: **1.2x**

- **Business Criticality** (high): Criticality is High and raises migration risk tolerance requirements.
- **Technology Debt** (medium): Technology debt includes 0 EOL and 1 outdated component(s).
- **Deployment Model** (high): Deployment includes on-premise infrastructure, increasing migration and network dependency complexity.
- **Data Volume** (high): Database size is 1000GB, increasing cutover and data migration effort.
- **Delivery Automation** (medium): CI/CD is not present, so deployment automation and regression confidence are weaker.
- **Runtime Portability** (medium): The workload is not containerized, reducing portability and slowing platform transitions.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | NOT_APPLICABLE | - | - | Operating system AIX 7.2 is already on a current supported release. |
| Switch to standard Linux Operating System | APPLICABLE | $360 | $400 | AIX 7.2 is not a standard Linux platform and can be standardized onto enterprise Linux. |
| Switch to ARM-based CPU | NOT_APPLICABLE | - | - | The application is on-premise only and not containerized, so ARM migration is not currently a fit. |
| Applications Server replacement | NOT_APPLICABLE | - | - | No standalone application server is recorded for this application. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | APPLICABLE | $6,000 | $3,000 | The deployment model includes on-premise infrastructure, so additional cloud migration remains available. |
| Application Containerization | APPLICABLE | $120,000 | $100,000 | The application is not containerized and could gain portability and operational consistency from container adoption. |
| Application Refactoring and De-coupling | APPLICABLE | $300,000 | $150,000 | The recorded architecture (1-Tier) suggests a layered or monolithic design suitable for decoupling. |
| Upgrade Legacy Databases | NOT_APPLICABLE | - | - | Database engine Oracle 19c is current. |
| Switch to Managed Database | APPLICABLE | $6,000 | $10,000 | Oracle 19c is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $6,000 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | APPLICABLE | $30,000 | $15,000 | Oracle 19c is a candidate for PostgreSQL standardization to reduce license and platform cost. |

## Business Case
- Applicable scenarios: switch_to_standard_linux_os, app_deployment_to_cloud, app_containerization, app_refactor_decoupling, switch_to_managed_db, managed_arm_db, switch_db_engine_postgresql
- Migration cost: $468,360
- Yearly savings: $283,400
- Three-year ROI: 81.5%
- Payback period: 1.65 years
