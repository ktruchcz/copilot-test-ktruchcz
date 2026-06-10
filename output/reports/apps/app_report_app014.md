# Application Report - DocumentApp-014

## App overview
| Field | Value |
| --- | --- |
| Application ID | app014 |
| Name | DocumentApp-014 |
| Description | Document management system for handling shipping documents, contracts, and regulatory paperwork |
| Status | Production |
| Criticality | Medium |
| Deployment | AWS |
| Solution type | Open Source |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | Windows Server | 2019 | CURRENT_VERSION | Windows Server 2019 remains supported in the extended support window until 2029. |
| database | MySQL | 8.0 | CURRENT_VERSION | MySQL 8.0 is the current supported major release. |
| language | C# | 6 | NO_KNOWLEDGE | The inventory entry represents a framework or runtime rather than an explicit language version, so language lifecycle support cannot be assessed directly. |
| framework | .NET | 6 | EOL | .NET 6 reached end of support in November 2024. |
| application_server | Microsoft IIS | 10.0 | NO_KNOWLEDGE | Microsoft IIS is recorded, but the modernization rule set does not provide lifecycle guidance for IIS versions. |

## Complexity score and label
- Complexity score: **6**
- Complexity label: **Medium**
- Indicative migration effort: **3-6 months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'Medium' adjusted score by +0.
- 1 EOL component(s) contributed +1 points (capped at +3).
- Server count of 2 contributed +1 points.
- Dependency count of 9 using external_interface_count proxy contributed +1 points.
- Solution type 'Open Source' contributed +0 points for custom code.
- Containerized='No' adjusted score by +0.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Update outdated components | High | The technology assessment found 1 component(s) that are EOL or outdated. | Rewrite or Refactor or Replace application for better security, agility and maintainability. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Update outdated components | EUR 0.00 | EUR 0.00 | EUR 0.00 | n/a |
