# Application Report - ERPApp-001

## App overview
| Field | Value |
| --- | --- |
| Application ID | app001 |
| Name | ERPApp-001 |
| Description | Core ERP system handling financial transactions, general ledger, and regulatory reporting |
| Status | Production |
| Criticality | High |
| Deployment | On-Premise |
| Solution type | Custom made |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | AIX | 7.2 | NO_KNOWLEDGE | AIX lifecycle data was not part of the supplied rule set, so support status cannot be assessed confidently from the inventory alone. |
| database | Oracle Database | 19c | CURRENT_VERSION | Oracle Database 19c is the current long-term support release until April 2027. |
| language | COBOL-2014 | 2014 | NO_KNOWLEDGE | Programming language lifecycle support could not be mapped confidently from the recorded value. |
| framework | Unknown | unknown | NO_KNOWLEDGE | No framework or runtime value could be inferred from the inventory record. |
| application_server | Unknown | unknown | NO_KNOWLEDGE | No application server value was provided in the application inventory. |

## Complexity score and label
- Complexity score: **7**
- Complexity label: **High**
- Indicative migration effort: **6-12 months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'High' adjusted score by +1.
- 0 EOL component(s) contributed +0 points (capped at +3).
- Server count of 2 contributed +1 points.
- Dependency count of 5 using external_interface_count proxy contributed +1 points.
- Solution type 'Custom made' contributed +1 points for custom code.
- Containerized='No' adjusted score by +0.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Switch to standard Linux Operating System | Medium | The current operating system (AIX 7.2) is not aligned with the standard Linux target baseline. | Standardize on widely supported operating systems that align with the customer's existing landscape standards to reduce the technology zoo, improve manageability, lower costs, and enhance security through simplified administration. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | High | The application is currently on-premise, so lift-and-shift cloud migration is applicable. | Deploy applications to public cloud infrastructure using a Lift(-tinker)-and-shift approach with modern deployment practices, maintaining existing architecture while gaining improved scalability, security, and compliance benefits. |
| Application Refactoring and De-coupling | High | The application is custom-built and shows legacy or integration complexity that makes decoupling valuable. | Refactor applications to decouple components for better agility and maintainability. |
| Switch DB Engine to open-source database solution | High | The application uses a proprietary database (Oracle 19c), so an open-source alternative is relevant. | Migrate commercial databases (like Oracle) to PostgreSQL or alternatives like MySQL to reduce licensing costs. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Switch to standard Linux Operating System | EUR 300.00 | EUR 420.00 | EUR 400.00 | 185.71% |
| Application Refactoring and De-coupling | EUR 250,000.00 | EUR 350,000.00 | EUR 150,000.00 | 28.57% |
| Switch DB Engine to open-source database solution | EUR 25,000.00 | EUR 35,000.00 | EUR 15,000.00 | 28.57% |
| Application Migration to Cloud Infrastructure (Lift & Shift) | EUR 5,000.00 | EUR 7,000.00 | EUR 3,000.00 | 28.57% |
