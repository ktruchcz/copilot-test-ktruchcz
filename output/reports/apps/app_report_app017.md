# Application Report - BackupApp-017
Application app017 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app017 |
| Name | BackupApp-017 |
| Status | Production |
| Solution Type | 3rd party software |
| Deployment Type | On-Premise |
| Business Criticality | High |
| Operating System | RHEL 7 |
| Programming Language | PowerShell |
| Application Server | Payara 5.0 |
| Database Engine | Oracle 12c |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | RHEL | 7 | EOL | Lifecycle rule matched for RHEL 7. |
| programming_language | PowerShell | unknown | NO_KNOWLEDGE | Programming language or runtime version is not covered by the provided lifecycle rules. |
| application_server | Payara 5.0 | unknown | NO_KNOWLEDGE | Application server technology is not covered by the provided lifecycle rules. |
| database | Oracle | 12c | EOL | Lifecycle rule matched for Oracle 12c. |

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
| Server Count | 2 |
| Server Adjustment | 1 |
| Dependency Proxy | external_interface_count |
| Dependency Count | 8 |
| Dependency Adjustment | 1 |
| Custom Code | False |
| Custom Code Adjustment | 0 |
| Containerized | False |
| Containerization Adjustment | 0 |

Started from base score 3, applied +1 for High criticality, +2 for 2 EOL component(s), +1 for 2 server(s), +1 using external interfaces as the dependency proxy (8), +0 for custom code indication, and +0 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | APPLICABLE | The operating system (RHEL 7) is assessed as EOL, so patching or upgrading is recommended. | Prioritize OS remediation to restore vendor support and security patch eligibility. |
| Applications Server replacement | APPLICABLE | The application uses Payara 5.0, which is a legacy-style middleware component worth evaluating for replacement. | Replace legacy middleware with a supported application platform or simplify the hosting stack. |
| Application Migration to Cloud Infrastructure (Lift & Shift) | APPLICABLE | The application is currently deployed as On-Premise, so lift-and-shift to cloud remains a valid option. | Evaluate lift-and-shift migration to reduce infrastructure management effort. |
| Application Containerization | APPLICABLE | The application is not containerized today, so containerization remains a relevant modernization option. | Containerize the workload to improve portability, release consistency, and scaling options. |
| Upgrade Legacy Databases | APPLICABLE | The database (Oracle 12c) is assessed as EOL, so an upgrade is justified. | Upgrade the database platform to remove lifecycle risk and improve supportability. |
| Update outdated components | APPLICABLE | The technology assessment found 2 EOL and 0 outdated component(s). | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Operating System Update | EUR 1,600.00 | EUR 500.00 | -6.25% |
| Applications Server replacement | EUR 16,000.00 | EUR 12,000.00 | 125.00% |
| Application Migration to Cloud Infrastructure (Lift & Shift) | EUR 8,000.00 | EUR 3,000.00 | 12.50% |
| Application Containerization | EUR 160,000.00 | EUR 100,000.00 | 87.50% |
| Upgrade Legacy Databases | EUR 16,000.00 | EUR 10,000.00 | 87.50% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 201,600.00**  
Total annual savings: **EUR 125,500.00**
