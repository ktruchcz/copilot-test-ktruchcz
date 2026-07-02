#!/usr/bin/env python3
"""
Full modernization assessment generator for the application portfolio.
Generates out-of-scope, technology assessment, complexity, scenario, business case,
and reporting outputs.
"""

import json
import os
import glob
import math
from datetime import datetime

# ─────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────
BASE = "/home/runner/work/copilot-test-ktruchcz/copilot-test-ktruchcz/discover/output"
APP_DIR = os.path.join(BASE, "applications/internal_app_model")
OUT_OOS = os.path.join(BASE, "out_of_scope_results")
OUT_TECH = os.path.join(BASE, "technology_assessment")
OUT_COMP = os.path.join(BASE, "complexity_results")
OUT_SCEN = os.path.join(BASE, "scenario_applicability_results")
OUT_BC   = os.path.join(BASE, "business_case_results")
OUT_RPT  = os.path.join(BASE, "reports")

TIMESTAMP = "2025-01-01T00:00:00Z"

# ─────────────────────────────────────────────
# LIFECYCLE MAPPING
# ─────────────────────────────────────────────
OS_MAP = {
    "aix 7.2":               "CURRENT_VERSION",
    "aix 6":                 "EOL",
    "rhel 7":                "EOL",
    "rhel 8":                "CURRENT_VERSION",
    "windows server 2012":   "EOL",
    "windows server 2019":   "CURRENT_VERSION",
    "windows server 2022":   "CURRENT_VERSION",
    "debian 6":              "EOL",
    "debian 7":              "EOL",
    "ubuntu 14":             "EOL",
    "centos 7":              "EOL",
}

LANG_MAP = {
    "cobol-2014":      "OUTDATED",
    "java 8":          "EOL",
    "java 11":         "OUTDATED",
    "java 17":         "CURRENT_VERSION",
    "python 3.7":      "EOL",
    "python 3.8":      "OUTDATED",
    "python 3.9":      "OUTDATED",
    "python 3.11":     "CURRENT_VERSION",
    "node.js 14":      "EOL",
    "node.js 18":      "OUTDATED",
    "go 1.16":         "OUTDATED",
    "go 1.19":         "OUTDATED",
    "ruby 2.7":        "EOL",
    "php 8.1":         "OUTDATED",
    ".net core":       "OUTDATED",
    "c# .net 6":       "OUTDATED",
    "asp.net core":    "CURRENT_VERSION",
    "vb.net":          "OUTDATED",
    "angular 15":      "OUTDATED",
    "react native":    "CURRENT_VERSION",
    "powershell":      "CURRENT_VERSION",
    "rust 1.70":       "OUTDATED",
    "c++ 17":          "CURRENT_VERSION",
    "scala 2.13":      "OUTDATED",
    "fortran 2018":    "OUTDATED",
    "perl":            "EOL",
}

SERVER_MAP = {
    "oracle weblogic 8.0":  "EOL",
    "websphere 7.0":        "EOL",
    "websphere 8.0":        "EOL",
    "websphere 8.5":        "OUTDATED",
    "apache tomcat 5.3":    "EOL",
    "apache tomcat 6.1":    "EOL",
    "apache tomcat 7.4":    "EOL",
    "apache tomcat 8.0":    "EOL",
    "glassfish 3.0":        "EOL",
    "glassfish 4.0":        "EOL",
    "glassfish 4.5":        "EOL",
    "glassfish 5.0":        "OUTDATED",
    "microsoft iis 8.0":    "EOL",
    "microsoft iis 8.5":    "EOL",
    "microsoft iis 10.0":   "CURRENT_VERSION",
    "payara 4.0":           "EOL",
    "payara 5.0":           "OUTDATED",
    "payara 6.0":           "CURRENT_VERSION",
    "weblogic 9.0":         "EOL",
}

DB_MAP = {
    "oracle 11g":          "EOL",
    "oracle 12c":          "EOL",
    "oracle 19c":          "CURRENT_VERSION",
    "sql server 2014":     "EOL",
    "sql server 2016":     "OUTDATED",
    "sql server 2019":     "CURRENT_VERSION",
    "sql server 2022":     "CURRENT_VERSION",
    "mysql 5.7":           "EOL",
    "mysql 8.0":           "CURRENT_VERSION",
    "postgresql 13":       "OUTDATED",
    "postgresql 14":       "OUTDATED",
    "postgresql 15":       "CURRENT_VERSION",
    "amazon rds mysql":    "CURRENT_VERSION",
    "aurora postgresql":   "CURRENT_VERSION",
    "mongodb":             "CURRENT_VERSION",
    "db2":                 "OUTDATED",
}

# DB engines already "managed" (no need for switch_to_managed_db)
MANAGED_DBS = {"amazon rds mysql", "aurora postgresql", "mongodb"}

# DB engines subject to switch_to_postgresql
POSTGRESQL_TARGET_DBS = {"oracle 11g", "oracle 12c", "oracle 19c",
                          "sql server 2014", "sql server 2016", "sql server 2019", "sql server 2022",
                          "mysql 5.7", "mysql 8.0", "amazon rds mysql", "db2"}
ALREADY_POSTGRESQL_DBS = {"postgresql 13", "postgresql 14", "postgresql 15", "aurora postgresql"}

# ─────────────────────────────────────────────
# FINANCE DATA
# ─────────────────────────────────────────────
FINANCE = {
    "os_update_security_patch":   {"migration": 1000, "yearly_savings": 500},
    "switch_to_standard_linux_os": {"migration": 300,  "yearly_savings": 400},
    "switch_to_arm_cpu":           {"migration": 5000, "yearly_savings": 1000},
    "application_server_replacement": {"migration": 10000, "yearly_savings": 12000},
    "app_deployment_to_cloud":    {"migration": 5000, "yearly_savings": 3000},
    "app_containerization":       {"migration": 100000, "yearly_savings": 100000},
    "app_refactor_decoupling":    {"migration": 250000, "yearly_savings": 150000},
    "upgrade_legacy_databases":   {"migration": 10000, "yearly_savings": 10000},
    "switch_to_managed_db":       {"migration": 5000,  "yearly_savings": 10000},
    "managed_arm_db":             {"migration": 5000,  "yearly_savings": 5000},
    "serverless_db_migration":    {"migration": 5000,  "yearly_savings": 15000},
    "switch_db_engine_postgresql":{"migration": 25000, "yearly_savings": 15000},
}

