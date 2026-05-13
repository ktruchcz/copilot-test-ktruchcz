# NotificationApp-028 (app028)

**Status:** Production | **Criticality:** Medium | **Solution Type:** 3rd party software

## Overview

| Field | Value |
|-------|-------|
| Description | Centralized notification system for sending emails, SMS, and push notifications across all applications |
| Business Unit | IT |
| Operating System | Windows Server 2019 |
| Programming Language | Java 17 |
| Database | Oracle 19c |
| Architecture | unknown |
| Containerized | Yes |
| CI/CD Present | Yes |
| Environments | 3 |
| Server Instances | sv41, sv42 |
| External Interfaces | 25 |
| Users | 850 |

## Technology Assessment

**Overall Status:** ❓ NO_KNOWLEDGE

| Component | Name | Status |
|-----------|------|--------|
| operating_system | Windows Server 2019 | ✅ CURRENT_VERSION |
| programming_language | Java 17 | ✅ CURRENT_VERSION |
| database | Oracle 19c | ✅ CURRENT_VERSION |
| application_server | Microsoft IIS 10.0 | ❓ NO_KNOWLEDGE |

## Complexity Assessment

**Score:** 5/10 — **Classification:** MEDIUM

| Factor | Score |
|--------|-------|
| Technology Age Eol | 0.5 |
| Integration Complexity | 2.0 |
| Infrastructure Scale | 1.05 |
| Business Criticality | 0.6 |
| Code And Architecture | 0.45 |
| Data Complexity | 0.7 |

## Scenario Analysis

| Scenario | Status | Reasoning |
|----------|--------|-----------|
| OS Update / Security Patch | NOT_APPLICABLE | OS Windows Server 2019 is current; no immediate patch needed. |
| Switch to Standard Linux OS | PARTIALLY_FULFILLED | Running on Windows Server 2019; switch to Linux may require vendor support confirmation for 3rd party software. |
| Switch to ARM CPU | PARTIALLY_FULFILLED | Containerized 3rd party app; ARM support depends on vendor. |
| Application Server Replacement | APPLICABLE | Uses application server Microsoft IIS 10.0; replacement/upgrade may be beneficial. |
| Cloud Migration (Lift & Shift) | APPLICABLE | 3rd party software; cloud-hosted or SaaS version likely available. |
| Containerization | FULFILLED | Application is already containerized. |
| Refactoring & Decoupling | BLOCKED | 3rd party software; source code refactoring is not feasible. |
| Upgrade Legacy Databases | NOT_APPLICABLE | Database Oracle 19c is current; no immediate upgrade needed. |
| Switch to Open Source DB | PARTIALLY_FULFILLED | 3rd party software using proprietary database Oracle 19c; switch feasibility depends on vendor. |
| Update Outdated Components | NOT_APPLICABLE | All components are current; no immediate updates needed. |

## Business Case

**Total Implementation Cost:** $15,085.18
**Total Annual Savings:** $13,500.00
**3-Year ROI:** 168.5%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| Application Server Replacement | $10,056.79 | $10,800.00 | 222.2% | 11.2 |
| Cloud Migration (Lift & Shift) | $5,028.39 | $2,700.00 | 61.1% | 22.3 |
