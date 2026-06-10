# Application Report - LegacyFinApp-026

## App overview
| Field | Value |
| --- | --- |
| Application ID | app026 |
| Name | LegacyFinApp-026 |
| Description | Legacy financial modeling system for complex calculations and risk assessments |
| Status | Production |
| Criticality | Critical |
| Deployment | On-Premise |
| Solution type | Custom made |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | AIX | 7.2 | NO_KNOWLEDGE | AIX lifecycle data was not part of the supplied rule set, so support status cannot be assessed confidently from the inventory alone. |
| database | DB2 | 2 | NO_KNOWLEDGE | The inventory lists DB2 without a version, so lifecycle support cannot be assessed. |
| language | FORTRAN | 2018 | NO_KNOWLEDGE | Programming language lifecycle support could not be mapped confidently from the recorded value. |
| framework | Unknown | unknown | NO_KNOWLEDGE | No framework or runtime value could be inferred from the inventory record. |
| application_server | Unknown | unknown | NO_KNOWLEDGE | No application server value was provided in the application inventory. |

## Complexity score and label
- Complexity score: **6**
- Complexity label: **Medium**
- Indicative migration effort: **3-6 months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'Critical' adjusted score by +2.
- 0 EOL component(s) contributed +0 points (capped at +3).
- Server count of 1 contributed +0 points.
- Dependency count of 1 using external_interface_count proxy contributed +0 points.
- Solution type 'Custom made' contributed +1 points for custom code.
- Containerized='No' adjusted score by +0.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Switch to standard Linux Operating System | Medium | The current operating system (AIX 7.2) is not aligned with the standard Linux target baseline. | Standardize on widely supported operating systems that align with the customer's existing landscape standards to reduce the technology zoo, improve manageability, lower costs, and enhance security through simplified administration. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | High | The application is currently on-premise, so lift-and-shift cloud migration is applicable. | Deploy applications to public cloud infrastructure using a Lift(-tinker)-and-shift approach with modern deployment practices, maintaining existing architecture while gaining improved scalability, security, and compliance benefits. |
| Application Refactoring and De-coupling | High | The application is custom-built and shows legacy or integration complexity that makes decoupling valuable. | Refactor applications to decouple components for better agility and maintainability. |
| Switch DB Engine to open-source database solution | High | The application uses a proprietary database (DB2), so an open-source alternative is relevant. | Migrate commercial databases (like Oracle) to PostgreSQL or alternatives like MySQL to reduce licensing costs. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Switch to standard Linux Operating System | EUR 300.00 | EUR 360.00 | EUR 400.00 | 233.33% |
| Application Refactoring and De-coupling | EUR 250,000.00 | EUR 300,000.00 | EUR 150,000.00 | 50.00% |
| Switch DB Engine to open-source database solution | EUR 25,000.00 | EUR 30,000.00 | EUR 15,000.00 | 50.00% |
| Application Migration to Cloud Infrastructure (Lift & Shift) | EUR 5,000.00 | EUR 6,000.00 | EUR 3,000.00 | 50.00% |