ALL_SCENARIOS = list(FINANCE.keys())

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def norm(s):
    """Normalise a string for lookup."""
    if s is None:
        return ""
    return str(s).strip().lower()

def lookup(s, mapping):
    n = norm(s)
    if not n:
        return None
    # exact match first
    if n in mapping:
        return mapping[n]
    # partial / fuzzy match
    for key, val in mapping.items():
        if key in n or n in key:
            return val
    return "NO_KNOWLEDGE"

def server_count(app):
    si = app.get("server_instances", [])
    if isinstance(si, list):
        return len(si)
    return 1

def is_windows_or_aix(os_str):
    n = norm(os_str)
    return "windows" in n or "aix" in n

def is_on_premise_only(dep):
    n = norm(dep)
    return "on-premise" in n and "aws" not in n and "azure" not in n and "gcp" not in n and "cloud" not in n

def is_cloud_deployed(dep):
    n = norm(dep)
    return "aws" in n or "azure" in n or "gcp" in n or "cloud" in n

def is_fully_cloud(dep):
    n = norm(dep)
    return is_cloud_deployed(dep) and "on-premise" not in n and "on-prem" not in n

def is_containerized(app):
    return norm(app.get("is_containerized", "no")) == "yes"

def arch_type(app):
    a = norm(app.get("application_architecture", ""))
    return a  # "1-tier", "2-tier", "3-tier", "unknown"

# ─────────────────────────────────────────────
# STEP 1: LOAD ALL APPS
# ─────────────────────────────────────────────
apps = {}
for path in sorted(glob.glob(os.path.join(APP_DIR, "app*.json"))):
    with open(path) as f:
        a = json.load(f)
    apps[a["app_id"]] = a

print(f"Loaded {len(apps)} apps")

# ─────────────────────────────────────────────
# STEP 2: OUT-OF-SCOPE ASSESSMENT
# ─────────────────────────────────────────────
RETIRED_IDS = {"app005", "app007", "app009", "app029"}

def make_oos(app):
    status = norm(app.get("application_status", ""))
    sol_type = norm(app.get("solution_type", ""))
    is_retired = status == "retired"
    is_sap = "sap" in sol_type
    oos = is_retired or is_sap
    reasons = []
    if is_retired:
        reasons.append("Application status is Retired")
    if is_sap:
        reasons.append("Solution type is SAP")
    return {
        "app_id": app["app_id"],
        "app_name": app["app_name"],
        "out_of_scope": oos,
        "reasons": reasons if reasons else ["In scope for assessment"],
        "application_status": app.get("application_status"),
        "solution_type": app.get("solution_type"),
        "analysis_timestamp": TIMESTAMP
    }

for app_id, app in apps.items():
    result = make_oos(app)
    path = os.path.join(OUT_OOS, f"out_of_scope_{app_id}.json")
    with open(path, "w") as f:
        json.dump(result, f, indent=2)

print("Out-of-scope files written")

# In-scope apps
in_scope = {k: v for k, v in apps.items() if k not in RETIRED_IDS}
print(f"In-scope apps: {len(in_scope)}")

# ─────────────────────────────────────────────
# STEP 3: TECHNOLOGY ASSESSMENT
# ─────────────────────────────────────────────
def assess_component(name, status, category):
    if not name or norm(name) in ("", "none", "null"):
        return None
    return {
        "component_name": name,
        "component_category": category,
        "version_identified": name,
        "lifecycle_status": status if status else "NO_KNOWLEDGE",
        "analysis_timestamp": TIMESTAMP
    }

def make_tech_assessment(app):
    os_str  = app.get("operating_system")
    lang    = app.get("programming_language")
    server  = app.get("application_server")
    db      = app.get("database_engine")

    os_status   = lookup(os_str, OS_MAP)
    lang_status = lookup(lang, LANG_MAP)
    db_status   = lookup(db, DB_MAP)

    # app server – normalise messy strings
    server_key = norm(server)
    srv_status = None
    if server_key and server_key not in ("none", "null", ""):
        srv_status = lookup(server_key, SERVER_MAP)

    components = []
    if os_str:
        components.append(assess_component(os_str, os_status, "Operating System"))
    if lang:
        components.append(assess_component(lang, lang_status, "Programming Language"))
    if server and norm(server) not in ("none", "null", ""):
        components.append(assess_component(server, srv_status, "Application Server"))
    if db:
        components.append(assess_component(db, db_status, "Database Engine"))

    # overall risk
    statuses = [c["lifecycle_status"] for c in components if c]
    if "EOL" in statuses:
        overall = "HIGH_RISK"
    elif "OUTDATED" in statuses:
        overall = "MEDIUM_RISK"
    elif all(s == "CURRENT_VERSION" for s in statuses):
        overall = "LOW_RISK"
    else:
        overall = "UNKNOWN"

    return {
        "app_id": app["app_id"],
        "app_name": app["app_name"],
        "analysis_timestamp": TIMESTAMP,
        "overall_risk": overall,
        "components": components,
        "technology_summary": {
            "operating_system": {"name": os_str, "status": os_status},
            "programming_language": {"name": lang, "status": lang_status},
            "application_server": {"name": server, "status": srv_status},
            "database_engine": {"name": db, "status": db_status},
        }
    }

tech_results = {}
for app_id, app in in_scope.items():
    result = make_tech_assessment(app)
    tech_results[app_id] = result
    path = os.path.join(OUT_TECH, f"technology_assessment_{app_id}.json")
    with open(path, "w") as f:
        json.dump(result, f, indent=2)

print("Technology assessment files written")

