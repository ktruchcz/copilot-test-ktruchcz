# InventoryApp-008 (app008)

**Status:** Production | **Criticality:** High | **Solution Type:** Custom made

## Overview

| Field | Value |
|-------|-------|
| Description | Legacy inventory management system controlling warehouse stock levels and material movements |
| Business Unit | Operations |
| Operating System | AIX 6 |
| Programming Language | COBOL-2014 |
| Database | SQL Server 2019 |
| Architecture | 1-Tier |
| Containerized | No |
| CI/CD Present | No |
| Environments | 3 |
| Server Instances | sv11, sv01 |
| External Interfaces | 2 |
| Users | 875 |

## Technology Assessment

**Overall Status:** 🔴 EOL

| Component | Name | Status |
|-----------|------|--------|
| operating_system | AIX 6 | 🔴 EOL |
| programming_language | COBOL-2014 | ⚠️ OUTDATED |
| database | SQL Server 2019 | ✅ CURRENT_VERSION |
| application_server | Oracle Weblogic 8.0 | ❓ NO_KNOWLEDGE |

## Complexity Assessment

**Score:** 7/10 — **Classification:** HIGH

| Factor | Score |
|--------|-------|
| Technology Age Eol | 2.5 |
| Integration Complexity | 0.4 |
| Infrastructure Scale | 1.05 |
| Business Criticality | 1.05 |
| Code And Architecture | 1.35 |
| Data Complexity | 0.5 |

## Scenario Analysis

| Scenario | Status | Reasoning |
|----------|--------|-----------|
| OS Update / Security Patch | APPLICABLE | OS AIX 6 is EOL; security patch update is needed. |
| Switch to Standard Linux OS | APPLICABLE | Running on AIX 6 (UNIX); migrating to standard Linux would modernize infrastructure. |
| Switch to ARM CPU | APPLICABLE | ARM CPU migration is possible with recompilation/containerization effort. |
| Application Server Replacement | APPLICABLE | Uses application server Oracle Weblogic 8.0; replacement/upgrade may be beneficial. |
| Cloud Migration (Lift & Shift) | APPLICABLE | Application can be migrated to cloud (lift & shift). |
| Containerization | PARTIALLY_FULFILLED | Legacy architecture/language (COBOL-2014); containerization is complex but possible with effort. |
| Refactoring & Decoupling | APPLICABLE | Monolithic/legacy architecture with COBOL-2014; refactoring and decoupling recommended. |
| Upgrade Legacy Databases | NOT_APPLICABLE | Database SQL Server 2019 is current; no immediate upgrade needed. |
| Switch to Open Source DB | APPLICABLE | Uses proprietary database SQL Server 2019; switching to PostgreSQL/MySQL would reduce licensing costs. |
| Update Outdated Components | APPLICABLE | Multiple outdated components detected (OS: EOL, Lang: OUTDATED, DB: CURRENT_VERSION). |

## Business Case

**Total Implementation Cost:** $394,081.95
**Total Annual Savings:** $145,520.00
**3-Year ROI:** 10.8%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| OS Update / Security Patch | $1,330.01 | $400.00 | -9.8% | 39.9 |
| Switch to Standard Linux OS | $399.00 | $320.00 | 140.6% | 15.0 |
| Switch to ARM CPU | $6,650.05 | $800.00 | -63.9% | 99.8 |
| Application Server Replacement | $13,300.10 | $9,600.00 | 116.5% | 16.6 |
| Cloud Migration (Lift & Shift) | $6,650.05 | $2,400.00 | 8.3% | 33.3 |
| Refactoring & Decoupling | $332,502.49 | $120,000.00 | 8.3% | 33.3 |
| Switch to Open Source DB | $33,250.25 | $12,000.00 | 8.3% | 33.3 |
