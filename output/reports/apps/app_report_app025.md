# Application Report - PortalApp-025
Application app025 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app025 |
| Name | PortalApp-025 |
| Status | Production |
| Solution Type | Custom made |
| Deployment Type | AWS |
| Business Criticality | Medium |
| Operating System | Windows Server 2019 |
| Programming Language | ASP.NET Core |
| Application Server | Microsoft IIS 10.0 |
| Database Engine | PostgreSQL 15 |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | Windows Server | 2019 | CURRENT_VERSION | Lifecycle rule matched for Windows Server 2019. |
| programming_language | .NET | unknown | NO_KNOWLEDGE | The application uses .NET, but no supported version was provided. |
| application_server | Microsoft IIS 10.0 | unknown | NO_KNOWLEDGE | Application server technology is not covered by the provided lifecycle rules. |
| database | PostgreSQL | 15 | CURRENT_VERSION | Lifecycle rule matched for PostgreSQL 15. |

Overall technology risk: **MEDIUM**.

## Complexity Assessment
Complexity score: **6** (Medium) — estimated effort **3-6 months**.

| Factor | Value |
| --- | --- |
| Base Score | 3 |
| Business Criticality | Medium |
| Criticality Adjustment | 0 |
| Eol Components | 0 |
| Eol Adjustment | 0 |
| Server Count | 2 |
| Server Adjustment | 1 |
| Dependency Proxy | external_interface_count |
| Dependency Count | 15 |
| Dependency Adjustment | 2 |
| Custom Code | True |
| Custom Code Adjustment | 1 |
| Containerized | True |
| Containerization Adjustment | -1 |

Started from base score 3, applied +0 for Medium criticality, +0 for 0 EOL component(s), +1 for 2 server(s), +2 using external interfaces as the dependency proxy (15), +1 for custom code indication, and -1 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Switch to ARM-based CPU | APPLICABLE | The application is already deployed on AWS and uses a portable stack, so ARM-based hosting is a credible optimization option. | Pilot ARM on portable workloads to validate performance and cost savings before broad adoption. |
| Application Refactoring and De-coupling | APPLICABLE | The application is custom-built and integration-heavy, so decoupling and refactoring would likely improve modernization outcomes. | Refactor tightly coupled functionality to reduce change risk and improve modernization flexibility. |
| Update outdated components | PARTIALLY_FULFILLED | Known components are current, but some technologies could not be dated from the available application data. | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Switch to ARM-based CPU | EUR 6,000.00 | EUR 1,000.00 | -50.00% |
| Application Refactoring and De-coupling | EUR 300,000.00 | EUR 150,000.00 | 50.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 306,000.00**  
Total annual savings: **EUR 151,000.00**
