# Application Report - PortalApp-025

## App overview
| Field | Value |
| --- | --- |
| Application ID | app025 |
| Name | PortalApp-025 |
| Description | Customer self-service portal for shipment tracking, billing, and service requests |
| Status | Production |
| Criticality | Medium |
| Deployment | AWS |
| Solution type | Custom made |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | Windows Server | 2019 | CURRENT_VERSION | Windows Server 2019 remains supported in the extended support window until 2029. |
| database | PostgreSQL | 15 | CURRENT_VERSION | PostgreSQL 15 remains a current supported release. |
| language | ASP.NET | unknown | NO_KNOWLEDGE | The inventory entry represents a framework or runtime rather than an explicit language version, so language lifecycle support cannot be assessed directly. |
| framework | ASP.NET Core | unknown | NO_KNOWLEDGE | ASP.NET Core is listed without a version, so lifecycle support cannot be assessed. |
| application_server | Microsoft IIS | 10.0 | NO_KNOWLEDGE | Microsoft IIS is recorded, but the modernization rule set does not provide lifecycle guidance for IIS versions. |

## Complexity score and label
- Complexity score: **6**
- Complexity label: **Medium**
- Indicative migration effort: **3-6 months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'Medium' adjusted score by +0.
- 0 EOL component(s) contributed +0 points (capped at +3).
- Server count of 2 contributed +1 points.
- Dependency count of 15 using external_interface_count proxy contributed +2 points.
- Solution type 'Custom made' contributed +1 points for custom code.
- Containerized='Yes' adjusted score by -1.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Switch to ARM-based CPU | Medium | The application already runs in cloud and uses a portable stack, so ARM-based infrastructure is a viable optimization path. | Adopt ARM-based CPU infrastructure for better energy efficiency and cost savings. |
| Application Refactoring and De-coupling | High | The application is custom-built and shows legacy or integration complexity that makes decoupling valuable. | Refactor applications to decouple components for better agility and maintainability. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Application Refactoring and De-coupling | EUR 250,000.00 | EUR 300,000.00 | EUR 150,000.00 | 50.00% |
| Switch to ARM-based CPU | EUR 5,000.00 | EUR 6,000.00 | EUR 1,000.00 | -50.00% |
