# Application Report - AuditApp-024

## App overview
| Field | Value |
| --- | --- |
| Application ID | app024 |
| Name | AuditApp-024 |
| Description | Legacy audit management system for tracking financial audits and compliance activities |
| Status | Production |
| Criticality | High |
| Deployment | On-Premise |
| Solution type | Custom made |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | Windows Server | 2019 | CURRENT_VERSION | Windows Server 2019 remains supported in the extended support window until 2029. |
| database | SQL Server | 2014 | EOL | SQL Server 2014 is end-of-life. |
| language | VB.NET | unknown | NO_KNOWLEDGE | Programming language lifecycle support could not be mapped confidently from the recorded value. |
| framework | Unknown | unknown | NO_KNOWLEDGE | No framework or runtime value could be inferred from the inventory record. |
| application_server | Microsoft IIS | 10.0 | NO_KNOWLEDGE | Microsoft IIS is recorded, but the modernization rule set does not provide lifecycle guidance for IIS versions. |

## Complexity score and label
- Complexity score: **6**
- Complexity label: **Medium**
- Indicative migration effort: **3-6 months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'High' adjusted score by +1.
- 1 EOL component(s) contributed +1 points (capped at +3).
- Server count of 1 contributed +0 points.
- Dependency count of 3 using external_interface_count proxy contributed +0 points.
- Solution type 'Custom made' contributed +1 points for custom code.
- Containerized='No' adjusted score by +0.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Application Migration to Cloud Infrastructure (Lift & Shift) | High | The application is currently on-premise, so lift-and-shift cloud migration is applicable. | Deploy applications to public cloud infrastructure using a Lift(-tinker)-and-shift approach with modern deployment practices, maintaining existing architecture while gaining improved scalability, security, and compliance benefits. |
| Application Containerization | High | The application is not containerized and no blocking constraint is explicitly recorded in the inventory. | Containerize applications to improve scalability, portability, agility and resource efficiency. |
| Upgrade Legacy Databases | High | The database SQL Server 2014 is assessed as EOL. | Upgrade legacy databases to modern, supported versions or cloud-native alternatives. |
| Switch DB Engine to open-source database solution | High | The application uses a proprietary database (SQL Server 2014), so an open-source alternative is relevant. | Migrate commercial databases (like Oracle) to PostgreSQL or alternatives like MySQL to reduce licensing costs. |
| Update outdated components | High | The technology assessment found 1 component(s) that are EOL or outdated. | Rewrite or Refactor or Replace application for better security, agility and maintainability. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Application Containerization | EUR 100,000.00 | EUR 120,000.00 | EUR 100,000.00 | 150.00% |
| Upgrade Legacy Databases | EUR 10,000.00 | EUR 12,000.00 | EUR 10,000.00 | 150.00% |
| Switch DB Engine to open-source database solution | EUR 25,000.00 | EUR 30,000.00 | EUR 15,000.00 | 50.00% |
| Application Migration to Cloud Infrastructure (Lift & Shift) | EUR 5,000.00 | EUR 6,000.00 | EUR 3,000.00 | 50.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | EUR 0.00 | n/a |
