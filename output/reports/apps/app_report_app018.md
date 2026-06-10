# Application Report - VendorApp-018

## App overview
| Field | Value |
| --- | --- |
| Application ID | app018 |
| Name | VendorApp-018 |
| Description | Vendor management platform for handling supplier relationships, contracts, and procurement processes |
| Status | Production |
| Criticality | Medium |
| Deployment | On-Premise |
| Solution type | Custom made |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | RHEL | 7 | EOL | RHEL 7 reached end of maintenance support in June 2024. |
| database | PostgreSQL | 13 | OUTDATED | PostgreSQL 13 is behind the current supported baselines and nearing or beyond its support boundary. |
| language | Java | 8 | EOL | Java 8 premier support ended in March 2022. |
| framework | Unknown | unknown | NO_KNOWLEDGE | No framework or runtime value could be inferred from the inventory record. |
| application_server | GlassFish | 4.5 | NO_KNOWLEDGE | GlassFish is recorded, but the inventory does not map it to an agreed lifecycle rule in this assessment baseline. |

## Complexity score and label
- Complexity score: **8**
- Complexity label: **High**
- Indicative migration effort: **6-12 months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'Medium' adjusted score by +0.
- 2 EOL component(s) contributed +2 points (capped at +3).
- Server count of 2 contributed +1 points.
- Dependency count of 6 using external_interface_count proxy contributed +1 points.
- Solution type 'Custom made' contributed +1 points for custom code.
- Containerized='No' adjusted score by +0.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | High | The operating system RHEL 7 is assessed as EOL, so remediation is recommended. | Update the operating system to the latest supported version to address security vulnerabilities and compliance requirements. |
| Applications Server replacement | Medium | The application uses legacy-style middleware (Glassfish 4.5), so replacement remains relevant even though exact support status is unknown. | Modernize application server infrastructure through one of the following approaches: migrate from commercial to open-source solutions to reduce licensing costs, transition to Platform-as-a-Service (PaaS) managed services for simplified operations, or replace legacy application server technology with modern alternatives to improve performance and reduce overall costs. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | High | The application is currently on-premise, so lift-and-shift cloud migration is applicable. | Deploy applications to public cloud infrastructure using a Lift(-tinker)-and-shift approach with modern deployment practices, maintaining existing architecture while gaining improved scalability, security, and compliance benefits. |
| Application Containerization | High | The application is not containerized and no blocking constraint is explicitly recorded in the inventory. | Containerize applications to improve scalability, portability, agility and resource efficiency. |
| Application Refactoring and De-coupling | High | The application is custom-built and shows legacy or integration complexity that makes decoupling valuable. | Refactor applications to decouple components for better agility and maintainability. |
| Upgrade Legacy Databases | High | The database PostgreSQL 13 is assessed as OUTDATED. | Upgrade legacy databases to modern, supported versions or cloud-native alternatives. |
| Update outdated components | High | The technology assessment found 3 component(s) that are EOL or outdated. | Rewrite or Refactor or Replace application for better security, agility and maintainability. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Applications Server replacement | EUR 10,000.00 | EUR 16,000.00 | EUR 12,000.00 | 125.00% |
| Application Containerization | EUR 100,000.00 | EUR 160,000.00 | EUR 100,000.00 | 87.50% |
| Upgrade Legacy Databases | EUR 10,000.00 | EUR 16,000.00 | EUR 10,000.00 | 87.50% |
| Application Refactoring and De-coupling | EUR 250,000.00 | EUR 400,000.00 | EUR 150,000.00 | 12.50% |
| Application Migration to Cloud Infrastructure (Lift & Shift) | EUR 5,000.00 | EUR 8,000.00 | EUR 3,000.00 | 12.50% |
