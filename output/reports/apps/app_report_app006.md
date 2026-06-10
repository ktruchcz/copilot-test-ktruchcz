# Application Report - SupportApp-006
Application app006 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app006 |
| Name | SupportApp-006 |
| Status | Production |
| Solution Type | 3rd party software |
| Deployment Type | AWS |
| Business Criticality | Medium |
| Operating System | Debian 6 |
| Programming Language | Java 11 |
| Application Server | Glassfish 5.0 |
| Database Engine | PostgreSQL 13 |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | Debian 6 | unknown | NO_KNOWLEDGE | Operating system version is not covered by the provided lifecycle rules. |
| programming_language | Java | 11 | OUTDATED | Lifecycle rule matched for Java 11. |
| application_server | Glassfish 5.0 | unknown | NO_KNOWLEDGE | Application server technology is not covered by the provided lifecycle rules. |
| database | PostgreSQL | 13 | NO_KNOWLEDGE | PostgreSQL version is not covered by the provided lifecycle rules. |

Overall technology risk: **HIGH**.

## Complexity Assessment
Complexity score: **3** (Low) — estimated effort **1-2 months**.

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
| Dependency Count | 4 |
| Dependency Adjustment | 0 |
| Custom Code | False |
| Custom Code Adjustment | 0 |
| Containerized | False |
| Containerization Adjustment | 0 |

Started from base score 3, applied +0 for Medium criticality, +0 for 0 EOL component(s), +0 for 1 server(s), +0 using external interfaces as the dependency proxy (4), +0 for custom code indication, and +0 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Switch to standard Linux Operating System | PARTIALLY_FULFILLED | The workload already runs on Linux (Debian 6), but not on the target standard Linux distributions highlighted in the rules. | Standardize the platform on supported Linux distributions where stack constraints allow. |
| Applications Server replacement | APPLICABLE | The application uses Glassfish 5.0, which is a legacy-style middleware component worth evaluating for replacement. | Replace legacy middleware with a supported application platform or simplify the hosting stack. |
| Update outdated components | APPLICABLE | The technology assessment found 0 EOL and 1 outdated component(s). | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Switch to standard Linux Operating System | EUR 180.00 | EUR 400.00 | 566.67% |
| Applications Server replacement | EUR 6,000.00 | EUR 12,000.00 | 500.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 6,180.00**  
Total annual savings: **EUR 12,400.00**