# ─────────────────────────────────────────────
# STEP 4: COMPLEXITY ASSESSMENT
# ─────────────────────────────────────────────
def count_tech_debt(tech):
    """Count EOL + OUTDATED components."""
    count = 0
    for c in tech["components"]:
        if c and c["lifecycle_status"] in ("EOL", "OUTDATED"):
            count += 1
    return count

def score_complexity(app, tech):
    dep = app.get("deployment_type", "")
    sc  = server_count(app)
    ext = int(app.get("external_interface_count", 0) or 0)
    api = int(app.get("api_endpoint_count", 0) or 0)
    crit = norm(app.get("business_criticality", ""))
    db_gb = float(app.get("database_storage_gb", 0) or 0)
    cicd = norm(app.get("ci_cd_present", "no"))
    cont = is_containerized(app)
    debt = count_tech_debt(tech)

    # Factor scores
    f_servers = 1 if sc == 1 else 2 if sc <= 3 else 3
    f_ext = 0 if ext <= 4 else 1 if ext <= 10 else 2
    f_api = 0 if api <= 5 else 1 if api <= 20 else 2
    f_crit = {"low": 0, "medium": 1, "high": 2, "critical": 3}.get(crit, 1)
    f_debt = min(3, debt)
    f_dep = 0 if is_fully_cloud(dep) else 1 if is_cloud_deployed(dep) else 2
    f_db = 0 if db_gb < 200 else 1 if db_gb <= 1000 else 2
    f_cicd = 0 if cicd == "yes" else 1
    f_cont = 0 if cont else 1

    raw = f_servers + f_ext + f_api + f_crit + f_debt + f_dep + f_db + f_cicd + f_cont
    max_raw = 19
    score = max(1, min(10, 1 + round(raw / max_raw * 9)))

    if score <= 3:
        label = "Low"
        multiplier = 1.0
    elif score <= 6:
        label = "Medium"
        multiplier = 1.2
    else:
        label = "High"
        multiplier = 1.5

    return {
        "app_id": app["app_id"],
        "app_name": app["app_name"],
        "analysis_timestamp": TIMESTAMP,
        "complexity_score": score,
        "complexity_label": label,
        "cost_multiplier": multiplier,
        "raw_score": raw,
        "max_raw_score": max_raw,
        "factors": {
            "server_count": {"value": sc, "score": f_servers},
            "external_interfaces": {"value": ext, "score": f_ext},
            "api_endpoints": {"value": api, "score": f_api},
            "business_criticality": {"value": app.get("business_criticality"), "score": f_crit},
            "tech_debt_components": {"value": debt, "score": f_debt},
            "deployment_type": {"value": dep, "score": f_dep},
            "database_storage_gb": {"value": db_gb, "score": f_db},
            "ci_cd_present": {"value": app.get("ci_cd_present"), "score": f_cicd},
            "is_containerized": {"value": app.get("is_containerized"), "score": f_cont},
        }
    }

complexity_results = {}
for app_id, app in in_scope.items():
    result = score_complexity(app, tech_results[app_id])
    complexity_results[app_id] = result
    path = os.path.join(OUT_COMP, f"complexity_{app_id}.json")
    with open(path, "w") as f:
        json.dump(result, f, indent=2)

print("Complexity files written")

# ─────────────────────────────────────────────
# STEP 5: SCENARIO ASSESSMENT
# ─────────────────────────────────────────────
def assess_scenarios(app, tech, comp):
    dep   = app.get("deployment_type", "")
    cont  = is_containerized(app)
    arch  = arch_type(app)
    db_gb = float(app.get("database_storage_gb", 0) or 0)

    ts = tech["technology_summary"]
    os_status  = ts["operating_system"]["status"]
    srv_status = ts["application_server"]["status"]
    db_status  = ts["database_engine"]["status"]

    os_name  = norm(ts["operating_system"]["name"] or "")
    db_name  = norm(ts["database_engine"]["name"] or "")
    srv_name = norm(ts["application_server"]["name"] or "")

    fully_cloud    = is_fully_cloud(dep)
    cloud_deployed = is_cloud_deployed(dep)
    on_prem_only   = is_on_premise_only(dep)

    scenarios = {}

    # 1. os_update_security_patch
    if os_status in ("EOL", "OUTDATED"):
        scenarios["os_update_security_patch"] = "APPLICABLE"
    elif os_status == "CURRENT_VERSION":
        scenarios["os_update_security_patch"] = "NOT_APPLICABLE"
    else:
        scenarios["os_update_security_patch"] = "LACK_OF_DATA"

    # 2. switch_to_standard_linux_os
    if is_windows_or_aix(ts["operating_system"]["name"]):
        scenarios["switch_to_standard_linux_os"] = "APPLICABLE"
    else:
        scenarios["switch_to_standard_linux_os"] = "NOT_APPLICABLE"

    # 3. switch_to_arm_cpu
    if cloud_deployed or cont:
        scenarios["switch_to_arm_cpu"] = "APPLICABLE"
    else:
        scenarios["switch_to_arm_cpu"] = "NOT_APPLICABLE"

    # 4. application_server_replacement
    if srv_status in ("EOL", "OUTDATED"):
        scenarios["application_server_replacement"] = "APPLICABLE"
    elif srv_status == "CURRENT_VERSION":
        scenarios["application_server_replacement"] = "NOT_APPLICABLE"
    elif srv_name in ("", "none", "null") or ts["application_server"]["name"] is None:
        scenarios["application_server_replacement"] = "NOT_APPLICABLE"
    else:
        scenarios["application_server_replacement"] = "LACK_OF_DATA"

    # 5. app_deployment_to_cloud
    if fully_cloud:
        scenarios["app_deployment_to_cloud"] = "FULFILLED"
    else:
        scenarios["app_deployment_to_cloud"] = "APPLICABLE"

    # 6. app_containerization
    if cont:
        scenarios["app_containerization"] = "FULFILLED"
    else:
        scenarios["app_containerization"] = "APPLICABLE"

    # 7. app_refactor_decoupling
    if "1-tier" in arch or "monolith" in arch:
        scenarios["app_refactor_decoupling"] = "APPLICABLE"
    elif "3-tier" in arch:
        scenarios["app_refactor_decoupling"] = "APPLICABLE"
    elif "2-tier" in arch:
        scenarios["app_refactor_decoupling"] = "NOT_APPLICABLE"
    else:
        scenarios["app_refactor_decoupling"] = "LACK_OF_DATA"

    # 8. upgrade_legacy_databases
    if db_status in ("EOL", "OUTDATED"):
        scenarios["upgrade_legacy_databases"] = "APPLICABLE"
    elif db_status == "CURRENT_VERSION":
        scenarios["upgrade_legacy_databases"] = "NOT_APPLICABLE"
    else:
        scenarios["upgrade_legacy_databases"] = "LACK_OF_DATA"

    # 9. switch_to_managed_db
    if db_name in MANAGED_DBS:
        scenarios["switch_to_managed_db"] = "NOT_APPLICABLE"
    else:
        scenarios["switch_to_managed_db"] = "APPLICABLE"

    # 10. managed_arm_db (applicable if switch_to_managed_db is APPLICABLE)
    if scenarios["switch_to_managed_db"] == "APPLICABLE":
        scenarios["managed_arm_db"] = "APPLICABLE"
    else:
        scenarios["managed_arm_db"] = "NOT_APPLICABLE"

    # 11. serverless_db_migration
    if db_gb < 100 and cloud_deployed:
        scenarios["serverless_db_migration"] = "APPLICABLE"
    else:
        scenarios["serverless_db_migration"] = "NOT_APPLICABLE"

    # 12. switch_db_engine_postgresql
    if db_name in POSTGRESQL_TARGET_DBS:
        scenarios["switch_db_engine_postgresql"] = "APPLICABLE"
    elif db_name in ALREADY_POSTGRESQL_DBS:
        scenarios["switch_db_engine_postgresql"] = "NOT_APPLICABLE"
    else:
        scenarios["switch_db_engine_postgresql"] = "NOT_APPLICABLE"

    # Build structured list
    scenario_list = []
    for scen_id in ALL_SCENARIOS:
        status = scenarios.get(scen_id, "LACK_OF_DATA")
        fin = FINANCE.get(scen_id, {})
        scenario_list.append({
            "scenario_id": scen_id,
            "status": status,
            "migration_cost_base": fin.get("migration", 0),
            "yearly_savings_base": fin.get("yearly_savings", 0),
        })

    return {
        "app_id": app["app_id"],
        "app_name": app["app_name"],
        "analysis_timestamp": TIMESTAMP,
        "complexity_label": comp["complexity_label"],
        "cost_multiplier": comp["cost_multiplier"],
        "scenarios": scenario_list,
    }

