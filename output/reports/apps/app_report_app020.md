# Application Report - TrainingApp-020
Application app020 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app020 |
| Name | TrainingApp-020 |
| Status | Production |
| Solution Type | 3rd party software |
| Deployment Type | AWS |
| Business Criticality | Low |
| Operating System | Windows Server 2012 |
| Programming Language | Angular 15 |
| Application Server | Microsoft IIS 8.5 |
| Database Engine | SQL Server 2016 |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | Windows Server | 2012 | EOL | Lifecycle rule matched for Windows Server 2012. |
| programming_language | Angular | 15 | EOL | Lifecycle rule matched for Angular 15. |
| application_server | Microsoft IIS 8.5 | unknown | NO_KNOWLEDGE | Application server technology is not covered by the provided lifecycle rules. |
| database | SQL Server | 2016 | OUTDATED | Lifecycle rule matched for SQL Server 2016. |

Overall technology risk: **CRITICAL**.

## Complexity Assessment
Complexity score: **5** (Medium) — estimated effort **3-6 months**.

| Factor | Value |
| --- | --- |
| Base Score | 3 |
| Business Criticality | Low |
| Criticality Adjustment | -1 |
| Eol Components | 2 |
| Eol Adjustment | 2 |
| Server Count | 1 |
| Server Adjustment | 0 |
| Dependency Proxy | external_interface_count |
| Dependency Count | 7 |
| Dependency Adjustment | 1 |
| Custom Code | False |
| Custom Code Adjustment | 0 |
| Containerized | False |
| Containerization Adjustment | 0 |

Started from base score 3, applied -1 for Low criticality, +2 for 2 EOL component(s), +0 for 1 server(s), +1 using external interfaces as the dependency proxy (7), +0 for custom code indication, and +0 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | APPLICABLE | The operating system (Windows Server 2012) is assessed as EOL, so patching or upgrading is recommended. | Prioritize OS remediation to restore vendor support and security patch eligibility. |
| Application Containerization | PARTIALLY_FULFILLED | The application is already cloud-hosted, but the source data does not show containerization yet. | Containerize the workload to improve portability, release consistency, and scaling options. |
| Upgrade Legacy Databases | APPLICABLE | The database (SQL Server 2016) is assessed as OUTDATED, so an upgrade is justified. | Upgrade the database platform to remove lifecycle risk and improve supportability. |
| Update outdated components | APPLICABLE | The technology assessment found 2 EOL and 1 outdated component(s). | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Operating System Update | EUR 1,000.00 | EUR 500.00 | 50.00% |
| Application Containerization | EUR 100,000.00 | EUR 100,000.00 | 200.00% |
| Upgrade Legacy Databases | EUR 10,000.00 | EUR 10,000.00 | 200.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 111,000.00**  
Total annual savings: **EUR 110,500.00**
