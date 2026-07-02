# QualityApp-019 (app019)

## Application Overview
- Status: Production
- Solution type: Custom made
- Criticality: High
- Deployment: AWS, On-premise
- Users: 180
- Architecture: 3-Tier
- Containerized: No
- CI/CD: Yes

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | RHEL 8 | CURRENT_VERSION | 2029-05-31 | RHEL 8 is still within its active support window. |
| programming_language | Python 3.8 | OUTDATED | 2024-10-07 | Python 3.8 is at or beyond the end of its support window and should be upgraded. |
| application_server | Apache Tomcat 8.0 | EOL | 2018-06-30 | Apache Tomcat 8.0 is end-of-life. |
| database | MySQL 8.0 | CURRENT_VERSION | n/a | MySQL 8.0 remains a current supported release line. |

## Complexity Assessment
- Complexity score: **6 / 10**
- Complexity label: **Medium**
- Cost multiplier: **1.2x**

- **Business Criticality** (high): Criticality is High and raises migration risk tolerance requirements.
- **Technology Debt** (high): Technology debt includes 1 EOL and 1 outdated component(s).
- **Deployment Model** (medium): Deployment includes on-premise infrastructure, increasing migration and network dependency complexity.
- **Runtime Portability** (medium): The workload is not containerized, reducing portability and slowing platform transitions.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | NOT_APPLICABLE | - | - | Operating system RHEL 8 is already on a current supported release. |
| Switch to standard Linux Operating System | NOT_APPLICABLE | - | - | RHEL 8 is already a Linux-based operating system. |
| Switch to ARM-based CPU | APPLICABLE | $6,000 | $1,000 | The application has cloud or container portability characteristics that make ARM migration feasible. |
| Applications Server replacement | APPLICABLE | $12,000 | $12,000 | Application server Apache Tomcat 8.0 is EOL and should be replaced or upgraded. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | APPLICABLE | $6,000 | $3,000 | The deployment model includes on-premise infrastructure, so additional cloud migration remains available. |
| Application Containerization | APPLICABLE | $120,000 | $100,000 | The application is not containerized and could gain portability and operational consistency from container adoption. |
| Application Refactoring and De-coupling | APPLICABLE | $300,000 | $150,000 | The recorded architecture (3-Tier) suggests a layered or monolithic design suitable for decoupling. |
| Upgrade Legacy Databases | NOT_APPLICABLE | - | - | Database engine MySQL 8.0 is current. |
| Switch to Managed Database | APPLICABLE | $6,000 | $10,000 | MySQL 8.0 is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $6,000 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | APPLICABLE | $30,000 | $15,000 | MySQL 8.0 is a candidate for PostgreSQL standardization to reduce license and platform cost. |

## Business Case
- Applicable scenarios: switch_to_arm_cpu, application_server_replacement, app_deployment_to_cloud, app_containerization, app_refactor_decoupling, switch_to_managed_db, managed_arm_db, switch_db_engine_postgresql
- Migration cost: $486,000
- Yearly savings: $296,000
- Three-year ROI: 82.7%
- Payback period: 1.64 years