scenario_results = {}
for app_id, app in in_scope.items():
    result = assess_scenarios(app, tech_results[app_id], complexity_results[app_id])
    scenario_results[app_id] = result
    path = os.path.join(OUT_SCEN, f"scenario_assessment_{app_id}.json")
    with open(path, "w") as f:
        json.dump(result, f, indent=2)

print("Scenario assessment files written")

# ─────────────────────────────────────────────
# STEP 6: BUSINESS CASE
# ─────────────────────────────────────────────
COUNTED_STATUSES = {"APPLICABLE", "PARTIALLY_FULFILLED"}

business_case_apps = []
portfolio_total_cost = 0.0
portfolio_total_savings = 0.0

for app_id, scen_data in scenario_results.items():
    app = in_scope[app_id]
    mult = scen_data["cost_multiplier"]
    app_cost = 0.0
    app_savings = 0.0
    applicable_scenarios = []

    for s in scen_data["scenarios"]:
        if s["status"] in COUNTED_STATUSES:
            cost = s["migration_cost_base"] * mult
            savings = s["yearly_savings_base"]
            app_cost += cost
            app_savings += savings
            applicable_scenarios.append({
                "scenario_id": s["scenario_id"],
                "status": s["status"],
                "migration_cost": round(cost, 2),
                "yearly_savings": savings,
            })

    if app_cost > 0:
        roi_3yr = round((3 * app_savings - app_cost) / app_cost * 100, 1)
        payback = round(app_cost / app_savings, 2) if app_savings > 0 else None
    else:
        roi_3yr = 0
        payback = None

    portfolio_total_cost += app_cost
    portfolio_total_savings += app_savings

    business_case_apps.append({
        "app_id": app_id,
        "app_name": app["app_name"],
        "complexity_label": scen_data["complexity_label"],
        "cost_multiplier": mult,
        "total_migration_cost": round(app_cost, 2),
        "total_yearly_savings": round(app_savings, 2),
        "roi_3yr_pct": roi_3yr,
        "payback_years": payback,
        "applicable_scenarios": applicable_scenarios,
    })

# portfolio metrics
if portfolio_total_cost > 0 and portfolio_total_savings > 0:
    portfolio_roi_3yr = round((3 * portfolio_total_savings - portfolio_total_cost) / portfolio_total_cost * 100, 1)
    portfolio_payback = round(portfolio_total_cost / portfolio_total_savings, 2)
else:
    portfolio_roi_3yr = 0
    portfolio_payback = None

business_case = {
    "analysis_timestamp": TIMESTAMP,
    "portfolio_summary": {
        "total_in_scope_apps": len(in_scope),
        "total_migration_cost": round(portfolio_total_cost, 2),
        "total_yearly_savings": round(portfolio_total_savings, 2),
        "portfolio_roi_3yr_pct": portfolio_roi_3yr,
        "portfolio_payback_years": portfolio_payback,
    },
    "applications": sorted(business_case_apps, key=lambda x: -x["total_migration_cost"])
}

bc_path = os.path.join(OUT_BC, "business_case.json")
with open(bc_path, "w") as f:
    json.dump(business_case, f, indent=2)

print("Business case written")
print(f"  Total migration cost:  ${portfolio_total_cost:,.0f}")
print(f"  Total yearly savings:  ${portfolio_total_savings:,.0f}")
print(f"  Portfolio 3yr ROI:     {portfolio_roi_3yr}%")
print(f"  Portfolio payback:     {portfolio_payback} years")

