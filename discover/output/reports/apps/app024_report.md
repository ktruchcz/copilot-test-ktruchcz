# AuditApp-024 (app024)

## Application Overview
- Status: Production
- Solution type: Custom made
- Criticality: High
- Deployment: On-Premise
- Users: 95
- Architecture: 2-Tier
- Containerized: No
- CI/CD: No

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | Windows Server 2019 | CURRENT_VERSION | 2029-01-09 | Windows Server 2019 remains a supported enterprise platform. |
| programming_language | VB.NET | OUTDATED | n/a | VB.NET remains supported within .NET but is considered a legacy language for modernization planning. |
| application_server | Microsoft IIS 10.0 | CURRENT_VERSION | n/a | IIS 10.0 remains current when hosted on supported Windows Server releases. |
| database | SQL Server 2014 | EOL | 2024-07-09 | SQL Server 2014 reached end-of-life in July 2024. |

## Complexity Assessment
- Complexity score: **7 / 10**
- Complexity label: **High**
- Cost multiplier: **1.5x**

- **Business Criticality** (high): Criticality is High and raises migration risk tolerance requirements.
- **Technology Debt** (high): Technology debt includes 1 EOL and 1 outdated component(s).
- **Deployment Model** (high): Deployment includes on-premise infrastructure, increasing migration and network dependency complexity.
- **Delivery Automation** (medium): CI/CD is not present, so deployment automation and regression confidence are weaker.
- **Runtime Portability** (medium): The workload is not containerized, reducing portability and slowing platform transitions.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | NOT_APPLICABLE | - | - | Operating system Windows Server 2019 is already on a current supported release. |
| Switch to standard Linux Operating System | APPLICABLE | $450 | $400 | Windows Server 2019 is not a standard Linux platform and can be standardized onto enterprise Linux. |
| Switch to ARM-based CPU | NOT_APPLICABLE | - | - | The application is on-premise only and not containerized, so ARM migration is not currently a fit. |
| Applications Server replacement | NOT_APPLICABLE | - | - | Application server Microsoft IIS 10.0 is current. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | APPLICABLE | $7,500 | $3,000 | The deployment model includes on-premise infrastructure, so additional cloud migration remains available. |
| Application Containerization | APPLICABLE | $150,000 | $100,000 | The application is not containerized and could gain portability and operational consistency from container adoption. |
| Application Refactoring and De-coupling | APPLICABLE | $375,000 | $150,000 | The recorded architecture (2-Tier) suggests a layered or monolithic design suitable for decoupling. |
| Upgrade Legacy Databases | APPLICABLE | $15,000 | $10,000 | Database engine SQL Server 2014 is EOL and should be upgraded. |
| Switch to Managed Database | APPLICABLE | $7,500 | $10,000 | SQL Server 2014 is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $7,500 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | APPLICABLE | $37,500 | $15,000 | SQL Server 2014 is a candidate for PostgreSQL standardization to reduce license and platform cost. |

## Business Case
- Applicable scenarios: switch_to_standard_linux_os, app_deployment_to_cloud, app_containerization, app_refactor_decoupling, upgrade_legacy_databases, switch_to_managed_db, managed_arm_db, switch_db_engine_postgresql
- Migration cost: $600,450
- Yearly savings: $293,400
- Three-year ROI: 46.6%
- Payback period: 2.05 years
