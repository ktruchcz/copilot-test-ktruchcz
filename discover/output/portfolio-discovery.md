# Portfolio Discovery Report

**Generated**: 2026-05-05 11:12 UTC
**Source**: `discover/input/apps_db_complete.xlsx`

---

## 1. Executive Summary

The portfolio comprises **30 applications** across multiple business units. Of these, **26** are currently in production and **4** are retired. **13** applications (43%) rely on legacy or end-of-life technologies and represent the highest modernization risk. **13** applications (43%) are fully or partially on-premise and are candidates for cloud migration. **9** applications lack CI/CD pipelines, indicating significant DevOps maturity gaps.

---

## 2. Portfolio Overview

| Metric | Value |
|--------|-------|
| Total Applications | 30 |
| Production | 26 |
| Retired | 4 |
| Custom-Made | 19 |
| 3rd Party / SaaS | 7 |
| Open Source | 4 |

### 2.1 Criticality Distribution

| Criticality | Count | % |
|-------------|-------|---|
| Critical | 4 | 13% |
| High | 11 | 36% |
| Medium | 10 | 33% |
| Low | 5 | 16% |

### 2.2 Deployment Distribution

| Deployment Type | Count | % |
|-----------------|-------|---|
| AWS | 17 | 56% |
| On-Premise | 9 | 30% |
| AWS, On-premise | 4 | 13% |

### 2.3 Architecture Distribution

| Architecture | Count |
|--------------|-------|
| 3-Tier | 13 |
| 2-Tier | 8 |
| unknown | 6 |
| 1-Tier | 3 |

---

## 3. Technology Assessment

### 3.1 Programming Languages

| Language | Count | Maturity |
|----------|-------|----------|
| Java 11 | 3 | Legacy |
| COBOL-2014 | 2 | Legacy |
| Java 17 | 2 | Modern |
| Python 3.9 | 1 | Current |
| .NET Core | 1 | Current |
| Node.js 14 | 1 | Legacy |
| Python 3.7 | 1 | Legacy |
| Go 1.16 | 1 | Current |
| Ruby 2.7 | 1 | Legacy |
| Python 3.11 | 1 | Modern |
| Rust 1.70 | 1 | Modern |
| C# .NET 6 | 1 | Current |
| PHP 8.1 | 1 | Current |
| React Native | 1 | Current |
| PowerShell | 1 | Current |
| Java 8 | 1 | Legacy |
| Python 3.8 | 1 | Legacy |
| Angular 15 | 1 | Current |
| C++ 17 | 1 | Current |
| Scala 2.13 | 1 | Current |
| Node.js 18 | 1 | Modern |
| VB.NET | 1 | Legacy |
| ASP.NET Core | 1 | Modern |
| FORTRAN 2018 | 1 | Legacy |
| Perl | 1 | Legacy |
| Go 1.19 | 1 | Modern |

### 3.2 Technology Maturity Summary

| Maturity | Count | % |
|----------|-------|---|
| Legacy | 13 | 43% |
| Current | 10 | 33% |
| Modern | 7 | 23% |

### 3.3 Legacy Applications (High Priority)

| App ID | Name | Language | Criticality | Deployment | Strategy |
|--------|------|----------|-------------|------------|----------|
| app005 | EComApp-005 | Node.js 14 | Critical | AWS | Retire |
| app026 | LegacyFinApp-026 | FORTRAN 2018 | Critical | On-Premise | Retire |
| app001 | ERPApp-001 | COBOL-2014 | High | On-Premise | Retire |
| app007 | FinanceApp-007 | Python 3.7 | High | AWS | Retire |
| app008 | InventoryApp-008 | COBOL-2014 | High | On-Premise | Retire |
| app019 | QualityApp-019 | Python 3.8 | High | AWS, On-premise | Refactor/Re-architect |
| app024 | AuditApp-024 | VB.NET | High | On-Premise | Refactor/Re-architect |
| app027 | DataWarehouseApp-027 | Java 11 | High | AWS, On-premise | Refactor/Re-architect |
| app002 | CRMApp-002 | Java 11 | Medium | AWS | Repurchase |
| app006 | SupportApp-006 | Java 11 | Medium | AWS | Repurchase |
| app010 | PayrollApp-010 | Ruby 2.7 | Medium | AWS | Repurchase |
| app018 | VendorApp-018 | Java 8 | Medium | On-Premise | Replatform |
| app029 | ConfigApp-029 | Perl | Low | On-Premise | Retire |

### 3.4 Operating Systems

| OS | Count |
|----|-------|
| RHEL 7 | 9 |
| Windows Server 2019 | 6 |
| Windows Server 2012 | 3 |
| RHEL 8 | 3 |
| AIX 7.2 | 2 |
| Windows Server 2022 | 2 |
| Debian 6 | 1 |
| Ubuntu 14 | 1 |
| AIX 6 | 1 |
| CentOS 7 | 1 |
| Debian 7 | 1 |

