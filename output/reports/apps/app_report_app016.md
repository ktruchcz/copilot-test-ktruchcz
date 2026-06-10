# Application Report - MobileApp-016
Application app016 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app016 |
| Name | MobileApp-016 |
| Status | Production |
| Solution Type | Custom made |
| Deployment Type | AWS |
| Business Criticality | Medium |
| Operating System | RHEL 7 |
| Programming Language | React Native |
| Application Server | Payara 4.0 |
| Database Engine | SQL Server 2019 |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | RHEL | 7 | EOL | Lifecycle rule matched for RHEL 7. |
| programming_language | React Native | unknown | NO_KNOWLEDGE | Programming language or runtime version is not covered by the provided lifecycle rules. |
| application_server | Payara 4.0 | unknown | NO_KNOWLEDGE | Application server technology is not covered by the provided lifecycle rules. |
| database | SQL Server | 2019 | CURRENT_VERSION | Lifecycle rule matched for SQL Server 2019. |

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
| Dependency Count | 10 |
| Dependency Adjustment | 1 |
| Custom Code | True |
| Custom Code Adjustment | 1 |
| Containerized | True |
| Containerization Adjustment | -1 |

Started from base score 3, applied +0 for Medium criticality, +1 for 1 EOL component(s), +1 for 2 server(s), +1 using external interfaces as the dependency proxy (10), +1 for custom code indication, and -1 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | APPLICABLE | The operating system (RHEL 7) is assessed as EOL, so patching or upgrading is recommended. | Prioritize OS remediation to restore vendor support and security patch eligibility. |
| Switch to ARM-based CPU | APPLICABLE | The application is already deployed on AWS and uses a portable stack, so ARM-based hosting is a credible optimization option. | Pilot ARM on portable workloads to validate performance and cost savings before broad adoption. |
| Applications Server replacement | APPLICABLE | The application uses Payara 4.0, which is a legacy-style middleware component worth evaluating for replacement. | Replace legacy middleware with a supported application platform or simplify the hosting stack. |
| Application Refactoring and De-coupling | APPLICABLE | The application is custom-built and integration-heavy, so decoupling and refactoring would likely improve modernization outcomes. | Refactor tightly coupled functionality to reduce change risk and improve modernization flexibility. |
| Switch DB Engine to open-source database solution | APPLICABLE | The application uses a proprietary database (SQL Server 2019), so an open-source alternative could reduce cost and lock-in. | Assess a move to an open-source database to reduce licensing costs and lock-in. |
| Update outdated components | APPLICABLE | The technology assessment found 1 EOL and 0 outdated component(s). | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Operating System Update | EUR 1,200.00 | EUR 500.00 | 25.00% |
| Switch to ARM-based CPU | EUR 6,000.00 | EUR 1,000.00 | -50.00% |
| Applications Server replacement | EUR 12,000.00 | EUR 12,000.00 | 200.00% |
| Application Refactoring and De-coupling | EUR 300,000.00 | EUR 150,000.00 | 50.00% |
| Switch DB Engine to open-source database solution | EUR 30,000.00 | EUR 15,000.00 | 50.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 349,200.00**  
Total annual savings: **EUR 178,500.00**
