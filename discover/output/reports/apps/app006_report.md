# SupportApp-006 (app006) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** IT  
**Criticality:** Medium  
**Status:** Production  
**Deployment:** AWS  
**Architecture:** unknown  
**Containerized:** No  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | Debian 6 | 🔴 EOL |
| Programming Language | Java 11 | ⚠️ OUTDATED |
| Application Server | Glassfish 5.0 | ⚠️ OUTDATED |
| Database Engine | PostgreSQL 13 | ⚠️ OUTDATED |

**Overall Risk:** `HIGH_RISK`

## Complexity Assessment

**Score:** 5/10 — **Medium** (Cost Multiplier: 1.2x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 1 | 1 |
| External Interfaces | 4 | 0 |
| Api Endpoints | 6 | 1 |
| Business Criticality | Medium | 1 |
| Tech Debt Components | 4 | 3 |
| Deployment Type | AWS | 0 |
| Database Storage Gb | 200.0 | 1 |
| Ci Cd Present | Yes | 0 |
| Is Containerized | No | 1 |

## Scenario Applicability

| Scenario | Status |
|----------|--------|
| OS Security Patch | APPLICABLE |
| Switch to Linux | NOT_APPLICABLE |
| ARM CPU Migration | APPLICABLE |
| App Server Replacement | APPLICABLE |
| Cloud Deployment | FULFILLED |
| Containerization | APPLICABLE |
| Refactor/Decouple | LACK_OF_DATA |
| DB Upgrade | APPLICABLE |
| Managed DB | APPLICABLE |
| Managed ARM DB | APPLICABLE |
| Serverless DB | NOT_APPLICABLE |
| Switch to PostgreSQL | NOT_APPLICABLE |

## Business Case

| Metric | Value |
|--------|-------|
| Total Migration Cost | $163,200 |
| Total Yearly Savings | $138,500 |
| 3-Year ROI | 154.6% |
| Payback Period | 1.18 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| OS Security Patch | $1,200 | $500 |
| ARM CPU Migration | $6,000 | $1,000 |
| App Server Replacement | $12,000 | $12,000 |
| Containerization | $120,000 | $100,000 |
| DB Upgrade | $12,000 | $10,000 |
| Managed DB | $6,000 | $10,000 |
| Managed ARM DB | $6,000 | $5,000 |