---

## 4. Cloud Migration Analysis

### 4.1 On-Premise Applications (13 total)

| App ID | Name | Criticality | Architecture | Containerized | CI/CD | Strategy |
|--------|------|-------------|--------------|---------------|-------|----------|
| app013 | SecurityApp-013 | Critical | 3-Tier | No | Yes | Rehost |
| app022 | ComplianceApp-022 | Critical | 3-Tier | Yes | Yes | Rehost |
| app026 | LegacyFinApp-026 | Critical | 1-Tier | No | No | Retire |
| app001 | ERPApp-001 | High | 1-Tier | No | No | Retire |
| app004 | HRApp-004 | High | 2-Tier | Yes | Yes | Rehost |
| app008 | InventoryApp-008 | High | 1-Tier | No | No | Retire |
| app017 | BackupApp-017 | High | unknown | No | No | Repurchase |
| app019 | QualityApp-019 | High | 3-Tier | No | Yes | Refactor/Re-architect |
| app021 | FleetApp-021 | High | 2-Tier | No | No | Rehost |
| app024 | AuditApp-024 | High | 2-Tier | No | No | Refactor/Re-architect |
| app027 | DataWarehouseApp-027 | High | 3-Tier | No | Yes | Refactor/Re-architect |
| app018 | VendorApp-018 | Medium | 3-Tier | No | No | Replatform |
| app029 | ConfigApp-029 | Low | 3-Tier | No | No | Retire |

### 4.2 Database Analysis

| Database | Count |
|----------|-------|
| PostgreSQL 14 | 4 |
| Oracle 19c | 3 |
| PostgreSQL 13 | 3 |
| SQL Server 2019 | 3 |
| MySQL 8.0 | 3 |
| Amazon RDS MySQL | 2 |
| SQL Server 2022 | 2 |
| MongoDB | 2 |
| Aurora PostgreSQL | 1 |
| Oracle 12c | 1 |
| SQL Server 2016 | 1 |
| Oracle 11g | 1 |
| SQL Server 2014 | 1 |
| PostgreSQL 15 | 1 |
| DB2 | 1 |
| MySQL 5.7 | 1 |

**Applications with licensed databases**: 13 (43%) — consider open-source alternatives or managed cloud services.

**Total DB Storage**: 21,760 GB across all applications.

---

## 5. DevOps & Operational Readiness

| Indicator | Yes | No | % Ready |
|-----------|-----|-----|---------|
| CI/CD Pipeline | 21 | 9 | 70% |
| Containerized | 12 | 18 | 40% |
| Logging Solution | 27 | 3 | 90% |
| Monitoring Tool | 22 | 8 | 73% |

### 5.1 Applications Without CI/CD

| App ID | Name | Criticality | Language | Deployment |
|--------|------|-------------|----------|------------|
| app001 | ERPApp-001 | High | COBOL-2014 | On-Premise |
| app007 | FinanceApp-007 | High | Python 3.7 | AWS |
| app008 | InventoryApp-008 | High | COBOL-2014 | On-Premise |
| app017 | BackupApp-017 | High | PowerShell | On-Premise |
| app018 | VendorApp-018 | Medium | Java 8 | On-Premise |
| app021 | FleetApp-021 | High | C++ 17 | On-Premise |
| app024 | AuditApp-024 | High | VB.NET | On-Premise |
| app026 | LegacyFinApp-026 | Critical | FORTRAN 2018 | On-Premise |
| app029 | ConfigApp-029 | Low | Perl | On-Premise |

---

## 6. Modernization Strategy (7-R Model)

| Strategy | Count | % |
|----------|-------|---|
| Repurchase | 10 | 33% |
| Retire | 7 | 23% |
| Retain | 5 | 16% |
| Rehost | 4 | 13% |
| Refactor/Re-architect | 3 | 10% |
| Replatform | 1 | 3% |

### 6.1 Strategy Descriptions

- **Retire**: Application is no longer needed; decommission it.
- **Retain**: Keep as-is; revisit later (too risky or costly to change now).
- **Rehost**: Lift-and-shift to cloud with minimal changes.
- **Replatform**: Lift-and-reshape: minor optimisations to cloud-native services.
- **Repurchase**: Move to a SaaS or 3rd-party commercial product.
- **Refactor/Re-architect**: Redesign to be cloud-native (microservices, containers).

### 6.2 Full Application Strategy Map

