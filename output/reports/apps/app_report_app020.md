# Application Report - TrainingApp-020

## App overview
| Field | Value |
| --- | --- |
| Application ID | app020 |
| Name | TrainingApp-020 |
| Description | Learning management system for employee training programs and professional development tracking |
| Status | Production |
| Criticality | Low |
| Deployment | AWS |
| Solution type | 3rd party software |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | Windows Server | 2012 | EOL | Windows Server 2012 reached end of support in October 2023. |
| database | SQL Server | 2016 | OUTDATED | SQL Server 2016 is still usable but well behind current supported releases. |
| language | Angular | 15 | NO_KNOWLEDGE | The inventory entry represents a framework or runtime rather than an explicit language version, so language lifecycle support cannot be assessed directly. |
| framework | Angular | 15 | EOL | Angular 15 is below the currently supported baseline and treated as end-of-life. |
| application_server | Microsoft IIS | 8.5 | NO_KNOWLEDGE | Microsoft IIS is recorded, but the modernization rule set does not provide lifecycle guidance for IIS versions. |

## Complexity score and label
- Complexity score: **5**
- Complexity label: **Medium**
- Indicative migration effort: **3-6 months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'Low' adjusted score by -1.
- 2 EOL component(s) contributed +2 points (capped at +3).
- Server count of 1 contributed +0 points.
- Dependency count of 7 using external_interface_count proxy contributed +1 points.
- Solution type '3rd party software' contributed +0 points for custom code.
- Containerized='No' adjusted score by +0.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | High | The operating system Windows Server 2012 is assessed as EOL, so remediation is recommended. | Update the operating system to the latest supported version to address security vulnerabilities and compliance requirements. |
| Upgrade Legacy Databases | High | The database SQL Server 2016 is assessed as OUTDATED. | Upgrade legacy databases to modern, supported versions or cloud-native alternatives. |
| Update outdated components | High | The technology assessment found 3 component(s) that are EOL or outdated. | Rewrite or Refactor or Replace application for better security, agility and maintainability. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Upgrade Legacy Databases | EUR 10,000.00 | EUR 10,000.00 | EUR 10,000.00 | 200.00% |
| Operating System Update | EUR 1,000.00 | EUR 1,000.00 | EUR 500.00 | 50.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | EUR 0.00 | n/a |
