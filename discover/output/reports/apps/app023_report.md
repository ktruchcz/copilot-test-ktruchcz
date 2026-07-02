# ChatbotApp-023 (app023)

## Application Overview
- Status: Production
- Solution type: Open Source
- Criticality: Medium
- Deployment: AWS
- Users: 1100
- Architecture: 3-Tier
- Containerized: Yes
- CI/CD: Yes

## Technology Assessment
| Component Type | Component | Status | Support / EOL Date | Reason |
|---|---|---|---|---|
| os | RHEL 8 | CURRENT_VERSION | 2029-05-31 | RHEL 8 is still within its active support window. |
| programming_language | Node.js 18 | OUTDATED | 2025-04-30 | Node.js 18 is an older LTS line and should be advanced to a newer supported release. |
| application_server | Apache Tomcat 7.4 | EOL | 2021-03-31 | Apache Tomcat 7.x is end-of-life. |
| database | MongoDB | CURRENT_VERSION | n/a | MongoDB is treated as current; no version was provided, but the service is assumed to be on a supported release. |

## Complexity Assessment
- Complexity score: **6 / 10**
- Complexity label: **Medium**
- Cost multiplier: **1.2x**

- **Business Criticality** (medium): Criticality is Medium and requires controlled cutover planning.
- **Technology Debt** (high): Technology debt includes 1 EOL and 1 outdated component(s).
- **Integration Surface** (high): The application exposes 22 API endpoints and 8 external interfaces.

## Applicable Scenarios
| Scenario | Status | Migration Cost | Yearly Savings | Reason |
|---|---|---:|---:|---|
| Operating System Update | NOT_APPLICABLE | - | - | Operating system RHEL 8 is already on a current supported release. |
| Switch to standard Linux Operating System | NOT_APPLICABLE | - | - | RHEL 8 is already a Linux-based operating system. |
| Switch to ARM-based CPU | APPLICABLE | $6,000 | $1,000 | The application has cloud or container portability characteristics that make ARM migration feasible. |
| Applications Server replacement | APPLICABLE | $12,000 | $12,000 | Application server Apache Tomcat 7.4 is EOL and should be replaced or upgraded. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | FULFILLED | - | - | The application is already fully deployed in AWS. |
| Application Containerization | FULFILLED | - | - | The application is already containerized. |
| Application Refactoring and De-coupling | APPLICABLE | $300,000 | $150,000 | The recorded architecture (3-Tier) suggests a layered or monolithic design suitable for decoupling. |
| Upgrade Legacy Databases | NOT_APPLICABLE | - | - | Database engine MongoDB is current. |
| Switch to Managed Database | NOT_APPLICABLE | - | - | MongoDB is already treated as a managed database service. |
| Managed ARM Database | NOT_APPLICABLE | - | - | Managed ARM database migration depends on first moving to a managed database platform, which is already satisfied or not needed. |
| Serverless Database Migration | NOT_APPLICABLE | - | - | Serverless database migration is targeted at cloud workloads with database sizes below 100GB. |
| Switch Database Engine to PostgreSQL | NOT_APPLICABLE | - | - | MongoDB is not in the relational database set targeted by this scenario. |

## Business Case
- Applicable scenarios: switch_to_arm_cpu, application_server_replacement, app_refactor_decoupling
- Migration cost: $318,000
- Yearly savings: $163,000
- Three-year ROI: 53.8%
- Payback period: 1.95 years