| App ID | Name | Business Unit | Criticality | Language | Current Deploy | Strategy |
|--------|------|---------------|-------------|----------|----------------|----------|
| app019 | QualityApp-019 | Quality | High | Python 3.8 | AWS, On-premise | Refactor/Re-architect |
| app024 | AuditApp-024 | Finance | High | VB.NET | On-Premise | Refactor/Re-architect |
| app027 | DataWarehouseApp-027 | BI | High | Java 11 | AWS, On-premise | Refactor/Re-architect |
| app013 | SecurityApp-013 | Security | Critical | Java 17 | On-Premise | Rehost |
| app022 | ComplianceApp-022 | Compliance | Critical | Scala 2.13 | AWS, On-premise | Rehost |
| app004 | HRApp-004 | HR | High | .NET Core | AWS, On-premise | Rehost |
| app021 | FleetApp-021 | Operations | High | C++ 17 | On-Premise | Rehost |
| app018 | VendorApp-018 | Procurement | Medium | Java 8 | On-Premise | Replatform |
| app017 | BackupApp-017 | IT | High | PowerShell | On-Premise | Repurchase |
| app030 | APIGatewayApp-030 | IT | High | Go 1.19 | AWS | Repurchase |
| app003 | AnalyticsApp-003 | IT | Low | Python 3.9 | AWS | Repurchase |
| app020 | TrainingApp-020 | HR | Low | Angular 15 | AWS | Repurchase |
| app002 | CRMApp-002 | Marketing | Medium | Java 11 | AWS | Repurchase |
| app006 | SupportApp-006 | IT | Medium | Java 11 | AWS | Repurchase |
| app010 | PayrollApp-010 | HR | Medium | Ruby 2.7 | AWS | Repurchase |
| app014 | DocumentApp-014 | Operations | Medium | C# .NET 6 | AWS | Repurchase |
| app023 | ChatbotApp-023 | Customer Service | Medium | Node.js 18 | AWS | Repurchase |
| app028 | NotificationApp-028 | IT | Medium | Java 17 | AWS | Repurchase |
| app012 | IoTSensorApp-012 | R&D | High | Rust 1.70 | AWS | Retain |
| app015 | ReportingApp-015 | Finance | Low | PHP 8.1 | AWS | Retain |
| app011 | RouteOptApp-011 | R&D | Medium | Python 3.11 | AWS | Retain |
| app016 | MobileApp-016 | Operations | Medium | React Native | AWS | Retain |
| app025 | PortalApp-025 | Operations | Medium | ASP.NET Core | AWS | Retain |
| app005 | EComApp-005 | Operations | Critical | Node.js 14 | AWS | Retire |
| app026 | LegacyFinApp-026 | Finance | Critical | FORTRAN 2018 | On-Premise | Retire |
| app001 | ERPApp-001 | Finance | High | COBOL-2014 | On-Premise | Retire |
| app007 | FinanceApp-007 | Finance | High | Python 3.7 | AWS | Retire |
| app008 | InventoryApp-008 | Operations | High | COBOL-2014 | On-Premise | Retire |
| app009 | MarketingApp-009 | Marketing | Low | Go 1.16 | AWS | Retire |
| app029 | ConfigApp-029 | IT | Low | Perl | On-Premise | Retire |

---

## 7. Risk Assessment

| Risk | Applications Affected | Severity |
|------|-----------------------|----------|
| Legacy/EOL technology | 13 | High |
| No CI/CD pipeline | 9 | High |
| On-Premise infrastructure | 13 | Medium |
| Not containerized (production) | 16 | Medium |
| Proprietary DB licensing | 13 | Medium |
| Unknown architecture | 6 | Low |
| No monitoring | 8 | Low |

---

## 8. Recommendations

### Priority 1 — Immediate Actions

1. **Address Legacy Critical Apps**: 8 applications with legacy technology are critical/high-criticality. Initiate refactoring or rebuild plans immediately.
2. **Implement CI/CD**: 9 applications lack automated pipelines. Implement CI/CD for all production applications to reduce deployment risk.

### Priority 2 — Short-Term (3-6 months)

3. **Cloud Migration**: 13 on-premise applications should be assessed for cloud migration (Rehost or Replatform). Begin with low-criticality, non-legacy apps.
4. **Containerization**: 16 production applications are not containerized. Containerize applications before cloud migration to simplify operations.

### Priority 3 — Medium-Term (6-12 months)

5. **DB Licensing**: 13 applications use licensed databases. Evaluate migration to open-source (PostgreSQL, MySQL) or managed cloud database services to reduce costs.
6. **Observability**: Standardize on a single logging and monitoring stack across all applications.
7. **Architecture Modernization**: 6 applications have unknown architecture. Document and assess these for potential 3-tier or microservices refactoring.

---

*Report generated by `discover/analyze_portfolio.py` from `discover/input/apps_db_complete.xlsx`.*
