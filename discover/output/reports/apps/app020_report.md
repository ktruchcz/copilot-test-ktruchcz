# TrainingApp-020 (app020)

## Application Overview
- Status: Production
- Solution type: 3rd party software
- Criticality: Low
- Deployment: AWS
- Users: 750
- Architecture: 2-Tier
- Containerized: No
- CI/CD: Yes

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | Windows Server 2012 | EOL | 2023-10-10 | Windows Server 2012 reached end of support in October 2023. |
| programming_language | Angular 15 | OUTDATED | 2024-05-31 | Angular 15 is no longer a current supported major version. |
| application_server | Microsoft IIS 8.5 | EOL | 2023-10-10 | IIS 8.5 inherits Windows Server 2012 end-of-support constraints. |
| database | SQL Server 2016 | OUTDATED | 2026-07-14 | SQL Server 2016 is only in extended support and is outdated. |

## Complexity Assessment
- Complexity score: **6 / 10**
- Complexity label: **Medium**
- Cost multiplier: **1.2x**

- **Technology Debt** (high): Technology debt includes 2 EOL and 2 outdated component(s).
- **Integration Surface** (high): The application exposes 14 API endpoints and 7 external interfaces.
- **Data Volume** (medium): Database size is 600GB, increasing cutover and data migration effort.
- **Runtime Portability** (medium): The workload is not containerized, reducing portability and slowing platform transitions.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | APPLICABLE | $1,200 | $500 | Operating system Windows Server 2012 is EOL and should be moved to a supported baseline. |
| Switch to standard Linux Operating System | APPLICABLE | $360 | $400 | Windows Server 2012 is not a standard Linux platform and can be standardized onto enterprise Linux. |
| Switch to ARM-based CPU | APPLICABLE | $6,000 | $1,000 | The application has cloud or container portability characteristics that make ARM migration feasible. |
| Applications Server replacement | APPLICABLE | $12,000 | $12,000 | Application server Microsoft IIS 8.5 is EOL and should be replaced or upgraded. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | FULFILLED | - | - | The application is already fully deployed in AWS. |
| Application Containerization | APPLICABLE | $120,000 | $100,000 | The application is not containerized and could gain portability and operational consistency from container adoption. |
| Application Refactoring and De-coupling | APPLICABLE | $300,000 | $150,000 | The recorded architecture (2-Tier) suggests a layered or monolithic design suitable for decoupling. |
| Upgrade Legacy Databases | APPLICABLE | $12,000 | $10,000 | Database engine SQL Server 2016 is OUTDATED and should be upgraded. |
| Switch to Managed Database | APPLICABLE | $6,000 | $10,000 | SQL Server 2016 is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $6,000 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | APPLICABLE | $30,000 | $15,000 | SQL Server 2016 is a candidate for PostgreSQL standardization to reduce license and platform cost. |

## Business Case
- Applicable scenarios: os_update_security_patch, switch_to_standard_linux_os, switch_to_arm_cpu, application_server_replacement, app_containerization, app_refactor_decoupling, upgrade_legacy_databases, switch_to_managed_db, managed_arm_db, switch_db_engine_postgresql
- Migration cost: $493,560
- Yearly savings: $303,900
- Three-year ROI: 84.7%
- Payback period: 1.62 years