# ─────────────────────────────────────────────
# STEP 7: REPORTING
# ─────────────────────────────────────────────

STATUS_EMOJI = {"CURRENT_VERSION": "✅", "OUTDATED": "⚠️", "EOL": "🔴", "NO_KNOWLEDGE": "❓", None: "❓"}
RISK_COLOR = {"LOW_RISK": "#2ecc71", "MEDIUM_RISK": "#f39c12", "HIGH_RISK": "#e74c3c", "UNKNOWN": "#95a5a6"}
SCENARIO_LABELS = {
    "os_update_security_patch":        "OS Security Patch",
    "switch_to_standard_linux_os":     "Switch to Linux",
    "switch_to_arm_cpu":               "ARM CPU Migration",
    "application_server_replacement":  "App Server Replacement",
    "app_deployment_to_cloud":         "Cloud Deployment",
    "app_containerization":            "Containerization",
    "app_refactor_decoupling":         "Refactor/Decouple",
    "upgrade_legacy_databases":        "DB Upgrade",
    "switch_to_managed_db":            "Managed DB",
    "managed_arm_db":                  "Managed ARM DB",
    "serverless_db_migration":         "Serverless DB",
    "switch_db_engine_postgresql":     "Switch to PostgreSQL",
}

# ── Per-app markdown ──────────────────────────────────────────────────────────
def make_app_md(app_id):
    app   = in_scope[app_id]
    tech  = tech_results[app_id]
    comp  = complexity_results[app_id]
    scen  = scenario_results[app_id]
    # business case entry
    bc_entry = next((a for a in business_case["applications"] if a["app_id"] == app_id), None)

    lines = []
    lines.append(f"# {app['app_name']} ({app_id}) — Modernization Report\n")
    lines.append(f"**Analysis Date:** {TIMESTAMP}  ")
    lines.append(f"**Business Unit:** {app.get('business_unit', 'N/A')}  ")
    lines.append(f"**Criticality:** {app.get('business_criticality', 'N/A')}  ")
    lines.append(f"**Status:** {app.get('application_status', 'N/A')}  ")
    lines.append(f"**Deployment:** {app.get('deployment_type', 'N/A')}  ")
    lines.append(f"**Architecture:** {app.get('application_architecture', 'N/A')}  ")
    lines.append(f"**Containerized:** {app.get('is_containerized', 'N/A')}  \n")

    lines.append("## Technology Assessment\n")
    lines.append("| Component | Version | Status |")
    lines.append("|-----------|---------|--------|")
    for c in tech["components"]:
        emoji = STATUS_EMOJI.get(c["lifecycle_status"], "❓")
        lines.append(f"| {c['component_category']} | {c['component_name']} | {emoji} {c['lifecycle_status']} |")
    lines.append(f"\n**Overall Risk:** `{tech['overall_risk']}`\n")

    lines.append("## Complexity Assessment\n")
    lines.append(f"**Score:** {comp['complexity_score']}/10 — **{comp['complexity_label']}** (Cost Multiplier: {comp['cost_multiplier']}x)\n")
    lines.append("| Factor | Value | Points |")
    lines.append("|--------|-------|--------|")
    for k, v in comp["factors"].items():
        lines.append(f"| {k.replace('_',' ').title()} | {v['value']} | {v['score']} |")

    lines.append("\n## Scenario Applicability\n")
    lines.append("| Scenario | Status |")
    lines.append("|----------|--------|")
    for s in scen["scenarios"]:
        label = SCENARIO_LABELS.get(s["scenario_id"], s["scenario_id"])
        lines.append(f"| {label} | {s['status']} |")

    if bc_entry:
        lines.append("\n## Business Case\n")
        lines.append(f"| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Total Migration Cost | ${bc_entry['total_migration_cost']:,.0f} |")
        lines.append(f"| Total Yearly Savings | ${bc_entry['total_yearly_savings']:,.0f} |")
        lines.append(f"| 3-Year ROI | {bc_entry['roi_3yr_pct']}% |")
        lines.append(f"| Payback Period | {bc_entry['payback_years']} years |")
        lines.append("\n### Applicable Scenarios Breakdown\n")
        lines.append("| Scenario | Migration Cost | Yearly Savings |")
        lines.append("|----------|----------------|----------------|")
        for s in bc_entry["applicable_scenarios"]:
            label = SCENARIO_LABELS.get(s["scenario_id"], s["scenario_id"])
            lines.append(f"| {label} | ${s['migration_cost']:,.0f} | ${s['yearly_savings']:,.0f} |")

    return "\n".join(lines) + "\n"

for app_id in in_scope:
    md = make_app_md(app_id)
    path = os.path.join(OUT_RPT, "apps", f"{app_id}_report.md")
    with open(path, "w") as f:
        f.write(md)

print("Per-app markdown reports written")

