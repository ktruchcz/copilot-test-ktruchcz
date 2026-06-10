# Application Report - APIGatewayApp-030

## App overview
| Field | Value |
| --- | --- |
| Application ID | app030 |
| Name | APIGatewayApp-030 |
| Description | Modern API gateway for managing microservices communication and external API access |
| Status | Production |
| Criticality | High |
| Deployment | AWS |
| Solution type | Open Source |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | RHEL | 8 | CURRENT_VERSION | RHEL 8 remains in vendor support until May 2029. |
| database | MySQL | 5.7 | EOL | MySQL 5.7 reached end of life in October 2023. |
| language | Go | 1.19 | EOL | Go 1.19 is no longer within the two-release support window. |
| framework | Unknown | unknown | NO_KNOWLEDGE | No framework or runtime value could be inferred from the inventory record. |
| application_server | GlassFish | 3.0 | NO_KNOWLEDGE | GlassFish is recorded, but the inventory does not map it to an agreed lifecycle rule in this assessment baseline. |

## Complexity score and label
- Complexity score: **8**
- Complexity label: **High**
- Indicative migration effort: **6-12 months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'High' adjusted score by +1.
- 2 EOL component(s) contributed +2 points (capped at +3).
- Server count of 2 contributed +1 points.
- Dependency count of 30 using external_interface_count proxy contributed +2 points.
- Solution type 'Open Source' contributed +0 points for custom code.
- Containerized='Yes' adjusted score by -1.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Switch to ARM-based CPU | Medium | The application already runs in cloud and uses a portable stack, so ARM-based infrastructure is a viable optimization path. | Adopt ARM-based CPU infrastructure for better energy efficiency and cost savings. |
| Applications Server replacement | Medium | The application uses legacy-style middleware (Glassfish 3.0), so replacement remains relevant even though exact support status is unknown. | Modernize application server infrastructure through one of the following approaches: migrate from commercial to open-source solutions to reduce licensing costs, transition to Platform-as-a-Service (PaaS) managed services for simplified operations, or replace legacy application server technology with modern alternatives to improve performance and reduce overall costs. |
| Upgrade Legacy Databases | High | The database MySQL 5.7 is assessed as EOL. | Upgrade legacy databases to modern, supported versions or cloud-native alternatives. |
| Update outdated components | High | The technology assessment found 2 component(s) that are EOL or outdated. | Rewrite or Refactor or Replace application for better security, agility and maintainability. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Applications Server replacement | EUR 10,000.00 | EUR 16,000.00 | EUR 12,000.00 | 125.00% |
| Upgrade Legacy Databases | EUR 10,000.00 | EUR 16,000.00 | EUR 10,000.00 | 87.50% |
| Switch to ARM-based CPU | EUR 5,000.00 | EUR 8,000.00 | EUR 1,000.00 | -62.50% |
| Update outdated components | EUR 0.00 | EUR 0.00 | EUR 0.00 | n/a |
