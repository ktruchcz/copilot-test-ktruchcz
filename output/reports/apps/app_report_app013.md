# Application Report - SecurityApp-013

## App overview
| Field | Value |
| --- | --- |
| Application ID | app013 |
| Name | SecurityApp-013 |
| Description | Enterprise security platform for monitoring threats, managing access controls, and ensuring compliance |
| Status | Production |
| Criticality | Critical |
| Deployment | On-Premise |
| Solution type | Custom made |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | Debian | 7 | EOL | Debian 7 is end-of-life. |
| database | SQL Server | 2022 | CURRENT_VERSION | SQL Server 2022 is a current supported release. |
| language | Java | 17 | CURRENT_VERSION | Java 17 is a current LTS release. |
| framework | Unknown | unknown | NO_KNOWLEDGE | No framework or runtime value could be inferred from the inventory record. |
| application_server | WebSphere | 8.0 | EOL | WebSphere 8.x is end-of-life. |

## Complexity score and label
- Complexity score: **10**
- Complexity label: **Very high**
- Indicative migration effort: **12+ months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'Critical' adjusted score by +2.
- 2 EOL component(s) contributed +2 points (capped at +3).
- Server count of 2 contributed +1 points.
- Dependency count of 15 using external_interface_count proxy contributed +2 points.
- Solution type 'Custom made' contributed +1 points for custom code.
- Containerized='No' adjusted score by +0.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | High | The operating system Debian 7 is assessed as EOL, so remediation is recommended. | Update the operating system to the latest supported version to address security vulnerabilities and compliance requirements. |
| Switch to standard Linux Operating System | Medium | The current operating system (Debian 7) is not aligned with the standard Linux target baseline. | Standardize on widely supported operating systems that align with the customer's existing landscape standards to reduce the technology zoo, improve manageability, lower costs, and enhance security through simplified administration. |
| Applications Server replacement | Medium | The application server Websphere 8.0 is assessed as EOL. | Modernize application server infrastructure through one of the following approaches: migrate from commercial to open-source solutions to reduce licensing costs, transition to Platform-as-a-Service (PaaS) managed services for simplified operations, or replace legacy application server technology with modern alternatives to improve performance and reduce overall costs. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | High | The application is currently on-premise, so lift-and-shift cloud migration is applicable. | Deploy applications to public cloud infrastructure using a Lift(-tinker)-and-shift approach with modern deployment practices, maintaining existing architecture while gaining improved scalability, security, and compliance benefits. |
| Application Containerization | High | The application is not containerized and no blocking constraint is explicitly recorded in the inventory. | Containerize applications to improve scalability, portability, agility and resource efficiency. |
| Application Refactoring and De-coupling | High | The application is custom-built and shows legacy or integration complexity that makes decoupling valuable. | Refactor applications to decouple components for better agility and maintainability. |
| Switch DB Engine to open-source database solution | High | The application uses a proprietary database (SQL Server 2022), so an open-source alternative is relevant. | Migrate commercial databases (like Oracle) to PostgreSQL or alternatives like MySQL to reduce licensing costs. |
| Update outdated components | High | The technology assessment found 2 component(s) that are EOL or outdated. | Rewrite or Refactor or Replace application for better security, agility and maintainability. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Switch to standard Linux Operating System | EUR 300.00 | EUR 600.00 | EUR 400.00 | 100.00% |
| Applications Server replacement | EUR 10,000.00 | EUR 20,000.00 | EUR 12,000.00 | 80.00% |
| Application Containerization | EUR 100,000.00 | EUR 200,000.00 | EUR 100,000.00 | 50.00% |
| Application Refactoring and De-coupling | EUR 250,000.00 | EUR 500,000.00 | EUR 150,000.00 | -10.00% |
| Switch DB Engine to open-source database solution | EUR 25,000.00 | EUR 50,000.00 | EUR 15,000.00 | -10.00% |
