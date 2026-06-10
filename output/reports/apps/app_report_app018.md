# Application Report - VendorApp-018
Application app018 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app018 |
| Name | VendorApp-018 |
| Status | Production |
| Solution Type | Custom made |
| Deployment Type | On-Premise |
| Business Criticality | Medium |
| Operating System | RHEL 7 |
| Programming Language | Java 8 |
| Application Server | Glassfish 4.5 |
| Database Engine | PostgreSQL 13 |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | RHEL | 7 | EOL | Lifecycle rule matched for RHEL 7. |
| programming_language | Java | 8 | EOL | Lifecycle rule matched for Java 8. |
| application_server | Glassfish 4.5 | unknown | NO_KNOWLEDGE | Application server technology is not covered by the provided lifecycle rules. |
| database | PostgreSQL | 13 | NO_KNOWLEDGE | PostgreSQL version is not covered by the provided lifecycle rules. |

Overall technology risk: **CRITICAL**.

## Complexity Assessment
Complexity score: **8** (High) — estimated effort **6-12 months**.

| Factor | Value |
| --- | --- |
| Base Score | 3 |
| Business Criticality | Medium |
| Criticality Adjustment | 0 |
| Eol Components | 2 |
| Eol Adjustment | 2 |
| Server Count | 2 |
| Server Adjustment | 1 |
| Dependency Proxy | external_interface_count |
| Dependency Count | 6 |
| Dependency Adjustment | 1 |
| Custom Code | True |
| Custom Code Adjustment | 1 |
| Containerized | False |
| Containerization Adjustment | 0 |

Started from base score 3, applied +0 for Medium criticality, +2 for 2 EOL component(s), +1 for 2 server(s), +1 using external interfaces as the dependency proxy (6), +1 for custom code indication, and +0 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | APPLICABLE | The operating system (RHEL 7) is assessed as EOL, so patching or upgrading is recommended. | Prioritize OS remediation to restore vendor support and security patch eligibility. |
| Applications Server replacement | APPLICABLE | The application uses Glassfish 4.5, which is a legacy-style middleware component worth evaluating for replacement. | Replace legacy middleware with a supported application platform or simplify the hosting stack. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | APPLICABLE | The application is currently deployed as On-Premise, so lift-and-shift to cloud remains a valid option. | Evaluate lift-and-shift migration to reduce infrastructure management effort. |
| Application Containerization | APPLICABLE | The application is not containerized today, so containerization remains a relevant modernization option. | Containerize the workload to improve portability, release consistency, and scaling options. |
| Application Refactoring and De-coupling | APPLICABLE | The application is custom-built and integration-heavy, so decoupling and refactoring would likely improve modernization outcomes. | Refactor tightly coupled functionality to reduce change risk and improve modernization flexibility. |
| Update outdated components | APPLICABLE | The technology assessment found 2 EOL and 0 outdated component(s). | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Operating System Update | EUR 1,600.00 | EUR 500.00 | -6.25% |
| Applications Server replacement | EUR 16,000.00 | EUR 12,000.00 | 125.00% |
| Application Migration to Cloud Infrastructure (Lift & Shift) | EUR 8,000.00 | EUR 3,000.00 | 12.50% |
| Application Containerization | EUR 160,000.00 | EUR 100,000.00 | 87.50% |
| Application Refactoring and De-coupling | EUR 400,000.00 | EUR 150,000.00 | 12.50% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 585,600.00**  
Total annual savings: **EUR 265,500.00**
