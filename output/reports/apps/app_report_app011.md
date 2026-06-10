# Application Report - RouteOptApp-011

## App overview
| Field | Value |
| --- | --- |
| Application ID | app011 |
| Name | RouteOptApp-011 |
| Description | Advanced route optimization system using machine learning algorithms for delivery planning |
| Status | Production |
| Criticality | Medium |
| Deployment | AWS |
| Solution type | Custom made |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | CentOS | 7 | EOL | CentOS 7 reached end of life in June 2024. |
| database | PostgreSQL | 14 | CURRENT_VERSION | PostgreSQL 14 remains a current supported release. |
| language | Python | 3.11 | CURRENT_VERSION | Python 3.11 is a current supported release. |
| framework | Unknown | unknown | NO_KNOWLEDGE | No framework or runtime value could be inferred from the inventory record. |
| application_server | GlassFish | 4.0 | NO_KNOWLEDGE | GlassFish is recorded, but the inventory does not map it to an agreed lifecycle rule in this assessment baseline. |

## Complexity score and label
- Complexity score: **5**
- Complexity label: **Medium**
- Indicative migration effort: **3-6 months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'Medium' adjusted score by +0.
- 1 EOL component(s) contributed +1 points (capped at +3).
- Server count of 1 contributed +0 points.
- Dependency count of 5 using external_interface_count proxy contributed +1 points.
- Solution type 'Custom made' contributed +1 points for custom code.
- Containerized='Yes' adjusted score by -1.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | High | The operating system CentOS 7 is assessed as EOL, so remediation is recommended. | Update the operating system to the latest supported version to address security vulnerabilities and compliance requirements. |
| Switch to standard Linux Operating System | Medium | The current operating system (CentOS 7) is not aligned with the standard Linux target baseline. | Standardize on widely supported operating systems that align with the customer's existing landscape standards to reduce the technology zoo, improve manageability, lower costs, and enhance security through simplified administration. |
| Switch to ARM-based CPU | Medium | The application already runs in cloud and uses a portable stack, so ARM-based infrastructure is a viable optimization path. | Adopt ARM-based CPU infrastructure for better energy efficiency and cost savings. |
| Applications Server replacement | Medium | The application uses legacy-style middleware (Glassfish 4.0), so replacement remains relevant even though exact support status is unknown. | Modernize application server infrastructure through one of the following approaches: migrate from commercial to open-source solutions to reduce licensing costs, transition to Platform-as-a-Service (PaaS) managed services for simplified operations, or replace legacy application server technology with modern alternatives to improve performance and reduce overall costs. |
| Application Refactoring and De-coupling | High | The application is custom-built and shows legacy or integration complexity that makes decoupling valuable. | Refactor applications to decouple components for better agility and maintainability. |
| Update outdated components | High | The technology assessment found 1 component(s) that are EOL or outdated. | Rewrite or Refactor or Replace application for better security, agility and maintainability. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Switch to standard Linux Operating System | EUR 300.00 | EUR 300.00 | EUR 400.00 | 300.00% |
| Applications Server replacement | EUR 10,000.00 | EUR 10,000.00 | EUR 12,000.00 | 260.00% |
| Application Refactoring and De-coupling | EUR 250,000.00 | EUR 250,000.00 | EUR 150,000.00 | 80.00% |
| Operating System Update | EUR 1,000.00 | EUR 1,000.00 | EUR 500.00 | 50.00% |
| Switch to ARM-based CPU | EUR 5,000.00 | EUR 5,000.00 | EUR 1,000.00 | -40.00% |
