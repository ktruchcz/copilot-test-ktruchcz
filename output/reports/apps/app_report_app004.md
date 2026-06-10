# Application Report - HRApp-004

## App overview
| Field | Value |
| --- | --- |
| Application ID | app004 |
| Name | HRApp-004 |
| Description | Human resources management system handling employee records, benefits, and HR workflows |
| Status | Production |
| Criticality | High |
| Deployment | AWS, On-premise |
| Solution type | Custom made |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | Windows Server | 2012 | EOL | Windows Server 2012 reached end of support in October 2023. |
| database | SQL Server | 2019 | CURRENT_VERSION | SQL Server 2019 remains supported. |
| language | .NET | unknown | NO_KNOWLEDGE | The inventory entry represents a framework or runtime rather than an explicit language version, so language lifecycle support cannot be assessed directly. |
| framework | .NET | unknown | NO_KNOWLEDGE | The workload uses .NET Core but no version is captured in the inventory. |
| application_server | Microsoft IIS | 8.0 | NO_KNOWLEDGE | Microsoft IIS is recorded, but the modernization rule set does not provide lifecycle guidance for IIS versions. |

## Complexity score and label
- Complexity score: **7**
- Complexity label: **High**
- Indicative migration effort: **6-12 months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'High' adjusted score by +1.
- 1 EOL component(s) contributed +1 points (capped at +3).
- Server count of 2 contributed +1 points.
- Dependency count of 6 using external_interface_count proxy contributed +1 points.
- Solution type 'Custom made' contributed +1 points for custom code.
- Containerized='Yes' adjusted score by -1.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | High | The operating system Windows Server 2012 is assessed as EOL, so remediation is recommended. | Update the operating system to the latest supported version to address security vulnerabilities and compliance requirements. |
| Application Refactoring and De-coupling | High | The application is custom-built and shows legacy or integration complexity that makes decoupling valuable. | Refactor applications to decouple components for better agility and maintainability. |
| Switch DB Engine to open-source database solution | High | The application uses a proprietary database (SQL Server 2019), so an open-source alternative is relevant. | Migrate commercial databases (like Oracle) to PostgreSQL or alternatives like MySQL to reduce licensing costs. |
| Update outdated components | High | The technology assessment found 1 component(s) that are EOL or outdated. | Rewrite or Refactor or Replace application for better security, agility and maintainability. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Application Refactoring and De-coupling | EUR 250,000.00 | EUR 350,000.00 | EUR 150,000.00 | 28.57% |
| Switch DB Engine to open-source database solution | EUR 25,000.00 | EUR 35,000.00 | EUR 15,000.00 | 28.57% |
| Operating System Update | EUR 1,000.00 | EUR 1,400.00 | EUR 500.00 | 7.14% |
| Update outdated components | EUR 0.00 | EUR 0.00 | EUR 0.00 | n/a |
