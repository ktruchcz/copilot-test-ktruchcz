# Application Report - DataWarehouseApp-027

## App overview
| Field | Value |
| --- | --- |
| Application ID | app027 |
| Name | DataWarehouseApp-027 |
| Description | Enterprise data warehouse for consolidating business data from multiple sources |
| Status | Production |
| Criticality | High |
| Deployment | AWS, On-premise |
| Solution type | Custom made |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | RHEL | 7 | EOL | RHEL 7 reached end of maintenance support in June 2024. |
| database | SQL Server | 2022 | CURRENT_VERSION | SQL Server 2022 is a current supported release. |
| language | Java | 11 | OUTDATED | Java 11 remains supported but is behind newer LTS releases. |
| framework | Unknown | unknown | NO_KNOWLEDGE | No framework or runtime value could be inferred from the inventory record. |
| application_server | WebSphere | 8.5 | EOL | WebSphere 8.5 is end-of-life. |

## Complexity score and label
- Complexity score: **10**
- Complexity label: **Very high**
- Indicative migration effort: **12+ months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'High' adjusted score by +1.
- 2 EOL component(s) contributed +2 points (capped at +3).
- Server count of 2 contributed +1 points.
- Dependency count of 20 using external_interface_count proxy contributed +2 points.
- Solution type 'Custom made' contributed +1 points for custom code.
- Containerized='No' adjusted score by +0.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | High | The operating system RHEL 7 is assessed as EOL, so remediation is recommended. | Update the operating system to the latest supported version to address security vulnerabilities and compliance requirements. |
| Applications Server replacement | Medium | The application server Websphere 8.5 is assessed as EOL. | Modernize application server infrastructure through one of the following approaches: migrate from commercial to open-source solutions to reduce licensing costs, transition to Platform-as-a-Service (PaaS) managed services for simplified operations, or replace legacy application server technology with modern alternatives to improve performance and reduce overall costs. |
| Application Refactoring and De-coupling | High | The application is custom-built and shows legacy or integration complexity that makes decoupling valuable. | Refactor applications to decouple components for better agility and maintainability. |
| Switch DB Engine to open-source database solution | High | The application uses a proprietary database (SQL Server 2022), so an open-source alternative is relevant. | Migrate commercial databases (like Oracle) to PostgreSQL or alternatives like MySQL to reduce licensing costs. |
| Update outdated components | High | The technology assessment found 3 component(s) that are EOL or outdated. | Rewrite or Refactor or Replace application for better security, agility and maintainability. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Applications Server replacement | EUR 10,000.00 | EUR 20,000.00 | EUR 12,000.00 | 80.00% |
| Application Refactoring and De-coupling | EUR 250,000.00 | EUR 500,000.00 | EUR 150,000.00 | -10.00% |
| Switch DB Engine to open-source database solution | EUR 25,000.00 | EUR 50,000.00 | EUR 15,000.00 | -10.00% |
| Operating System Update | EUR 1,000.00 | EUR 2,000.00 | EUR 500.00 | -25.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | EUR 0.00 | n/a |
