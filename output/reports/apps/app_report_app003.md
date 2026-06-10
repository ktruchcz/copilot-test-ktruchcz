# Application Report - AnalyticsApp-003
Application app003 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app003 |
| Name | AnalyticsApp-003 |
| Status | Production |
| Solution Type | Open Source |
| Deployment Type | AWS |
| Business Criticality | Low |
| Operating System | RHEL 7 |
| Programming Language | Python 3.9 |
| Application Server | Apache Tomcat 6.1 |
| Database Engine | PostgreSQL 13 |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | RHEL | 7 | EOL | Lifecycle rule matched for RHEL 7. |
| programming_language | Python | 3.9 | OUTDATED | Lifecycle rule matched for Python 3.9. |
| application_server | Tomcat | 6.1 | NO_KNOWLEDGE | Tomcat version is not covered by the provided lifecycle rules. |
| database | PostgreSQL | 13 | NO_KNOWLEDGE | PostgreSQL version is not covered by the provided lifecycle rules. |

Overall technology risk: **CRITICAL**.

## Complexity Assessment
Complexity score: **2** (Low) — estimated effort **1-2 months**.

| Factor | Value |
| --- | --- |
| Base Score | 3 |
| Business Criticality | Low |
| Criticality Adjustment | -1 |
| Eol Components | 1 |
| Eol Adjustment | 1 |
| Server Count | 1 |
| Server Adjustment | 0 |
| Dependency Proxy | external_interface_count |
| Dependency Count | 3 |
| Dependency Adjustment | 0 |
| Custom Code | False |
| Custom Code Adjustment | 0 |
| Containerized | True |
| Containerization Adjustment | -1 |

Started from base score 3, applied -1 for Low criticality, +1 for 1 EOL component(s), +0 for 1 server(s), +0 using external interfaces as the dependency proxy (3), +0 for custom code indication, and -1 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | APPLICABLE | The operating system (RHEL 7) is assessed as EOL, so patching or upgrading is recommended. | Prioritize OS remediation to restore vendor support and security patch eligibility. |
| Switch to ARM-based CPU | APPLICABLE | The application is already deployed on AWS and uses a portable stack, so ARM-based hosting is a credible optimization option. | Pilot ARM on portable workloads to validate performance and cost savings before broad adoption. |
| Applications Server replacement | APPLICABLE | The application uses Apache Tomcat 6.1, which is a legacy-style middleware component worth evaluating for replacement. | Replace legacy middleware with a supported application platform or simplify the hosting stack. |
| Update outdated components | APPLICABLE | The technology assessment found 1 EOL and 1 outdated component(s). | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Operating System Update | EUR 400.00 | EUR 500.00 | 275.00% |
| Switch to ARM-based CPU | EUR 2,000.00 | EUR 1,000.00 | 50.00% |
| Applications Server replacement | EUR 4,000.00 | EUR 12,000.00 | 800.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 6,400.00**  
Total annual savings: **EUR 13,500.00**
