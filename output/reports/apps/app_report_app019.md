# Application Report - QualityApp-019

## App overview
| Field | Value |
| --- | --- |
| Application ID | app019 |
| Name | QualityApp-019 |
| Description | Quality management system for tracking service quality metrics and managing audit processes |
| Status | Production |
| Criticality | High |
| Deployment | AWS, On-premise |
| Solution type | Custom made |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | RHEL | 8 | CURRENT_VERSION | RHEL 8 remains in vendor support until May 2029. |
| database | MySQL | 8.0 | CURRENT_VERSION | MySQL 8.0 is the current supported major release. |
| language | Python | 3.8 | EOL | Python 3.8 is end-of-life. |
| framework | Unknown | unknown | NO_KNOWLEDGE | No framework or runtime value could be inferred from the inventory record. |
| application_server | Tomcat | 8.0 | EOL | Tomcat 8.x is end-of-life. |

## Complexity score and label
- Complexity score: **8**
- Complexity label: **High**
- Indicative migration effort: **6-12 months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'High' adjusted score by +1.
- 2 EOL component(s) contributed +2 points (capped at +3).
- Server count of 1 contributed +0 points.
- Dependency count of 5 using external_interface_count proxy contributed +1 points.
- Solution type 'Custom made' contributed +1 points for custom code.
- Containerized='No' adjusted score by +0.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Applications Server replacement | Medium | The application server Apache Tomcat  8.0 is assessed as EOL. | Modernize application server infrastructure through one of the following approaches: migrate from commercial to open-source solutions to reduce licensing costs, transition to Platform-as-a-Service (PaaS) managed services for simplified operations, or replace legacy application server technology with modern alternatives to improve performance and reduce overall costs. |
| Application Refactoring and De-coupling | High | The application is custom-built and shows legacy or integration complexity that makes decoupling valuable. | Refactor applications to decouple components for better agility and maintainability. |
| Update outdated components | High | The technology assessment found 2 component(s) that are EOL or outdated. | Rewrite or Refactor or Replace application for better security, agility and maintainability. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Applications Server replacement | EUR 10,000.00 | EUR 16,000.00 | EUR 12,000.00 | 125.00% |
| Application Refactoring and De-coupling | EUR 250,000.00 | EUR 400,000.00 | EUR 150,000.00 | 12.50% |
| Update outdated components | EUR 0.00 | EUR 0.00 | EUR 0.00 | n/a |
