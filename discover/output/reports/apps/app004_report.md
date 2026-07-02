# HRApp-004 (app004) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** HR  
**Criticality:** High  
**Status:** Production  
**Deployment:** AWS, On-premise  
**Architecture:** 2-Tier  
**Containerized:** Yes  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | Windows Server 2012 | 🔴 EOL |
| Programming Language | .NET Core | ⚠️ OUTDATED |
| Application Server | Microsoft IIS 8.0 | 🔴 EOL |
| Database Engine | SQL Server 2019 | ✅ CURRENT_VERSION |

**Overall Risk:** `HIGH_RISK`

## Complexity Assessment

**Score:** 6/10 — **Medium** (Cost Multiplier: 1.2x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 2 | 2 |
| External Interfaces | 6 | 1 |
| Api Endpoints | 12 | 1 |
| Business Criticality | High | 2 |
| Tech Debt Components | 3 | 3 |
| Deployment Type | AWS, On-premise | 1 |
| Database Storage Gb | 750.0 | 1 |
| Ci Cd Present | Yes | 0 |
| Is Containerized | Yes | 0 |

## Scenario Applicability

| Scenario | Status |
|----------|--------|
| OS Security Patch | APPLICABLE |
| Switch to Linux | APPLICABLE |
| ARM CPU Migration | APPLICABLE |
| App Server Replacement | APPLICABLE |
| Cloud Deployment | APPLICABLE |
| Containerization | FULFILLED |
| Refactor/Decouple | NOT_APPLICABLE |
| DB Upgrade | NOT_APPLICABLE |
| Managed DB | APPLICABLE |
| Managed ARM DB | APPLICABLE |
| Serverless DB | NOT_APPLICABLE |
| Switch to PostgreSQL | APPLICABLE |

## Business Case

| Metric | Value |
|--------|-------|
| Total Migration Cost | $67,560 |
| Total Yearly Savings | $46,900 |
| 3-Year ROI | 108.3% |
| Payback Period | 1.44 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| OS Security Patch | $1,200 | $500 |
| Switch to Linux | $360 | $400 |
| ARM CPU Migration | $6,000 | $1,000 |
| App Server Replacement | $12,000 | $12,000 |
| Cloud Deployment | $6,000 | $3,000 |
| Managed DB | $6,000 | $10,000 |
| Managed ARM DB | $6,000 | $5,000 |
| Switch to PostgreSQL | $30,000 | $15,000 |
