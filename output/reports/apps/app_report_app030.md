# Application Report - APIGatewayApp-030
Application app030 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app030 |
| Name | APIGatewayApp-030 |
| Status | Production |
| Solution Type | Open Source |
| Deployment Type | AWS |
| Business Criticality | High |
| Operating System | RHEL 8 |
| Programming Language | Go 1.19 |
| Application Server | Glassfish 3.0 |
| Database Engine | MySQL 5.7 |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | RHEL | 8 | CURRENT_VERSION | Lifecycle rule matched for RHEL 8. |
| programming_language | Go 1.19 | unknown | NO_KNOWLEDGE | Programming language or runtime version is not covered by the provided lifecycle rules. |
| application_server | Glassfish 3.0 | unknown | NO_KNOWLEDGE | Application server technology is not covered by the provided lifecycle rules. |
| database | MySQL | 5.7 | EOL | Lifecycle rule matched for MySQL 5.7. |

Overall technology risk: **CRITICAL**.

## Complexity Assessment
Complexity score: **7** (High) — estimated effort **6-12 months**.

| Factor | Value |
| --- | --- |
| Base Score | 3 |
| Business Criticality | High |
| Criticality Adjustment | 1 |
| Eol Components | 1 |
| Eol Adjustment | 1 |
| Server Count | 2 |
| Server Adjustment | 1 |
| Dependency Proxy | external_interface_count |
| Dependency Count | 30 |
| Dependency Adjustment | 2 |
| Custom Code | False |
| Custom Code Adjustment | 0 |
| Containerized | True |
| Containerization Adjustment | -1 |

Started from base score 3, applied +1 for High criticality, +1 for 1 EOL component(s), +1 for 2 server(s), +2 using external interfaces as the dependency proxy (30), +0 for custom code indication, and -1 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Switch to ARM-based CPU | APPLICABLE | The application is already deployed on AWS and uses a portable stack, so ARM-based hosting is a credible optimization option. | Pilot ARM on portable workloads to validate performance and cost savings before broad adoption. |
| Applications Server replacement | APPLICABLE | The application uses Glassfish 3.0, which is a legacy-style middleware component worth evaluating for replacement. | Replace legacy middleware with a supported application platform or simplify the hosting stack. |
| Upgrade Legacy Databases | APPLICABLE | The database (MySQL 5.7) is assessed as EOL, so an upgrade is justified. | Upgrade the database platform to remove lifecycle risk and improve supportability. |
| Update outdated components | APPLICABLE | The technology assessment found 1 EOL and 0 outdated component(s). | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Switch to ARM-based CPU | EUR 7,000.00 | EUR 1,000.00 | -57.14% |
| Applications Server replacement | EUR 14,000.00 | EUR 12,000.00 | 157.14% |
| Upgrade Legacy Databases | EUR 14,000.00 | EUR 10,000.00 | 114.29% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 35,000.00**  
Total annual savings: **EUR 23,000.00**
