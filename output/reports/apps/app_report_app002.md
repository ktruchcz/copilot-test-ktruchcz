# Application Report - CRMApp-002
Application app002 assessment generated from the extracted portfolio dataset.

## App Overview
| Field | Value |
| --- | --- |
| App ID | app002 |
| Name | CRMApp-002 |
| Status | Production |
| Solution Type | 3rd party software |
| Deployment Type | AWS |
| Business Criticality | Medium |
| Operating System | RHEL 7 |
| Programming Language | Java 11 |
| Application Server | Websphere 7.0 |
| Database Engine | Amazon RDS MySQL |

## Technology Assessment
| Component Type | Name | Version | Status | Notes |
| --- | --- | --- | --- | --- |
| operating_system | RHEL | 7 | EOL | Lifecycle rule matched for RHEL 7. |
| programming_language | Java | 11 | OUTDATED | Lifecycle rule matched for Java 11. |
| application_server | WebSphere | 7.0 | NO_KNOWLEDGE | WebSphere version is not covered by the provided lifecycle rules. |
| database | MySQL | unknown | NO_KNOWLEDGE | MySQL is identified, but no supported version is present. |

Overall technology risk: **CRITICAL**.

## Complexity Assessment
Complexity score: **6** (Medium) — estimated effort **3-6 months**.

| Factor | Value |
| --- | --- |
| Base Score | 3 |
| Business Criticality | Medium |
| Criticality Adjustment | 0 |
| Eol Components | 1 |
| Eol Adjustment | 1 |
| Server Count | 2 |
| Server Adjustment | 1 |
| Dependency Proxy | external_interface_count |
| Dependency Count | 8 |
| Dependency Adjustment | 1 |
| Custom Code | False |
| Custom Code Adjustment | 0 |
| Containerized | False |
| Containerization Adjustment | 0 |

Started from base score 3, applied +0 for Medium criticality, +1 for 1 EOL component(s), +1 for 2 server(s), +1 using external interfaces as the dependency proxy (8), +0 for custom code indication, and +0 for containerization.

## Scenario Analysis
| Scenario | Status | Rationale | Recommendation |
| --- | --- | --- | --- |
| Operating System Update | APPLICABLE | The operating system (RHEL 7) is assessed as EOL, so patching or upgrading is recommended. | Prioritize OS remediation to restore vendor support and security patch eligibility. |
| Applications Server replacement | APPLICABLE | The application uses Websphere 7.0, which is a legacy-style middleware component worth evaluating for replacement. | Replace legacy middleware with a supported application platform or simplify the hosting stack. |
| Update outdated components | APPLICABLE | The technology assessment found 1 EOL and 1 outdated component(s). | Bundle outdated component upgrades into a coordinated remediation plan. |

## Business Case
| Scenario | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- |
| Operating System Update | EUR 1,200.00 | EUR 500.00 | 25.00% |
| Applications Server replacement | EUR 12,000.00 | EUR 12,000.00 | 200.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | n/a |

Total investment: **EUR 13,200.00**  
Total annual savings: **EUR 12,500.00**
