# Application Report - ERPApp-001
Application app001 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app001 |
| Name | ERPApp-001 |
| Status | Production |
| Solution Type | Custom made |
| Deployment Type | On-Premise |
| Business Criticality | High |
| Operating System | AIX 7.2 |
| Programming Language | COBOL-2014 |
| Application Server |  |
| Database Engine | Oracle 19c |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | AIX 7.2 | unknown | NO_KNOWLEDGE | Operating system version is not covered by the provided lifecycle rules. |
| programming_language | COBOL-2014 | unknown | NO_KNOWLEDGE | Programming language or runtime version is not covered by the provided lifecycle rules. |
| database | Oracle | 19c | CURRENT_VERSION | Lifecycle rule matched for Oracle 19c. |

Overall technology risk: **MEDIUM**.

## Complexity Assessment
Complexity score: **7** (High) — estimated effort **6-12 months**.

| Factor | Value |
| --- | --- |
| Base Score | 3 |
| Business Criticality | High |
| Criticality Adjustment | 1 |
| Eol Components | 0 |
| Eol Adjustment | 0 |
| Server Count | 2 |
| Server Adjustment | 1 |
| Dependency Proxy | external_interface_count |
| Dependency Count | 5 |
| Dependency Adjustment | 1 |
| Custom Code | True |
| Custom Code Adjustment | 1 |
| Containerized | False |
| Containerization Adjustment | 0 |

Started from base score 3, applied +1 for High criticality, +0 for 0 EOL component(s), +1 for 2 server(s), +1 using external interfaces as the dependency proxy (5), +1 for custom code indication, and +0 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Switch to standard Linux Operating System | APPLICABLE | The application runs on AIX 7.2, so moving to standard Linux is a viable modernization path. | Standardize the platform on supported Linux distributions where stack constraints allow. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | APPLICABLE | The application is currently deployed as On-Premise, so lift-and-shift to cloud remains a valid option. | Evaluate lift-and-shift migration to reduce infrastructure management effort. |
| Application Refactoring and De-coupling | APPLICABLE | The application is custom-built and integration-heavy, so decoupling and refactoring would likely improve modernization outcomes. | Refactor tightly coupled functionality to reduce change risk and improve modernization flexibility. |
| Switch DB Engine to open-source database solution | APPLICABLE | The application uses a proprietary database (Oracle 19c), so an open-source alternative could reduce cost and lock-in. | Assess a move to an open-source database to reduce licensing costs and lock-in. |
| Update outdated components | PARTIALLY_FULFILLED | Known components are current, but some technologies could not be dated from the available application data. | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Switch to standard Linux Operating System | EUR 420.00 | EUR 400.00 | 185.71% |
| Application Migration to Cloud Infrastructure (Lift & Shift) | EUR 7,000.00 | EUR 3,000.00 | 28.57% |
| Application Refactoring and De-coupling | EUR 350,000.00 | EUR 150,000.00 | 28.57% |
| Switch DB Engine to open-source database solution | EUR 35,000.00 | EUR 15,000.00 | 28.57% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 392,420.00**  
Total annual savings: **EUR 168,400.00**
