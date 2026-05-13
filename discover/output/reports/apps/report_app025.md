# PortalApp-025 (app025)

**Status:** Production | **Criticality:** Medium | **Solution Type:** Custom made

## Overview

| Field | Value |
|-------|-------|
| Description | Customer self-service portal for shipment tracking, billing, and service requests |
| Business Unit | Operations |
| Operating System | Windows Server 2019 |
| Programming Language | ASP.NET Core |
| Database | PostgreSQL 15 |
| Architecture | 2-Tier |
| Containerized | Yes |
| CI/CD Present | Yes |
| Environments | 3 |
| Server Instances | sv36, sv37 |
| External Interfaces | 15 |
| Users | 2200 |

## Technology Assessment

**Overall Status:** ❓ NO_KNOWLEDGE

| Component | Name | Status |
|-----------|------|--------|
| operating_system | Windows Server 2019 | ✅ CURRENT_VERSION |
| programming_language | ASP.NET Core | ✅ CURRENT_VERSION |
| database | PostgreSQL 15 | ✅ CURRENT_VERSION |
| application_server | Microsoft IIS 10.0 | ❓ NO_KNOWLEDGE |

## Complexity Assessment

**Score:** 4/10 — **Classification:** MEDIUM

| Factor | Score |
|--------|-------|
| Technology Age Eol | 0.5 |
| Integration Complexity | 1.4 |
| Infrastructure Scale | 1.05 |
| Business Criticality | 0.6 |
| Code And Architecture | 0.45 |
| Data Complexity | 0.5 |

## Scenario Analysis

| Scenario | Status | Reasoning |
|----------|--------|-----------|
| OS Update / Security Patch | NOT_APPLICABLE | OS Windows Server 2019 is current; no immediate patch needed. |
| Switch to Standard Linux OS | APPLICABLE | Running on Windows Server 2019; migrating to standard Linux would reduce licensing costs. |
| Switch to ARM CPU | APPLICABLE | Application is containerized; ARM CPU adoption is feasible with image rebuilds. |
| Application Server Replacement | APPLICABLE | Uses application server Microsoft IIS 10.0; replacement/upgrade may be beneficial. |
| Cloud Migration (Lift & Shift) | APPLICABLE | Application can be migrated to cloud (lift & shift). |
| Containerization | FULFILLED | Application is already containerized. |
| Refactoring & Decoupling | APPLICABLE | Refactoring would improve maintainability and reduce technical debt. |
| Upgrade Legacy Databases | NOT_APPLICABLE | Database PostgreSQL 15 is current; no immediate upgrade needed. |
| Switch to Open Source DB | NOT_APPLICABLE | Already using open source or managed database (PostgreSQL 15). |
| Update Outdated Components | NOT_APPLICABLE | All components are current; no immediate updates needed. |

## Business Case

**Total Implementation Cost:** $236,378.20
**Total Annual Savings:** $149,760.00
**3-Year ROI:** 90.1%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| Switch to Standard Linux OS | $262.35 | $360.00 | 311.7% | 8.7 |
| Switch to ARM CPU | $4,372.52 | $900.00 | -38.3% | 58.3 |
| Application Server Replacement | $8,745.03 | $10,800.00 | 270.5% | 9.7 |
| Cloud Migration (Lift & Shift) | $4,372.52 | $2,700.00 | 85.2% | 19.4 |
| Refactoring & Decoupling | $218,625.78 | $135,000.00 | 85.2% | 19.4 |