# ── Portfolio markdown ────────────────────────────────────────────────────────
def make_portfolio_md():
    bc = business_case["portfolio_summary"]
    lines = []
    lines.append("# Portfolio Modernization Report\n")
    lines.append(f"**Analysis Date:** {TIMESTAMP}  ")
    lines.append(f"**In-Scope Applications:** {bc['total_in_scope_apps']}  ")
    lines.append(f"**Total Migration Cost:** ${bc['total_migration_cost']:,.0f}  ")
    lines.append(f"**Total Yearly Savings:** ${bc['total_yearly_savings']:,.0f}  ")
    lines.append(f"**3-Year ROI:** {bc['portfolio_roi_3yr_pct']}%  ")
    lines.append(f"**Payback Period:** {bc['portfolio_payback_years']} years\n")

    # Risk distribution
    risk_counts = {}
    for app_id, tech in tech_results.items():
        r = tech["overall_risk"]
        risk_counts[r] = risk_counts.get(r, 0) + 1
    lines.append("## Portfolio Risk Distribution\n")
    lines.append("| Risk Level | Count |")
    lines.append("|------------|-------|")
    for r, c in sorted(risk_counts.items()):
        lines.append(f"| {r} | {c} |")

    # Complexity distribution
    comp_counts = {}
    for app_id, comp in complexity_results.items():
        lbl = comp["complexity_label"]
        comp_counts[lbl] = comp_counts.get(lbl, 0) + 1
    lines.append("\n## Complexity Distribution\n")
    lines.append("| Complexity | Count |")
    lines.append("|------------|-------|")
    for lbl in ["Low", "Medium", "High"]:
        lines.append(f"| {lbl} | {comp_counts.get(lbl, 0)} |")

    # Scenario frequency
    scen_freq = {s: 0 for s in ALL_SCENARIOS}
    for scen_data in scenario_results.values():
        for s in scen_data["scenarios"]:
            if s["status"] in ("APPLICABLE", "PARTIALLY_FULFILLED"):
                scen_freq[s["scenario_id"]] += 1

    lines.append("\n## Scenario Applicability Frequency\n")
    lines.append("| Scenario | Applicable Apps | Bar |")
    lines.append("|----------|-----------------|-----|")
    for scen_id, cnt in sorted(scen_freq.items(), key=lambda x: -x[1]):
        bar = "█" * cnt
        label = SCENARIO_LABELS.get(scen_id, scen_id)
        lines.append(f"| {label} | {cnt} | {bar} |")

    # Top apps by cost
    lines.append("\n## Top Applications by Migration Cost\n")
    lines.append("| App | Name | Cost | Savings/yr | 3yr ROI | Complexity |")
    lines.append("|-----|------|------|-----------|---------|------------|")
    for a in business_case["applications"][:10]:
        lines.append(f"| {a['app_id']} | {a['app_name']} | ${a['total_migration_cost']:,.0f} | ${a['total_yearly_savings']:,.0f} | {a['roi_3yr_pct']}% | {a['complexity_label']} |")

    # All apps summary
    lines.append("\n## All In-Scope Applications Summary\n")
    lines.append("| App ID | Name | Risk | Complexity | Migration Cost | 3yr ROI |")
    lines.append("|--------|------|------|------------|---------------|---------|")
    for app_id in sorted(in_scope.keys()):
        tech = tech_results[app_id]
        comp = complexity_results[app_id]
        bc_e = next((a for a in business_case["applications"] if a["app_id"] == app_id), None)
        cost_str = f"${bc_e['total_migration_cost']:,.0f}" if bc_e else "N/A"
        roi_str  = f"{bc_e['roi_3yr_pct']}%" if bc_e else "N/A"
        lines.append(f"| {app_id} | {in_scope[app_id]['app_name']} | {tech['overall_risk']} | {comp['complexity_label']} | {cost_str} | {roi_str} |")

    return "\n".join(lines) + "\n"

pf_md = make_portfolio_md()
with open(os.path.join(OUT_RPT, "portfolio_report.md"), "w") as f:
    f.write(pf_md)

print("Portfolio markdown report written")

# ─────────────────────────────────────────────
# HTML REPORTS
# ─────────────────────────────────────────────
CSS = """
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
         background: #f4f6f9; color: #2c3e50; }
  .container { max-width: 1200px; margin: 0 auto; padding: 24px; }
  h1 { font-size: 2rem; color: #1a252f; margin-bottom: 8px; }
  h2 { font-size: 1.4rem; color: #2c3e50; margin: 24px 0 12px; border-bottom: 2px solid #3498db; padding-bottom: 6px; }
  h3 { font-size: 1.1rem; color: #34495e; margin: 16px 0 8px; }
  .subtitle { color: #7f8c8d; font-size: 0.95rem; margin-bottom: 24px; }
  .cards { display: flex; flex-wrap: wrap; gap: 16px; margin: 16px 0; }
  .card { background: #fff; border-radius: 10px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,.08);
          flex: 1; min-width: 180px; }
  .card .label { font-size: 0.8rem; color: #7f8c8d; text-transform: uppercase; letter-spacing: .5px; }
  .card .value { font-size: 1.8rem; font-weight: 700; color: #2c3e50; margin-top: 4px; }
  .card .sub { font-size: 0.85rem; color: #95a5a6; margin-top: 2px; }
  .badge { display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 0.78rem;
           font-weight: 600; text-transform: uppercase; letter-spacing: .4px; }
  .badge-EOL          { background: #fde8e8; color: #c0392b; }
  .badge-OUTDATED     { background: #fef9e7; color: #d35400; }
  .badge-CURRENT_VERSION { background: #eafaf1; color: #1e8449; }
  .badge-NO_KNOWLEDGE { background: #f4f6f9; color: #7f8c8d; }
  .badge-APPLICABLE   { background: #ebf5fb; color: #1a5276; }
  .badge-FULFILLED    { background: #eafaf1; color: #1e8449; }
  .badge-NOT_APPLICABLE { background: #f4f6f9; color: #7f8c8d; }
  .badge-LACK_OF_DATA { background: #fef9e7; color: #9b7e00; }
  .badge-HIGH_RISK    { background: #fde8e8; color: #c0392b; }
  .badge-MEDIUM_RISK  { background: #fef9e7; color: #d35400; }
  .badge-LOW_RISK     { background: #eafaf1; color: #1e8449; }
  .badge-High   { background: #fde8e8; color: #c0392b; }
  .badge-Medium { background: #fef9e7; color: #d35400; }
  .badge-Low    { background: #eafaf1; color: #1e8449; }
  table { width: 100%; border-collapse: collapse; font-size: 0.88rem; background: #fff;
          border-radius: 8px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
  th { background: #2c3e50; color: #ecf0f1; padding: 10px 12px; text-align: left; }
  td { padding: 9px 12px; border-bottom: 1px solid #ecf0f1; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: #f8f9fa; }
  .chart-bar { display: inline-block; height: 16px; background: #3498db; border-radius: 3px;
               vertical-align: middle; min-width: 4px; }
  .app-card { background: #fff; border-radius: 10px; padding: 16px; margin: 12px 0;
              box-shadow: 0 2px 6px rgba(0,0,0,.07); border-left: 4px solid #3498db; }
  .app-card.high-risk { border-left-color: #e74c3c; }
  .app-card.medium-risk { border-left-color: #f39c12; }
  .app-card.low-risk { border-left-color: #2ecc71; }
  .mermaid-wrap { background: #fff; border-radius: 10px; padding: 20px;
                  box-shadow: 0 2px 8px rgba(0,0,0,.08); margin: 16px 0; }
  .section { background: #fff; border-radius: 10px; padding: 20px;
             box-shadow: 0 2px 8px rgba(0,0,0,.08); margin: 16px 0; }
  .flex2 { display: flex; gap: 16px; flex-wrap: wrap; }
  .flex2 > * { flex: 1; min-width: 300px; }
</style>
"""

