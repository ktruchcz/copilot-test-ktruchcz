# Application Report - FleetApp-021
Application app021 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app021 |
| Name | FleetApp-021 |
| Status | Production |
| Solution Type | Custom made |
| Deployment Type | On-Premise |
| Business Criticality | High |
| Operating System | Windows Server 2022 |
| Programming Language | C++ 17 |
| Application Server | Microsoft IIS 10.0 |
| Database Engine | Oracle 11g |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | Windows Server | 2022 | CURRENT_VERSION | Lifecycle rule matched for Windows Server 2022. |
| programming_language | C++ 17 | unknown | NO_KNOWLEDGE | Programming language or runtime version is not covered by the provided lifecycle rules. |
| application_server | Microsoft IIS 10.0 | unknown | NO_KNOWLEDGE | Application server technology is not covered by the provided lifecycle rules. |
| database | Oracle | unknown | NO_KNOWLEDGE | Oracle version is not covered by the provided lifecycle rules. |

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
| Dependency Count | 4 |
| Dependency Adjustment | 0 |
| Custom Code | True |
| Custom Code Adjustment | 1 |
| Containerized | False |
| Containerization Adjustment | 0 |

Started from base score 3, applied +1 for High criticality, +0 for 0 EOL component(s), +1 for 2 server(s), +0 using external interfaces as the dependency proxy (4), +1 for custom code indication, and +0 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Application Migration to Cloud Infrastructure (Lift & Shift) | APPLICABLE | The application is currently deployed as On-Premise, so lift-and-shift to cloud remains a valid option. | Evaluate lift-and-shift migration to reduce infrastructure management effort. |
| Application Containerization | APPLICABLE | The application is not containerized today, so containerization remains a relevant modernization option. | Containerize the workload to improve portability, release consistency, and scaling options. |
| Application Refactoring and De-coupling | PARTIALLY_FULFILLED | The application is custom-built, but the current data shows only moderate integration pressure for deeper refactoring. | Refactor tightly coupled functionality to reduce change risk and improve modernization flexibility. |
| Switch DB Engine to open-source database solution | APPLICABLE | The application uses a proprietary database (Oracle 11g), so an open-source alternative could reduce cost and lock-in. | Assess a move to an open-source database to reduce licensing costs and lock-in. |
| Update outdated components | PARTIALLY_FULFILLED | Known components are current, but some technologies could not be dated from the available application data. | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Application Migration to Cloud Infrastructure (Lift & Shift) | EUR 6,000.00 | EUR 3,000.00 | 50.00% |
| Application Containerization | EUR 120,000.00 | EUR 100,000.00 | 150.00% |
| Application Refactoring and De-coupling | EUR 300,000.00 | EUR 150,000.00 | 50.00% |
| Switch DB Engine to open-source database solution | EUR 30,000.00 | EUR 15,000.00 | 50.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 456,000.00**  
Total annual savings: **EUR 268,000.00**
