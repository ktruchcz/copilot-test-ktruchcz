# SupportApp-006 (app006)

## Application Overview
- Status: Production
- Solution type: 3rd party software
- Criticality: Medium
- Deployment: AWS
- Users: 290
- Architecture: unknown
- Containerized: No
- CI/CD: Yes

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | Debian 6 | EOL | 2014-02-15 | Debian 6 is long past end-of-life. |
| programming_language | Java 11 | OUTDATED | n/a | Java 11 is still used but has been superseded by newer LTS releases such as Java 17 and 21. |
| application_server | Glassfish 5.0 | OUTDATED | n/a | Glassfish 5.0 is outdated and has limited community support. |
| database | PostgreSQL 13 | OUTDATED | 2025-11-13 | PostgreSQL 13 is nearing end-of-life and should be upgraded. |

## Complexity Assessment
- Complexity score: **5 / 10**
- Complexity label: **Medium**
- Cost multiplier: **1.2x**

- **Business Criticality** (medium): Criticality is Medium and requires controlled cutover planning.
- **Technology Debt** (high): Technology debt includes 1 EOL and 3 outdated component(s).
- **Runtime Portability** (medium): The workload is not containerized, reducing portability and slowing platform transitions.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | APPLICABLE | $1,200 | $500 | Operating system Debian 6 is EOL and should be moved to a supported baseline. |
| Switch to standard Linux Operating System | NOT_APPLICABLE | - | - | Debian 6 is already a Linux-based operating system. |
| Switch to ARM-based CPU | APPLICABLE | $6,000 | $1,000 | The application has cloud or container portability characteristics that make ARM migration feasible. |
| Applications Server replacement | APPLICABLE | $12,000 | $12,000 | Application server Glassfish 5.0 is OUTDATED and should be replaced or upgraded. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | FULFILLED | - | - | The application is already fully deployed in AWS. |
| Application Containerization | APPLICABLE | $120,000 | $100,000 | The application is not containerized and could gain portability and operational consistency from container adoption. |
| Application Refactoring and De-coupling | NOT_APPLICABLE | - | - | The recorded architecture (unknown) does not clearly indicate a monolithic pattern. |
| Upgrade Legacy Databases | APPLICABLE | $12,000 | $10,000 | Database engine PostgreSQL 13 is OUTDATED and should be upgraded. |
| Switch to Managed Database | APPLICABLE | $6,000 | $10,000 | PostgreSQL 13 is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $6,000 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | NOT_APPLICABLE | - | - | PostgreSQL 13 is already PostgreSQL-based. |

## Business Case
- Applicable scenarios: os_update_security_patch, switch_to_arm_cpu, application_server_replacement, app_containerization, upgrade_legacy_databases, switch_to_managed_db, managed_arm_db
- Migration cost: $163,200
- Yearly savings: $138,500
- Three-year ROI: 154.6%
- Payback period: 1.18 years
