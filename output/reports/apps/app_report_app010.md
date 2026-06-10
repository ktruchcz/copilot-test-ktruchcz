# Application Report - PayrollApp-010

## App overview
| Field | Value |
| --- | --- |
| Application ID | app010 |
| Name | PayrollApp-010 |
| Description | Payroll processing system handling salary calculations, tax deductions, and compensation reporting |
| Status | Production |
| Criticality | Medium |
| Deployment | AWS |
| Solution type | 3rd party software |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | Windows Server | 2019 | CURRENT_VERSION | Windows Server 2019 remains supported in the extended support window until 2029. |
| database | MySQL | 8.0 | CURRENT_VERSION | MySQL 8.0 is the current supported major release. |
| language | Ruby | 2.7 | EOL | Ruby 2.7 is end-of-life. |
| framework | Unknown | unknown | NO_KNOWLEDGE | No framework or runtime value could be inferred from the inventory record. |
| application_server | Microsoft IIS | 10.0 | NO_KNOWLEDGE | Microsoft IIS is recorded, but the modernization rule set does not provide lifecycle guidance for IIS versions. |

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
| Update outdated components | High | The technology assessment found 1 component(s) that are EOL or outdated. | Rewrite or Refactor or Replace application for better security, agility and maintainability. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Update outdated components | EUR 0.00 | EUR 0.00 | EUR 0.00 | n/a |
