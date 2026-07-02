# Portfolio Modernization Assessment

## Executive Summary
- Total applications: 30
- In scope: 26
- Out of scope: 4
- Total migration cost: $10,152,870
- Total yearly savings: $5,730,700
- Three-year ROI: 69.3%
- Payback period: 1.77 years

### Key Findings
- 19 in-scope applications contain at least one EOL technology component.
- 23 applications can still move to managed database services.
- 16 applications remain strong candidates for containerization.
- Portfolio investment is $10,152,870 with payback in about 1.77 years.

## Technology Risk Overview
- EOL components: 31
- Outdated components: 28
- Current components: 43
- No knowledge / missing version components: 2

| Risk Level | Applications |
|---|---:|
| High | 19 |
| Medium | 6 |
| Low | 1 |

## Top Modernization Opportunities
| Scenario | Applicable Apps | Aggregate Cost | Aggregate Yearly Savings | 3-Year ROI |
|---|---:|---:|---:|---:|
| Switch to Managed Database | 23 | $147,000 | $230,000 | 369.4% |
| Managed ARM Database | 23 | $147,000 | $115,000 | 134.7% |
| Application Refactoring and De-coupling | 21 | $6,675,000 | $3,150,000 | 41.6% |
| Switch to ARM-based CPU | 18 | $111,000 | $18,000 | -51.4% |
| Switch Database Engine to PostgreSQL | 17 | $547,500 | $255,000 | 39.7% |
| Application Containerization | 16 | $2,070,000 | $1,600,000 | 131.9% |

## Per-Application Summary Table
| App ID | Application | Technology Risk | Complexity | Applicable Scenarios | Migration Cost | Yearly Savings | 3-Year ROI |
|---|---|---|---|---:|---:|---:|---:|
| app001 | ERPApp-001 | Medium | Medium (6) | 7 | $468,360 | $283,400 | 81.5% |
| app002 | CRMApp-002 | High | Medium (6) | 5 | $169,200 | $128,500 | 127.8% |
| app003 | AnalyticsApp-003 | High | Medium (4) | 7 | $343,200 | $188,500 | 64.8% |
| app004 | HRApp-004 | High | Medium (6) | 9 | $367,560 | $196,900 | 60.7% |
| app006 | SupportApp-006 | High | Medium (5) | 7 | $163,200 | $138,500 | 154.6% |
| app008 | InventoryApp-008 | High | Medium (6) | 9 | $481,560 | $295,900 | 84.3% |
| app010 | PayrollApp-010 | High | Medium (4) | 6 | $168,360 | $131,400 | 134.1% |
| app011 | RouteOptApp-011 | High | Medium (4) | 7 | $343,200 | $188,500 | 64.8% |
| app012 | IoTSensorApp-012 | Medium | Medium (6) | 6 | $330,360 | $176,400 | 60.2% |
| app013 | SecurityApp-013 | High | High (7) | 8 | $601,500 | $295,500 | 47.4% |
| app014 | DocumentApp-014 | Medium | Medium (5) | 7 | $468,360 | $281,400 | 80.2% |
| app015 | ReportingApp-015 | Medium | Medium (4) | 4 | $426,360 | $251,400 | 76.9% |
| app016 | MobileApp-016 | High | High (7) | 7 | $451,500 | $193,500 | 28.6% |
| app017 | BackupApp-017 | High | High (8) | 8 | $241,500 | $155,500 | 93.2% |
| app018 | VendorApp-018 | High | High (7) | 8 | $579,000 | $290,500 | 50.5% |
| app019 | QualityApp-019 | High | Medium (6) | 8 | $486,000 | $296,000 | 82.7% |
| app020 | TrainingApp-020 | High | Medium (6) | 10 | $493,560 | $303,900 | 84.7% |
| app021 | FleetApp-021 | High | Medium (6) | 8 | $480,360 | $293,400 | 83.2% |
| app022 | ComplianceApp-022 | High | Medium (6) | 7 | $337,200 | $179,500 | 59.7% |
| app023 | ChatbotApp-023 | High | Medium (6) | 3 | $318,000 | $163,000 | 53.8% |
| app024 | AuditApp-024 | High | High (7) | 8 | $600,450 | $293,400 | 46.6% |
| app025 | PortalApp-025 | Medium | Medium (5) | 5 | $318,360 | $166,400 | 56.8% |
| app026 | LegacyFinApp-026 | Medium | Medium (6) | 8 | $480,360 | $293,400 | 83.2% |
| app027 | DataWarehouseApp-027 | High | High (8) | 9 | $609,000 | $296,500 | 46.1% |
| app028 | NotificationApp-028 | Low | Medium (5) | 5 | $48,360 | $31,400 | 94.8% |
| app030 | APIGatewayApp-030 | High | Medium (6) | 8 | $378,000 | $218,000 | 73.0% |

## Business Case Summary
- Portfolio investment required: $10,152,870
- Recurring yearly savings: $5,730,700
- Portfolio three-year ROI: 69.3%
- Estimated payback period: 1.77 years

## Recommended Modernization Roadmap
### Phase 1: Quick wins
- Upgrade EOL operating systems, runtimes, application servers, and databases where a direct version uplift is possible.
- Prioritize managed database adoption and PostgreSQL standardization for cost and operations reduction.
- Address low-complexity applications with strong ROI first to establish migration patterns.

### Phase 2: Platform modernization
- Containerize the remaining non-containerized workloads.
- Complete on-premise to cloud migrations for hybrid and on-premise applications.
- Standardize non-Linux operating systems onto enterprise Linux where feasible.

### Phase 3: Application transformation
- Refactor 1-tier, 2-tier, and 3-tier monoliths into more decoupled services.
- Target the highest-cost legacy platforms for broader architecture transformation after platform risk is removed.
- Use data platform modernization to retire paid legacy database estates and reduce license exposure.
