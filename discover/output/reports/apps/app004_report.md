# HRApp-004 (app004)

## Application Overview
- Status: Production
- Solution type: Custom made
- Criticality: High
- Deployment: AWS, On-premise
- Users: 670
- Architecture: 2-Tier
- Containerized: Yes
- CI/CD: Yes

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | Windows Server 2012 | EOL | 2023-10-10 | Windows Server 2012 reached end of support in October 2023. |
| programming_language | .NET Core | OUTDATED | n/a | The generic '.NET Core' label lacks a specific version; older .NET Core trains are out of support and modernization to a current .NET LTS is recommended. |
| application_server | Microsoft IIS 8.0 | EOL | 2023-10-10 | IIS 8.0 inherits Windows Server 2012 end-of-support constraints. |
| database | SQL Server 2019 | CURRENT_VERSION | 2030-01-08 | SQL Server 2019 remains within support. |

## Complexity Assessment
- Complexity score: **6 / 10**
- Complexity label: **Medium**
- Cost multiplier: **1.2x**

- **Business Criticality** (high): Criticality is High and raises migration risk tolerance requirements.
- **Technology Debt** (high): Technology debt includes 2 EOL and 1 outdated component(s).
- **Integration Surface** (medium): The application exposes 12 API endpoints and 6 external interfaces.
- **Deployment Model** (medium): Deployment includes on-premise infrastructure, increasing migration and network dependency complexity.
- **Data Volume** (medium): Database size is 750GB, increasing cutover and data migration effort.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | APPLICABLE | $1,200 | $500 | Operating system Windows Server 2012 is EOL and should be moved to a supported baseline. |
| Switch to standard Linux Operating System | APPLICABLE | $360 | $400 | Windows Server 2012 is not a standard Linux platform and can be standardized onto enterprise Linux. |
| Switch to ARM-based CPU | APPLICABLE | $6,000 | $1,000 | The application has cloud or container portability characteristics that make ARM migration feasible. |
| Applications Server replacement | APPLICABLE | $12,000 | $12,000 | Application server Microsoft IIS 8.0 is EOL and should be replaced or upgraded. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | APPLICABLE | $6,000 | $3,000 | The deployment model includes on-premise infrastructure, so additional cloud migration remains available. |
| Application Containerization | FULFILLED | - | - | The application is already containerized. |
| Application Refactoring and De-coupling | APPLICABLE | $300,000 | $150,000 | The recorded architecture (2-Tier) suggests a layered or monolithic design suitable for decoupling. |
| Upgrade Legacy Databases | NOT_APPLICABLE | - | - | Database engine SQL Server 2019 is current. |
| Switch to Managed Database | APPLICABLE | $6,000 | $10,000 | SQL Server 2019 is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $6,000 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | APPLICABLE | $30,000 | $15,000 | SQL Server 2019 is a candidate for PostgreSQL standardization to reduce license and platform cost. |

## Business Case
- Applicable scenarios: os_update_security_patch, switch_to_standard_linux_os, switch_to_arm_cpu, application_server_replacement, app_deployment_to_cloud, app_refactor_decoupling, switch_to_managed_db, managed_arm_db, switch_db_engine_postgresql
- Migration cost: $367,560
- Yearly savings: $196,900
- Three-year ROI: 60.7%
- Payback period: 1.87 years
