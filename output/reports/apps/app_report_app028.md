# Application Report - NotificationApp-028
Application app028 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app028 |
| Name | NotificationApp-028 |
| Status | Production |
| Solution Type | 3rd party software |
| Deployment Type | AWS |
| Business Criticality | Medium |
| Operating System | Windows Server 2019 |
| Programming Language | Java 17 |
| Application Server | Microsoft IIS 10.0 |
| Database Engine | Oracle 19c |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | Windows Server | 2019 | CURRENT_VERSION | Lifecycle rule matched for Windows Server 2019. |
| programming_language | Java | 17 | CURRENT_VERSION | Lifecycle rule matched for Java 17. |
| application_server | Microsoft IIS 10.0 | unknown | NO_KNOWLEDGE | Application server technology is not covered by the provided lifecycle rules. |
| database | Oracle | 19c | CURRENT_VERSION | Lifecycle rule matched for Oracle 19c. |

Overall technology risk: **MEDIUM**.

## Complexity Assessment
Complexity score: **5** (Medium) — estimated effort **3-6 months**.

| Factor | Value |
| --- | --- |
| Base Score | 3 |
| Business Criticality | Medium |
| Criticality Adjustment | 0 |
| Eol Components | 0 |
| Eol Adjustment | 0 |
| Server Count | 2 |
| Server Adjustment | 1 |
| Dependency Proxy | external_interface_count |
| Dependency Count | 25 |
| Dependency Adjustment | 2 |
| Custom Code | False |
| Custom Code Adjustment | 0 |
| Containerized | True |
| Containerization Adjustment | -1 |

Started from base score 3, applied +0 for Medium criticality, +0 for 0 EOL component(s), +1 for 2 server(s), +2 using external interfaces as the dependency proxy (25), +0 for custom code indication, and -1 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Switch to ARM-based CPU | APPLICABLE | The application is already deployed on AWS and uses a portable stack, so ARM-based hosting is a credible optimization option. | Pilot ARM on portable workloads to validate performance and cost savings before broad adoption. |
| Update outdated components | PARTIALLY_FULFILLED | Known components are current, but some technologies could not be dated from the available application data. | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Switch to ARM-based CPU | EUR 5,000.00 | EUR 1,000.00 | -40.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 5,000.00**  
Total annual savings: **EUR 1,000.00**
