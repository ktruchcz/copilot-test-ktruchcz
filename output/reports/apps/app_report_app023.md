# Application Report - ChatbotApp-023
Application app023 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app023 |
| Name | ChatbotApp-023 |
| Status | Production |
| Solution Type | Open Source |
| Deployment Type | AWS |
| Business Criticality | Medium |
| Operating System | RHEL 8 |
| Programming Language | Node.js 18 |
| Application Server | Apache Tomcat. 7.4 |
| Database Engine | MongoDB |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | RHEL | 8 | CURRENT_VERSION | Lifecycle rule matched for RHEL 8. |
| programming_language | Node | 18 | OUTDATED | Lifecycle rule matched for Node 18. |
| application_server | Tomcat | 7.4 | NO_KNOWLEDGE | Tomcat version is not covered by the provided lifecycle rules. |
| database | MongoDB | unknown | NO_KNOWLEDGE | Database engine is not covered by the provided lifecycle rules. |

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
| Dependency Count | 8 |
| Dependency Adjustment | 1 |
| Custom Code | False |
| Custom Code Adjustment | 0 |
| Containerized | True |
| Containerization Adjustment | -1 |

Started from base score 3, applied +0 for Medium criticality, +0 for 0 EOL component(s), +0 for 1 server(s), +1 using external interfaces as the dependency proxy (8), +0 for custom code indication, and -1 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Switch to ARM-based CPU | APPLICABLE | The application is already deployed on AWS and uses a portable stack, so ARM-based hosting is a credible optimization option. | Pilot ARM on portable workloads to validate performance and cost savings before broad adoption. |
| Applications Server replacement | APPLICABLE | The application uses Apache Tomcat. 7.4, which is a legacy-style middleware component worth evaluating for replacement. | Replace legacy middleware with a supported application platform or simplify the hosting stack. |
| Update outdated components | APPLICABLE | The technology assessment found 0 EOL and 1 outdated component(s). | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Switch to ARM-based CPU | EUR 3,000.00 | EUR 1,000.00 | 0.00% |
| Applications Server replacement | EUR 6,000.00 | EUR 12,000.00 | 500.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 9,000.00**  
Total annual savings: **EUR 13,000.00**
