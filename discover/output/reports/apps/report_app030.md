# APIGatewayApp-030 (app030)

**Status:** Production | **Criticality:** High | **Solution Type:** Open Source

## Overview

| Field | Value |
|-------|-------|
| Description | Modern API gateway for managing microservices communication and external API access |
| Business Unit | IT |
| Operating System | RHEL 8 |
| Programming Language | Go 1.19 |
| Database | MySQL 5.7 |
| Architecture | 3-Tier |
| Containerized | Yes |
| CI/CD Present | Yes |
| Environments | 4 |
| Server Instances | sv44, sv45 |
| External Interfaces | 30 |
| Users | 1800 |

## Technology Assessment

**Overall Status:** 🔴 EOL

| Component | Name | Status |
|-----------|------|--------|
| operating_system | RHEL 8 | ✅ CURRENT_VERSION |
| programming_language | Go 1.19 | ⚠️ OUTDATED |
| database | MySQL 5.7 | 🔴 EOL |
| application_server | Glassfish 3.0 | ❓ NO_KNOWLEDGE |

## Complexity Assessment

**Score:** 7/10 — **Classification:** HIGH

| Factor | Score |
|--------|-------|
| Technology Age Eol | 2.5 |
| Integration Complexity | 2.0 |
| Infrastructure Scale | 1.2 |
| Business Criticality | 1.05 |
| Code And Architecture | 0.15 |
| Data Complexity | 0.3 |

## Scenario Analysis

| Scenario | Status | Reasoning |
|----------|--------|-----------|
| OS Update / Security Patch | NOT_APPLICABLE | OS RHEL 8 is current; no immediate patch needed. |
| Switch to Standard Linux OS | FULFILLED | Already running on standard Linux (RHEL 8). |
| Switch to ARM CPU | APPLICABLE | Application is containerized; ARM CPU adoption is feasible with image rebuilds. |
| Application Server Replacement | APPLICABLE | Uses application server Glassfish 3.0; replacement/upgrade may be beneficial. |
| Cloud Migration (Lift & Shift) | APPLICABLE | Application can be migrated to cloud (lift & shift). |
| Containerization | FULFILLED | Application is already containerized. |
| Refactoring & Decoupling | APPLICABLE | High complexity (7/10); refactoring would reduce technical debt. |
| Upgrade Legacy Databases | APPLICABLE | Database MySQL 5.7 is EOL; upgrade is critical for security. |
| Switch to Open Source DB | NOT_APPLICABLE | Already using open source or managed database (MySQL 5.7). |
| Update Outdated Components | APPLICABLE | Multiple outdated components detected (OS: CURRENT_VERSION, Lang: OUTDATED, DB: EOL). |

## Business Case

**Total Implementation Cost:** $372,402.79
**Total Annual Savings:** $140,800.00
**3-Year ROI:** 13.4%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| Switch to ARM CPU | $6,650.05 | $800.00 | -63.9% | 99.8 |
| Application Server Replacement | $13,300.10 | $9,600.00 | 116.5% | 16.6 |
| Cloud Migration (Lift & Shift) | $6,650.05 | $2,400.00 | 8.3% | 33.3 |
| Refactoring & Decoupling | $332,502.49 | $120,000.00 | 8.3% | 33.3 |
| Upgrade Legacy Databases | $13,300.10 | $8,000.00 | 80.4% | 20.0 |
