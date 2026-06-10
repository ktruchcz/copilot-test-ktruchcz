# Application Report - ComplianceApp-022

## App overview
| Field | Value |
| --- | --- |
| Application ID | app022 |
| Name | ComplianceApp-022 |
| Description | Comprehensive compliance management platform for regulatory adherence and risk management |
| Status | Production |
| Criticality | Critical |
| Deployment | AWS, On-premise |
| Solution type | Custom made |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | RHEL | 7 | EOL | RHEL 7 reached end of maintenance support in June 2024. |
| database | PostgreSQL | 14 | CURRENT_VERSION | PostgreSQL 14 remains a current supported release. |
| language | Scala | 2.13 | NO_KNOWLEDGE | Programming language lifecycle support could not be mapped confidently from the recorded value. |
| framework | Unknown | unknown | NO_KNOWLEDGE | No framework or runtime value could be inferred from the inventory record. |
| application_server | Payara | 6.0 | NO_KNOWLEDGE | Payara is recorded, but the inventory does not map it to an agreed lifecycle rule in this assessment baseline. |

## Complexity score and label
- Complexity score: **9**
- Complexity label: **High**
- Indicative migration effort: **6-12 months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'Critical' adjusted score by +2.
- 1 EOL component(s) contributed +1 points (capped at +3).
- Server count of 2 contributed +1 points.
- Dependency count of 12 using external_interface_count proxy contributed +2 points.
- Solution type 'Custom made' contributed +1 points for custom code.
- Containerized='Yes' adjusted score by -1.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | High | The operating system RHEL 7 is assessed as EOL, so remediation is recommended. | Update the operating system to the latest supported version to address security vulnerabilities and compliance requirements. |
| Applications Server replacement | Medium | The application uses legacy-style middleware (Payara 6.0), so replacement remains relevant even though exact support status is unknown. | Modernize application server infrastructure through one of the following approaches: migrate from commercial to open-source solutions to reduce licensing costs, transition to Platform-as-a-Service (PaaS) managed services for simplified operations, or replace legacy application server technology with modern alternatives to improve performance and reduce overall costs. |
| Application Refactoring and De-coupling | High | The application is custom-built and shows legacy or integration complexity that makes decoupling valuable. | Refactor applications to decouple components for better agility and maintainability. |
| Update outdated components | High | The technology assessment found 1 component(s) that are EOL or outdated. | Rewrite or Refactor or Replace application for better security, agility and maintainability. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Applications Server replacement | EUR 10,000.00 | EUR 18,000.00 | EUR 12,000.00 | 100.00% |
| Operating System Update | EUR 1,000.00 | EUR 1,800.00 | EUR 500.00 | -16.67% |
| Application Refactoring and De-coupling | EUR 250,000.00 | EUR 450,000.00 | EUR 150,000.00 | 0.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | EUR 0.00 | n/a |
