# CRMApp-002 (app002)

## Application Overview
- Status: Production
- Solution type: 3rd party software
- Criticality: Medium
- Deployment: AWS
- Users: 1200
- Architecture: unknown
- Containerized: No
- CI/CD: Yes

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | RHEL 7 | EOL | 2024-06-30 | RHEL 7 reached end of maintenance support in June 2024. |
| programming_language | Java 11 | OUTDATED | n/a | Java 11 is still used but has been superseded by newer LTS releases such as Java 17 and 21. |
| application_server | Websphere 7.0 | EOL | n/a | Websphere 7.0 is end-of-life. |
| database | Amazon RDS MySQL | CURRENT_VERSION | n/a | Amazon RDS MySQL is treated as current because the managed service keeps platform support aligned by the provider. |

## Complexity Assessment
- Complexity score: **6 / 10**
- Complexity label: **Medium**
- Cost multiplier: **1.2x**

- **Business Criticality** (medium): Criticality is Medium and requires controlled cutover planning.
- **Technology Debt** (high): Technology debt includes 2 EOL and 1 outdated component(s).
- **Integration Surface** (high): The application exposes 15 API endpoints and 8 external interfaces.
- **Data Volume** (medium): Database size is 500GB, increasing cutover and data migration effort.
- **Runtime Portability** (medium): The workload is not containerized, reducing portability and slowing platform transitions.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | APPLICABLE | $1,200 | $500 | Operating system RHEL 7 is EOL and should be moved to a supported baseline. |
| Switch to standard Linux Operating System | NOT_APPLICABLE | - | - | RHEL 7 is already a Linux-based operating system. |
| Switch to ARM-based CPU | APPLICABLE | $6,000 | $1,000 | The application has cloud or container portability characteristics that make ARM migration feasible. |
| Applications Server replacement | APPLICABLE | $12,000 | $12,000 | Application server Websphere 7.0 is EOL and should be replaced or upgraded. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | FULFILLED | - | - | The application is already fully deployed in AWS. |
| Application Containerization | APPLICABLE | $120,000 | $100,000 | The application is not containerized and could gain portability and operational consistency from container adoption. |
| Application Refactoring and De-coupling | NOT_APPLICABLE | - | - | The recorded architecture (unknown) does not clearly indicate a monolithic pattern. |
| Upgrade Legacy Databases | NOT_APPLICABLE | - | - | Database engine Amazon RDS MySQL is current. |
| Switch to Managed Database | NOT_APPLICABLE | - | - | Amazon RDS MySQL is already treated as a managed database service. |
| Managed ARM Database | NOT_APPLICABLE | - | - | Managed ARM database migration depends on first moving to a managed database platform, which is already satisfied or not needed. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | APPLICABLE | $30,000 | $15,000 | Amazon RDS MySQL is a candidate for PostgreSQL standardization to reduce license and platform cost. |

## Business Case
- Applicable scenarios: os_update_security_patch, switch_to_arm_cpu, application_server_replacement, app_containerization, switch_db_engine_postgresql
- Migration cost: $169,200
- Yearly savings: $128,500
- Three-year ROI: 127.8%
- Payback period: 1.32 years
