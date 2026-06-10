# Application Report - HRApp-004
Application app004 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app004 |
| Name | HRApp-004 |
| Status | Production |
| Solution Type | Custom made |
| Deployment Type | AWS, On-premise |
| Business Criticality | High |
| Operating System | Windows Server 2012 |
| Programming Language | .NET Core |
| Application Server | Microsoft IIS 8.0 |
| Database Engine | SQL Server 2019 |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | Windows Server | 2012 | EOL | Lifecycle rule matched for Windows Server 2012. |
| programming_language | .NET | unknown | NO_KNOWLEDGE | The application uses .NET, but no supported version was provided. |
| application_server | Microsoft IIS 8.0 | unknown | NO_KNOWLEDGE | Application server technology is not covered by the provided lifecycle rules. |
| database | SQL Server | 2019 | CURRENT_VERSION | Lifecycle rule matched for SQL Server 2019. |

Overall technology risk: **CRITICAL**.

## Complexity Assessment
Complexity score: **7** (High) — estimated effort **6-12 months**.

| Factor | Value |
| --- | --- |
| Base Score | 3 |
| Business Criticality | High |
| Criticality Adjustment | 1 |
| Eol Components | 1 |
| Eol Adjustment | 1 |
| Server Count | 2 |
| Server Adjustment | 1 |
| Dependency Proxy | external_interface_count |
| Dependency Count | 6 |
| Dependency Adjustment | 1 |
| Custom Code | True |
| Custom Code Adjustment | 1 |
| Containerized | True |
| Containerization Adjustment | -1 |

Started from base score 3, applied +1 for High criticality, +1 for 1 EOL component(s), +1 for 2 server(s), +1 using external interfaces as the dependency proxy (6), +1 for custom code indication, and -1 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | APPLICABLE | The operating system (Windows Server 2012) is assessed as EOL, so patching or upgrading is recommended. | Prioritize OS remediation to restore vendor support and security patch eligibility. |
| Switch to ARM-based CPU | APPLICABLE | The application is already deployed on AWS, On-premise and uses a portable stack, so ARM-based hosting is a credible optimization option. | Pilot ARM on portable workloads to validate performance and cost savings before broad adoption. |
| Application Refactoring and De-coupling | APPLICABLE | The application is custom-built and integration-heavy, so decoupling and refactoring would likely improve modernization outcomes. | Refactor tightly coupled functionality to reduce change risk and improve modernization flexibility. |
| Switch DB Engine to open-source database solution | APPLICABLE | The application uses a proprietary database (SQL Server 2019), so an open-source alternative could reduce cost and lock-in. | Assess a move to an open-source database to reduce licensing costs and lock-in. |
| Update outdated components | APPLICABLE | The technology assessment found 1 EOL and 0 outdated component(s). | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Operating System Update | EUR 1,400.00 | EUR 500.00 | 7.14% |
| Switch to ARM-based CPU | EUR 7,000.00 | EUR 1,000.00 | -57.14% |
| Application Refactoring and De-coupling | EUR 350,000.00 | EUR 150,000.00 | 28.57% |
| Switch DB Engine to open-source database solution | EUR 35,000.00 | EUR 15,000.00 | 28.57% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 393,400.00**  
Total annual savings: **EUR 166,500.00**
