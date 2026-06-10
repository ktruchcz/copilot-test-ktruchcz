# Application Report - ChatbotApp-023

## App overview
| Field | Value |
| --- | --- |
| Application ID | app023 |
| Name | ChatbotApp-023 |
| Description | AI-powered chatbot system for handling customer inquiries and providing automated support |
| Status | Production |
| Criticality | Medium |
| Deployment | AWS |
| Solution type | Open Source |

## Technology assessment summary
| Dimension | Family | Version | Status | Reason |
| --- | --- | --- | --- | --- |
| os | RHEL | 8 | CURRENT_VERSION | RHEL 8 remains in vendor support until May 2029. |
| database | MongoDB | unknown | NO_KNOWLEDGE | The inventory lists MongoDB but does not provide a version, so lifecycle support cannot be assessed. |
| language | Node.js | 18 | OUTDATED | Node.js 18 is behind current support baselines. |
| framework | Node.js | 18 | OUTDATED | Node.js 18 is still recognizable but behind current long-term support releases. |
| application_server | Tomcat | 7.4 | EOL | Tomcat 7.x is end-of-life. |

## Complexity score and label
- Complexity score: **4**
- Complexity label: **Medium**
- Indicative migration effort: **3-6 months**

Scoring factors:
- Base score of 3 applied.
- Business criticality 'Medium' adjusted score by +0.
- 1 EOL component(s) contributed +1 points (capped at +3).
- Server count of 1 contributed +0 points.
- Dependency count of 8 using external_interface_count proxy contributed +1 points.
- Solution type 'Open Source' contributed +0 points for custom code.
- Containerized='Yes' adjusted score by -1.

## Applicable scenarios with recommendations
| Scenario | Priority | Rationale | Recommendation |
| --- | --- | --- | --- |
| Switch to ARM-based CPU | Medium | The application already runs in cloud and uses a portable stack, so ARM-based infrastructure is a viable optimization path. | Adopt ARM-based CPU infrastructure for better energy efficiency and cost savings. |
| Applications Server replacement | Medium | The application server Apache Tomcat. 7.4 is assessed as EOL. | Modernize application server infrastructure through one of the following approaches: migrate from commercial to open-source solutions to reduce licensing costs, transition to Platform-as-a-Service (PaaS) managed services for simplified operations, or replace legacy application server technology with modern alternatives to improve performance and reduce overall costs. |
| Update outdated components | High | The technology assessment found 3 component(s) that are EOL or outdated. | Rewrite or Refactor or Replace application for better security, agility and maintainability. |

## Business case for top scenarios
| Scenario | Base Cost | Adjusted Cost | Annual Savings | 3-Year ROI |
| --- | --- | --- | --- | --- |
| Applications Server replacement | EUR 10,000.00 | EUR 8,000.00 | EUR 12,000.00 | 350.00% |
| Switch to ARM-based CPU | EUR 5,000.00 | EUR 4,000.00 | EUR 1,000.00 | -25.00% |
| Update outdated components | EUR 0.00 | EUR 0.00 | EUR 0.00 | n/a |
