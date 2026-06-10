# Application Report - SecurityApp-013
Application app013 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app013 |
| Name | SecurityApp-013 |
| Status | Production |
| Solution Type | Custom made |
| Deployment Type | On-Premise |
| Business Criticality | Critical |
| Operating System | Debian 7 |
| Programming Language | Java 17 |
| Application Server | Websphere 8.0 |
| Database Engine | SQL Server 2022 |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | Debian 7 | unknown | NO_KNOWLEDGE | Operating system version is not covered by the provided lifecycle rules. |
| programming_language | Java | 17 | CURRENT_VERSION | Lifecycle rule matched for Java 17. |
| application_server | WebSphere | 8.0 | EOL | Lifecycle rule matched for WebSphere 8.x. |
| database | SQL Server | 2022 | CURRENT_VERSION | Lifecycle rule matched for SQL Server 2022. |

Overall technology risk: **CRITICAL**.

## Complexity Assessment
Complexity score: **10** (Very High) — estimated effort **12+ months**.

| Factor | Value |
| --- | --- |
| Base Score | 3 |
| Business Criticality | Critical |
| Criticality Adjustment | 2 |
| Eol Components | 1 |
| Eol Adjustment | 1 |
| Server Count | 2 |
| Server Adjustment | 1 |
| Dependency Proxy | external_interface_count |
| Dependency Count | 15 |
| Dependency Adjustment | 2 |
| Custom Code | True |
| Custom Code Adjustment | 1 |
| Containerized | False |
| Containerization Adjustment | 0 |

Started from base score 3, applied +2 for Critical criticality, +1 for 1 EOL component(s), +1 for 2 server(s), +2 using external interfaces as the dependency proxy (15), +1 for custom code indication, and +0 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Switch to standard Linux Operating System | PARTIALLY_FULFILLED | The workload already runs on Linux (Debian 7), but not on the target standard Linux distributions highlighted in the rules. | Standardize the platform on supported Linux distributions where stack constraints allow. |
| Applications Server replacement | APPLICABLE | The current application server (Websphere 8.0) is assessed as EOL, which makes replacement relevant. | Replace legacy middleware with a supported application platform or simplify the hosting stack. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | APPLICABLE | The application is currently deployed as On-Premise, so lift-and-shift to cloud remains a valid option. | Evaluate lift-and-shift migration to reduce infrastructure management effort. |
| Application Refactoring and De-coupling | APPLICABLE | The application is custom-built and integration-heavy, so decoupling and refactoring would likely improve modernization outcomes. | Refactor tightly coupled functionality to reduce change risk and improve modernization flexibility. |
| Switch DB Engine to open-source database solution | APPLICABLE | The application uses a proprietary database (SQL Server 2022), so an open-source alternative could reduce cost and lock-in. | Assess a move to an open-source database to reduce licensing costs and lock-in. |
| Update outdated components | APPLICABLE | The technology assessment found 1 EOL and 0 outdated component(s). | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Switch to standard Linux Operating System | EUR 600.00 | EUR 400.00 | 100.00% |
| Applications Server replacement | EUR 20,000.00 | EUR 12,000.00 | 80.00% |
| Application Migration to Cloud Infrastructure (Lift & Shift) | EUR 10,000.00 | EUR 3,000.00 | -10.00% |
| Application Refactoring and De-coupling | EUR 500,000.00 | EUR 150,000.00 | -10.00% |
| Switch DB Engine to open-source database solution | EUR 50,000.00 | EUR 15,000.00 | -10.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 580,600.00**  
Total annual savings: **EUR 180,400.00**
