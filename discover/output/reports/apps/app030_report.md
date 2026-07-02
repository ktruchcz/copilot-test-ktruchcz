# APIGatewayApp-030 (app030) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** IT  
**Criticality:** High  
**Status:** Production  
**Deployment:** AWS  
**Architecture:** 3-Tier  
**Containerized:** Yes  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | RHEL 8 | ✅ CURRENT_VERSION |
| Programming Language | Go 1.19 | ⚠️ OUTDATED |
| Application Server | Glassfish 3.0 | 🔴 EOL |
| Database Engine | MySQL 5.7 | 🔴 EOL |

**Overall Risk:** `HIGH_RISK`

## Complexity Assessment

**Score:** 6/10 — **Medium** (Cost Multiplier: 1.2x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 2 | 2 |
| External Interfaces | 30 | 2 |
| Api Endpoints | 50 | 2 |
| Business Criticality | High | 2 |
| Tech Debt Components | 3 | 3 |
| Deployment Type | AWS | 0 |
| Database Storage Gb | 80.0 | 0 |
| Ci Cd Present | Yes | 0 |
| Is Containerized | Yes | 0 |

## Scenario Applicability

| Scenario | Status |
|----------|--------|
| OS Security Patch | NOT_APPLICABLE |
| Switch to Linux | NOT_APPLICABLE |
| ARM CPU Migration | APPLICABLE |
| App Server Replacement | APPLICABLE |
| Cloud Deployment | FULFILLED |
| Containerization | FULFILLED |
| Refactor/Decouple | APPLICABLE |
| DB Upgrade | APPLICABLE |
| Managed DB | APPLICABLE |
| Managed ARM DB | APPLICABLE |
| Serverless DB | APPLICABLE |
| Switch to PostgreSQL | APPLICABLE |

## Business Case

| Metric | Value |
|--------|-------|
| Total Migration Cost | $378,000 |
| Total Yearly Savings | $218,000 |
| 3-Year ROI | 73.0% |
| Payback Period | 1.73 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| ARM CPU Migration | $6,000 | $1,000 |
| App Server Replacement | $12,000 | $12,000 |
| Refactor/Decouple | $300,000 | $150,000 |
| DB Upgrade | $12,000 | $10,000 |
| Managed DB | $6,000 | $10,000 |
| Managed ARM DB | $6,000 | $5,000 |
| Serverless DB | $6,000 | $15,000 |
| Switch to PostgreSQL | $30,000 | $15,000 |
