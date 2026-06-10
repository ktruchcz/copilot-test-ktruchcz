# Application Report - CRMApp-002

## App overview
| Field | Value |
| --- | --- |
| Application ID | app002 |
| Name | CRMApp-002 |
| Description | Customer relationship management system for tracking leads, opportunities, and customer interactions |
| Status | Production |
| Criticality | Medium |
| Deployment | AWS |
| Solution type | 3rd party software |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | RHEL | 7 | EOL | RHEL 7 reached end of maintenance support in June 2024. |
| database | MySQL | unknown | NO_KNOWLEDGE | The workload uses a managed MySQL service, but the service version is not recorded in the inventory. |
| language | Java | 11 | OUTDATED | Java 11 remains supported but is behind newer LTS releases. |
| framework | Unknown | unknown | NO_KNOWLEDGE | No framework or runtime value could be inferred from the inventory record. |
| application_server | WebSphere | 7.0 | EOL | WebSphere 7 is end-of-life. |

## Complexity score and label
- Complexity score: **7**
- Complexity label: **High**
- Indicative migration effort: **6-12 months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'Medium' adjusted score by +0.
- 2 EOL component(s) contributed +2 points (capped at +3).
- Server count of 2 contributed +1 points.
- Dependency count of 8 using external_interface_count proxy contributed +1 points.
- Solution type '3rd party software' contributed +0 points for custom code.
- Containerized='No' adjusted score by +0.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | High | The operating system RHEL 7 is assessed as EOL, so remediation is recommended. | Update the operating system to the latest supported version to address security vulnerabilities and compliance requirements. |
| Applications Server replacement | Medium | The application server Websphere 7.0 is assessed as EOL. | Modernize application server infrastructure through one of the following approaches: migrate from commercial to open-source solutions to reduce licensing costs, transition to Platform-as-a-Service (PaaS) managed services for simplified operations, or replace legacy application server technology with modern alternatives to improve performance and reduce overall costs. |
| Update outdated components | High | The technology assessment found 3 component(s) that are EOL or outdated. | Rewrite or Refactor or Replace application for better security, agility and maintainability. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Applications Server replacement | EUR 10,000.00 | EUR 14,000.00 | EUR 12,000.00 | 157.14% |
| Operating System Update | EUR 1,000.00 | EUR 1,400.00 | EUR 500.00 | 7.14% |
| Update outdated components | EUR 0.00 | EUR 0.00 | EUR 0.00 | n/a |
