# PayrollApp-010 (app010) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** HR  
**Criticality:** Medium  
**Status:** Production  
**Deployment:** AWS  
**Architecture:** unknown  
**Containerized:** No  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | Windows Server 2019 | ✅ CURRENT_VERSION |
| Programming Language | Ruby 2.7 | 🔴 EOL |
| Application Server | Microsoft IIS 10.0 | ✅ CURRENT_VERSION |
| Database Engine | MySQL 8.0 | ✅ CURRENT_VERSION |

**Overall Risk:** `HIGH_RISK`

## Complexity Assessment

**Score:** 3/10 — **Low** (Cost Multiplier: 1.0x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 1 | 1 |
| External Interfaces | 4 | 0 |
| Api Endpoints | 3 | 0 |
| Business Criticality | Medium | 1 |
| Tech Debt Components | 1 | 1 |
| Deployment Type | AWS | 0 |
| Database Storage Gb | 250.0 | 1 |
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
| Refactor/Decouple | LACK_OF_DATA |
| DB Upgrade | NOT_APPLICABLE |
| Managed DB | APPLICABLE |
| Managed ARM DB | APPLICABLE |
| Serverless DB | NOT_APPLICABLE |
| Switch to PostgreSQL | APPLICABLE |

## Business Case

| Metric | Value |
|--------|-------|
| Total Migration Cost | $140,300 |
| Total Yearly Savings | $131,400 |
| 3-Year ROI | 181.0% |
| Payback Period | 1.07 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| Switch to Linux | $300 | $400 |
| ARM CPU Migration | $5,000 | $1,000 |
| Containerization | $100,000 | $100,000 |
| Managed DB | $5,000 | $10,000 |
| Managed ARM DB | $5,000 | $5,000 |
| Switch to PostgreSQL | $25,000 | $15,000 |
