# DocumentApp-014 (app014) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** Operations  
**Criticality:** Medium  
**Status:** Production  
**Deployment:** AWS  
**Architecture:** 2-Tier  
**Containerized:** No  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | Windows Server 2019 | ✅ CURRENT_VERSION |
| Programming Language | C# .NET 6 | ⚠️ OUTDATED |
| Application Server | Microsoft IIS 10.0 | ✅ CURRENT_VERSION |
| Database Engine | MySQL 8.0 | ✅ CURRENT_VERSION |

**Overall Risk:** `MEDIUM_RISK`

## Complexity Assessment

**Score:** 4/10 — **Medium** (Cost Multiplier: 1.2x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 2 | 2 |
| External Interfaces | 9 | 1 |
| Api Endpoints | 18 | 1 |
| Business Criticality | Medium | 1 |
| Tech Debt Components | 1 | 1 |
| Deployment Type | AWS | 0 |
| Database Storage Gb | 120.0 | 0 |
| Ci Cd Present | Yes | 0 |
| Is Containerized | No | 1 |

## Scenario Applicability

| Scenario | Status |
|----------|--------|
| OS Security Patch | NOT_APPLICABLE |
| Switch to Linux | APPLICABLE |
| ARM CPU Migration | APPLICABLE |
| App Server Replacement | NOT_APPLICABLE |
| Cloud Deployment | FULFILLED |
| Containerization | APPLICABLE |
| Refactor/Decouple | NOT_APPLICABLE |
| DB Upgrade | NOT_APPLICABLE |
| Managed DB | APPLICABLE |
| Managed ARM DB | APPLICABLE |
| Serverless DB | NOT_APPLICABLE |
| Switch to PostgreSQL | APPLICABLE |

## Business Case

| Metric | Value |
|--------|-------|
| Total Migration Cost | $168,360 |
| Total Yearly Savings | $131,400 |
| 3-Year ROI | 134.1% |
| Payback Period | 1.28 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| Switch to Linux | $360 | $400 |
| ARM CPU Migration | $6,000 | $1,000 |
| Containerization | $120,000 | $100,000 |
| Managed DB | $6,000 | $10,000 |
| Managed ARM DB | $6,000 | $5,000 |
| Switch to PostgreSQL | $30,000 | $15,000 |
