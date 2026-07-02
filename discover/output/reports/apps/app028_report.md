# NotificationApp-028 (app028) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** IT  
**Criticality:** Medium  
**Status:** Production  
**Deployment:** AWS  
**Architecture:** unknown  
**Containerized:** Yes  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | Windows Server 2019 | ✅ CURRENT_VERSION |
| Programming Language | Java 17 | ✅ CURRENT_VERSION |
| Application Server | Microsoft IIS 10.0 | ✅ CURRENT_VERSION |
| Database Engine | Oracle 19c | ✅ CURRENT_VERSION |

**Overall Risk:** `LOW_RISK`

## Complexity Assessment

**Score:** 5/10 — **Medium** (Cost Multiplier: 1.2x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 2 | 2 |
| External Interfaces | 25 | 2 |
| Api Endpoints | 18 | 1 |
| Business Criticality | Medium | 1 |
| Tech Debt Components | 0 | 0 |
| Deployment Type | AWS | 0 |
| Database Storage Gb | 3000.0 | 2 |
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
| Refactor/Decouple | LACK_OF_DATA |
| DB Upgrade | NOT_APPLICABLE |
| Managed DB | APPLICABLE |
| Managed ARM DB | APPLICABLE |
| Serverless DB | NOT_APPLICABLE |
| Switch to PostgreSQL | APPLICABLE |

## Business Case

| Metric | Value |
|--------|-------|
| Total Migration Cost | $48,360 |
| Total Yearly Savings | $31,400 |
| 3-Year ROI | 94.8% |
| Payback Period | 1.54 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| Switch to Linux | $360 | $400 |
| ARM CPU Migration | $6,000 | $1,000 |
| Managed DB | $6,000 | $10,000 |
| Managed ARM DB | $6,000 | $5,000 |
| Switch to PostgreSQL | $30,000 | $15,000 |
