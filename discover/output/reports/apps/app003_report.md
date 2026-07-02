# AnalyticsApp-003 (app003)

## Application Overview
- Status: Production
- Solution type: Open Source
- Criticality: Low
- Deployment: AWS
- Users: 480
- Architecture: 3-Tier
- Containerized: Yes
- CI/CD: Yes

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | RHEL 7 | EOL | 2024-06-30 | RHEL 7 reached end of maintenance support in June 2024. |
| programming_language | Python 3.9 | OUTDATED | 2025-10-31 | Python 3.9 is approaching end-of-life and is no longer a preferred current runtime. |
| application_server | Apache Tomcat 6.1 | EOL | 2016-12-31 | Apache Tomcat 6.x is end-of-life. |
| database | PostgreSQL 13 | OUTDATED | 2025-11-13 | PostgreSQL 13 is nearing end-of-life and should be upgraded. |

## Complexity Assessment
- Complexity score: **4 / 10**
- Complexity label: **Medium**
- Cost multiplier: **1.2x**

- **Technology Debt** (high): Technology debt includes 2 EOL and 2 outdated component(s).

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | APPLICABLE | $1,200 | $500 | Operating system RHEL 7 is EOL and should be moved to a supported baseline. |
| Switch to standard Linux Operating System | NOT_APPLICABLE | - | - | RHEL 7 is already a Linux-based operating system. |
| Switch to ARM-based CPU | APPLICABLE | $6,000 | $1,000 | The application has cloud or container portability characteristics that make ARM migration feasible. |
| Applications Server replacement | APPLICABLE | $12,000 | $12,000 | Application server Apache Tomcat 6.1 is EOL and should be replaced or upgraded. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | FULFILLED | - | - | The application is already fully deployed in AWS. |
| Application Containerization | FULFILLED | - | - | The application is already containerized. |
| Application Refactoring and De-coupling | APPLICABLE | $300,000 | $150,000 | The recorded architecture (3-Tier) suggests a layered or monolithic design suitable for decoupling. |
| Upgrade Legacy Databases | APPLICABLE | $12,000 | $10,000 | Database engine PostgreSQL 13 is OUTDATED and should be upgraded. |
| Switch to Managed Database | APPLICABLE | $6,000 | $10,000 | PostgreSQL 13 is not a managed database service and could be moved to a managed offering. |
| Managed ARM Database | APPLICABLE | $6,000 | $5,000 | A managed database move would also enable ARM-based managed database optimization. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | NOT_APPLICABLE | - | - | PostgreSQL 13 is already PostgreSQL-based. |

## Business Case
- Applicable scenarios: os_update_security_patch, switch_to_arm_cpu, application_server_replacement, app_refactor_decoupling, upgrade_legacy_databases, switch_to_managed_db, managed_arm_db
- Migration cost: $343,200
- Yearly savings: $188,500
- Three-year ROI: 64.8%
- Payback period: 1.82 years
