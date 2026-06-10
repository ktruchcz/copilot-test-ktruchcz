# Application Report - BackupApp-017

## App overview
| Field | Value |
| --- | --- |
| Application ID | app017 |
| Name | BackupApp-017 |
| Description | Automated backup and disaster recovery system for critical business applications and data |
| Status | Production |
| Criticality | High |
| Deployment | On-Premise |
| Solution type | 3rd party software |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | RHEL | 7 | EOL | RHEL 7 reached end of maintenance support in June 2024. |
| database | Oracle Database | 12c | EOL | Oracle Database 12c is end-of-life. |
| language | PowerShell | unknown | NO_KNOWLEDGE | Programming language lifecycle support could not be mapped confidently from the recorded value. |
| framework | Unknown | unknown | NO_KNOWLEDGE | No framework or runtime value could be inferred from the inventory record. |
| application_server | Payara | 5.0 | NO_KNOWLEDGE | Payara is recorded, but the inventory does not map it to an agreed lifecycle rule in this assessment baseline. |

## Complexity score and label
- Complexity score: **8**
- Complexity label: **High**
- Indicative migration effort: **6-12 months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'High' adjusted score by +1.
- 2 EOL component(s) contributed +2 points (capped at +3).
- Server count of 2 contributed +1 points.
- Dependency count of 8 using external_interface_count proxy contributed +1 points.
- Solution type '3rd party software' contributed +0 points for custom code.
- Containerized='No' adjusted score by +0.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | High | The operating system RHEL 7 is assessed as EOL, so remediation is recommended. | Update the operating system to the latest supported version to address security vulnerabilities and compliance requirements. |
| Applications Server replacement | Medium | The application uses legacy-style middleware (Payara 5.0), so replacement remains relevant even though exact support status is unknown. | Modernize application server infrastructure through one of the following approaches: migrate from commercial to open-source solutions to reduce licensing costs, transition to Platform-as-a-Service (PaaS) managed services for simplified operations, or replace legacy application server technology with modern alternatives to improve performance and reduce overall costs. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | High | The application is currently on-premise, so lift-and-shift cloud migration is applicable. | Deploy applications to public cloud infrastructure using a Lift(-tinker)-and-shift approach with modern deployment practices, maintaining existing architecture while gaining improved scalability, security, and compliance benefits. |
| Application Containerization | High | The application is not containerized and no blocking constraint is explicitly recorded in the inventory. | Containerize applications to improve scalability, portability, agility and resource efficiency. |
| Upgrade Legacy Databases | High | The database Oracle 12c is assessed as EOL. | Upgrade legacy databases to modern, supported versions or cloud-native alternatives. |
| Update outdated components | High | The technology assessment found 2 component(s) that are EOL or outdated. | Rewrite or Refactor or Replace application for better security, agility and maintainability. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Applications Server replacement | EUR 10,000.00 | EUR 16,000.00 | EUR 12,000.00 | 125.00% |
| Application Containerization | EUR 100,000.00 | EUR 160,000.00 | EUR 100,000.00 | 87.50% |
| Upgrade Legacy Databases | EUR 10,000.00 | EUR 16,000.00 | EUR 10,000.00 | 87.50% |
| Application Migration to Cloud Infrastructure (Lift & Shift) | EUR 5,000.00 | EUR 8,000.00 | EUR 3,000.00 | 12.50% |
| Operating System Update | EUR 1,000.00 | EUR 1,600.00 | EUR 500.00 | -6.25% |
