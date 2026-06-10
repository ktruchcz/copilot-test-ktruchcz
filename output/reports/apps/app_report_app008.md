# Application Report - InventoryApp-008
Application app008 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app008 |
| Name | InventoryApp-008 |
| Status | Production |
| Solution Type | Custom made |
| Deployment Type | On-Premise |
| Business Criticality | High |
| Operating System | AIX 6 |
| Programming Language | COBOL-2014 |
| Application Server | Oracle Weblogic 8.0 |
| Database Engine | SQL Server 2019 |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | AIX 6 | unknown | NO_KNOWLEDGE | Operating system version is not covered by the provided lifecycle rules. |
| programming_language | COBOL-2014 | unknown | NO_KNOWLEDGE | Programming language or runtime version is not covered by the provided lifecycle rules. |
| application_server | WebLogic | unknown | NO_KNOWLEDGE | WebLogic version is not covered by the provided lifecycle rules. |
| database | SQL Server | 2019 | CURRENT_VERSION | Lifecycle rule matched for SQL Server 2019. |

Overall technology risk: **MEDIUM**.

## Complexity Assessment
Complexity score: **6** (Medium) — estimated effort **3-6 months**.

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
| Dependency Count | 2 |
| Dependency Adjustment | 0 |
| Custom Code | True |
| Custom Code Adjustment | 1 |
| Containerized | False |
| Containerization Adjustment | 0 |

Started from base score 3, applied +1 for High criticality, +0 for 0 EOL component(s), +1 for 2 server(s), +0 using external interfaces as the dependency proxy (2), +1 for custom code indication, and +0 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Switch to standard Linux Operating System | APPLICABLE | The application runs on AIX 6, so moving to standard Linux is a viable modernization path. | Standardize the platform on supported Linux distributions where stack constraints allow. |
| Applications Server replacement | APPLICABLE | The application uses Oracle Weblogic 8.0, which is a legacy-style middleware component worth evaluating for replacement. | Replace legacy middleware with a supported application platform or simplify the hosting stack. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | APPLICABLE | The application is currently deployed as On-Premise, so lift-and-shift to cloud remains a valid option. | Evaluate lift-and-shift migration to reduce infrastructure management effort. |
| Application Refactoring and De-coupling | PARTIALLY_FULFILLED | The application is custom-built, but the current data shows only moderate integration pressure for deeper refactoring. | Refactor tightly coupled functionality to reduce change risk and improve modernization flexibility. |
| Switch DB Engine to open-source database solution | APPLICABLE | The application uses a proprietary database (SQL Server 2019), so an open-source alternative could reduce cost and lock-in. | Assess a move to an open-source database to reduce licensing costs and lock-in. |
| Update outdated components | PARTIALLY_FULFILLED | Known components are current, but some technologies could not be dated from the available application data. | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Switch to standard Linux Operating System | EUR 360.00 | EUR 400.00 | 233.33% |
| Applications Server replacement | EUR 12,000.00 | EUR 12,000.00 | 200.00% |
| Application Migration to Cloud Infrastructure (Lift & Shift) | EUR 6,000.00 | EUR 3,000.00 | 50.00% |
| Application Refactoring and De-coupling | EUR 300,000.00 | EUR 150,000.00 | 50.00% |
| Switch DB Engine to open-source database solution | EUR 30,000.00 | EUR 15,000.00 | 50.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 348,360.00**  
Total annual savings: **EUR 180,400.00**
