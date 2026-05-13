# CRMApp-002 (app002)

**Status:** Production | **Criticality:** Medium | **Solution Type:** 3rd party software

## Overview

| Field | Value |
|-------|-------|
| Description | Customer relationship management system for tracking leads, opportunities, and customer interactions |
| Business Unit | Marketing |
| Operating System | RHEL 7 |
| Programming Language | Java 11 |
| Database | Amazon RDS MySQL |
| Architecture | unknown |
| Containerized | No |
| CI/CD Present | Yes |
| Environments | 2 |
| Server Instances | sv05, sv07 |
| External Interfaces | 8 |
| Users | 1200 |

## Technology Assessment

**Overall Status:** 🔴 EOL

| Component | Name | Status |
|-----------|------|--------|
| operating_system | RHEL 7 | 🔴 EOL |
| programming_language | Java 11 | ⚠️ OUTDATED |
| database | Amazon RDS MySQL | ✅ CURRENT_VERSION |
| application_server | Websphere 7.0 | ❓ NO_KNOWLEDGE |

## Complexity Assessment

**Score:** 6/10 — **Classification:** MEDIUM

| Factor | Score |
|--------|-------|
| Technology Age Eol | 2.5 |
| Integration Complexity | 0.8 |
| Infrastructure Scale | 0.9 |
| Business Criticality | 0.6 |
| Code And Architecture | 0.75 |
| Data Complexity | 0.5 |

## Scenario Analysis

| Scenario | Status | Reasoning |
|----------|--------|-----------|
| OS Update / Security Patch | APPLICABLE | OS RHEL 7 is EOL; security patch update is needed. |
| Switch to Standard Linux OS | FULFILLED | Already running on standard Linux (RHEL 7). |
| Switch to ARM CPU | BLOCKED | 3rd party software; ARM support depends on vendor roadmap. |
| Application Server Replacement | APPLICABLE | Uses application server Websphere 7.0; replacement/upgrade may be beneficial. |
| Cloud Migration (Lift & Shift) | APPLICABLE | 3rd party software; cloud-hosted or SaaS version likely available. |
| Containerization | BLOCKED | 3rd party software; containerization depends on vendor support. |
| Refactoring & Decoupling | BLOCKED | 3rd party software; source code refactoring is not feasible. |
| Upgrade Legacy Databases | NOT_APPLICABLE | Database Amazon RDS MySQL is current; no immediate upgrade needed. |
| Switch to Open Source DB | NOT_APPLICABLE | Already using open source or managed database (Amazon RDS MySQL). |
| Update Outdated Components | PARTIALLY_FULFILLED | 3rd party software with outdated components; updates depend on vendor release schedule. |

## Business Case

**Total Implementation Cost:** $18,504.48
**Total Annual Savings:** $13,950.00
**3-Year ROI:** 126.2%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| OS Update / Security Patch | $1,156.53 | $450.00 | 16.7% | 30.8 |
| Application Server Replacement | $11,565.30 | $10,800.00 | 180.1% | 12.9 |
| Cloud Migration (Lift & Shift) | $5,782.65 | $2,700.00 | 40.1% | 25.7 |
