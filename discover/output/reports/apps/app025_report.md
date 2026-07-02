# PortalApp-025 (app025) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** Operations  
**Criticality:** Medium  
**Status:** Production  
**Deployment:** AWS  
**Architecture:** 2-Tier  
**Containerized:** Yes  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | Windows Server 2019 | ✅ CURRENT_VERSION |
| Programming Language | ASP.NET Core | ✅ CURRENT_VERSION |
| Application Server | Microsoft IIS 10.0 | ✅ CURRENT_VERSION |
| Database Engine | PostgreSQL 15 | ✅ CURRENT_VERSION |

**Overall Risk:** `LOW_RISK`

## Complexity Assessment

**Score:** 5/10 — **Medium** (Cost Multiplier: 1.2x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 2 | 2 |
| External Interfaces | 15 | 2 |
| Api Endpoints | 35 | 2 |
| Business Criticality | Medium | 1 |
| Tech Debt Components | 0 | 0 |
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
| DB Upgrade | NOT_APPLICABLE |
| Managed DB | APPLICABLE |
| Managed ARM DB | APPLICABLE |
| Serverless DB | NOT_APPLICABLE |
| Switch to PostgreSQL | NOT_APPLICABLE |

## Business Case

| Metric | Value |
|--------|-------|
| Total Migration Cost | $18,360 |
| Total Yearly Savings | $16,400 |
| 3-Year ROI | 168.0% |
| Payback Period | 1.12 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| Switch to Linux | $360 | $400 |
| ARM CPU Migration | $6,000 | $1,000 |
| Managed DB | $6,000 | $10,000 |
| Managed ARM DB | $6,000 | $5,000 |
