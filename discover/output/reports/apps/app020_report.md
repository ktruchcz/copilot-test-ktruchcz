# TrainingApp-020 (app020) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** HR  
**Criticality:** Low  
**Status:** Production  
**Deployment:** AWS  
**Architecture:** 2-Tier  
**Containerized:** No  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | Windows Server 2012 | 🔴 EOL |
| Programming Language | Angular 15 | ⚠️ OUTDATED |
| Application Server | Microsoft IIS 8.5 | 🔴 EOL |
| Database Engine | SQL Server 2016 | ⚠️ OUTDATED |

**Overall Risk:** `HIGH_RISK`

## Complexity Assessment

**Score:** 5/10 — **Medium** (Cost Multiplier: 1.2x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 1 | 1 |
| External Interfaces | 7 | 1 |
| Api Endpoints | 14 | 1 |
| Business Criticality | Low | 0 |
| Tech Debt Components | 4 | 3 |
| Deployment Type | AWS | 0 |
| Database Storage Gb | 600.0 | 1 |
| Ci Cd Present | Yes | 0 |
| Is Containerized | No | 1 |

## Scenario Applicability

| Scenario | Status |
|----------|--------|
| OS Security Patch | APPLICABLE |
| Switch to Linux | APPLICABLE |
| ARM CPU Migration | APPLICABLE |
| App Server Replacement | APPLICABLE |
| Cloud Deployment | FULFILLED |
| Containerization | APPLICABLE |
| Refactor/Decouple | NOT_APPLICABLE |
| DB Upgrade | APPLICABLE |
| Managed DB | APPLICABLE |
| Managed ARM DB | APPLICABLE |
| Serverless DB | NOT_APPLICABLE |
| Switch to PostgreSQL | APPLICABLE |

## Business Case

| Metric | Value |
|--------|-------|
| Total Migration Cost | $193,560 |
| Total Yearly Savings | $153,900 |
| 3-Year ROI | 138.5% |
| Payback Period | 1.26 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| OS Security Patch | $1,200 | $500 |
| Switch to Linux | $360 | $400 |
| ARM CPU Migration | $6,000 | $1,000 |
| App Server Replacement | $12,000 | $12,000 |
| Containerization | $120,000 | $100,000 |
| DB Upgrade | $12,000 | $10,000 |
| Managed DB | $6,000 | $10,000 |
| Managed ARM DB | $6,000 | $5,000 |
| Switch to PostgreSQL | $30,000 | $15,000 |
