# Application Report - DocumentApp-014
Application app014 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app014 |
| Name | DocumentApp-014 |
| Status | Production |
| Solution Type | Open Source |
| Deployment Type | AWS |
| Business Criticality | Medium |
| Operating System | Windows Server 2019 |
| Programming Language | C# .NET 6 |
| Application Server | Microsoft IIS 10.0 |
| Database Engine | MySQL 8.0 |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | Windows Server | 2019 | CURRENT_VERSION | Lifecycle rule matched for Windows Server 2019. |
| programming_language | .NET | 6 | EOL | Lifecycle rule matched for .NET 6. |
| application_server | Microsoft IIS 10.0 | unknown | NO_KNOWLEDGE | Application server technology is not covered by the provided lifecycle rules. |
| database | MySQL | 8 | CURRENT_VERSION | Lifecycle rule matched for MySQL 8. |

Overall technology risk: **CRITICAL**.

## Complexity Assessment
Complexity score: **6** (Medium) — estimated effort **3-6 months**.

| Factor | Value |
| --- | --- |
| Base Score | 3 |
| Business Criticality | Medium |
| Criticality Adjustment | 0 |
| Eol Components | 1 |
| Eol Adjustment | 1 |
| Server Count | 2 |
| Server Adjustment | 1 |
| Dependency Proxy | external_interface_count |
| Dependency Count | 9 |
| Dependency Adjustment | 1 |
| Custom Code | False |
| Custom Code Adjustment | 0 |
| Containerized | False |
| Containerization Adjustment | 0 |

Started from base score 3, applied +0 for Medium criticality, +1 for 1 EOL component(s), +1 for 2 server(s), +1 using external interfaces as the dependency proxy (9), +0 for custom code indication, and +0 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Application Containerization | PARTIALLY_FULFILLED | The application is already cloud-hosted, but the source data does not show containerization yet. | Containerize the workload to improve portability, release consistency, and scaling options. |
| Update outdated components | APPLICABLE | The technology assessment found 1 EOL and 0 outdated component(s). | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Application Containerization | EUR 120,000.00 | EUR 100,000.00 | 150.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 120,000.00**  
Total annual savings: **EUR 100,000.00**
