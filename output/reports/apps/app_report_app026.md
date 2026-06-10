# Application Report - LegacyFinApp-026
Application app026 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app026 |
| Name | LegacyFinApp-026 |
| Status | Production |
| Solution Type | Custom made |
| Deployment Type | On-Premise |
| Business Criticality | Critical |
| Operating System | AIX 7.2 |
| Programming Language | FORTRAN 2018 |
| Application Server |  |
| Database Engine | DB2 |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | AIX 7.2 | unknown | NO_KNOWLEDGE | Operating system version is not covered by the provided lifecycle rules. |
| programming_language | FORTRAN 2018 | unknown | NO_KNOWLEDGE | Programming language or runtime version is not covered by the provided lifecycle rules. |
| database | DB2 | unknown | NO_KNOWLEDGE | Database engine is not covered by the provided lifecycle rules. |

Overall technology risk: **MEDIUM**.

## Complexity Assessment
Complexity score: **6** (Medium) — estimated effort **3-6 months**.

| Factor | Value |
| --- | --- |
| Base Score | 3 |
| Business Criticality | Critical |
| Criticality Adjustment | 2 |
| Eol Components | 0 |
| Eol Adjustment | 0 |
| Server Count | 1 |
| Server Adjustment | 0 |
| Dependency Proxy | external_interface_count |
| Dependency Count | 1 |
| Dependency Adjustment | 0 |
| Custom Code | True |
| Custom Code Adjustment | 1 |
| Containerized | False |
| Containerization Adjustment | 0 |

Started from base score 3, applied +2 for Critical criticality, +0 for 0 EOL component(s), +0 for 1 server(s), +0 using external interfaces as the dependency proxy (1), +1 for custom code indication, and +0 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Switch to standard Linux Operating System | APPLICABLE | The application runs on AIX 7.2, so moving to standard Linux is a viable modernization path. | Standardize the platform on supported Linux distributions where stack constraints allow. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | APPLICABLE | The application is currently deployed as On-Premise, so lift-and-shift to cloud remains a valid option. | Evaluate lift-and-shift migration to reduce infrastructure management effort. |
| Application Refactoring and De-coupling | PARTIALLY_FULFILLED | The application is custom-built, but the current data shows only moderate integration pressure for deeper refactoring. | Refactor tightly coupled functionality to reduce change risk and improve modernization flexibility. |
| Switch DB Engine to open-source database solution | APPLICABLE | The application uses a proprietary database (DB2), so an open-source alternative could reduce cost and lock-in. | Assess a move to an open-source database to reduce licensing costs and lock-in. |
| Update outdated components | PARTIALLY_FULFILLED | Known components are current, but some technologies could not be dated from the available application data. | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Switch to standard Linux Operating System | EUR 360.00 | EUR 400.00 | 233.33% |
| Application Migration to Cloud Infrastructure (Lift & Shift) | EUR 6,000.00 | EUR 3,000.00 | 50.00% |
| Application Refactoring and De-coupling | EUR 300,000.00 | EUR 150,000.00 | 50.00% |
| Switch DB Engine to open-source database solution | EUR 30,000.00 | EUR 15,000.00 | 50.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 336,360.00**  
Total annual savings: **EUR 168,400.00**
