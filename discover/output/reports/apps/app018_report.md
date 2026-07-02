# VendorApp-018 (app018)

## Application Overview
- Status: Production
- Solution type: Custom made
- Criticality: Medium
- Deployment: On-Premise
- Users: 260
- Architecture: 3-Tier
- Containerized: No
- CI/CD: No

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | RHEL 7 | EOL | 2024-06-30 | RHEL 7 reached end of maintenance support in June 2024. |
| programming_language | Java 8 | EOL | 2022-03-31 | Java 8 is considered end-of-life for most enterprise modernization programs. |
| application_server | Glassfish 4.5 | EOL | n/a | Glassfish 4.5 is end-of-life. |
| database | PostgreSQL 13 | OUTDATED | 2025-11-13 | PostgreSQL 13 is nearing end-of-life and should be upgraded. |

## Complexity Assessment
- Complexity score: **7 / 10**
- Complexity label: **High**
- Cost multiplier: **1.5x**

- **Business Criticality** (medium): Criticality is Medium and requires controlled cutover planning.
- **Technology Debt** (high): Technology debt includes 3 EOL and 1 outdated component(s).
- **Integration Surface** (medium): The application exposes 5 API endpoints and 6 external interfaces.
- **Deployment Model** (high): Deployment includes on-premise infrastructure, increasing migration and network dependency complexity.
- **Delivery Automation** (medium): CI/CD is not present, so deployment automation and regression confidence are weaker.
- **Runtime Portability** (medium): The workload is not containerized, reducing portability and slowing platform transitions.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | APPLICABLE | $1,500 | $500 | Operating system RHEL 7 is EOL and should be moved to a supported baseline. |
| Switch to standard Linux Operating System | NOT_APPLICABLE | - | - | RHEL 7 is already a Linux-based operating system. |
| Switch to ARM-based CPU | NOT_APPLICABLE | - | - | The application is on-premise only and not containerized, so ARM migration is not currently a fit. |
| Applications Server replacement | APPLICABLE | $15,000 | $12,000 | Application server Glassfish 4.5 is EOL and should be replaced or upgraded. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | APPLICABLE | $7,500 | $3,000 | The deployment model includes on-premise infrastructure, so additional cloud migration remains available. |
| Application Containerization | APPLICABLE | $150,000 | $100,000 | The application is not containerized and could gain portability and operational consistency from container adoption. |
| Application Refactoring and De-coupling | APPLICABLE | $375,000 | $150,000 | The recorded architecture (3-Tier) suggests a layered or monolithic design suitable for decoupling. |
| Upgrade Legacy Databases | APPLICABLE | $15,000 | $10,000 | Database engine PostgreSQL 13 is OUTDATED and should be upgraded. |
| Switch to Managed Database | APPLICABLE | $7,500 | $10,000 | PostgreSQL 13 is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $7,500 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | NOT_APPLICABLE | - | - | PostgreSQL 13 is already PostgreSQL-based. |

## Business Case
- Applicable scenarios: os_update_security_patch, application_server_replacement, app_deployment_to_cloud, app_containerization, app_refactor_decoupling, upgrade_legacy_databases, switch_to_managed_db, managed_arm_db
- Migration cost: $579,000
- Yearly savings: $290,500
- Three-year ROI: 50.5%
- Payback period: 1.99 years
