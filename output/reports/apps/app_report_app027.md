# Application Report - DataWarehouseApp-027
Application app027 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app027 |
| Name | DataWarehouseApp-027 |
| Status | Production |
| Solution Type | Custom made |
| Deployment Type | AWS, On-premise |
| Business Criticality | High |
| Operating System | RHEL 7 |
| Programming Language | Java 11 |
| Application Server | Websphere 8.5 |
| Database Engine | SQL Server 2022 |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | RHEL | 7 | EOL | Lifecycle rule matched for RHEL 7. |
| programming_language | Java | 11 | OUTDATED | Lifecycle rule matched for Java 11. |
| application_server | WebSphere | 8.5 | EOL | Lifecycle rule matched for WebSphere 8.x. |
| database | SQL Server | 2022 | CURRENT_VERSION | Lifecycle rule matched for SQL Server 2022. |

Overall technology risk: **CRITICAL**.

## Complexity Assessment
Complexity score: **10** (Very High) — estimated effort **12+ months**.

| Factor | Value |
| --- | --- |
| Base Score | 3 |
| Business Criticality | High |
| Criticality Adjustment | 1 |
| Eol Components | 2 |
| Eol Adjustment | 2 |
| Server Count | 2 |
| Server Adjustment | 1 |
| Dependency Proxy | external_interface_count |
| Dependency Count | 20 |
| Dependency Adjustment | 2 |
| Custom Code | True |
| Custom Code Adjustment | 1 |
| Containerized | False |
| Containerization Adjustment | 0 |

Started from base score 3, applied +1 for High criticality, +2 for 2 EOL component(s), +1 for 2 server(s), +2 using external interfaces as the dependency proxy (20), +1 for custom code indication, and +0 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | APPLICABLE | The operating system (RHEL 7) is assessed as EOL, so patching or upgrading is recommended. | Prioritize OS remediation to restore vendor support and security patch eligibility. |
| Applications Server replacement | APPLICABLE | The current application server (Websphere 8.5) is assessed as EOL, which makes replacement relevant. | Replace legacy middleware with a supported application platform or simplify the hosting stack. |
| Application Refactoring and De-coupling | APPLICABLE | The application is custom-built and integration-heavy, so decoupling and refactoring would likely improve modernization outcomes. | Refactor tightly coupled functionality to reduce change risk and improve modernization flexibility. |
| Switch DB Engine to open-source database solution | APPLICABLE | The application uses a proprietary database (SQL Server 2022), so an open-source alternative could reduce cost and lock-in. | Assess a move to an open-source database to reduce licensing costs and lock-in. |
| Update outdated components | APPLICABLE | The technology assessment found 2 EOL and 1 outdated component(s). | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Operating System Update | EUR 2,000.00 | EUR 500.00 | -25.00% |
| Applications Server replacement | EUR 20,000.00 | EUR 12,000.00 | 80.00% |
| Application Refactoring and De-coupling | EUR 500,000.00 | EUR 150,000.00 | -10.00% |
| Switch DB Engine to open-source database solution | EUR 50,000.00 | EUR 15,000.00 | -10.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 572,000.00**  
Total annual savings: **EUR 177,500.00**
