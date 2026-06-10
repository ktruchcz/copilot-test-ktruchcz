# Application Report - NotificationApp-028

## App overview
| Field | Value |
| --- | --- |
| Application ID | app028 |
| Name | NotificationApp-028 |
| Description | Centralized notification system for sending emails, SMS, and push notifications across all applications |
| Status | Production |
| Criticality | Medium |
| Deployment | AWS |
| Solution type | 3rd party software |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | Windows Server | 2019 | CURRENT_VERSION | Windows Server 2019 remains supported in the extended support window until 2029. |
| database | Oracle Database | 19c | CURRENT_VERSION | Oracle Database 19c is the current long-term support release until April 2027. |
| language | Java | 17 | CURRENT_VERSION | Java 17 is a current LTS release. |
| framework | Unknown | unknown | NO_KNOWLEDGE | No framework or runtime value could be inferred from the inventory record. |
| application_server | Microsoft IIS | 10.0 | NO_KNOWLEDGE | Microsoft IIS is recorded, but the modernization rule set does not provide lifecycle guidance for IIS versions. |

## Complexity score and label
- Complexity score: **5**
- Complexity label: **Medium**
- Indicative migration effort: **3-6 months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'Medium' adjusted score by +0.
- 0 EOL component(s) contributed +0 points (capped at +3).
- Server count of 2 contributed +1 points.
- Dependency count of 25 using external_interface_count proxy contributed +2 points.
- Solution type '3rd party software' contributed +0 points for custom code.
- Containerized='Yes' adjusted score by -1.

## Applicable scenarios with recommendations
No APPLICABLE modernization scenarios were identified from the available source data.

## Business case for top scenarios
No quantified APPLICABLE scenarios were available in the finance model.
