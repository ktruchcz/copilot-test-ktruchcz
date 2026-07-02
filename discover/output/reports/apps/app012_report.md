# IoTSensorApp-012 (app012) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** R&D  
**Criticality:** High  
**Status:** Production  
**Deployment:** AWS  
**Architecture:** 2-Tier  
**Containerized:** Yes  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | Windows Server 2022 | ✅ CURRENT_VERSION |
| Programming Language | Rust 1.70 | ⚠️ OUTDATED |
| Application Server | Microsoft IIS 10.0 | ✅ CURRENT_VERSION |
| Database Engine | PostgreSQL 14 | ⚠️ OUTDATED |

**Overall Risk:** `MEDIUM_RISK`

## Complexity Assessment

**Score:** 5/10 — **Medium** (Cost Multiplier: 1.2x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 2 | 2 |
| External Interfaces | 8 | 1 |
| Api Endpoints | 20 | 1 |
| Business Criticality | High | 2 |
| Tech Debt Components | 2 | 2 |
| Deployment Type | AWS | 0 |
| Database Storage Gb | 800.0 | 1 |
| Ci Cd Present | Yes | 0 |
| Is Containerized | Yes | 0 |

## Scenario Applicability

| Scenario | Status |
|----------|--------|
| OS Security Patch | NOT_APPLICABLE |
| Switch to Linux | APPLICABLE |
| ARM CPU Migration | APPLICABLE |
| App Server Replacement | NOT_APPLICABLE |
| Cloud Deployment | FULFILLED |
| Containerization | FULFILLED |
| Refactor/Decouple | NOT_APPLICABLE |
| DB Upgrade | APPLICABLE |
| Managed DB | APPLICABLE |
| Managed ARM DB | APPLICABLE |
| Serverless DB | NOT_APPLICABLE |
| Switch to PostgreSQL | NOT_APPLICABLE |

## Business Case

| Metric | Value |
|--------|-------|
| Total Migration Cost | $30,360 |
| Total Yearly Savings | $26,400 |
| 3-Year ROI | 160.9% |
| Payback Period | 1.15 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| Switch to Linux | $360 | $400 |
| ARM CPU Migration | $6,000 | $1,000 |
| DB Upgrade | $12,000 | $10,000 |
| Managed DB | $6,000 | $10,000 |
| Managed ARM DB | $6,000 | $5,000 |
