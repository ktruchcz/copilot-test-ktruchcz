# Application Report - PayrollApp-010
Application app010 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app010 |
| Name | PayrollApp-010 |
| Status | Production |
| Solution Type | 3rd party software |
| Deployment Type | AWS |
| Business Criticality | Medium |
| Operating System | Windows Server 2019 |
| Programming Language | Ruby 2.7 |
| Application Server | Microsoft IIS 10.0 |
| Database Engine | MySQL 8.0 |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | Windows Server | 2019 | CURRENT_VERSION | Lifecycle rule matched for Windows Server 2019. |
| programming_language | Ruby 2.7 | unknown | NO_KNOWLEDGE | Programming language or runtime version is not covered by the provided lifecycle rules. |
| application_server | Microsoft IIS 10.0 | unknown | NO_KNOWLEDGE | Application server technology is not covered by the provided lifecycle rules. |
| database | MySQL | 8 | CURRENT_VERSION | Lifecycle rule matched for MySQL 8. |

Overall technology risk: **MEDIUM**.

## Complexity Assessment
Complexity score: **3** (Low) — estimated effort **1-2 months**.

| Factor | Value |
| --- | --- |
| Base Score | 3 |
| Business Criticality | Medium |
| Criticality Adjustment | 0 |
| Eol Components | 0 |
| Eol Adjustment | 0 |
| Server Count | 1 |
| Server Adjustment | 0 |
| Dependency Proxy | external_interface_count |
| Dependency Count | 4 |
| Dependency Adjustment | 0 |
| Custom Code | False |
| Custom Code Adjustment | 0 |
| Containerized | False |
| Containerization Adjustment | 0 |

Started from base score 3, applied +0 for Medium criticality, +0 for 0 EOL component(s), +0 for 1 server(s), +0 using external interfaces as the dependency proxy (4), +0 for custom code indication, and +0 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Application Containerization | PARTIALLY_FULFILLED | The application is already cloud-hosted, but the source data does not show containerization yet. | Containerize the workload to improve portability, release consistency, and scaling options. |
| Update outdated components | PARTIALLY_FULFILLED | Known components are current, but some technologies could not be dated from the available application data. | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Application Containerization | EUR 60,000.00 | EUR 100,000.00 | 400.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 60,000.00**  
Total annual savings: **EUR 100,000.00**
