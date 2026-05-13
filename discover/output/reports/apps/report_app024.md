# AuditApp-024 (app024)

**Status:** Production | **Criticality:** High | **Solution Type:** Custom made

## Overview

| Field | Value |
|-------|-------|
| Description | Legacy audit management system for tracking financial audits and compliance activities |
| Business Unit | Finance |
| Operating System | Windows Server 2019 |
| Programming Language | VB.NET |
| Database | SQL Server 2014 |
| Architecture | 2-Tier |
| Containerized | No |
| CI/CD Present | No |
| Environments | 2 |
| Server Instances | sv35 |
| External Interfaces | 3 |
| Users | 95 |

## Technology Assessment

**Overall Status:** 🔴 EOL

| Component | Name | Status |
|-----------|------|--------|
| operating_system | Windows Server 2019 | ✅ CURRENT_VERSION |
| programming_language | VB.NET | ⚠️ OUTDATED |
| database | SQL Server 2014 | 🔴 EOL |
| application_server | Microsoft IIS 10.0 | ❓ NO_KNOWLEDGE |

## Complexity Assessment

**Score:** 6/10 — **Classification:** MEDIUM

| Factor | Score |
|--------|-------|
| Technology Age Eol | 2.5 |
| Integration Complexity | 0.4 |
| Infrastructure Scale | 0.6 |
| Business Criticality | 1.05 |
| Code And Architecture | 0.9 |
| Data Complexity | 0.5 |

## Scenario Analysis

| Scenario | Status | Reasoning |
|----------|--------|-----------|
| OS Update / Security Patch | NOT_APPLICABLE | OS Windows Server 2019 is current; no immediate patch needed. |
| Switch to Standard Linux OS | APPLICABLE | Running on Windows Server 2019; migrating to standard Linux would reduce licensing costs. |
| Switch to ARM CPU | APPLICABLE | ARM CPU migration is possible with recompilation/containerization effort. |
| Application Server Replacement | APPLICABLE | Uses application server Microsoft IIS 10.0; replacement/upgrade may be beneficial. |
| Cloud Migration (Lift & Shift) | APPLICABLE | Application can be migrated to cloud (lift & shift). |
| Containerization | APPLICABLE | Application can be containerized to improve portability and scalability. |
| Refactoring & Decoupling | APPLICABLE | Refactoring would improve maintainability and reduce technical debt. |
| Upgrade Legacy Databases | APPLICABLE | Database SQL Server 2014 is EOL; upgrade is critical for security. |
| Switch to Open Source DB | APPLICABLE | Uses proprietary database SQL Server 2014; switching to PostgreSQL/MySQL would reduce licensing costs. |
| Update Outdated Components | APPLICABLE | Multiple outdated components detected (OS: CURRENT_VERSION, Lang: OUTDATED, DB: EOL). |

## Business Case

**Total Implementation Cost:** $468,741.76
**Total Annual Savings:** $233,120.00
**3-Year ROI:** 49.2%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| Switch to Standard Linux OS | $346.96 | $320.00 | 176.7% | 13.0 |
| Switch to ARM CPU | $5,782.65 | $800.00 | -58.5% | 86.7 |
| Application Server Replacement | $11,565.30 | $9,600.00 | 149.0% | 14.5 |
| Cloud Migration (Lift & Shift) | $5,782.65 | $2,400.00 | 24.5% | 28.9 |
| Containerization | $115,653.04 | $80,000.00 | 107.5% | 17.3 |
| Refactoring & Decoupling | $289,132.60 | $120,000.00 | 24.5% | 28.9 |
| Upgrade Legacy Databases | $11,565.30 | $8,000.00 | 107.5% | 17.3 |
| Switch to Open Source DB | $28,913.26 | $12,000.00 | 24.5% | 28.9 |