MERMAID_CDN = '<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>\n<script>mermaid.initialize({startOnLoad:true});</script>'

def badge(text):
    cls = text.replace(" ", "_").replace("/", "_")
    return f'<span class="badge badge-{cls}">{text}</span>'

def make_app_html(app_id):
    app  = in_scope[app_id]
    tech = tech_results[app_id]
    comp = complexity_results[app_id]
    scen = scenario_results[app_id]
    bc_e = next((a for a in business_case["applications"] if a["app_id"] == app_id), None)

    risk_cls = tech["overall_risk"].lower().replace("_", "-")

    # Mermaid pie for risk
    risk_counts_local = {}
    for c in tech["components"]:
        s = c["lifecycle_status"]
        risk_counts_local[s] = risk_counts_local.get(s, 0) + 1
    pie_data = " ".join([f'"{k}" : {v}' for k, v in risk_counts_local.items()])
    mermaid_pie = f'<div class="mermaid">pie title Component Status\n{pie_data}\n</div>'

    # Mermaid bar for scenarios (xychart)
    app_counts = {"APPLICABLE":0,"FULFILLED":0,"NOT_APPLICABLE":0,"LACK_OF_DATA":0}
    for s in scen["scenarios"]:
        k = s["status"]
        app_counts[k] = app_counts.get(k, 0) + 1
    bar_categories = ' '.join([f'"{k}"' for k in app_counts.keys()])
    bar_values     = ' '.join([str(v) for v in app_counts.values()])
    mermaid_bar = f'''<div class="mermaid">
xychart-beta
  title "Scenario Status Distribution"
  x-axis [{bar_categories}]
  y-axis "Count" 0 --> {max(app_counts.values())+1}
  bar [{bar_values}]
</div>'''

    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{app['app_name']} Modernization Report</title>
{CSS}
{MERMAID_CDN}
</head>
<body>
<div class="container">
  <h1>{app['app_name']}</h1>
  <p class="subtitle">{app_id} &nbsp;|&nbsp; {app.get('business_unit','N/A')} &nbsp;|&nbsp; {app.get('app_description','')}</p>

  <div class="cards">
    <div class="card"><div class="label">Criticality</div><div class="value" style="font-size:1.2rem">{badge(app.get('business_criticality','N/A'))}</div></div>
    <div class="card"><div class="label">Overall Risk</div><div class="value" style="font-size:1.2rem">{badge(tech['overall_risk'])}</div></div>
    <div class="card"><div class="label">Complexity</div><div class="value">{comp['complexity_score']}/10</div><div class="sub">{badge(comp['complexity_label'])}</div></div>
    <div class="card"><div class="label">Migration Cost</div><div class="value" style="font-size:1.4rem">${f"{bc_e['total_migration_cost']:,.0f}" if bc_e else "0"}</div></div>
    <div class="card"><div class="label">Yearly Savings</div><div class="value" style="font-size:1.4rem">${f"{bc_e['total_yearly_savings']:,.0f}" if bc_e else "0"}</div></div>
    <div class="card"><div class="label">3-Year ROI</div><div class="value">{bc_e['roi_3yr_pct'] if bc_e else 0}%</div></div>
  </div>

  <div class="flex2">
    <div class="mermaid-wrap">{mermaid_pie}</div>
    <div class="mermaid-wrap">{mermaid_bar}</div>
  </div>

  <h2>Technology Assessment</h2>
  <div class="section">
    <table>
      <tr><th>Category</th><th>Component</th><th>Status</th></tr>
"""
    for c in tech["components"]:
        html += f"      <tr><td>{c['component_category']}</td><td>{c['component_name']}</td><td>{badge(c['lifecycle_status'])}</td></tr>\n"
    html += "    </table>\n  </div>\n"

    html += "\n  <h2>Scenario Assessment</h2>\n  <div class=\"section\">\n    <table>\n      <tr><th>Scenario</th><th>Status</th><th>Migration Cost</th><th>Yearly Savings</th></tr>\n"
    for s in scen["scenarios"]:
        label = SCENARIO_LABELS.get(s["scenario_id"], s["scenario_id"])
        fin   = FINANCE.get(s["scenario_id"], {})
        mult  = comp["cost_multiplier"]
        cost_str = f"${fin['migration'] * mult:,.0f}" if s["status"] in COUNTED_STATUSES else "—"
        sav_str  = f"${fin['yearly_savings']:,.0f}" if s["status"] in COUNTED_STATUSES else "—"
        html += f"      <tr><td>{label}</td><td>{badge(s['status'])}</td><td>{cost_str}</td><td>{sav_str}</td></tr>\n"
    html += "    </table>\n  </div>\n"

    if bc_e:
        html += f"""
  <h2>Business Case</h2>
  <div class="section">
    <div class="cards">
      <div class="card"><div class="label">Total Cost</div><div class="value" style="font-size:1.3rem">${bc_e['total_migration_cost']:,.0f}</div></div>
      <div class="card"><div class="label">Yearly Savings</div><div class="value" style="font-size:1.3rem">${bc_e['total_yearly_savings']:,.0f}</div></div>
      <div class="card"><div class="label">3-Year ROI</div><div class="value">{bc_e['roi_3yr_pct']}%</div></div>
      <div class="card"><div class="label">Payback</div><div class="value">{bc_e['payback_years']} yrs</div></div>
    </div>
  </div>
