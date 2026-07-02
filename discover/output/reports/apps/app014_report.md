# DocumentApp-014 (app014)

## Application Overview
- Status: Production
- Solution type: Open Source
- Criticality: Medium
- Deployment: AWS
- Users: 890
- Architecture: 2-Tier
- Containerized: No
- CI/CD: Yes

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | Windows Server 2019 | CURRENT_VERSION | 2029-01-09 | Windows Server 2019 remains a supported enterprise platform. |
| programming_language | C# .NET 6 | OUTDATED | 2024-05-14 | .NET 6 reached end-of-support in May 2024. |
| application_server | Microsoft IIS 10.0 | CURRENT_VERSION | n/a | IIS 10.0 remains current when hosted on supported Windows Server releases. |
| database | MySQL 8.0 | CURRENT_VERSION | n/a | MySQL 8.0 remains a current supported release line. |

## Complexity Assessment
- Complexity score: **5 / 10**
- Complexity label: **Medium**
- Cost multiplier: **1.2x**

- **Business Criticality** (medium): Criticality is Medium and requires controlled cutover planning.
- **Technology Debt** (medium): Technology debt includes 0 EOL and 1 outdated component(s).
- **Integration Surface** (high): The application exposes 18 API endpoints and 9 external interfaces.
- **Runtime Portability** (medium): The workload is not containerized, reducing portability and slowing platform transitions.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | NOT_APPLICABLE | - | - | Operating system Windows Server 2019 is already on a current supported release. |
| Switch to standard Linux Operating System | APPLICABLE | $360 | $400 | Windows Server 2019 is not a standard Linux platform and can be standardized onto enterprise Linux. |
| Switch to ARM-based CPU | APPLICABLE | $6,000 | $1,000 | The application has cloud or container portability characteristics that make ARM migration feasible. |
| Applications Server replacement | NOT_APPLICABLE | - | - | Application server Microsoft IIS 10.0 is current. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | FULFILLED | - | - | The application is already fully deployed in AWS. |
| Application Containerization | APPLICABLE | $120,000 | $100,000 | The application is not containerized and could gain portability and operational consistency from container adoption. |
| Application Refactoring and De-coupling | APPLICABLE | $300,000 | $150,000 | The recorded architecture (2-Tier) suggests a layered or monolithic design suitable for decoupling. |
| Upgrade Legacy Databases | NOT_APPLICABLE | - | - | Database engine MySQL 8.0 is current. |
| Switch to Managed Database | APPLICABLE | $6,000 | $10,000 | MySQL 8.0 is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $6,000 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | APPLICABLE | $30,000 | $15,000 | MySQL 8.0 is a candidate for PostgreSQL standardization to reduce license and platform cost. |

## Business Case
- Applicable scenarios: switch_to_standard_linux_os, switch_to_arm_cpu, app_containerization, app_refactor_decoupling, switch_to_managed_db, managed_arm_db, switch_db_engine_postgresql
- Migration cost: $468,360
- Yearly savings: $281,400
- Three-year ROI: 80.2%
- Payback period: 1.66 years
