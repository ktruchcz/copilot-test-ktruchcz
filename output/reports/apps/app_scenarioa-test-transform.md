# Application Report: COBOL transform

**Application ID:** scenarioa-test-transform  
**Analysis date:** 2026-07-02

## Summary
COBOL transform is a production finance ERP platform supporting accounting, budgeting, and financial planning. It remains in scope for modernization, but the 2027 decommission target materially changes investment priorities: urgent platform and database risk reduction remain justified, while large-scale refactoring does not.

## Key Characteristics
| Attribute | Value |
|---|---|
| Solution type | Custom made |
| Business criticality | High |
| Application status | Production |
| Deployment type | On-Premise |
| Business unit | Finance |
| Data classification | Confidential |
| Architecture | 1-Tier |
| Containerized | No |
| Users | 350 |
| External interfaces | 5 |
| API endpoints | 0 |
| Operating system | AIX 7.2 |
| Programming language | COBOL-2014 |
| Database | Oracle 19c |
| Database size | 1000 GB |
| CI/CD present | No |
| Servers | sv01, sv02 |
| Planned decommission | 2027 |

## Technology Assessment
| Component | Status | Assessment |
|---|---|---|
| AIX 7.2 | **OUTDATED** | Standard support ended in April 2023; Extended Support runs to April 2028. |
| COBOL-2014 | **OUTDATED** | Superseded by COBOL 2023 and increasingly constrained by talent scarcity. |
| Oracle 19c | **OUTDATED** | Premier Support ended in January 2024; Extended Support ends in January 2027, creating near-term urgency. |

## Complexity
- **Score:** 8/10
- **Label:** High
- **Multiplier:** 1.8

| Factor | Score | Rationale |
|---|---:|---|
| technology_age | 2.0 | Legacy AIX and COBOL stack drives very high platform modernization effort. |
| eol_outdated_components | 1.5 | All assessed components are outdated. |
| business_criticality | 1.5 | Finance-critical workload and confidential data increase delivery risk. |
| database_complexity | 1.0 | 1TB Oracle estate and license dependency complicate migration. |
| architecture | 1.0 | 1-Tier monolith with no CI/CD increases change risk. |
| external_interfaces | 1.0 | Five integrations require careful regression coordination. |
| server_count | 0.5 | Two server instances create moderate infrastructure scope. |
| decommission_timeline | 0.5 | 2027 retirement compresses the economically viable window. |

## Scenario Applicability
| Scenario | Status | Reasoning |
|---|---|---|
| os_update_security_patch | APPLICABLE | AIX 7.2 is beyond standard support and should be addressed to reduce security and support risk. |
| switch_to_standard_linux_os | APPLICABLE | AIX is a proprietary Unix platform and a clear Linux replatform candidate. |
| switch_to_arm_cpu | NOT_APPLICABLE | IBM POWER/AIX architecture and proprietary runtime do not fit the ARM migration path. |
| application_server_replacement | NOT_APPLICABLE | No application server layer exists in the current 1-Tier design. |
| app_deployment_to_cloud | APPLICABLE | On-premise deployment makes lift-and-shift feasible, though still complex. |
| app_containerization | BLOCKED | Linux migration and decomposition are prerequisites. |
| app_refactor_decoupling | BLOCKED | Planned decommission in 2027 makes a large refactoring investment unjustified. |
| upgrade_legacy_databases | APPLICABLE | Oracle 19c Extended Support ends in January 2027, creating urgent action needs. |
| switch_db_engine_open_source | APPLICABLE | Oracle licensing cost and custom code flexibility support PostgreSQL migration analysis. |
| update_outdated_components | APPLICABLE | The full stack is outdated and warrants targeted modernization. |

## Business Case
| Scenario | Adjusted Cost | Yearly Savings | 3-Year ROI | 5-Year ROI |
|---|---:|---:|---:|---:|
| Operating System Update | $1,800 | $500 | -16.7% | 38.9% |
| Switch to standard Linux Operating System | $540 | $400 | 122.2% | 270.4% |
| Application Migration to Cloud Infrastructure (Lift & Shift) | $9,000 | $3,000 | 0.0% | 66.7% |
| Upgrade Legacy Databases | $18,000 | $10,000 | 66.7% | 177.8% |
| Switch DB Engine to open-source database solution | $45,000 | $15,000 | 0.0% | 66.7% |

**Excluded from totals:**
- `app_containerization` and `app_refactor_decoupling` are **BLOCKED**.
- `update_outdated_components` has no finance model.

**Total app business case:**
- Adjusted cost: **$74,340**
- Yearly savings: **$28,900**
- 3-year total savings: **$86,700**
- 3-year ROI: **16.6%**
- 5-year total savings: **$144,500**
- 5-year ROI: **94.4%**

## Recommendation
Prioritize a pragmatic, short-horizon roadmap: reduce AIX exposure, make an urgent Oracle 19c decision before January 2027, and evaluate Linux/cloud landing zones. Avoid heavy de-coupling work because the planned 2027 decommission materially limits the payback window.