"""
    html += "</div></body></html>\n"
    return html

for app_id in in_scope:
    html = make_app_html(app_id)
    path = os.path.join(OUT_RPT, "application_reports", f"application_report_{app_id}.html")
    with open(path, "w") as f:
        f.write(html)

print("Per-app HTML reports written")

# ── Portfolio HTML ─────────────────────────────────────────────────────────────
def make_portfolio_html():
    bc = business_case["portfolio_summary"]

    # risk distribution for pie
    risk_counts = {}
    for app_id, tech in tech_results.items():
        r = tech["overall_risk"]
        risk_counts[r] = risk_counts.get(r, 0) + 1
    pie_data = "\n".join([f'"{k}" : {v}' for k, v in risk_counts.items()])
    mermaid_pie = f'<div class="mermaid">pie title Portfolio Risk\n{pie_data}\n</div>'

    # scenario frequency bar
    scen_freq = {s: 0 for s in ALL_SCENARIOS}
    for scen_data in scenario_results.values():
        for s in scen_data["scenarios"]:
            if s["status"] in ("APPLICABLE", "PARTIALLY_FULFILLED"):
                scen_freq[s["scenario_id"]] += 1

    top_scens = sorted(scen_freq.items(), key=lambda x: -x[1])[:8]
    bar_cats   = " ".join([f'"{SCENARIO_LABELS.get(s,"")[:15]}"' for s, _ in top_scens])
    bar_vals   = " ".join([str(c) for _, c in top_scens])
    max_val    = max(c for _, c in top_scens) + 2
    mermaid_bar = f'''<div class="mermaid">
xychart-beta
  title "Top Scenario Applicability Count"
  x-axis [{bar_cats}]
  y-axis "Apps" 0 --> {max_val}
  bar [{bar_vals}]
</div>'''

    # scenario text-based chart
    scen_chart_rows = ""
    max_cnt = max(scen_freq.values()) if scen_freq else 1
    for scen_id in ALL_SCENARIOS:
        cnt = scen_freq[scen_id]
        bar_pct = int(cnt / max_cnt * 200) if max_cnt > 0 else 0
        label = SCENARIO_LABELS.get(scen_id, scen_id)
        scen_chart_rows += f"""
      <tr>
        <td style="width:200px;white-space:nowrap">{label}</td>
        <td><div class="chart-bar" style="width:{bar_pct}px"></div> {cnt}</td>
      </tr>"""

    # app cards
    app_cards_html = ""
    for a in business_case["applications"]:
        tech = tech_results[a["app_id"]]
        risk_cls = tech["overall_risk"].lower().replace("_", "-")
        app_cards_html += f"""
    <div class="app-card {risk_cls}">
      <strong>{a['app_name']}</strong> ({a['app_id']})
      &nbsp;{badge(tech['overall_risk'])}&nbsp;{badge(a['complexity_label'])}
      &nbsp;&nbsp;Cost: <strong>${a['total_migration_cost']:,.0f}</strong>
      &nbsp;Savings: <strong>${a['total_yearly_savings']:,.0f}/yr</strong>
      &nbsp;ROI: <strong>{a['roi_3yr_pct']}%</strong>
    </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Portfolio Modernization Report</title>
{CSS}
{MERMAID_CDN}
</head>
<body>
<div class="container">
  <h1>Portfolio Modernization Report</h1>
  <p class="subtitle">Analysis Date: {TIMESTAMP} &nbsp;|&nbsp; In-Scope Applications: {bc['total_in_scope_apps']}</p>

  <div class="cards">
    <div class="card"><div class="label">In-Scope Apps</div><div class="value">{bc['total_in_scope_apps']}</div></div>
    <div class="card"><div class="label">Total Migration Cost</div><div class="value" style="font-size:1.3rem">${bc['total_migration_cost']:,.0f}</div></div>
    <div class="card"><div class="label">Total Yearly Savings</div><div class="value" style="font-size:1.3rem">${bc['total_yearly_savings']:,.0f}</div></div>
    <div class="card"><div class="label">3-Year Portfolio ROI</div><div class="value">{bc['portfolio_roi_3yr_pct']}%</div></div>
    <div class="card"><div class="label">Payback Period</div><div class="value">{bc['portfolio_payback_years']} yrs</div></div>
  </div>

  <div class="flex2">
    <div class="mermaid-wrap">{mermaid_pie}</div>
    <div class="mermaid-wrap">{mermaid_bar}</div>
  </div>

  <h2>Scenario Applicability Frequency</h2>
  <div class="section">
    <table><tr><th>Scenario</th><th>Count (out of {bc['total_in_scope_apps']} apps)</th></tr>
    {scen_chart_rows}
    </table>
  </div>

  <h2>Business Case Summary</h2>
  <div class="section">
    <table>
      <tr><th>App ID</th><th>Name</th><th>Risk</th><th>Complexity</th><th>Migration Cost</th><th>Yearly Savings</th><th>3yr ROI</th><th>Payback</th></tr>
"""
    for a in sorted(business_case["applications"], key=lambda x: x["app_id"]):
        tech = tech_results[a["app_id"]]
        html += f"""      <tr>
        <td>{a['app_id']}</td><td>{a['app_name']}</td>
        <td>{badge(tech['overall_risk'])}</td>
        <td>{badge(a['complexity_label'])}</td>
        <td>${a['total_migration_cost']:,.0f}</td>
        <td>${a['total_yearly_savings']:,.0f}</td>
        <td>{a['roi_3yr_pct']}%</td>
        <td>{a['payback_years']} yrs</td>
      </tr>\n"""

    html += f"""    </table>
  </div>

  <h2>Per-Application Cards</h2>
  {app_cards_html}

</div>
</body></html>
"""
    return html

pf_html = make_portfolio_html()
with open(os.path.join(OUT_RPT, "portfolio_modernization_report.html"), "w") as f:
    f.write(pf_html)

print("Portfolio HTML report written")
print("\n✅ All outputs generated successfully!")
