# Portfolio Discovery Report

**Project**: copilot-test-ktruchcz  
**Date**: 2026-05-05  
**Source**: `apps_db_complete.xlsx` — App Details (30 applications)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Application Inventory](#2-application-inventory)
3. [Portfolio Analysis](#3-portfolio-analysis)
   - 3.1 [Application Status](#31-application-status)
   - 3.2 [Criticality Distribution](#32-criticality-distribution)
   - 3.3 [Solution Type](#33-solution-type)
   - 3.4 [Programming Languages & Runtimes](#34-programming-languages--runtimes)
   - 3.5 [Deployment Model](#35-deployment-model)
   - 3.6 [Containerisation](#36-containerisation)
   - 3.7 [Application Architecture](#37-application-architecture)
   - 3.8 [CI/CD Adoption](#38-cicd-adoption)
   - 3.9 [Operating Systems](#39-operating-systems)
   - 3.10 [Database & Licensing](#310-database--licensing)
   - 3.11 [Observability](#311-observability)
4. [Key Findings & Risks](#4-key-findings--risks)
5. [Modernisation Opportunities](#5-modernisation-opportunities)
6. [Application Detail Cards](#6-application-detail-cards)

---

## 1. Executive Summary

The portfolio consists of **30 applications** spanning 12 business units. Of these, **26 are in active production** and **4 are retired**. The estate is highly heterogeneous: 26 distinct technology stacks are in use, infrastructure spans on-premises data centres and AWS, and only 40 % of production applications are containerised.

| Metric | Value |
|--------|-------|
| Total applications | 30 |
| Active (Production) | 26 |
| Retired | 4 |
| Unique programming languages/runtimes | 26 |
| Applications with CI/CD | 21 (70 %) |
| Containerised applications | 12 (40 %) |
| Cloud-only (AWS) deployments | 17 (57 %) |
| On-premises or hybrid deployments | 13 (43 %) |
| Applications requiring paid DB licences | 13 (43 %) |
| High/Critical criticality apps | 15 (50 %) |

**Top three modernisation priorities identified:**
1. **Retire/replace legacy language stacks** — COBOL, FORTRAN, VB.NET, Java 8 apps running in production.
2. **Complete containerisation** — 14 production apps are not containerised; 6 have no CI/CD pipeline.
3. **Consolidate on-premises workloads to cloud** — 9 apps run exclusively on-premises, exposing the organisation to infrastructure risk and increasing operational cost.

---

## 2. Application Inventory

| App ID | Name | Business Unit | Language | Deploy | Container | CI/CD | Status | Criticality |
|--------|------|---------------|----------|--------|-----------|-------|--------|-------------|
| app001 | ERPApp-001 | Finance | COBOL-2014 | On-Premise | No | No | Production | High |
| app002 | CRMApp-002 | Marketing | Java 11 | AWS | No | Yes | Production | Medium |
| app003 | AnalyticsApp-003 | IT | Python 3.9 | AWS | Yes | Yes | Production | Low |
| app004 | HRApp-004 | HR | .NET Core | AWS, On-premise | Yes | Yes | Production | High |
| app005 | EComApp-005 | Operations | Node.js 14 | AWS | Yes | Yes | Retired | Critical |
| app006 | SupportApp-006 | IT | Java 11 | AWS | No | Yes | Production | Medium |
| app007 | FinanceApp-007 | Finance | Python 3.7 | AWS | No | No | Retired | High |
| app008 | InventoryApp-008 | Operations | COBOL-2014 | On-Premise | No | No | Production | High |
| app009 | MarketingApp-009 | Marketing | Go 1.16 | AWS | Yes | Yes | Retired | Low |
| app010 | PayrollApp-010 | HR | Ruby 2.7 | AWS | No | Yes | Production | Medium |
| app011 | RouteOptApp-011 | R&D | Python 3.11 | AWS | Yes | Yes | Production | Medium |
| app012 | IoTSensorApp-012 | R&D | Rust 1.70 | AWS | Yes | Yes | Production | High |
| app013 | SecurityApp-013 | Security | Java 17 | On-Premise | No | Yes | Production | Critical |
| app014 | DocumentApp-014 | Operations | C# .NET 6 | AWS | No | Yes | Production | Medium |
| app015 | ReportingApp-015 | Finance | PHP 8.1 | AWS | No | Yes | Production | Low |
| app016 | MobileApp-016 | Operations | React Native | AWS | Yes | Yes | Production | Medium |
| app017 | BackupApp-017 | IT | PowerShell | On-Premise | No | No | Production | High |
| app018 | VendorApp-018 | Procurement | Java 8 | On-Premise | No | No | Production | Medium |
| app019 | QualityApp-019 | Quality | Python 3.8 | AWS, On-premise | No | Yes | Production | High |
| app020 | TrainingApp-020 | HR | Angular 15 | AWS | No | Yes | Production | Low |
| app021 | FleetApp-021 | Operations | C++ 17 | On-Premise | No | No | Production | High |
| app022 | ComplianceApp-022 | Compliance | Scala 2.13 | AWS, On-premise | Yes | Yes | Production | Critical |
| app023 | ChatbotApp-023 | Customer Service | Node.js 18 | AWS | Yes | Yes | Production | Medium |
| app024 | AuditApp-024 | Finance | VB.NET | On-Premise | No | No | Production | High |
| app025 | PortalApp-025 | Operations | ASP.NET Core | AWS | Yes | Yes | Production | Medium |
| app026 | LegacyFinApp-026 | Finance | FORTRAN 2018 | On-Premise | No | No | Production | Critical |
| app027 | DataWarehouseApp-027 | BI | Java 11 | AWS, On-premise | No | Yes | Production | High |
| app028 | NotificationApp-028 | IT | Java 17 | AWS | Yes | Yes | Production | Medium |
| app029 | ConfigApp-029 | IT | Perl | On-Premise | No | No | Retired | Low |
| app030 | APIGatewayApp-030 | IT | Go 1.19 | AWS | Yes | Yes | Production | High |

---

## 3. Portfolio Analysis

### 3.1 Application Status

| Status | Count | % |
|--------|-------|---|
| Production | 26 | 87 % |
| Retired | 4 | 13 % |

Four applications are **retired** (app005, app007, app009, app029). These should be fully decommissioned — infrastructure, data archival, and licence termination should be confirmed.

Planned decommission dates for production apps:

| App ID | Name | Decommission Date |
|--------|------|-------------------|
| app001 | ERPApp-001 | 2027 |
| app008 | InventoryApp-008 | 2027 |
| app017 | BackupApp-017 | 2028 |
| app026 | LegacyFinApp-026 | 2027 |

---

### 3.2 Criticality Distribution

| Criticality | Count | Apps |
|-------------|-------|------|
| Critical | 4 | app005 (Retired), app013, app022, app026 |
| High | 11 | app001, app004, app007 (Retired), app008, app012, app017, app019, app021, app024, app027, app030 |
| Medium | 10 | app002, app006, app010, app011, app014, app016, app018, app023, app025, app028 |
| Low | 5 | app003, app009 (Retired), app015, app020, app029 (Retired) |

**50 % of the portfolio is High or Critical criticality**, requiring careful change management for any modernisation activities.

---

### 3.3 Solution Type

| Type | Count | % |
|------|-------|---|
| Custom made | 19 | 63 % |
| 3rd party software | 7 | 23 % |
| Open Source | 4 | 13 % |

The predominance of **custom-made applications** (63 %) means the organisation has significant flexibility to modernise but also carries the full maintenance burden. Third-party applications (23 %) require vendor coordination before any platform changes.

---

### 3.4 Programming Languages & Runtimes

| Language / Runtime | Count | Production Apps | Notes |
|--------------------|-------|-----------------|-------|
| Java 11 | 3 | app002, app006, app027 | EOL — upgrade to Java 21 recommended |
| COBOL-2014 | 2 | app001, app008 | Legacy — rewrite or wrap with modern APIs |
| Java 17 | 2 | app013, app028 | LTS — upgrade to Java 21 when possible |
| .NET Core | 1 | app004 | Identify exact version; upgrade to .NET 8 LTS |
| Python 3.9 | 1 | app003 | EOL Jan 2026 — upgrade to 3.12+ |
| Node.js 14 | 1 | app005 (Retired) | EOL — already retired |
| Python 3.7 | 1 | app007 (Retired) | EOL — already retired |
| Go 1.16 | 1 | app009 (Retired) | EOL — already retired |
| Ruby 2.7 | 1 | app010 | EOL — upgrade to Ruby 3.3+ |
| Python 3.11 | 1 | app011 | Current LTS |
| Rust 1.70 | 1 | app012 | Update to latest stable |
| C# .NET 6 | 1 | app014 | EOL — upgrade to .NET 8 LTS |
| PHP 8.1 | 1 | app015 | EOL Dec 2024 — upgrade to PHP 8.3+ |
| React Native | 1 | app016 | Update to latest version |
| PowerShell | 1 | app017 | Update to PowerShell 7+ |
| Java 8 | 1 | app018 | EOL — upgrade to Java 21 LTS urgently |
| Python 3.8 | 1 | app019 | EOL Oct 2024 — upgrade to 3.12+ |
| Angular 15 | 1 | app020 | EOL — upgrade to latest LTS |
| C++ 17 | 1 | app021 | Consider modernisation to C++20/23 |
| Scala 2.13 | 1 | app022 | Consider migration to Scala 3 |
| Node.js 18 | 1 | app023 | EOL Apr 2025 — upgrade to Node.js 22 LTS |
| VB.NET | 1 | app024 | Legacy — rewrite in C# .NET 8 recommended |
| ASP.NET Core | 1 | app025 | Identify exact version; target .NET 8 LTS |
| FORTRAN 2018 | 1 | app026 | Legacy — rewrite or wrap with modern service |
| Perl | 1 | app029 (Retired) | EOL — already retired |
| Go 1.19 | 1 | app030 | Upgrade to Go 1.22+ |

**Languages requiring urgent attention (EOL or security risk) in production:**

| App | Language | EOL Status |
|-----|----------|------------|
| app018 | Java 8 | EOL since 2030 (commercial support ended earlier for open-source builds) — **upgrade urgently** |
| app019 | Python 3.8 | EOL October 2024 |
| app003 | Python 3.9 | EOL October 2025 |
| app014 | C# .NET 6 | EOL November 2024 |
| app015 | PHP 8.1 | EOL December 2024 |
| app023 | Node.js 18 | EOL April 2025 |
| app002, app006, app027 | Java 11 | EOL September 2023 (community) |
| app010 | Ruby 2.7 | EOL March 2023 |
| app024 | VB.NET | No active development; rewrite recommended |
| app026 | FORTRAN 2018 | No modern cloud-native support |

---

### 3.5 Deployment Model

| Deployment | Count | % |
|------------|-------|---|
| AWS | 17 | 57 % |
| On-Premise | 9 | 30 % |
| AWS + On-Premise (hybrid) | 4 | 13 % |

**On-premise-only applications** (9 total) represent the highest infrastructure risk and cost. Prioritised for cloud migration:

| App ID | Name | Criticality | Language | Notes |
|--------|------|-------------|----------|-------|
| app001 | ERPApp-001 | High | COBOL-2014 | Decommission 2027; complex migration |
| app008 | InventoryApp-008 | High | COBOL-2014 | Decommission 2027 |
| app013 | SecurityApp-013 | Critical | Java 17 | On-premise by policy; review required |
| app017 | BackupApp-017 | High | PowerShell | Decommission 2028 |
| app018 | VendorApp-018 | Medium | Java 8 | Cloud migration candidate |
| app021 | FleetApp-021 | High | C++ 17 | On-premise latency requirements; review |
| app024 | AuditApp-024 | High | VB.NET | Legacy rewrite + cloud migration |
| app026 | LegacyFinApp-026 | Critical | FORTRAN 2018 | Decommission 2027; complex migration |

---

### 3.6 Containerisation

| Containerised | Count | % |
|---------------|-------|---|
| Yes | 12 | 40 % |
| No | 18 | 60 % |

Only **12 of 30 applications** (40 %) are containerised. Among the 26 production applications, **14 are not containerised**, limiting deployment flexibility and scalability. High-priority containerisation candidates (production, cloud-deployed, not containerised):

| App ID | Name | Criticality | Language | Deploy |
|--------|------|-------------|----------|--------|
| app002 | CRMApp-002 | Medium | Java 11 | AWS |
| app006 | SupportApp-006 | Medium | Java 11 | AWS |
| app010 | PayrollApp-010 | Medium | Ruby 2.7 | AWS |
| app014 | DocumentApp-014 | Medium | C# .NET 6 | AWS |
| app015 | ReportingApp-015 | Low | PHP 8.1 | AWS |
| app020 | TrainingApp-020 | Low | Angular 15 | AWS |
| app027 | DataWarehouseApp-027 | High | Java 11 | AWS, On-premise |

---

### 3.7 Application Architecture

| Architecture | Count | % |
|--------------|-------|---|
| 3-Tier | 13 | 43 % |
| 2-Tier | 8 | 27 % |
| unknown | 6 | 20 % |
| 1-Tier | 3 | 10 % |

Six applications have **unknown architecture**, indicating missing documentation. Architecture review workshops should be scheduled for these apps (app002, app005, app006, app017, app028).

---

### 3.8 CI/CD Adoption

| CI/CD Present | Count | % |
|---------------|-------|---|
| Yes | 21 | 70 % |
| No | 9 | 30 % |

Nine applications lack CI/CD pipelines. Among production apps without CI/CD:

| App ID | Name | Criticality | Language |
|--------|------|-------------|----------|
| app001 | ERPApp-001 | High | COBOL-2014 |
| app008 | InventoryApp-008 | High | COBOL-2014 |
| app017 | BackupApp-017 | High | PowerShell |
| app018 | VendorApp-018 | Medium | Java 8 |
| app021 | FleetApp-021 | High | C++ 17 |
| app024 | AuditApp-024 | High | VB.NET |
| app026 | LegacyFinApp-026 | Critical | FORTRAN 2018 |

Notably, **5 of these 7 are also on-premises and non-containerised**, making them the most operationally rigid applications in the portfolio.

---

### 3.9 Operating Systems

| Operating System | Count | Notes |
|------------------|-------|-------|
| RHEL 7 | 9 | EOL June 2024 — extended lifecycle support or upgrade needed |
| Windows Server 2019 | 6 | Supported until 2029 |
| Windows Server 2012 | 3 | EOL October 2023 — upgrade urgently |
| RHEL 8 | 3 | Supported until 2029 |
| AIX 7.2 | 2 | Legacy IBM platform |
| Windows Server 2022 | 2 | Supported until 2031 |
| Debian 6 | 1 | EOL 2016 — **critical security risk** |
| Ubuntu 14 | 1 | EOL 2019 — already retired app (app007) |
| AIX 6 | 1 | EOL 2017 — **critical security risk** (app008) |
| CentOS 7 | 1 | EOL June 2024 |
| Debian 7 | 1 | EOL 2018 — **critical security risk** (app013) |

**Critical OS security risks:**
- `app006` runs on **Debian 6** (EOL 2016).
- `app008` runs on **AIX 6** (EOL 2017).
- `app013` (Critical) runs on **Debian 7** (EOL 2018).
- Three apps run on **Windows Server 2012** (EOL Oct 2023).
- Nine apps run on **RHEL 7** (EOL June 2024).

---

### 3.10 Database & Licensing

| DB Engine | Count |
|-----------|-------|
| PostgreSQL (various) | 8 |
| SQL Server (various) | 7 |
| MySQL (various) | 4 |
| Oracle (various) | 4 |
| MongoDB | 2 |
| Aurora PostgreSQL | 1 |
| DB2 | 1 |
| Amazon RDS MySQL | 2 |

**Applications requiring paid database licences** (13 total):

| App ID | Name | DB Engine | DB Storage (GB) |
|--------|------|-----------|-----------------|
| app001 | ERPApp-001 | Oracle 19c | 1,000 |
| app004 | HRApp-004 | SQL Server 2019 | 750 |
| app007 | FinanceApp-007 (Retired) | Oracle 19c | 500 |
| app008 | InventoryApp-008 | SQL Server 2019 | 400 |
| app013 | SecurityApp-013 | SQL Server 2022 | 600 |
| app016 | MobileApp-016 | SQL Server 2019 | 2,000 |
| app017 | BackupApp-017 | Oracle 12c | 350 |
| app020 | TrainingApp-020 | SQL Server 2016 | 600 |
| app021 | FleetApp-021 | Oracle 11g | 400 |
| app024 | AuditApp-024 | SQL Server 2014 | 300 |
| app026 | LegacyFinApp-026 | DB2 | 1,500 |
| app027 | DataWarehouseApp-027 | SQL Server 2022 | 5,000 |
| app028 | NotificationApp-028 | Oracle 19c | 3,000 |

Notable risks:
- **SQL Server 2014** (app024) — EOL July 2024, security risk.
- **SQL Server 2016** (app020) — EOL July 2026, plan upgrade.
- **Oracle 11g** (app021) — EOL October 2013 — **critical security risk**.
- **Oracle 12c** (app017) — EOL July 2022.
- **DB2** (app026) — proprietary, expensive; migration to open-source DB recommended.
- **MySQL 5.7** (app030, APIGatewayApp-030) — EOL October 2023; **upgrade to MySQL 8.0 urgently** (app030 is High-criticality handling 1,800 users and 50 API endpoints).

---

### 3.11 Observability

| Logging Solution | Count |
|-----------------|-------|
| CloudWatch | 8 |
| ELK | 6 |
| Splunk | 4 |
| None | 6 |
| Windows Event Log | 2 |
| Syslog | 2 |
| Log4j | 1 |

| Monitoring Tool | Count |
|----------------|-------|
| None | 8 |
| Prometheus | 7 |
| Datadog | 6 |
| CloudWatch | 5 |
| Grafana | 2 |
| SCOM | 1 |

**6 applications have no logging** and **8 have no monitoring** — a significant observability gap for production systems. Critical/High-criticality apps without monitoring:

| App ID | Name | Criticality | Monitoring |
|--------|------|-------------|------------|
| app001 | ERPApp-001 | High | None |
| app008 | InventoryApp-008 | High | None |
| app021 | FleetApp-021 | High | None |
| app024 | AuditApp-024 | High | None |
| app026 | LegacyFinApp-026 | Critical | None |

---

## 4. Key Findings & Risks

### Risk: End-of-Life Operating Systems & Runtimes

| Severity | Finding |
|----------|---------|
| 🔴 Critical | `app006` on Debian 6 (EOL 2016); `app008` on AIX 6 (EOL 2017); `app013` on Debian 7 (EOL 2018) |
| 🔴 Critical | `app021` using Oracle 11g (EOL 2013); `app024` on SQL Server 2014 (EOL 2024); `app030` (High, 1,800 users, 50 endpoints) using MySQL 5.7 (EOL Oct 2023) |
| 🔴 Critical | `app018` on Java 8; `app010` on Ruby 2.7 (EOL 2023); `app014` on .NET 6 (EOL 2024) |
| 🟠 High | 9 apps on RHEL 7 (EOL June 2024); 3 apps on Windows Server 2012 (EOL Oct 2023) |
| 🟠 High | `app002`, `app006`, `app027` on Java 11 (community EOL Sept 2023) |
| 🟡 Medium | `app023` on Node.js 18 (EOL April 2025); `app003` on Python 3.9 (EOL Oct 2025) |

### Risk: Legacy Technology Stacks

| Severity | Finding |
|----------|---------|
| 🔴 Critical | 2 production COBOL-2014 apps with no CI/CD, no containers, and no monitoring |
| 🔴 Critical | 1 production FORTRAN 2018 app (app026, Critical criticality) with no CI/CD, no container, no monitoring |
| 🟠 High | 1 production VB.NET app (app024) with no CI/CD, no container, no monitoring |
| 🟠 High | `app018` Java 8 on-premises with no CI/CD |

### Risk: Observability Gaps

| Severity | Finding |
|----------|---------|
| 🔴 Critical | 5 High/Critical-criticality production apps have no monitoring at all |
| 🟠 High | 6 production apps have no logging solution |

### Risk: No CI/CD in Production

| Severity | Finding |
|----------|---------|
| 🟠 High | 7 production apps have no CI/CD pipeline, limiting deployment agility and auditability |

### Risk: Decommissioned Apps Still Resourced

| Severity | Finding |
|----------|---------|
| 🟡 Medium | 4 retired apps (app005, app007, app009, app029) should be confirmed fully decommissioned (licence, infra, data archival) |

---

## 5. Modernisation Opportunities

### Opportunity 1 — Language Runtime Upgrades (Quick Wins)

Upgrade in-support applications to the latest LTS versions without architectural changes:

| Priority | App | Current | Target | Effort |
|----------|-----|---------|--------|--------|
| P1 | app018 (VendorApp-018) | Java 8 | Java 21 LTS | Medium |
| P1 | app019 (QualityApp-019) | Python 3.8 | Python 3.12 | Low |
| P1 | app003 (AnalyticsApp-003) | Python 3.9 | Python 3.12 | Low |
| P1 | app014 (DocumentApp-014) | C# .NET 6 | .NET 8 LTS | Low |
| P1 | app015 (ReportingApp-015) | PHP 8.1 | PHP 8.3 | Low |
| P1 | app010 (PayrollApp-010) | Ruby 2.7 | Ruby 3.3 | Medium |
| P1 | app023 (ChatbotApp-023) | Node.js 18 | Node.js 22 LTS | Low |
| P2 | app002 (CRMApp-002) | Java 11 | Java 21 LTS | Medium |
| P2 | app006 (SupportApp-006) | Java 11 | Java 21 LTS | Medium |
| P2 | app027 (DataWarehouseApp-027) | Java 11 | Java 21 LTS | Medium |
| P2 | app030 (APIGatewayApp-030) | Go 1.19 | Go 1.22+ | Low |

### Opportunity 2 — OS Refresh

Replace EOL operating systems on production hosts:

| Priority | App(s) | Current OS | Target OS |
|----------|--------|-----------|-----------|
| P1 | app006 | Debian 6 | Debian 12 or RHEL 9 |
| P1 | app008 | AIX 6 | AIX 7.2 or Linux |
| P1 | app013 | Debian 7 | Debian 12 or RHEL 9 |
| P1 | app004, app005, app020 | Windows Server 2012 | Windows Server 2022 |
| P2 | 9 apps on RHEL 7 | RHEL 7 | RHEL 9 |
| P2 | app001 | AIX 7.2 | Migrate off AIX |

### Opportunity 3 — Containerisation

Containerise production cloud-deployed applications without containers, enabling Kubernetes or ECS deployment:

Target apps: app002, app006, app010, app014, app015, app020, app027.

Expected benefits: standardised deployments, improved resource utilisation, simplified scaling.

### Opportunity 4 — CI/CD Pipeline Adoption

Establish CI/CD pipelines for the 7 production apps lacking them. Priority: app017, app018, app021, app024.

Expected benefits: automated testing, faster deployments, auditability.

### Opportunity 5 — Observability Uplift

Implement logging and monitoring for the 5 High/Critical-criticality apps with no observability:

- app001, app008, app021, app024, app026.

Recommended tooling: integrate with existing CloudWatch, ELK, or Prometheus stack already in use across the portfolio.

### Opportunity 6 — Database Licence Reduction

Migrate from expensive proprietary databases to open-source alternatives where feasible:

| App | Current DB | Target DB | Estimated Storage |
|-----|-----------|-----------|------------------|
| app021 | Oracle 11g (EOL) | PostgreSQL 16 | 400 GB |
| app017 | Oracle 12c (EOL) | PostgreSQL 16 | 350 GB |
| app026 | DB2 | PostgreSQL 16 | 1,500 GB |
| app024 | SQL Server 2014 (EOL) | PostgreSQL 16 | 300 GB |
| app020 | SQL Server 2016 | PostgreSQL 16 | 600 GB |

### Opportunity 7 — Legacy Rewrite Programme

Long-running strategic initiative for the most complex legacy apps:

| App | Technology | Complexity | Suggested Approach |
|-----|-----------|------------|-------------------|
| app001 | COBOL-2014 / AIX 7.2 | Very High | Incremental strangler-fig pattern using REST APIs |
| app008 | COBOL-2014 / AIX 6 | Very High | Incremental strangler-fig pattern; OS refresh first |
| app024 | VB.NET | High | Rewrite in C# .NET 8 |
| app026 | FORTRAN 2018 / DB2 | Very High | Wrap with service API; rewrite in Python or Java |

---

## 6. Application Detail Cards

<details>
<summary>app001 — ERPApp-001</summary>

| Field | Value |
|-------|-------|
| Description | Core ERP system handling financial transactions, general ledger, and regulatory reporting |
| Solution Type | Custom made |
| Criticality | High |
| Status | Production (decommission: 2027) |
| Business Unit | Finance |
| Users | 350 |
| Language | COBOL-2014 |
| OS | AIX 7.2 |
| App Server | None |
| Architecture | 1-Tier |
| Deployment | On-Premise |
| Containerised | No |
| Environments | 2 |
| CI/CD | No |
| API Endpoints | 0 |
| External Interfaces | 5 |
| Database | Oracle 19c (1,000 GB) |
| DB Licence | Yes |
| Logging | None |
| Monitoring | None |
| Data Classification | Confidential |

**Key risks**: EOL OS (AIX 7.2), COBOL legacy stack, no CI/CD, no observability. Planned decommission 2027.
</details>

<details>
<summary>app002 — CRMApp-002</summary>

| Field | Value |
|-------|-------|
| Description | Customer relationship management system for tracking leads, opportunities, and customer interactions |
| Solution Type | 3rd party software |
| Criticality | Medium |
| Status | Production |
| Business Unit | Marketing |
| Users | 1,200 |
| Language | Java 11 |
| OS | RHEL 7 |
| App Server | Websphere 7.0 |
| Architecture | unknown |
| Deployment | AWS |
| Containerised | No |
| Environments | 2 |
| CI/CD | Yes |
| API Endpoints | 15 |
| External Interfaces | 8 |
| Database | Amazon RDS MySQL (500 GB) |
| DB Licence | No |
| Logging | CloudWatch |
| Monitoring | Datadog |
| Data Classification | Internal |

**Key risks**: Java 11 EOL, RHEL 7 EOL, WebSphere 7.0 (very old), not containerised, unknown architecture.
</details>

<details>
<summary>app003 — AnalyticsApp-003</summary>

| Field | Value |
|-------|-------|
| Description | Analytics platform for generating operational reports and business insights from logistics data |
| Solution Type | Open Source |
| Criticality | Low |
| Status | Production |
| Business Unit | IT |
| Users | 480 |
| Language | Python 3.9 |
| OS | RHEL 7 |
| App Server | Apache Tomcat 6.1 |
| Architecture | 3-Tier |
| Deployment | AWS |
| Containerised | Yes |
| Environments | 1 |
| CI/CD | Yes |
| API Endpoints | 8 |
| External Interfaces | 3 |
| Database | PostgreSQL 13 (200 GB) |
| DB Licence | No |
| Logging | ELK |
| Monitoring | Prometheus |
| Data Classification | Public |

**Key risks**: Python 3.9 EOL Oct 2025, RHEL 7 EOL, Apache Tomcat 6.1 (EOL).
</details>

<details>
<summary>app004 — HRApp-004</summary>

| Field | Value |
|-------|-------|
| Description | Human resources management system handling employee records, benefits, and HR workflows |
| Solution Type | Custom made |
| Criticality | High |
| Status | Production |
| Business Unit | HR |
| Users | 670 |
| Language | .NET Core |
| OS | Windows Server 2012 |
| App Server | Microsoft IIS 8.0 |
| Architecture | 2-Tier |
| Deployment | AWS, On-premise |
| Containerised | Yes |
| Environments | 2 |
| CI/CD | Yes |
| API Endpoints | 12 |
| External Interfaces | 6 |
| Database | SQL Server 2019 (750 GB) |
| DB Licence | Yes |
| Logging | Splunk |
| Monitoring | CloudWatch |
| Data Classification | Internal |

**Key risks**: Windows Server 2012 EOL, .NET Core version unclear (likely EOL), hybrid deployment complexity.
</details>

<details>
<summary>app005 — EComApp-005 (Retired)</summary>

| Field | Value |
|-------|-------|
| Description | E-commerce platform for online logistics services booking and customer self-service portal |
| Status | **Retired** |
| Language | Node.js 14 |
| Criticality | Critical |

**Action**: Confirm full decommission — infrastructure shutdown, data archival, licence termination.
</details>

<details>
<summary>app006 — SupportApp-006</summary>

| Field | Value |
|-------|-------|
| Description | IT service desk application for handling internal support tickets and IT service requests |
| Solution Type | 3rd party software |
| Criticality | Medium |
| Status | Production |
| Business Unit | IT |
| Users | 290 |
| Language | Java 11 |
| OS | **Debian 6** |
| App Server | Glassfish 5.0 |
| Architecture | unknown |
| Deployment | AWS |
| Containerised | No |
| Environments | 2 |
| CI/CD | Yes |
| API Endpoints | 6 |
| External Interfaces | 4 |
| Database | PostgreSQL 13 (200 GB) |
| DB Licence | No |
| Logging | ELK |
| Monitoring | None |
| Data Classification | Internal |

**Key risks**: Debian 6 EOL since 2016 — **CRITICAL security risk**. Java 11 EOL. No monitoring.
</details>

<details>
<summary>app007 — FinanceApp-007 (Retired)</summary>

| Field | Value |
|-------|-------|
| Description | Specialized financial application for logistics cost accounting and invoice processing |
| Status | **Retired** |
| Language | Python 3.7 |
| Criticality | High |

**Action**: Confirm full decommission — data archival, Oracle 19c licence review.
</details>

<details>
<summary>app008 — InventoryApp-008</summary>

| Field | Value |
|-------|-------|
| Description | Legacy inventory management system controlling warehouse stock levels and material movements |
| Solution Type | Custom made |
| Criticality | High |
| Status | Production (decommission: 2027) |
| Business Unit | Operations |
| Users | 875 |
| Language | COBOL-2014 |
| OS | **AIX 6** |
| App Server | Oracle Weblogic 8.0 |
| Architecture | 1-Tier |
| Deployment | On-Premise |
| Containerised | No |
| Environments | 3 |
| CI/CD | No |
| API Endpoints | 0 |
| External Interfaces | 2 |
| Database | SQL Server 2019 (400 GB) |
| DB Licence | Yes |
| Logging | None |
| Monitoring | None |
| Data Classification | Confidential |

**Key risks**: AIX 6 EOL 2017 — **CRITICAL security risk**. COBOL legacy. WebLogic 8.0 EOL. No CI/CD, no observability.
</details>

<details>
<summary>app009 — MarketingApp-009 (Retired)</summary>

| Field | Value |
|-------|-------|
| Description | Marketing automation platform for managing digital campaigns and customer communications |
| Status | **Retired** |
| Language | Go 1.16 |

**Action**: Confirm full decommission.
</details>

<details>
<summary>app010 — PayrollApp-010</summary>

| Field | Value |
|-------|-------|
| Description | Payroll processing system handling salary calculations, tax deductions, and compensation reporting |
| Solution Type | 3rd party software |
| Criticality | Medium |
| Status | Production |
| Business Unit | HR |
| Users | 315 |
| Language | Ruby 2.7 |
| OS | Windows Server 2019 |
| App Server | Microsoft IIS 10.0 |
| Architecture | unknown |
| Deployment | AWS |
| Containerised | No |
| Environments | 1 |
| CI/CD | Yes |
| API Endpoints | 3 |
| External Interfaces | 4 |
| Database | MySQL 8.0 (250 GB) |
| DB Licence | No |
| Logging | ELK |
| Monitoring | CloudWatch |
| Data Classification | Internal |

**Key risks**: Ruby 2.7 EOL March 2023. Not containerised. Unknown architecture.
</details>

<details>
<summary>app011 — RouteOptApp-011</summary>

| Field | Value |
|-------|-------|
| Description | Advanced route optimization system using machine learning algorithms for delivery planning |
| Solution Type | Custom made |
| Criticality | Medium |
| Status | Production |
| Business Unit | R&D |
| Users | 125 |
| Language | Python 3.11 |
| OS | CentOS 7 |
| App Server | Glassfish 4.0 |
| Architecture | 3-Tier |
| Deployment | AWS |
| Containerised | Yes |
| Environments | 1 |
| CI/CD | Yes |
| API Endpoints | 12 |
| External Interfaces | 5 |
| Database | PostgreSQL 14 (180 GB) |
| DB Licence | No |
| Logging | CloudWatch |
| Monitoring | Prometheus |
| Data Classification | Internal |

**Key risks**: CentOS 7 EOL June 2024. Glassfish 4.0 (community EOL).
</details>

<details>
<summary>app012 — IoTSensorApp-012</summary>

| Field | Value |
|-------|-------|
| Description | IoT sensor data collection and analysis platform for tracking vehicle performance and cargo conditions |
| Solution Type | Custom made |
| Criticality | High |
| Status | Production |
| Business Unit | R&D |
| Users | 85 |
| Language | Rust 1.70 |
| OS | Windows Server 2022 |
| App Server | Microsoft IIS 10.0 |
| Architecture | 2-Tier |
| Deployment | AWS |
| Containerised | Yes |
| Environments | 2 |
| CI/CD | Yes |
| API Endpoints | 20 |
| External Interfaces | 8 |
| Database | PostgreSQL 14 (800 GB) |
| DB Licence | No |
| Logging | CloudWatch |
| Monitoring | Grafana |
| Data Classification | Confidential |

**Key risks**: Rust 1.70 — update to latest stable. Otherwise well-managed.
</details>

<details>
<summary>app013 — SecurityApp-013</summary>

| Field | Value |
|-------|-------|
| Description | Enterprise security platform for monitoring threats, managing access controls, and ensuring compliance |
| Solution Type | Custom made |
| Criticality | **Critical** |
| Status | Production |
| Business Unit | Security |
| Users | 520 |
| Language | Java 17 |
| OS | **Debian 7** |
| App Server | Websphere 8.0 |
| Architecture | 3-Tier |
| Deployment | On-Premise |
| Containerised | No |
| Environments | 3 |
| CI/CD | Yes |
| API Endpoints | 8 |
| External Interfaces | 15 |
| Database | SQL Server 2022 (600 GB) |
| DB Licence | Yes |
| Logging | Splunk |
| Monitoring | Datadog |
| Data Classification | Confidential |

**Key risks**: Debian 7 EOL 2018 — **CRITICAL security risk for a security platform**. Not containerised. WebSphere 8.0 EOL.
</details>

<details>
<summary>app014 — DocumentApp-014</summary>

| Field | Value |
|-------|-------|
| Description | Document management system for handling shipping documents, contracts, and regulatory paperwork |
| Solution Type | Open Source |
| Criticality | Medium |
| Status | Production |
| Business Unit | Operations |
| Users | 890 |
| Language | C# .NET 6 |
| OS | Windows Server 2019 |
| App Server | Microsoft IIS 10.0 |
| Architecture | 2-Tier |
| Deployment | AWS |
| Containerised | No |
| Environments | 2 |
| CI/CD | Yes |
| API Endpoints | 18 |
| External Interfaces | 9 |
| Database | MySQL 8.0 (120 GB) |
| DB Licence | No |
| Logging | ELK |
| Monitoring | CloudWatch |
| Data Classification | Internal |

**Key risks**: .NET 6 EOL November 2024. Upgrade to .NET 8 LTS.
</details>

<details>
<summary>app015 — ReportingApp-015</summary>

| Field | Value |
|-------|-------|
| Description | Financial reporting tool for generating executive dashboards and regulatory compliance reports |
| Solution Type | Custom made |
| Criticality | Low |
| Status | Production |
| Business Unit | Finance |
| Users | 340 |
| Language | PHP 8.1 |
| OS | Windows Server 2019 |
| App Server | Microsoft IIS 10.0 |
| Architecture | 2-Tier |
| Deployment | AWS |
| Containerised | No |
| Environments | 4 |
| CI/CD | Yes |
| API Endpoints | 6 |
| External Interfaces | 4 |
| Database | MongoDB (400 GB) |
| DB Licence | No |
| Logging | CloudWatch |
| Monitoring | Prometheus |
| Data Classification | Public |

**Key risks**: PHP 8.1 EOL December 2024. Upgrade to PHP 8.3+.
</details>

<details>
<summary>app016 — MobileApp-016</summary>

| Field | Value |
|-------|-------|
| Description | Mobile application for drivers and customers to track shipments and manage delivery operations |
| Solution Type | Custom made |
| Criticality | Medium |
| Status | Production |
| Business Unit | Operations |
| Users | 1,580 |
| Language | React Native |
| OS | RHEL 7 |
| App Server | Payara 4.0 |
| Architecture | 3-Tier |
| Deployment | AWS |
| Containerised | Yes |
| Environments | 3 |
| CI/CD | Yes |
| API Endpoints | 30 |
| External Interfaces | 10 |
| Database | SQL Server 2019 (2,000 GB) |
| DB Licence | Yes |
| Logging | CloudWatch |
| Monitoring | Datadog |
| Data Classification | Internal |

**Key risks**: RHEL 7 EOL, Payara 4.0 EOL, large SQL Server licence cost.
</details>

<details>
<summary>app017 — BackupApp-017</summary>

| Field | Value |
|-------|-------|
| Description | Automated backup and disaster recovery system for critical business applications and data |
| Solution Type | 3rd party software |
| Criticality | High |
| Status | Production (decommission: 2028) |
| Business Unit | IT |
| Users | 45 |
| Language | PowerShell |
| OS | RHEL 7 |
| App Server | Payara 5.0 |
| Architecture | unknown |
| Deployment | On-Premise |
| Containerised | No |
| Environments | 5 |
| CI/CD | No |
| API Endpoints | 2 |
| External Interfaces | 8 |
| Database | Oracle 12c (350 GB) |
| DB Licence | Yes |
| Logging | Windows Event Log |
| Monitoring | SCOM |
| Data Classification | Confidential |

**Key risks**: Oracle 12c EOL July 2022. RHEL 7 EOL. No CI/CD.
</details>

<details>
<summary>app018 — VendorApp-018</summary>

| Field | Value |
|-------|-------|
| Description | Vendor management platform for handling supplier relationships, contracts, and procurement processes |
| Solution Type | Custom made |
| Criticality | Medium |
| Status | Production |
| Business Unit | Procurement |
| Users | 260 |
| Language | **Java 8** |
| OS | RHEL 7 |
| App Server | Glassfish 4.5 |
| Architecture | 3-Tier |
| Deployment | On-Premise |
| Containerised | No |
| Environments | 6 |
| CI/CD | No |
| API Endpoints | 5 |
| External Interfaces | 6 |
| Database | PostgreSQL 13 (250 GB) |
| DB Licence | No |
| Logging | Log4j |
| Monitoring | None |
| Data Classification | Internal |

**Key risks**: Java 8 EOL. RHEL 7 EOL. No CI/CD, no monitoring. Log4j — confirm version for Log4Shell vulnerability.
</details>

<details>
<summary>app019 — QualityApp-019</summary>

| Field | Value |
|-------|-------|
| Description | Quality management system for tracking service quality metrics and managing audit processes |
| Solution Type | Custom made |
| Criticality | High |
| Status | Production |
| Business Unit | Quality |
| Users | 180 |
| Language | Python 3.8 |
| OS | RHEL 8 |
| App Server | Apache Tomcat 8.0 |
| Architecture | 3-Tier |
| Deployment | AWS, On-premise |
| Containerised | No |
| Environments | 1 |
| CI/CD | Yes |
| API Endpoints | 9 |
| External Interfaces | 5 |
| Database | MySQL 8.0 (180 GB) |
| DB Licence | No |
| Logging | ELK |
| Monitoring | CloudWatch |
| Data Classification | Confidential |

**Key risks**: Python 3.8 EOL October 2024. Apache Tomcat 8.0 EOL. Not containerised.
</details>

<details>
<summary>app020 — TrainingApp-020</summary>

| Field | Value |
|-------|-------|
| Description | Learning management system for employee training programs and professional development tracking |
| Solution Type | 3rd party software |
| Criticality | Low |
| Status | Production |
| Business Unit | HR |
| Users | 750 |
| Language | Angular 15 |
| OS | Windows Server 2012 |
| App Server | Microsoft IIS 8.5 |
| Architecture | 2-Tier |
| Deployment | AWS |
| Containerised | No |
| Environments | 3 |
| CI/CD | Yes |
| API Endpoints | 14 |
| External Interfaces | 7 |
| Database | SQL Server 2016 (600 GB) |
| DB Licence | Yes |
| Logging | CloudWatch |
| Monitoring | Prometheus |
| Data Classification | Public |

**Key risks**: Windows Server 2012 EOL, Angular 15 EOL, SQL Server 2016 EOL 2026, IIS 8.5 EOL.
</details>

<details>
<summary>app021 — FleetApp-021</summary>

| Field | Value |
|-------|-------|
| Description | Fleet management system for tracking vehicle locations, maintenance schedules, and driver assignments |
| Solution Type | Custom made |
| Criticality | High |
| Status | Production |
| Business Unit | Operations |
| Users | 420 |
| Language | C++ 17 |
| OS | Windows Server 2022 |
| App Server | Microsoft IIS 10.0 |
| Architecture | 2-Tier |
| Deployment | On-Premise |
| Containerised | No |
| Environments | 3 |
| CI/CD | No |
| API Endpoints | 3 |
| External Interfaces | 4 |
| Database | **Oracle 11g** (400 GB) |
| DB Licence | Yes |
| Logging | Syslog |
| Monitoring | None |
| Data Classification | Internal |

**Key risks**: Oracle 11g EOL October 2013 — **CRITICAL database risk**. No CI/CD, no monitoring.
</details>

<details>
<summary>app022 — ComplianceApp-022</summary>

| Field | Value |
|-------|-------|
| Description | Comprehensive compliance management platform for regulatory adherence and risk management |
| Solution Type | Custom made |
| Criticality | **Critical** |
| Status | Production |
| Business Unit | Compliance |
| Users | 310 |
| Language | Scala 2.13 |
| OS | RHEL 7 |
| App Server | Payara 6.0 |
| Architecture | 3-Tier |
| Deployment | AWS, On-premise |
| Containerised | Yes |
| Environments | 3 |
| CI/CD | Yes |
| API Endpoints | 16 |
| External Interfaces | 12 |
| Database | PostgreSQL 14 (500 GB) |
| DB Licence | No |
| Logging | ELK |
| Monitoring | Grafana |
| Data Classification | Confidential |

**Key risks**: RHEL 7 EOL. Consider migration to Scala 3 for long-term support.
</details>

<details>
<summary>app023 — ChatbotApp-023</summary>

| Field | Value |
|-------|-------|
| Description | AI-powered chatbot system for handling customer inquiries and providing automated support |
| Solution Type | Open Source |
| Criticality | Medium |
| Status | Production |
| Business Unit | Customer Service |
| Users | 1,100 |
| Language | Node.js 18 |
| OS | RHEL 8 |
| App Server | Apache Tomcat 7.4 |
| Architecture | 3-Tier |
| Deployment | AWS |
| Containerised | Yes |
| Environments | 2 |
| CI/CD | Yes |
| API Endpoints | 22 |
| External Interfaces | 8 |
| Database | MongoDB (200 GB) |
| DB Licence | No |
| Logging | CloudWatch |
| Monitoring | Datadog |
| Data Classification | Internal |

**Key risks**: Node.js 18 EOL April 2025 — upgrade to Node.js 22 LTS.
</details>

<details>
<summary>app024 — AuditApp-024</summary>

| Field | Value |
|-------|-------|
| Description | Legacy audit management system for tracking financial audits and compliance activities |
| Solution Type | Custom made |
| Criticality | High |
| Status | Production |
| Business Unit | Finance |
| Users | 95 |
| Language | VB.NET |
| OS | Windows Server 2019 |
| App Server | Microsoft IIS 10.0 |
| Architecture | 2-Tier |
| Deployment | On-Premise |
| Containerised | No |
| Environments | 2 |
| CI/CD | No |
| API Endpoints | 2 |
| External Interfaces | 3 |
| Database | **SQL Server 2014** (300 GB) |
| DB Licence | Yes |
| Logging | Windows Event Log |
| Monitoring | None |
| Data Classification | Confidential |

**Key risks**: VB.NET legacy language, SQL Server 2014 EOL July 2024 — **CRITICAL database risk**. No CI/CD, no monitoring.
</details>

<details>
<summary>app025 — PortalApp-025</summary>

| Field | Value |
|-------|-------|
| Description | Customer self-service portal for shipment tracking, billing, and service requests |
| Solution Type | Custom made |
| Criticality | Medium |
| Status | Production |
| Business Unit | Operations |
| Users | 2,200 |
| Language | ASP.NET Core |
| OS | Windows Server 2019 |
| App Server | Microsoft IIS 10.0 |
| Architecture | 2-Tier |
| Deployment | AWS |
| Containerised | Yes |
| Environments | 3 |
| CI/CD | Yes |
| API Endpoints | 35 |
| External Interfaces | 15 |
| Database | PostgreSQL 15 (800 GB) |
| DB Licence | No |
| Logging | CloudWatch |
| Monitoring | Prometheus |
| Data Classification | Internal |

**Key risks**: ASP.NET Core version not specified — confirm it is .NET 8 LTS.
</details>

<details>
<summary>app026 — LegacyFinApp-026</summary>

| Field | Value |
|-------|-------|
| Description | Legacy financial modeling system for complex calculations and risk assessments |
| Solution Type | Custom made |
| Criticality | **Critical** |
| Status | Production (decommission: 2027) |
| Business Unit | Finance |
| Users | 150 |
| Language | FORTRAN 2018 |
| OS | AIX 7.2 |
| App Server | None |
| Architecture | 1-Tier |
| Deployment | On-Premise |
| Containerised | No |
| Environments | 2 |
| CI/CD | No |
| API Endpoints | 0 |
| External Interfaces | 1 |
| Database | DB2 (1,500 GB) |
| DB Licence | Yes |
| Logging | None |
| Monitoring | None |
| Data Classification | Confidential |

**Key risks**: FORTRAN / AIX / DB2 — complete legacy stack. Critical criticality with zero observability. No CI/CD.
</details>

<details>
<summary>app027 — DataWarehouseApp-027</summary>

| Field | Value |
|-------|-------|
| Description | Enterprise data warehouse for consolidating business data from multiple sources |
| Solution Type | Custom made |
| Criticality | High |
| Status | Production |
| Business Unit | BI |
| Users | 320 |
| Language | Java 11 |
| OS | RHEL 7 |
| App Server | Websphere 8.5 |
| Architecture | 3-Tier |
| Deployment | AWS, On-premise |
| Containerised | No |
| Environments | 3 |
| CI/CD | Yes |
| API Endpoints | 5 |
| External Interfaces | 20 |
| Database | SQL Server 2022 (5,000 GB) |
| DB Licence | Yes |
| Logging | Splunk |
| Monitoring | CloudWatch |
| Data Classification | Internal |

**Key risks**: Java 11 EOL. RHEL 7 EOL. WebSphere 8.5 EOL. Not containerised. 5 TB SQL Server — large licence cost.
</details>

<details>
<summary>app028 — NotificationApp-028</summary>

| Field | Value |
|-------|-------|
| Description | Centralized notification system for sending emails, SMS, and push notifications across all applications |
| Solution Type | 3rd party software |
| Criticality | Medium |
| Status | Production |
| Business Unit | IT |
| Users | 850 |
| Language | Java 17 |
| OS | Windows Server 2019 |
| App Server | Microsoft IIS 10.0 |
| Architecture | unknown |
| Deployment | AWS |
| Containerised | Yes |
| Environments | 3 |
| CI/CD | Yes |
| API Endpoints | 18 |
| External Interfaces | 25 |
| Database | Oracle 19c (3,000 GB) |
| DB Licence | Yes |
| Logging | CloudWatch |
| Monitoring | Datadog |
| Data Classification | Internal |

**Key risks**: Oracle 19c — large licence cost (3 TB). Unknown architecture.
</details>

<details>
<summary>app029 — ConfigApp-029 (Retired)</summary>

| Field | Value |
|-------|-------|
| Description | Legacy configuration management tool for system settings and deployment automation |
| Status | **Retired** |
| Language | Perl |

**Action**: Confirm full decommission.
</details>

<details>
<summary>app030 — APIGatewayApp-030</summary>

| Field | Value |
|-------|-------|
| Description | Modern API gateway for managing microservices communication and external API access |
| Solution Type | Open Source |
| Criticality | High |
| Status | Production |
| Business Unit | IT |
| Users | 1,800 |
| Language | Go 1.19 |
| OS | RHEL 8 |
| App Server | Glassfish 3.0 |
| Architecture | 3-Tier |
| Deployment | AWS |
| Containerised | Yes |
| Environments | 4 |
| CI/CD | Yes |
| API Endpoints | 50 |
| External Interfaces | 30 |
| Database | MySQL 5.7 (80 GB) |
| DB Licence | No |
| Logging | CloudWatch |
| Monitoring | Prometheus |
| Data Classification | Internal |

**Key risks**: Go 1.19 — upgrade to Go 1.22+. MySQL 5.7 EOL October 2023 — **upgrade to MySQL 8.0**. Glassfish 3.0 (very old, community EOL).
</details>
