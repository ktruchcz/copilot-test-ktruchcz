# Application Report: COBOL transform

**Application ID:** scenarioa-test-transform  
**Analysis date:** 2025-01-01

## Summary
COBOL transform is a production finance ERP application running on a fully outdated stack: AIX 7.2, COBOL-2014, and Oracle 19c. It is business-critical, handles confidential data, and has a high modernization complexity score of 8/10.

## Key Characteristics
- Solution type: Custom made
- Deployment: On-Premise
- Architecture: 1-Tier
- Users: 350
- External interfaces: 5
- Database: Oracle 19c, 1000 GB
- CI/CD: No
- Decommission target: 2027

## Technology Assessment
| Component | Status | Reason |
|---|---|---|
| AIX 7.2 | OUTDATED | Past standard support; only extended support remains. |
| COBOL-2014 | OUTDATED | Superseded standard with shrinking ecosystem. |
| Oracle 19c | OUTDATED | Past Premier Support and now in Extended Support. |

## Complexity
- **Score:** 8/10
- **Label:** High
- **Multiplier:** 1.8

Primary complexity drivers are the legacy COBOL/AIX stack, monolithic architecture, Oracle dependency, finance criticality, and lack of CI/CD.

## Scenario Assessment
| Scenario | Status | Interpretation |
|---|---|---|
| os_update_security_patch | APPLICABLE | Reduce platform risk. |
| switch_to_standard_linux_os | APPLICABLE | Strong replatform opportunity. |
| switch_to_arm_cpu | NOT_APPLICABLE | Platform mismatch. |
| application_server_replacement | NOT_APPLICABLE | No app server exists. |
| app_deployment_to_cloud | APPLICABLE | Technically valid but complex. |
| app_containerization | BLOCKED | Requires Linux migration and decomposition first. |
| app_refactor_decoupling | APPLICABLE | Monolith and zero-API posture justify refactoring. |
| upgrade_legacy_databases | APPLICABLE | Oracle support posture is aging. |
| switch_db_engine_open_source | APPLICABLE | PostgreSQL migration can reduce license cost. |
| update_outdated_components | APPLICABLE | Entire stack is outdated. |

## Business Case
| Scenario | Adjusted Cost | Yearly Savings | 3-Year ROI | 5-Year ROI |
|---|---:|---:|---:|---:|
| OS update | $1,800 | $500 | -16.7% | 38.9% |
| Switch to Linux | $540 | $400 | 122.2% | 270.4% |
| Cloud lift & shift | $9,000 | $3,000 | 0.0% | 66.7% |
| Refactor & decouple | $450,000 | $150,000 | 0.0% | 66.7% |
| Upgrade legacy DB | $18,000 | $10,000 | 66.7% | 177.8% |
| Switch DB to PostgreSQL | $45,000 | $15,000 | 0.0% | 66.7% |

**Total app business case:**
- Adjusted cost: **$524,340**
- Yearly savings: **$178,900**
- 3-year ROI: **2.4%**
- 5-year ROI: **70.6%**

## Recommendation
A phased modernization strategy is recommended: update risk-heavy infrastructure, migrate off AIX, modernize the database platform, then incrementally decouple the application architecture.
