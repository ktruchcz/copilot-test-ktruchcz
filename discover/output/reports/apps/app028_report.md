# NotificationApp-028 (app028)

## Application Overview
- Status: Production
- Solution type: 3rd party software
- Criticality: Medium
- Deployment: AWS
- Users: 850
- Architecture: unknown
- Containerized: Yes
- CI/CD: Yes

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | Windows Server 2019 | CURRENT_VERSION | 2029-01-09 | Windows Server 2019 remains a supported enterprise platform. |
| programming_language | Java 17 | CURRENT_VERSION | 2029-09-30 | Java 17 is a current LTS release with active support. |
| application_server | Microsoft IIS 10.0 | CURRENT_VERSION | n/a | IIS 10.0 remains current when hosted on supported Windows Server releases. |
| database | Oracle 19c | CURRENT_VERSION | 2027-04-30 | Oracle 19c remains a supported long-term release. |

## Complexity Assessment
- Complexity score: **5 / 10**
- Complexity label: **Medium**
- Cost multiplier: **1.2x**

- **Business Criticality** (medium): Criticality is Medium and requires controlled cutover planning.
- **Integration Surface** (high): The application exposes 18 API endpoints and 25 external interfaces.
- **Data Volume** (high): Database size is 3000GB, increasing cutover and data migration effort.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | NOT_APPLICABLE | - | - | Operating system Windows Server 2019 is already on a current supported release. |
| Switch to standard Linux Operating System | APPLICABLE | $360 | $400 | Windows Server 2019 is not a standard Linux platform and can be standardized onto enterprise Linux. |
| Switch to ARM-based CPU | APPLICABLE | $6,000 | $1,000 | The application has cloud or container portability characteristics that make ARM migration feasible. |
| Applications Server replacement | NOT_APPLICABLE | - | - | Application server Microsoft IIS 10.0 is current. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | FULFILLED | - | - | The application is already fully deployed in AWS. |
| Application Containerization | FULFILLED | - | - | The application is already containerized. |
| Application Refactoring and De-coupling | NOT_APPLICABLE | - | - | The recorded architecture (unknown) does not clearly indicate a monolithic pattern. |
| Upgrade Legacy Databases | NOT_APPLICABLE | - | - | Database engine Oracle 19c is current. |
| Switch to Managed Database | APPLICABLE | $6,000 | $10,000 | Oracle 19c is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $6,000 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | APPLICABLE | $30,000 | $15,000 | Oracle 19c is a candidate for PostgreSQL standardization to reduce license and platform cost. |

## Business Case
- Applicable scenarios: switch_to_standard_linux_os, switch_to_arm_cpu, switch_to_managed_db, managed_arm_db, switch_db_engine_postgresql
- Migration cost: $48,360
- Yearly savings: $31,400
- Three-year ROI: 94.8%
- Payback period: 1.54 years
