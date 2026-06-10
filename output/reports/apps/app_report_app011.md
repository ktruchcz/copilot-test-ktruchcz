# Application Report - RouteOptApp-011
Application app011 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app011 |
| Name | RouteOptApp-011 |
| Status | Production |
| Solution Type | Custom made |
| Deployment Type | AWS |
| Business Criticality | Medium |
| Operating System | CentOS 7 |
| Programming Language | Python 3.11 |
| Application Server | Glassfish 4.0 |
| Database Engine | PostgreSQL 14 |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | CentOS 7 | unknown | NO_KNOWLEDGE | Operating system version is not covered by the provided lifecycle rules. |
| programming_language | Python | 3.11 | CURRENT_VERSION | Lifecycle rule matched for Python 3.11. |
| application_server | Glassfish 4.0 | unknown | NO_KNOWLEDGE | Application server technology is not covered by the provided lifecycle rules. |
| database | PostgreSQL | 14 | CURRENT_VERSION | Lifecycle rule matched for PostgreSQL 14. |

Overall technology risk: **MEDIUM**.

## Complexity Assessment
Complexity score: **4** (Medium) — estimated effort **3-6 months**.

| Factor | Value |
| --- | --- |
| Base Score | 3 |
| Business Criticality | Medium |
| Criticality Adjustment | 0 |
| Eol Components | 0 |
| Eol Adjustment | 0 |
| Server Count | 1 |
| Server Adjustment | 0 |
| Dependency Proxy | external_interface_count |
| Dependency Count | 5 |
| Dependency Adjustment | 1 |
| Custom Code | True |
| Custom Code Adjustment | 1 |
| Containerized | True |
| Containerization Adjustment | -1 |

Started from base score 3, applied +0 for Medium criticality, +0 for 0 EOL component(s), +0 for 1 server(s), +1 using external interfaces as the dependency proxy (5), +1 for custom code indication, and -1 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Switch to standard Linux Operating System | PARTIALLY_FULFILLED | The workload already runs on Linux (CentOS 7), but not on the target standard Linux distributions highlighted in the rules. | Standardize the platform on supported Linux distributions where stack constraints allow. |
| Switch to ARM-based CPU | APPLICABLE | The application is already deployed on AWS and uses a portable stack, so ARM-based hosting is a credible optimization option. | Pilot ARM on portable workloads to validate performance and cost savings before broad adoption. |
| Applications Server replacement | APPLICABLE | The application uses Glassfish 4.0, which is a legacy-style middleware component worth evaluating for replacement. | Replace legacy middleware with a supported application platform or simplify the hosting stack. |
| Application Refactoring and De-coupling | PARTIALLY_FULFILLED | The application is custom-built, but the current data shows only moderate integration pressure for deeper refactoring. | Refactor tightly coupled functionality to reduce change risk and improve modernization flexibility. |
| Update outdated components | PARTIALLY_FULFILLED | Known components are current, but some technologies could not be dated from the available application data. | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Switch to standard Linux Operating System | EUR 240.00 | EUR 400.00 | 400.00% |
| Switch to ARM-based CPU | EUR 4,000.00 | EUR 1,000.00 | -25.00% |
| Applications Server replacement | EUR 8,000.00 | EUR 12,000.00 | 350.00% |
| Application Refactoring and De-coupling | EUR 200,000.00 | EUR 150,000.00 | 125.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 212,240.00**  
Total annual savings: **EUR 163,400.00**
