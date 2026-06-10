# Application Report - ReportingApp-015
Application app015 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app015 |
| Name | ReportingApp-015 |
| Status | Production |
| Solution Type | Custom made |
| Deployment Type | AWS |
| Business Criticality | Low |
| Operating System | Windows Server 2019 |
| Programming Language | PHP 8.1 |
| Application Server | Microsoft IIS 10.0 |
| Database Engine | MongoDB |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | Windows Server | 2019 | CURRENT_VERSION | Lifecycle rule matched for Windows Server 2019. |
| programming_language | PHP 8.1 | unknown | NO_KNOWLEDGE | Programming language or runtime version is not covered by the provided lifecycle rules. |
| application_server | Microsoft IIS 10.0 | unknown | NO_KNOWLEDGE | Application server technology is not covered by the provided lifecycle rules. |
| database | MongoDB | unknown | NO_KNOWLEDGE | Database engine is not covered by the provided lifecycle rules. |

Overall technology risk: **MEDIUM**.

## Complexity Assessment
Complexity score: **3** (Low) — estimated effort **1-2 months**.

| Factor | Value |
| --- | --- |
| Base Score | 3 |
| Business Criticality | Low |
| Criticality Adjustment | -1 |
| Eol Components | 0 |
| Eol Adjustment | 0 |
| Server Count | 1 |
| Server Adjustment | 0 |
| Dependency Proxy | external_interface_count |
| Dependency Count | 4 |
| Dependency Adjustment | 0 |
| Custom Code | True |
| Custom Code Adjustment | 1 |
| Containerized | False |
| Containerization Adjustment | 0 |

Started from base score 3, applied -1 for Low criticality, +0 for 0 EOL component(s), +0 for 1 server(s), +0 using external interfaces as the dependency proxy (4), +1 for custom code indication, and +0 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Switch to ARM-based CPU | APPLICABLE | The application is already deployed on AWS and uses a portable stack, so ARM-based hosting is a credible optimization option. | Pilot ARM on portable workloads to validate performance and cost savings before broad adoption. |
| Application Containerization | PARTIALLY_FULFILLED | The application is already cloud-hosted, but the source data does not show containerization yet. | Containerize the workload to improve portability, release consistency, and scaling options. |
| Application Refactoring and De-coupling | PARTIALLY_FULFILLED | The application is custom-built, but the current data shows only moderate integration pressure for deeper refactoring. | Refactor tightly coupled functionality to reduce change risk and improve modernization flexibility. |
| Update outdated components | PARTIALLY_FULFILLED | Known components are current, but some technologies could not be dated from the available application data. | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Switch to ARM-based CPU | EUR 3,000.00 | EUR 1,000.00 | 0.00% |
| Application Containerization | EUR 60,000.00 | EUR 100,000.00 | 400.00% |
| Application Refactoring and De-coupling | EUR 150,000.00 | EUR 150,000.00 | 200.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 213,000.00**  
Total annual savings: **EUR 251,000.00**
