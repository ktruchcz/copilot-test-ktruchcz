# CRMApp-002 (app002) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** Marketing  
**Criticality:** Medium  
**Status:** Production  
**Deployment:** AWS  
**Architecture:** unknown  
**Containerized:** No  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | RHEL 7 | 🔴 EOL |
| Programming Language | Java 11 | ⚠️ OUTDATED |
| Application Server | Websphere 7.0 | 🔴 EOL |
| Database Engine | Amazon RDS MySQL | ✅ CURRENT_VERSION |

**Overall Risk:** `HIGH_RISK`

## Complexity Assessment

**Score:** 6/10 — **Medium** (Cost Multiplier: 1.2x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 2 | 2 |
| External Interfaces | 8 | 1 |
| Api Endpoints | 15 | 1 |
| Business Criticality | Medium | 1 |
| Tech Debt Components | 3 | 3 |
| Deployment Type | AWS | 0 |
| Database Storage Gb | 500.0 | 1 |
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
| DB Upgrade | NOT_APPLICABLE |
| Managed DB | NOT_APPLICABLE |
| Managed ARM DB | NOT_APPLICABLE |
| Serverless DB | NOT_APPLICABLE |
| Switch to PostgreSQL | APPLICABLE |

## Business Case

| Metric | Value |
|--------|-------|
| Total Migration Cost | $169,200 |
| Total Yearly Savings | $128,500 |
| 3-Year ROI | 127.8% |
| Payback Period | 1.32 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| OS Security Patch | $1,200 | $500 |
| ARM CPU Migration | $6,000 | $1,000 |
| App Server Replacement | $12,000 | $12,000 |
| Containerization | $120,000 | $100,000 |
| Switch to PostgreSQL | $30,000 | $15,000 |
