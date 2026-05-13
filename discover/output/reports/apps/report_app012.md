# IoTSensorApp-012 (app012)

**Status:** Production | **Criticality:** High | **Solution Type:** Custom made

## Overview

| Field | Value |
|-------|-------|
| Description | IoT sensor data collection and analysis platform for tracking vehicle performance and cargo conditions |
| Business Unit | R&D |
| Operating System | Windows Server 2022 |
| Programming Language | Rust 1.70 |
| Database | PostgreSQL 14 |
| Architecture | 2-Tier |
| Containerized | Yes |
| CI/CD Present | Yes |
| Environments | 2 |
| Server Instances | sv15, sv16 |
| External Interfaces | 8 |
| Users | 85 |

## Technology Assessment

**Overall Status:** ❓ NO_KNOWLEDGE

| Component | Name | Status |
|-----------|------|--------|
| operating_system | Windows Server 2022 | ✅ CURRENT_VERSION |
| programming_language | Rust 1.70 | ✅ CURRENT_VERSION |
| database | PostgreSQL 14 | ✅ CURRENT_VERSION |
| application_server | Microsoft IIS 10.0 | ❓ NO_KNOWLEDGE |

## Complexity Assessment

**Score:** 4/10 — **Classification:** MEDIUM

| Factor | Score |
|--------|-------|
| Technology Age Eol | 0.5 |
| Integration Complexity | 0.8 |
| Infrastructure Scale | 0.9 |
| Business Criticality | 1.05 |
| Code And Architecture | 0.45 |
| Data Complexity | 0.5 |

## Scenario Analysis

| Scenario | Status | Reasoning |
|----------|--------|-----------|
| OS Update / Security Patch | NOT_APPLICABLE | OS Windows Server 2022 is current; no immediate patch needed. |
| Switch to Standard Linux OS | APPLICABLE | Running on Windows Server 2022; migrating to standard Linux would reduce licensing costs. |
| Switch to ARM CPU | APPLICABLE | Application is containerized; ARM CPU adoption is feasible with image rebuilds. |
| Application Server Replacement | APPLICABLE | Uses application server Microsoft IIS 10.0; replacement/upgrade may be beneficial. |
| Cloud Migration (Lift & Shift) | APPLICABLE | Application can be migrated to cloud (lift & shift). |
| Containerization | FULFILLED | Application is already containerized. |
| Refactoring & Decoupling | APPLICABLE | Refactoring would improve maintainability and reduce technical debt. |
| Upgrade Legacy Databases | NOT_APPLICABLE | Database PostgreSQL 14 is current; no immediate upgrade needed. |
| Switch to Open Source DB | NOT_APPLICABLE | Already using open source or managed database (PostgreSQL 14). |
| Update Outdated Components | NOT_APPLICABLE | All components are current; no immediate updates needed. |

## Business Case

**Total Implementation Cost:** $236,378.20
**Total Annual Savings:** $133,120.00
**3-Year ROI:** 68.9%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| Switch to Standard Linux OS | $262.35 | $320.00 | 265.9% | 9.8 |
| Switch to ARM CPU | $4,372.52 | $800.00 | -45.1% | 65.6 |
| Application Server Replacement | $8,745.03 | $9,600.00 | 229.3% | 10.9 |
| Cloud Migration (Lift & Shift) | $4,372.52 | $2,400.00 | 64.7% | 21.9 |
| Refactoring & Decoupling | $218,625.78 | $120,000.00 | 64.7% | 21.9 |
