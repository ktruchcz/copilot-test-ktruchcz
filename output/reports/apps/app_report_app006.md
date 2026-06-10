# Application Report - SupportApp-006

## App overview
| Field | Value |
| --- | --- |
| Application ID | app006 |
| Name | SupportApp-006 |
| Description | IT service desk application for handling internal support tickets and IT service requests |
| Status | Production |
| Criticality | Medium |
| Deployment | AWS |
| Solution type | 3rd party software |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | Debian | 6 | EOL | Debian 6 is end-of-life. |
| database | PostgreSQL | 13 | OUTDATED | PostgreSQL 13 is behind the current supported baselines and nearing or beyond its support boundary. |
| language | Java | 11 | OUTDATED | Java 11 remains supported but is behind newer LTS releases. |
| framework | Unknown | unknown | NO_KNOWLEDGE | No framework or runtime value could be inferred from the inventory record. |
| application_server | GlassFish | 5.0 | NO_KNOWLEDGE | GlassFish is recorded, but the inventory does not map it to an agreed lifecycle rule in this assessment baseline. |

## Complexity score and label
- Complexity score: **4**
- Complexity label: **Medium**
- Indicative migration effort: **3-6 months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'Medium' adjusted score by +0.
- 1 EOL component(s) contributed +1 points (capped at +3).
- Server count of 1 contributed +0 points.
- Dependency count of 4 using external_interface_count proxy contributed +0 points.
- Solution type '3rd party software' contributed +0 points for custom code.
- Containerized='No' adjusted score by +0.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | High | The operating system Debian 6 is assessed as EOL, so remediation is recommended. | Update the operating system to the latest supported version to address security vulnerabilities and compliance requirements. |
| Switch to standard Linux Operating System | Medium | The current operating system (Debian 6) is not aligned with the standard Linux target baseline. | Standardize on widely supported operating systems that align with the customer's existing landscape standards to reduce the technology zoo, improve manageability, lower costs, and enhance security through simplified administration. |
| Applications Server replacement | Medium | The application uses legacy-style middleware (Glassfish 5.0), so replacement remains relevant even though exact support status is unknown. | Modernize application server infrastructure through one of the following approaches: migrate from commercial to open-source solutions to reduce licensing costs, transition to Platform-as-a-Service (PaaS) managed services for simplified operations, or replace legacy application server technology with modern alternatives to improve performance and reduce overall costs. |
| Upgrade Legacy Databases | High | The database PostgreSQL 13 is assessed as OUTDATED. | Upgrade legacy databases to modern, supported versions or cloud-native alternatives. |
| Update outdated components | High | The technology assessment found 3 component(s) that are EOL or outdated. | Rewrite or Refactor or Replace application for better security, agility and maintainability. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Switch to standard Linux Operating System | EUR 300.00 | EUR 240.00 | EUR 400.00 | 400.00% |
| Applications Server replacement | EUR 10,000.00 | EUR 8,000.00 | EUR 12,000.00 | 350.00% |
| Upgrade Legacy Databases | EUR 10,000.00 | EUR 8,000.00 | EUR 10,000.00 | 275.00% |
| Operating System Update | EUR 1,000.00 | EUR 800.00 | EUR 500.00 | 87.50% |
| Update outdated components | EUR 0.00 | EUR 0.00 | EUR 0.00 | n/a |
