# Application Report - QualityApp-019
Application app019 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app019 |
| Name | QualityApp-019 |
| Status | Production |
| Solution Type | Custom made |
| Deployment Type | AWS, On-premise |
| Business Criticality | High |
| Operating System | RHEL 8 |
| Programming Language | Python 3.8 |
| Application Server | Apache Tomcat  8.0 |
| Database Engine | MySQL 8.0 |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | RHEL | 8 | CURRENT_VERSION | Lifecycle rule matched for RHEL 8. |
| programming_language | Python | 3.8 | EOL | Lifecycle rule matched for Python 3.8. |
| application_server | Tomcat | 8.0 | EOL | Lifecycle rule matched for Tomcat 8. |
| database | MySQL | 8 | CURRENT_VERSION | Lifecycle rule matched for MySQL 8. |

Overall technology risk: **CRITICAL**.

## Complexity Assessment
Complexity score: **8** (High) — estimated effort **6-12 months**.

| Factor | Value |
| --- | --- |
| Base Score | 3 |
| Business Criticality | High |
| Criticality Adjustment | 1 |
| Eol Components | 2 |
| Eol Adjustment | 2 |
| Server Count | 1 |
| Server Adjustment | 0 |
| Dependency Proxy | external_interface_count |
| Dependency Count | 5 |
| Dependency Adjustment | 1 |
| Custom Code | True |
| Custom Code Adjustment | 1 |
| Containerized | False |
| Containerization Adjustment | 0 |

Started from base score 3, applied +1 for High criticality, +2 for 2 EOL component(s), +0 for 1 server(s), +1 using external interfaces as the dependency proxy (5), +1 for custom code indication, and +0 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Switch to ARM-based CPU | APPLICABLE | The application is already deployed on AWS, On-premise and uses a portable stack, so ARM-based hosting is a credible optimization option. | Pilot ARM on portable workloads to validate performance and cost savings before broad adoption. |
| Applications Server replacement | APPLICABLE | The current application server (Apache Tomcat  8.0) is assessed as EOL, which makes replacement relevant. | Replace legacy middleware with a supported application platform or simplify the hosting stack. |
| Application Containerization | PARTIALLY_FULFILLED | The application is already cloud-hosted, but the source data does not show containerization yet. | Containerize the workload to improve portability, release consistency, and scaling options. |
| Application Refactoring and De-coupling | APPLICABLE | The application is custom-built and integration-heavy, so decoupling and refactoring would likely improve modernization outcomes. | Refactor tightly coupled functionality to reduce change risk and improve modernization flexibility. |
| Update outdated components | APPLICABLE | The technology assessment found 2 EOL and 0 outdated component(s). | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Switch to ARM-based CPU | EUR 8,000.00 | EUR 1,000.00 | -62.50% |
| Applications Server replacement | EUR 16,000.00 | EUR 12,000.00 | 125.00% |
| Application Containerization | EUR 160,000.00 | EUR 100,000.00 | 87.50% |
| Application Refactoring and De-coupling | EUR 400,000.00 | EUR 150,000.00 | 12.50% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 584,000.00**  
Total annual savings: **EUR 263,000.00**
