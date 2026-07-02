# ReportingApp-015 (app015)

## Application Overview
- Status: Production
- Solution type: Custom made
- Criticality: Low
- Deployment: AWS
- Users: 340
- Architecture: 2-Tier
- Containerized: No
- CI/CD: Yes

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | Windows Server 2019 | CURRENT_VERSION | 2029-01-09 | Windows Server 2019 remains a supported enterprise platform. |
| programming_language | PHP 8.1 | OUTDATED | 2025-12-31 | PHP 8.1 has moved out of mainstream support and should be upgraded. |
| application_server | Microsoft IIS 10.0 | CURRENT_VERSION | n/a | IIS 10.0 remains current when hosted on supported Windows Server releases. |
| database | MongoDB | CURRENT_VERSION | n/a | MongoDB is treated as current; no version was provided, but the service is assumed to be on a supported release. |

## Complexity Assessment
- Complexity score: **4 / 10**
- Complexity label: **Medium**
- Cost multiplier: **1.2x**

- **Technology Debt** (medium): Technology debt includes 0 EOL and 1 outdated component(s).
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
| Upgrade Legacy Databases | NOT_APPLICABLE | - | - | Database engine MongoDB is current. |
| Switch to Managed Database | NOT_APPLICABLE | - | - | MongoDB is already treated as a managed database service. |
| Managed ARM Database | NOT_APPLICABLE | - | - | Managed ARM database migration depends on first moving to a managed database platform, which is already satisfied or not needed. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | NOT_APPLICABLE | - | - | MongoDB is not in the relational database set targeted by this scenario. |

## Business Case
- Applicable scenarios: switch_to_standard_linux_os, switch_to_arm_cpu, app_containerization, app_refactor_decoupling
- Migration cost: $426,360
- Yearly savings: $251,400
- Three-year ROI: 76.9%
- Payback period: 1.70 years
