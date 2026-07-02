# MobileApp-016 (app016)

## Application Overview
- Status: Production
- Solution type: Custom made
- Criticality: Medium
- Deployment: AWS
- Users: 1580
- Architecture: 3-Tier
- Containerized: Yes
- CI/CD: Yes

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | RHEL 7 | EOL | 2024-06-30 | RHEL 7 reached end of maintenance support in June 2024. |
| programming_language | React Native | CURRENT_VERSION | n/a | React Native remains actively maintained; exact version was not provided but the platform is current. |
| application_server | Payara 4.0 | EOL | n/a | Payara 4.0 is end-of-life. |
| database | SQL Server 2019 | CURRENT_VERSION | 2030-01-08 | SQL Server 2019 remains within support. |

## Complexity Assessment
- Complexity score: **7 / 10**
- Complexity label: **High**
- Cost multiplier: **1.5x**

- **Business Criticality** (medium): Criticality is Medium and requires controlled cutover planning.
- **Technology Debt** (high): Technology debt includes 2 EOL and 0 outdated component(s).
- **Integration Surface** (high): The application exposes 30 API endpoints and 10 external interfaces.
- **Data Volume** (high): Database size is 2000GB, increasing cutover and data migration effort.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | APPLICABLE | $1,500 | $500 | Operating system RHEL 7 is EOL and should be moved to a supported baseline. |
| Switch to standard Linux Operating System | NOT_APPLICABLE | - | - | RHEL 7 is already a Linux-based operating system. |
| Switch to ARM-based CPU | APPLICABLE | $7,500 | $1,000 | The application has cloud or container portability characteristics that make ARM migration feasible. |
| Applications Server replacement | APPLICABLE | $15,000 | $12,000 | Application server Payara 4.0 is EOL and should be replaced or upgraded. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | FULFILLED | - | - | The application is already fully deployed in AWS. |
| Application Containerization | FULFILLED | - | - | The application is already containerized. |
| Application Refactoring and De-coupling | APPLICABLE | $375,000 | $150,000 | The recorded architecture (3-Tier) suggests a layered or monolithic design suitable for decoupling. |
| Upgrade Legacy Databases | NOT_APPLICABLE | - | - | Database engine SQL Server 2019 is current. |
| Switch to Managed Database | APPLICABLE | $7,500 | $10,000 | SQL Server 2019 is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $7,500 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | APPLICABLE | $37,500 | $15,000 | SQL Server 2019 is a candidate for PostgreSQL standardization to reduce license and platform cost. |

## Business Case
- Applicable scenarios: os_update_security_patch, switch_to_arm_cpu, application_server_replacement, app_refactor_decoupling, switch_to_managed_db, managed_arm_db, switch_db_engine_postgresql
- Migration cost: $451,500
- Yearly savings: $193,500
- Three-year ROI: 28.6%
- Payback period: 2.33 years
