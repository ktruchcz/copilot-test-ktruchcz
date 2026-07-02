# PortalApp-025 (app025)

## Application Overview
- Status: Production
- Solution type: Custom made
- Criticality: Medium
- Deployment: AWS
- Users: 2200
- Architecture: 2-Tier
- Containerized: Yes
- CI/CD: Yes

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | Windows Server 2019 | CURRENT_VERSION | 2029-01-09 | Windows Server 2019 remains a supported enterprise platform. |
| programming_language | ASP.NET Core | CURRENT_VERSION | n/a | ASP.NET Core is treated as current on the assumption the application is aligned to a modern supported .NET release. |
| application_server | Microsoft IIS 10.0 | CURRENT_VERSION | n/a | IIS 10.0 remains current when hosted on supported Windows Server releases. |
| database | PostgreSQL 15 | CURRENT_VERSION | 2027-11-11 | PostgreSQL 15 is a current supported major version. |

## Complexity Assessment
- Complexity score: **5 / 10**
- Complexity label: **Medium**
- Cost multiplier: **1.2x**

- **Business Criticality** (medium): Criticality is Medium and requires controlled cutover planning.
- **Integration Surface** (high): The application exposes 35 API endpoints and 15 external interfaces.
- **Data Volume** (medium): Database size is 800GB, increasing cutover and data migration effort.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | NOT_APPLICABLE | - | - | Operating system Windows Server 2019 is already on a current supported release. |
| Switch to standard Linux Operating System | APPLICABLE | $360 | $400 | Windows Server 2019 is not a standard Linux platform and can be standardized onto enterprise Linux. |
| Switch to ARM-based CPU | APPLICABLE | $6,000 | $1,000 | The application has cloud or container portability characteristics that make ARM migration feasible. |
| Applications Server replacement | NOT_APPLICABLE | - | - | Application server Microsoft IIS 10.0 is current. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | FULFILLED | - | - | The application is already fully deployed in AWS. |
| Application Containerization | FULFILLED | - | - | The application is already containerized. |
| Application Refactoring and De-coupling | APPLICABLE | $300,000 | $150,000 | The recorded architecture (2-Tier) suggests a layered or monolithic design suitable for decoupling. |
| Upgrade Legacy Databases | NOT_APPLICABLE | - | - | Database engine PostgreSQL 15 is current. |
| Switch to Managed Database | APPLICABLE | $6,000 | $10,000 | PostgreSQL 15 is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $6,000 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | NOT_APPLICABLE | - | - | PostgreSQL 15 is already PostgreSQL-based. |

## Business Case
- Applicable scenarios: switch_to_standard_linux_os, switch_to_arm_cpu, app_refactor_decoupling, switch_to_managed_db, managed_arm_db
- Migration cost: $318,360
- Yearly savings: $166,400
- Three-year ROI: 56.8%
- Payback period: 1.91 years
