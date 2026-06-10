# Application Report - AnalyticsApp-003

## App overview
| Field | Value |
| --- | --- |
| Application ID | app003 |
| Name | AnalyticsApp-003 |
| Description | Analytics platform for generating operational reports and business insights from logistics data |
| Status | Production |
| Criticality | Low |
| Deployment | AWS |
| Solution type | Open Source |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | RHEL | 7 | EOL | RHEL 7 reached end of maintenance support in June 2024. |
| database | PostgreSQL | 13 | OUTDATED | PostgreSQL 13 is behind the current supported baselines and nearing or beyond its support boundary. |
| language | Python | 3.9 | OUTDATED | Python 3.9 is behind current supported baselines. |
| framework | Unknown | unknown | NO_KNOWLEDGE | No framework or runtime value could be inferred from the inventory record. |
| application_server | Tomcat | 6.1 | EOL | Tomcat 6.x is long end-of-life. |

## Complexity score and label
- Complexity score: **3**
- Complexity label: **Low**
- Indicative migration effort: **1-2 months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'Low' adjusted score by -1.
- 2 EOL component(s) contributed +2 points (capped at +3).
- Server count of 1 contributed +0 points.
- Dependency count of 3 using external_interface_count proxy contributed +0 points.
- Solution type 'Open Source' contributed +0 points for custom code.
- Containerized='Yes' adjusted score by -1.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | High | The operating system RHEL 7 is assessed as EOL, so remediation is recommended. | Update the operating system to the latest supported version to address security vulnerabilities and compliance requirements. |
| Switch to ARM-based CPU | Medium | The application already runs in cloud and uses a portable stack, so ARM-based infrastructure is a viable optimization path. | Adopt ARM-based CPU infrastructure for better energy efficiency and cost savings. |
| Applications Server replacement | Medium | The application server Apache Tomcat 6.1 is assessed as EOL. | Modernize application server infrastructure through one of the following approaches: migrate from commercial to open-source solutions to reduce licensing costs, transition to Platform-as-a-Service (PaaS) managed services for simplified operations, or replace legacy application server technology with modern alternatives to improve performance and reduce overall costs. |
| Upgrade Legacy Databases | High | The database PostgreSQL 13 is assessed as OUTDATED. | Upgrade legacy databases to modern, supported versions or cloud-native alternatives. |
| Update outdated components | High | The technology assessment found 4 component(s) that are EOL or outdated. | Rewrite or Refactor or Replace application for better security, agility and maintainability. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Applications Server replacement | EUR 10,000.00 | EUR 6,000.00 | EUR 12,000.00 | 500.00% |
| Upgrade Legacy Databases | EUR 10,000.00 | EUR 6,000.00 | EUR 10,000.00 | 400.00% |
| Operating System Update | EUR 1,000.00 | EUR 600.00 | EUR 500.00 | 150.00% |
| Switch to ARM-based CPU | EUR 5,000.00 | EUR 3,000.00 | EUR 1,000.00 | 0.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | EUR 0.00 | n/a |
