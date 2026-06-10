# Application Report - MobileApp-016

## App overview
| Field | Value |
| --- | --- |
| Application ID | app016 |
| Name | MobileApp-016 |
| Description | Mobile application for drivers and customers to track shipments and manage delivery operations |
| Status | Production |
| Criticality | Medium |
| Deployment | AWS |
| Solution type | Custom made |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | RHEL | 7 | EOL | RHEL 7 reached end of maintenance support in June 2024. |
| database | SQL Server | 2019 | CURRENT_VERSION | SQL Server 2019 remains supported. |
| language | React | unknown | NO_KNOWLEDGE | The inventory entry represents a framework or runtime rather than an explicit language version, so language lifecycle support cannot be assessed directly. |
| framework | React Native | unknown | NO_KNOWLEDGE | React Native is listed without a version, so lifecycle support cannot be assessed. |
| application_server | Payara | 4.0 | NO_KNOWLEDGE | Payara is recorded, but the inventory does not map it to an agreed lifecycle rule in this assessment baseline. |

## Complexity score and label
- Complexity score: **6**
- Complexity label: **Medium**
- Indicative migration effort: **3-6 months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'Medium' adjusted score by +0.
- 1 EOL component(s) contributed +1 points (capped at +3).
- Server count of 2 contributed +1 points.
- Dependency count of 10 using external_interface_count proxy contributed +1 points.
- Solution type 'Custom made' contributed +1 points for custom code.
- Containerized='Yes' adjusted score by -1.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | High | The operating system RHEL 7 is assessed as EOL, so remediation is recommended. | Update the operating system to the latest supported version to address security vulnerabilities and compliance requirements. |
| Switch to ARM-based CPU | Medium | The application already runs in cloud and uses a portable stack, so ARM-based infrastructure is a viable optimization path. | Adopt ARM-based CPU infrastructure for better energy efficiency and cost savings. |
| Applications Server replacement | Medium | The application uses legacy-style middleware (Payara 4.0), so replacement remains relevant even though exact support status is unknown. | Modernize application server infrastructure through one of the following approaches: migrate from commercial to open-source solutions to reduce licensing costs, transition to Platform-as-a-Service (PaaS) managed services for simplified operations, or replace legacy application server technology with modern alternatives to improve performance and reduce overall costs. |
| Application Refactoring and De-coupling | High | The application is custom-built and shows legacy or integration complexity that makes decoupling valuable. | Refactor applications to decouple components for better agility and maintainability. |
| Switch DB Engine to open-source database solution | High | The application uses a proprietary database (SQL Server 2019), so an open-source alternative is relevant. | Migrate commercial databases (like Oracle) to PostgreSQL or alternatives like MySQL to reduce licensing costs. |
| Update outdated components | High | The technology assessment found 1 component(s) that are EOL or outdated. | Rewrite or Refactor or Replace application for better security, agility and maintainability. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Applications Server replacement | EUR 10,000.00 | EUR 12,000.00 | EUR 12,000.00 | 200.00% |
| Application Refactoring and De-coupling | EUR 250,000.00 | EUR 300,000.00 | EUR 150,000.00 | 50.00% |
| Switch DB Engine to open-source database solution | EUR 25,000.00 | EUR 30,000.00 | EUR 15,000.00 | 50.00% |
| Operating System Update | EUR 1,000.00 | EUR 1,200.00 | EUR 500.00 | 25.00% |
| Switch to ARM-based CPU | EUR 5,000.00 | EUR 6,000.00 | EUR 1,000.00 | -50.00% |
