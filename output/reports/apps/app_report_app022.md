# Application Report - ComplianceApp-022
Application app022 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app022 |
| Name | ComplianceApp-022 |
| Status | Production |
| Solution Type | Custom made |
| Deployment Type | AWS, On-premise |
| Business Criticality | Critical |
| Operating System | RHEL 7 |
| Programming Language | Scala 2.13 |
| Application Server | Payara 6.0 |
| Database Engine | PostgreSQL 14 |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | RHEL | 7 | EOL | Lifecycle rule matched for RHEL 7. |
| programming_language | Scala 2.13 | unknown | NO_KNOWLEDGE | Programming language or runtime version is not covered by the provided lifecycle rules. |
| application_server | Payara 6.0 | unknown | NO_KNOWLEDGE | Application server technology is not covered by the provided lifecycle rules. |
| database | PostgreSQL | 14 | CURRENT_VERSION | Lifecycle rule matched for PostgreSQL 14. |

Overall technology risk: **CRITICAL**.

## Complexity Assessment
Complexity score: **9** (High) — estimated effort **6-12 months**.

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
| Dependency Count | 12 |
| Dependency Adjustment | 2 |
| Custom Code | True |
| Custom Code Adjustment | 1 |
| Containerized | True |
| Containerization Adjustment | -1 |

Started from base score 3, applied +2 for Critical criticality, +1 for 1 EOL component(s), +1 for 2 server(s), +2 using external interfaces as the dependency proxy (12), +1 for custom code indication, and -1 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | APPLICABLE | The operating system (RHEL 7) is assessed as EOL, so patching or upgrading is recommended. | Prioritize OS remediation to restore vendor support and security patch eligibility. |
| Switch to ARM-based CPU | APPLICABLE | The application is already deployed on AWS, On-premise and uses a portable stack, so ARM-based hosting is a credible optimization option. | Pilot ARM on portable workloads to validate performance and cost savings before broad adoption. |
| Applications Server replacement | APPLICABLE | The application uses Payara 6.0, which is a legacy-style middleware component worth evaluating for replacement. | Replace legacy middleware with a supported application platform or simplify the hosting stack. |
| Application Refactoring and De-coupling | APPLICABLE | The application is custom-built and integration-heavy, so decoupling and refactoring would likely improve modernization outcomes. | Refactor tightly coupled functionality to reduce change risk and improve modernization flexibility. |
| Update outdated components | APPLICABLE | The technology assessment found 1 EOL and 0 outdated component(s). | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Operating System Update | EUR 1,800.00 | EUR 500.00 | -16.67% |
| Switch to ARM-based CPU | EUR 9,000.00 | EUR 1,000.00 | -66.67% |
| Applications Server replacement | EUR 18,000.00 | EUR 12,000.00 | 100.00% |
| Application Refactoring and De-coupling | EUR 450,000.00 | EUR 150,000.00 | 0.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 478,800.00**  
Total annual savings: **EUR 163,500.00**
