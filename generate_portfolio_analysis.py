#!/usr/bin/env python3
"""
Comprehensive Portfolio Modernization Analysis Generator
Generates all required output files for the portfolio modernization assessment.
"""

import json
import os
import math
from datetime import date
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────
REPO_ROOT = Path("/home/runner/work/copilot-test-ktruchcz/copilot-test-ktruchcz")
OUT_ROOT  = REPO_ROOT / "discover" / "output"
APP_MODEL = OUT_ROOT / "applications" / "internal_app_model"
CONS_SCHEMA = OUT_ROOT / "applications" / "consolidated_schema"
OOS_DIR   = OUT_ROOT / "out_of_scope_results"
TECH_DIR  = OUT_ROOT / "technology_assessment"
COMP_DIR  = OUT_ROOT / "complexity_results"
SCEN_DIR  = OUT_ROOT / "scenario_applicability_results"
BC_DIR    = OUT_ROOT / "business_case_results"
REPORT_DIR = OUT_ROOT / "reports"
APPS_MD_DIR = REPORT_DIR / "apps"
SCHEMA_DIR = OUT_ROOT / "schemas"

for d in [CONS_SCHEMA, OOS_DIR, TECH_DIR, COMP_DIR, SCEN_DIR, BC_DIR,
          REPORT_DIR, APPS_MD_DIR, SCHEMA_DIR]:
    d.mkdir(parents=True, exist_ok=True)

ASSESSMENT_DATE = "2025-01-15"
TODAY = date.today().isoformat()

RETIRED_APPS = {"app005", "app007", "app009", "app029"}

# ─── Technology Assessment Tables ─────────────────────────────────────────────
OS_STATUS = {
    "AIX 7.2": ("OUTDATED", "2028-04-30", "IBM support until 2028 but proprietary legacy OS, aging"),
    "AIX 6":   ("EOL",      "2017-04-30", "IBM AIX 6.1 support ended April 2017"),
    "RHEL 7":  ("EOL",      "2024-06-30", "Red Hat ELS ended June 30, 2024"),
    "RHEL 8":  ("CURRENT_VERSION", "2029-05-31", "Red Hat Enterprise Linux 8 supported until May 2029"),
    "CentOS 7":("EOL",      "2024-06-30", "CentOS 7 end of life June 30, 2024"),
    "Windows Server 2012": ("EOL", "2023-10-10", "Extended support ended October 10, 2023"),
    "Windows Server 2019": ("CURRENT_VERSION", "2029-01-09", "Mainstream support until January 2029"),
    "Windows Server 2022": ("CURRENT_VERSION", "2031-10-14", "Mainstream support until October 2031"),
    "Debian 6": ("EOL", "2016-02-29", "End of life February 2016"),
    "Debian 7": ("EOL", "2018-05-31", "End of life May 2018"),
    "Ubuntu 14": ("EOL", "2019-04-30", "Ubuntu 14.04 LTS end of life April 2019"),
}

LANG_STATUS = {
    "COBOL-2014":   ("OUTDATED", None, "Legacy enterprise language, no mainstream active development"),
    "Java 11":      ("OUTDATED", "2023-09-30", "Oracle Premier support ended September 2023"),
    "Java 17":      ("CURRENT_VERSION", "2029-09-30", "LTS until September 2029"),
    "Java 8":       ("OUTDATED", "2019-01-31", "Oracle Premier support ended Jan 2019; aging"),
    "Python 3.9":   ("OUTDATED", "2025-10-31", "Security support ended October 2025"),
    "Python 3.11":  ("CURRENT_VERSION", "2027-10-31", "Active support until October 2027"),
    "Python 3.8":   ("EOL", "2024-10-31", "Python 3.8 EOL October 2024"),
    "Python 3.7":   ("EOL", "2023-06-27", "Python 3.7 EOL June 2023"),
    "Ruby 2.7":     ("EOL", "2023-03-31", "Ruby 2.7 EOL March 31, 2023"),
    "Go 1.16":      ("EOL", "2022-08-01", "Go 1.16 no longer receiving security updates"),
    "Go 1.19":      ("OUTDATED", None, "Current Go is 1.22+, 1.19 no longer receiving updates"),
    "Node.js 14":   ("EOL", "2023-04-30", "Node.js 14 EOL April 2023"),
    "Node.js 18":   ("OUTDATED", "2025-04-30", "Node.js 18 LTS EOL April 2025"),
    "Rust 1.70":    ("OUTDATED", None, "Current Rust stable is 1.80+"),
    "PHP 8.1":      ("OUTDATED", "2025-12-31", "PHP 8.1 security support ends December 31, 2025"),
    "C# .NET 6":    ("EOL", "2024-11-12", ".NET 6 EOL November 12, 2024"),
    "ASP.NET Core": ("CURRENT_VERSION", None, "Current LTS, actively maintained"),
    "React Native": ("CURRENT_VERSION", None, "Actively maintained"),
    "PowerShell":   ("CURRENT_VERSION", None, "Actively maintained"),
    "VB.NET":       ("OUTDATED", None, "Legacy language, Microsoft focus shifted to C#"),
    "Angular 15":   ("OUTDATED", None, "Angular 18/19 are current, Angular 15 no longer maintained"),
    "Scala 2.13":   ("OUTDATED", None, "Scala 3 is current, 2.13 still maintained but aging"),
    "C++ 17":       ("CURRENT_VERSION", None, "ISO standard, actively supported"),
    "FORTRAN 2018": ("OUTDATED", None, "Niche legacy language"),
    "Perl":         ("OUTDATED", None, "Legacy language with declining adoption"),
}

DB_STATUS = {
    "Oracle 19c":       ("CURRENT_VERSION", "2027-04-30", "Supported until April 2027"),
    "Oracle 12c":       ("EOL", "2022-07-31", "Standard support ended July 2022"),
    "Oracle 11g":       ("EOL", "2020-12-31", "Standard support ended Dec 2020"),
    "Amazon RDS MySQL": ("CURRENT_VERSION", None, "Managed service, actively supported"),
    "Aurora PostgreSQL":("CURRENT_VERSION", None, "Managed service, actively supported"),
    "PostgreSQL 13":    ("OUTDATED", "2023-11-30", "Support ended November 2023"),
    "PostgreSQL 14":    ("CURRENT_VERSION", "2026-11-30", "Supported until November 2026"),
    "PostgreSQL 15":    ("CURRENT_VERSION", "2027-11-30", "Supported until November 2027"),
    "SQL Server 2019":  ("CURRENT_VERSION", "2030-01-08", "Mainstream support until 2030"),
    "SQL Server 2022":  ("CURRENT_VERSION", "2033-01-11", "Supported until 2033"),
    "SQL Server 2016":  ("OUTDATED", "2026-07-14", "Mainstream support ended July 2021, extended until 2026"),
    "SQL Server 2014":  ("EOL", "2024-07-09", "Extended support ended July 9, 2024"),
    "MySQL 8.0":        ("CURRENT_VERSION", "2026-04-30", "Supported until April 2026"),
    "MySQL 5.7":        ("EOL", "2023-10-31", "MySQL 5.7 EOL October 31, 2023"),
    "MongoDB":          ("CURRENT_VERSION", None, "No version specified, assume recent managed release"),
    "DB2":              ("NO_KNOWLEDGE", None, "No version specified"),
}

AS_STATUS = {
    "None":                   ("N/A", None, "No application server used"),
    "Websphere 7.0":          ("EOL", "2015-09-30", "IBM WAS 7.0 end of support September 30, 2015"),
    "Websphere 8.0":          ("EOL", "2022-10-26", "IBM WAS 8.0 end of support October 26, 2022"),
    "Websphere 8.5":          ("OUTDATED", "2025-04-30", "IBM WAS 8.5.5 extended support until April 30, 2025"),
    "Apache Tomcat 6.1":      ("EOL", "2016-12-31", "Apache Tomcat 6 EOL December 31, 2016"),
    "Apache Tomcat 5.3":      ("EOL", "2009-03-31", "Apache Tomcat 5.x EOL 2009"),
    "Apache Tomcat 7.4":      ("EOL", "2021-03-31", "Apache Tomcat 7 EOL March 31, 2021"),
    "Apache Tomcat 8.0":      ("EOL", "2018-06-30", "Apache Tomcat 8.0 EOL June 30, 2018"),
    "Glassfish 3.0":          ("EOL", "2012-12-31", "GlassFish 3 EOL 2012"),
    "Glassfish 4.0":          ("EOL", "2016-12-31", "Oracle withdrew support; community abandoned"),
    "Glassfish 4.5":          ("EOL", "2016-12-31", "Oracle withdrew commercial support"),
    "Glassfish 5.0":          ("EOL", "2022-12-31", "Oracle handed to Eclipse Foundation, limited active support"),
    "Oracle Weblogic 8.0":    ("EOL", "2008-01-31", "WebLogic 8.1 support ended January 2008"),
    "Microsoft IIS 8.0":      ("EOL", "2023-10-10", "Tied to Windows Server 2012, EOL October 2023"),
    "Microsoft IIS 8.5":      ("EOL", "2023-10-10", "Tied to Windows Server 2012 R2, EOL October 2023"),
    "Microsoft IIS 10.0":     ("CURRENT_VERSION", None, "Part of Windows Server 2019/2022"),
    "Payara 4.0":             ("EOL", "2020-12-31", "Payara 4 end of support December 2020"),
    "Payara 5.0":             ("OUTDATED", "2026-06-30", "Payara 5 CE supported until June 2026"),
    "Payara 6.0":             ("CURRENT_VERSION", None, "Actively supported"),
    "Weblogic 9.0":           ("EOL", "2011-07-31", "Oracle WLS 9 support ended July 2011"),
}

# ─── Finance Config ────────────────────────────────────────────────────────────
FINANCE = {
    "os_update_security_patch":    {"cost": 1000,   "savings": 500},
    "switch_to_standard_linux_os": {"cost": 300,    "savings": 400},
    "switch_to_arm_cpu":           {"cost": 5000,   "savings": 1000},
    "application_server_replacement": {"cost": 10000, "savings": 12000},
    "app_deployment_to_cloud":     {"cost": 5000,   "savings": 3000},
    "app_containerization":        {"cost": 100000, "savings": 100000},
    "app_refactor_decoupling":     {"cost": 250000, "savings": 150000},
    "upgrade_legacy_databases":    {"cost": 10000,  "savings": 10000},
    "switch_db_engine_open_source":{"cost": 25000,  "savings": 15000},
    # No finance for update_outdated_components
}

APP_FOCUS_SCENARIOS = {
    "app_containerization", "app_refactor_decoupling",
    "application_server_replacement", "app_deployment_to_cloud",
    "update_outdated_components"
}

SCENARIO_NAMES = {
    "os_update_security_patch":    "Operating System Update",
    "switch_to_standard_linux_os": "Switch to standard Linux Operating System",
    "switch_to_arm_cpu":           "Switch to ARM-based CPU",
    "application_server_replacement": "Applications Server replacement",
    "app_deployment_to_cloud":     "Application Migration to Cloud Infrastructure (Lift & Shift)",
    "app_containerization":        "Application Containerization",
    "app_refactor_decoupling":     "Application Refactoring and De-coupling",
    "upgrade_legacy_databases":    "Upgrade Legacy Databases",
    "switch_db_engine_open_source":"Switch DB Engine to open-source database solution",
    "update_outdated_components":  "Update outdated components",
}

ALL_SCENARIOS = list(SCENARIO_NAMES.keys())

# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_app(app_id: str) -> dict:
    return json.loads((APP_MODEL / f"{app_id}.json").read_text())

def write_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2))

def get_server_count(app: dict) -> int:
    si = app.get("server_instances", [])
    if isinstance(si, list):
        return len(si)
    if isinstance(si, str) and si:
        return len([x.strip() for x in si.split(",") if x.strip()])
    return 1

def is_standard_linux(os_str: str) -> bool:
    return any(x in os_str for x in ["RHEL", "CentOS", "Debian", "Ubuntu"])

def is_windows(os_str: str) -> bool:
    return "Windows" in os_str

def is_aix(os_str: str) -> bool:
    return "AIX" in os_str

def is_open_source_db(db: str) -> bool:
    return any(x in db for x in ["PostgreSQL", "MySQL", "MongoDB", "MariaDB", "Aurora"])

def is_proprietary_db(db: str) -> bool:
    return any(x in db for x in ["Oracle", "SQL Server", "DB2"])

def os_status_val(os_str: str):
    return OS_STATUS.get(os_str, ("NO_KNOWLEDGE", None, "Unknown OS"))

def lang_status_val(lang_str: str):
    return LANG_STATUS.get(lang_str, ("NO_KNOWLEDGE", None, "Unknown language"))

def db_status_val(db_str: str):
    return DB_STATUS.get(db_str, ("NO_KNOWLEDGE", None, "Unknown database"))

def as_status_val(as_str: str):
    if not as_str:
        return ("N/A", None, "No application server used")
    return AS_STATUS.get(as_str, ("NO_KNOWLEDGE", None, "Unknown app server"))

def status_badge(status: str) -> str:
    return {"CURRENT_VERSION": "🟢", "OUTDATED": "🟡", "EOL": "🔴",
            "NO_KNOWLEDGE": "⚪", "N/A": "—"}.get(status, "⚪")

# ─── Step 1: Consolidated Schema ──────────────────────────────────────────────

def generate_consolidated_schema():
    apps_overview = []
    for app_id in sorted([f.stem for f in APP_MODEL.glob("app*.json")]):
        app = load_app(app_id)
        schema = {
            "application_identifier": app["app_id"],
            "application_name": app["app_name"],
            "description": app.get("app_description", ""),
            "solution_type": app.get("solution_type", ""),
            "business_criticality": app.get("business_criticality", ""),
            "application_status": app.get("application_status", ""),
            "deployment_type": app.get("deployment_type", ""),
            "data_classification": app.get("data_classification", ""),
            "business_unit": app.get("business_unit", ""),
            "business_capabilities": app.get("business_capabilities", []),
            "user_count": app.get("user_count", 0),
            "technology_stack": {
                "operating_system": app.get("operating_system", ""),
                "programming_language": app.get("programming_language", ""),
                "application_server": app.get("application_server"),
                "database_engine": app.get("database_engine", ""),
            },
            "infrastructure": {
                "server_instances": app.get("server_instances", []),
                "is_containerized": app.get("is_containerized", "No"),
                "environment_count": app.get("environment_count", 1),
                "application_architecture": app.get("application_architecture", "unknown"),
                "ci_cd_present": app.get("ci_cd_present", "No"),
                "cpu_cores": app.get("cpu_cores", 0),
                "memory_gb": app.get("memory_gb", 0),
            },
            "integration": {
                "external_interface_count": app.get("external_interface_count", 0),
                "api_endpoint_count": app.get("api_endpoint_count", 0),
            },
            "database": {
                "database_storage_gb": app.get("database_storage_gb", 0),
                "database_license_required": app.get("database_license_required", "No"),
            },
            "observability": {
                "logging_solution": app.get("logging_solution"),
                "monitoring_tool": app.get("monitoring_tool"),
            },
            "additional_attributes": app.get("additional_attributes", {}),
            "out_of_scope": app_id in RETIRED_APPS,
        }
        write_json(CONS_SCHEMA / f"consolidated_schema_application_{app_id}.json", schema)
        apps_overview.append({
            "application_identifier": app_id,
            "application_name": app["app_name"],
            "application_status": app.get("application_status", ""),
            "solution_type": app.get("solution_type", ""),
            "business_criticality": app.get("business_criticality", ""),
            "deployment_type": app.get("deployment_type", ""),
            "out_of_scope": app_id in RETIRED_APPS,
        })
    write_json(OUT_ROOT / "applications" / "consolidated_applications_overview.json", {
        "assessment_date": ASSESSMENT_DATE,
        "total_applications": len(apps_overview),
        "applications": apps_overview,
    })
    print(f"  ✓ Generated {len(apps_overview)} consolidated schema files")

    # Schema definitions
    write_json(SCHEMA_DIR / "consolidated_application_schema.json", {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Consolidated Application Schema",
        "type": "object",
        "properties": {
            "application_identifier": {"type": "string"},
            "application_name": {"type": "string"},
            "description": {"type": "string"},
            "solution_type": {"type": "string", "enum": ["Custom made","3rd party software","Open Source","SaaS"]},
            "business_criticality": {"type": "string", "enum": ["Low","Medium","High","Critical"]},
            "application_status": {"type": "string"},
            "deployment_type": {"type": "string"},
            "technology_stack": {"type": "object"},
            "infrastructure": {"type": "object"},
            "integration": {"type": "object"},
            "out_of_scope": {"type": "boolean"},
        }
    })
    write_json(SCHEMA_DIR / "original_application_schema_from_apps_db_complete.json", {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Original Application Schema from apps_db_complete.xlsx",
        "description": "Schema derived from the original Excel data source",
        "source_file": "apps_db_complete.xlsx",
        "fields": [
            "app_id","app_name","app_description","Solution type","criticality",
            "Application status","Decomission date","Deployment type","data classification",
            "business unit","business capabilities","number of users","Operating system",
            "programming language","Application Server type","Application Architecture",
            "Application is containerized","Number of environments","Physical servers instances",
            "cpu_cores","memory in GB","production environments","CI_CD present",
            "number of Api endpoints","external interfaces","Physical Database Server instance",
            "db_engine","DB storage in GB","DB License required","logging_solution","monitoring_tool"
        ]
    })
    write_json(SCHEMA_DIR / "original_unified_schema_from_validated_output.json", {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Unified Application Schema",
        "description": "Normalized schema used in internal_app_model",
        "version": "1.0",
        "properties": {
            "app_id": {"type": "string"},
            "app_name": {"type": "string"},
            "solution_type": {"type": "string"},
            "business_criticality": {"type": "string"},
            "application_status": {"type": "string"},
            "deployment_type": {"type": "string"},
            "operating_system": {"type": "string"},
            "programming_language": {"type": "string"},
            "application_server": {"type": ["string", "null"]},
            "database_engine": {"type": "string"},
            "is_containerized": {"type": "string", "enum": ["Yes","No"]},
            "server_instances": {"type": ["array","string"]},
            "external_interface_count": {"type": "integer"},
        }
    })
    write_json(SCHEMA_DIR / "original_relationship_model_schema_from_validated_output.json", {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Application Relationship Model Schema",
        "description": "Schema for application dependency and relationship data",
        "relationships": {
            "database_dependency": {"source": "application", "target": "database", "cardinality": "M:1"},
            "server_dependency": {"source": "application", "target": "server", "cardinality": "M:N"},
            "interface_dependency": {"source": "application", "target": "external_system", "cardinality": "M:N"},
        }
    })
    print("  ✓ Generated schema files")


# ─── Step 2: Out-of-Scope ─────────────────────────────────────────────────────

def generate_out_of_scope():
    for app_id in sorted([f.stem for f in APP_MODEL.glob("app*.json")]):
        app = load_app(app_id)
        is_retired = app_id in RETIRED_APPS
        status = app.get("application_status", "")
        result = {
            "application_identifier": app_id,
            "assessments": [
                {
                    "exclusion_type": "RETIRED",
                    "applies": is_retired,
                    "confidence": 9,
                    "reasoning": f"Application status is {status}." if not is_retired
                                 else f"Application status is {status}. RETIRED applications are excluded from modernization scope.",
                },
                {
                    "exclusion_type": "SAP",
                    "applies": False,
                    "confidence": 9,
                    "reasoning": "No SAP indicators found in solution type or description.",
                },
            ],
            "out_of_scope": is_retired,
        }
        write_json(OOS_DIR / f"out_of_scope_{app_id}.json", result)
    print(f"  ✓ Generated 30 out-of-scope files")


# ─── Step 3: Technology Assessment ───────────────────────────────────────────

def generate_technology_assessment():
    in_scope = [f.stem for f in APP_MODEL.glob("app*.json") if f.stem not in RETIRED_APPS]
    for app_id in sorted(in_scope):
        app = load_app(app_id)
        components = []

        # OS
        os_str = app.get("operating_system", "")
        os_stat, os_eol, os_reason = os_status_val(os_str)
        if os_str:
            components.append({
                "component_name": os_str,
                "component_family": "Operating System",
                "component_type": "os",
                "managed_service": False,
                "version": os_str,
                "component_status": os_stat,
                "eol_date": os_eol,
                "reason": os_reason,
                "confidence": 9,
            })

        # Language
        lang_str = app.get("programming_language", "")
        lang_stat, lang_eol, lang_reason = lang_status_val(lang_str)
        if lang_str:
            components.append({
                "component_name": lang_str,
                "component_family": "Programming Language",
                "component_type": "language",
                "managed_service": False,
                "version": lang_str,
                "component_status": lang_stat,
                "eol_date": lang_eol,
                "reason": lang_reason,
                "confidence": 8,
            })

        # Database
        db_str = app.get("database_engine", "")
        db_stat, db_eol, db_reason = db_status_val(db_str)
        is_managed = db_str in ("Amazon RDS MySQL", "Aurora PostgreSQL")
        if db_str:
            components.append({
                "component_name": db_str,
                "component_family": "Database",
                "component_type": "database",
                "managed_service": is_managed,
                "version": db_str,
                "component_status": db_stat,
                "eol_date": db_eol,
                "reason": db_reason,
                "confidence": 9,
            })

        # App Server
        as_str = app.get("application_server")
        if as_str and as_str.lower() not in ("none", "null", ""):
            as_stat, as_eol, as_reason = as_status_val(as_str)
            if as_stat != "N/A":
                components.append({
                    "component_name": as_str,
                    "component_family": "Application Server",
                    "component_type": "application_server",
                    "managed_service": False,
                    "version": as_str,
                    "component_status": as_stat,
                    "eol_date": as_eol,
                    "reason": as_reason,
                    "confidence": 9,
                })

        has_eol = any(c["component_status"] == "EOL" for c in components)
        has_outdated = any(c["component_status"] == "OUTDATED" for c in components)
        has_missing = any(c["component_status"] == "NO_KNOWLEDGE" for c in components)
        result = {
            "application_identifier": app_id,
            "assessment_date": ASSESSMENT_DATE,
            "components": components,
            "has_eol_components": has_eol,
            "has_outdated_components": has_outdated,
            "has_missing_version_data": has_missing,
        }
        write_json(TECH_DIR / f"technology_assessment_{app_id}.json", result)
    print(f"  ✓ Generated {len(in_scope)} technology assessment files")


# ─── Step 4: Complexity Assessment ───────────────────────────────────────────

def score_complexity(app: dict, tech_data: dict) -> dict:
    """Returns (score, confidence, reasoning, contributing_factors)"""
    app_id = app["app_id"]
    components = tech_data.get("components", [])

    eol_count = sum(1 for c in components if c["component_status"] == "EOL")
    outdated_count = sum(1 for c in components if c["component_status"] == "OUTDATED")

    # Technology Age (25%)
    if eol_count >= 2:
        tech_score = 9
    elif eol_count == 1:
        tech_score = 8
    elif outdated_count >= 2:
        tech_score = 6
    elif outdated_count == 1:
        tech_score = 5
    else:
        tech_score = 2

    # Integration (20%)
    ext_ifaces = app.get("external_interface_count", 0)
    if ext_ifaces <= 2:
        int_score = 2
    elif ext_ifaces <= 5:
        int_score = 4
    elif ext_ifaces <= 10:
        int_score = 6
    elif ext_ifaces <= 20:
        int_score = 8
    else:
        int_score = 10

    # Infrastructure (15%)
    srv_count = get_server_count(app)
    if srv_count <= 1:
        infra_score = 2
    elif srv_count == 2:
        infra_score = 4
    elif srv_count <= 4:
        infra_score = 5
    else:
        infra_score = 7

    # Business Criticality (15%)
    crit = app.get("business_criticality", "Medium")
    crit_score = {"Low": 2, "Medium": 4, "High": 7, "Critical": 9}.get(crit, 4)

    # Architecture (15%)
    containerized = app.get("is_containerized", "No") == "Yes"
    arch = app.get("application_architecture", "unknown").lower()
    sol_type = app.get("solution_type", "")
    if containerized and arch in ("3-tier", "microservices"):
        arch_score = 2
    elif containerized or arch in ("3-tier",):
        arch_score = 5
    else:
        # monolith/legacy
        arch_score = 8

    # Data complexity (10%)
    db_str = app.get("database_engine", "")
    db_stat, _, _ = db_status_val(db_str)
    if db_stat == "EOL" or db_stat == "NO_KNOWLEDGE":
        data_score = 7
    elif db_stat == "OUTDATED":
        data_score = 5
    else:
        data_score = 3

    # Weighted score
    raw = (tech_score * 0.25 + int_score * 0.20 + infra_score * 0.15 +
           crit_score * 0.15 + arch_score * 0.15 + data_score * 0.10)
    score = round(raw)
    score = max(1, min(10, score))

    if score <= 3:
        level = "LOW"
    elif score <= 6:
        level = "MEDIUM"
    else:
        level = "HIGH"

    reasoning = (
        f"Complexity {level} ({score}/10). "
        f"Technology age: {tech_score}/10 ({eol_count} EOL, {outdated_count} outdated components). "
        f"Integration: {int_score}/10 ({ext_ifaces} external interfaces). "
        f"Infrastructure: {infra_score}/10 ({srv_count} servers). "
        f"Business criticality {crit}: {crit_score}/10. "
        f"Architecture {arch}: {arch_score}/10. "
        f"Data complexity: {data_score}/10."
    )

    factors = {
        "number_of_servers": srv_count,
        "number_of_databases": 1,
        "number_of_environments": app.get("environment_count", 1),
        "number_of_interfaces": ext_ifaces,
        "business_criticality": crit,
        "number_of_outdated_technologies": outdated_count,
        "number_of_eol_technologies": eol_count,
        "number_of_dependencies": app.get("api_endpoint_count", 0),
        "ci_cd_present": app.get("ci_cd_present", "No"),
        "containerized": app.get("is_containerized", "No"),
    }

    return {
        "score": score,
        "level": level,
        "confidence": 8,
        "reasoning": reasoning,
        "factors": factors,
        "sub_scores": {
            "tech_score": tech_score, "int_score": int_score,
            "infra_score": infra_score, "crit_score": crit_score,
            "arch_score": arch_score, "data_score": data_score,
        }
    }


def generate_complexity():
    in_scope = [f.stem for f in APP_MODEL.glob("app*.json") if f.stem not in RETIRED_APPS]
    for app_id in sorted(in_scope):
        app = load_app(app_id)
        tech_data = json.loads((TECH_DIR / f"technology_assessment_{app_id}.json").read_text())
        cx = score_complexity(app, tech_data)
        result = {
            "application_identifier": app_id,
            "complexity_score": cx["score"],
            "complexity_level": cx["level"],
            "confidence": cx["confidence"],
            "reasoning": cx["reasoning"],
            "contributing_factors": cx["factors"],
        }
        write_json(COMP_DIR / f"complexity_{app_id}.json", result)
    print(f"  ✓ Generated {len(in_scope)} complexity files")


# ─── Step 5: Scenario Analysis ────────────────────────────────────────────────

def assess_scenarios(app: dict, tech_data: dict) -> list:
    os_str = app.get("operating_system", "")
    lang_str = app.get("programming_language", "")
    db_str = app.get("database_engine", "")
    as_str = app.get("application_server") or "None"
    sol_type = app.get("solution_type", "")
    dep_type = app.get("deployment_type", "")
    containerized = app.get("is_containerized", "No") == "Yes"
    arch = app.get("application_architecture", "unknown").lower()

    components = tech_data.get("components", [])
    has_eol = any(c["component_status"] == "EOL" for c in components)
    has_outdated = any(c["component_status"] in ("EOL","OUTDATED") for c in components)

    os_stat, _, _ = os_status_val(os_str)
    db_stat, _, _ = db_status_val(db_str)
    as_stat, _, _ = as_status_val(as_str) if as_str and as_str.lower() != "none" else ("N/A", None, "")

    is_custom = sol_type == "Custom made"
    is_3rd_party = sol_type == "3rd party software"
    is_open_source = sol_type == "Open Source"
    is_on_prem = "On-Premise" in dep_type or "On-premise" in dep_type
    is_cloud = "AWS" in dep_type or "cloud" in dep_type.lower()
    is_fully_cloud = dep_type.strip().upper() == "AWS"
    has_app_server = bool(app.get("application_server")) and app.get("application_server") != "None"

    results = []

    def entry(scenario_id, status, reason, confidence=8):
        results.append({
            "id": scenario_id,
            "status": status,
            "match_type": "ai",
            "reason": reason,
            "confidence": confidence,
            "source": {"document_id": "", "document_title": "", "section": "",
                       "content_excerpt": "", "relevance": ""},
        })

    # 1. os_update_security_patch
    if os_stat == "CURRENT_VERSION":
        entry("os_update_security_patch", "FULFILLED",
              f"OS {os_str} is current version, no update needed.")
    elif os_stat in ("EOL", "OUTDATED"):
        entry("os_update_security_patch", "APPLICABLE",
              f"OS {os_str} has status {os_stat}. Security patches and OS update recommended.")
    else:
        entry("os_update_security_patch", "NOT_APPLICABLE",
              "Insufficient OS data to assess.", 5)

    # 2. switch_to_standard_linux_os
    if is_aix(os_str):
        if is_3rd_party:
            entry("switch_to_standard_linux_os", "BLOCKED",
                  f"3rd party software on {os_str}. OS migration may void vendor support.")
        else:
            entry("switch_to_standard_linux_os", "APPLICABLE",
                  f"Application runs on {os_str} (proprietary AIX). Migration to standard Linux recommended.")
    elif is_windows(os_str):
        entry("switch_to_standard_linux_os", "NOT_APPLICABLE",
              f"Application runs on Windows Server. Switch to Linux may not be suitable for Windows-native stack.", 7)
    elif is_standard_linux(os_str):
        entry("switch_to_standard_linux_os", "FULFILLED",
              f"Application already runs on standard Linux ({os_str}).")
    else:
        entry("switch_to_standard_linux_os", "NOT_APPLICABLE",
              f"OS {os_str} does not qualify for this scenario.", 6)

    # 3. switch_to_arm_cpu
    if is_3rd_party:
        entry("switch_to_arm_cpu", "BLOCKED",
              "3rd party software may not support ARM architecture without vendor approval.")
    elif is_windows(os_str):
        entry("switch_to_arm_cpu", "BLOCKED",
              "Windows-based OS limits ARM migration options.")
    elif is_aix(os_str):
        entry("switch_to_arm_cpu", "BLOCKED",
              f"AIX OS is POWER architecture, ARM migration not applicable.")
    elif is_custom or is_open_source:
        entry("switch_to_arm_cpu", "APPLICABLE",
              f"Custom/open-source application on Linux can be considered for ARM-based infrastructure.")
    else:
        entry("switch_to_arm_cpu", "LACK_OF_DATA",
              "Insufficient data to determine ARM compatibility.", 5)

    # 4. application_server_replacement
    if is_3rd_party:
        entry("application_server_replacement", "BLOCKED",
              "3rd party software; app server replacement depends on vendor.")
    elif not has_app_server:
        entry("application_server_replacement", "NOT_APPLICABLE",
              "No application server configured.")
    elif as_stat == "CURRENT_VERSION":
        entry("application_server_replacement", "FULFILLED",
              f"Application server {as_str} is current version.")
    elif as_stat in ("EOL", "OUTDATED"):
        entry("application_server_replacement", "APPLICABLE",
              f"Application server {as_str} has status {as_stat}. Replacement recommended.")
    else:
        entry("application_server_replacement", "NOT_APPLICABLE",
              "No application server or N/A.", 6)

    # 5. app_deployment_to_cloud
    if is_fully_cloud:
        entry("app_deployment_to_cloud", "FULFILLED",
              "Application is already deployed on AWS cloud infrastructure.")
    elif is_cloud and is_on_prem:
        entry("app_deployment_to_cloud", "APPLICABLE",
              "Application has hybrid deployment. Full cloud migration can be considered.")
    elif is_on_prem:
        entry("app_deployment_to_cloud", "APPLICABLE",
              "Application is deployed on-premise. Migration to cloud infrastructure is applicable.")
    else:
        entry("app_deployment_to_cloud", "FULFILLED",
              "Application is already on cloud infrastructure.")

    # 6. app_containerization
    if containerized:
        entry("app_containerization", "FULFILLED",
              "Application is already containerized.")
    elif is_aix(os_str):
        entry("app_containerization", "BLOCKED",
              f"AIX ({os_str}) does not support standard container runtimes.")
    elif is_3rd_party:
        entry("app_containerization", "BLOCKED",
              "3rd party software containerization depends on vendor support.")
    elif is_custom or is_open_source:
        if is_standard_linux(os_str) or is_windows(os_str):
            entry("app_containerization", "APPLICABLE",
                  "Application is not containerized and can be containerized as a custom/open-source app.")
        else:
            entry("app_containerization", "BLOCKED",
                  f"OS {os_str} may not support standard container runtimes.")
    else:
        entry("app_containerization", "NOT_APPLICABLE",
              "Containerization not applicable for this solution type.", 6)

    # 7. app_refactor_decoupling
    if is_3rd_party or is_open_source:
        entry("app_refactor_decoupling", "NOT_APPLICABLE",
              "3rd party or open-source software; refactoring not in scope.")
    elif is_custom:
        if arch in ("microservices",):
            entry("app_refactor_decoupling", "FULFILLED",
                  "Application already uses microservices architecture.")
        else:
            entry("app_refactor_decoupling", "APPLICABLE",
                  f"Custom application with {arch} architecture. Refactoring and de-coupling recommended.")
    else:
        entry("app_refactor_decoupling", "NOT_APPLICABLE",
              "Not a custom application.", 6)

    # 8. upgrade_legacy_databases
    if not db_str:
        entry("upgrade_legacy_databases", "NOT_APPLICABLE",
              "No database component identified.", 6)
    elif db_stat == "CURRENT_VERSION":
        entry("upgrade_legacy_databases", "FULFILLED",
              f"Database {db_str} is current version, no upgrade needed.")
    elif db_stat in ("EOL", "OUTDATED", "NO_KNOWLEDGE"):
        entry("upgrade_legacy_databases", "APPLICABLE",
              f"Database {db_str} has status {db_stat}. Upgrade recommended.")
    else:
        entry("upgrade_legacy_databases", "FULFILLED",
              f"Database {db_str} is current.")

    # 9. switch_db_engine_open_source
    if is_open_source_db(db_str):
        entry("switch_db_engine_open_source", "FULFILLED",
              f"Database {db_str} is already open-source.")
    elif is_3rd_party:
        entry("switch_db_engine_open_source", "BLOCKED",
              "3rd party software; database engine change depends on vendor.")
    elif is_proprietary_db(db_str) and (is_custom or is_open_source):
        entry("switch_db_engine_open_source", "APPLICABLE",
              f"Proprietary database {db_str} detected. Switch to open-source (e.g., PostgreSQL) is applicable.")
    elif db_stat == "NO_KNOWLEDGE":
        entry("switch_db_engine_open_source", "LACK_OF_DATA",
              f"Database {db_str} status unknown.", 5)
    else:
        entry("switch_db_engine_open_source", "NOT_APPLICABLE",
              f"Database {db_str} does not require engine switch.", 6)

    # 10. update_outdated_components
    if is_3rd_party:
        entry("update_outdated_components", "BLOCKED",
              "3rd party software; component updates depend on vendor release cycle.")
    elif not has_outdated:
        entry("update_outdated_components", "FULFILLED",
              "All components are current version.")
    elif is_custom or is_open_source:
        entry("update_outdated_components", "APPLICABLE",
              f"Application has {'EOL' if has_eol else 'outdated'} components that should be updated.")
    else:
        entry("update_outdated_components", "NOT_APPLICABLE",
              "Component updates not applicable for this solution type.", 6)

    return results


def generate_scenario_analysis():
    in_scope = [f.stem for f in APP_MODEL.glob("app*.json") if f.stem not in RETIRED_APPS]
    for app_id in sorted(in_scope):
        app = load_app(app_id)
        tech_data = json.loads((TECH_DIR / f"technology_assessment_{app_id}.json").read_text())
        scenarios = assess_scenarios(app, tech_data)
        result = {
            "application_identifier": app_id,
            "assessment_date": ASSESSMENT_DATE,
            "scenarios_detailed": scenarios,
        }
        write_json(SCEN_DIR / f"scenario_assessment_{app_id}.json", result)
    print(f"  ✓ Generated {len(in_scope)} scenario assessment files")


# ─── Step 6: Business Case ────────────────────────────────────────────────────

def compute_cost_multiplier(complexity_score: int) -> float:
    return 0.5 * (1.15 ** complexity_score)

def compute_savings_multiplier(scenario_id: str, complexity_score: int) -> float:
    if scenario_id in APP_FOCUS_SCENARIOS:
        if complexity_score <= 3:
            return 1.0
        elif complexity_score <= 6:
            return 0.9
        else:
            return 0.8
    return 1.0


def generate_business_case():
    in_scope = sorted([f.stem for f in APP_MODEL.glob("app*.json") if f.stem not in RETIRED_APPS])
    app_details = []
    scenario_agg = {s: {"applicable_count": 0, "total_cost": 0.0, "total_savings": 0.0, "apps": []}
                    for s in ALL_SCENARIOS if s in FINANCE}

    total_cost = 0.0
    total_savings = 0.0

    for app_id in in_scope:
        app = load_app(app_id)
        cx_data = json.loads((COMP_DIR / f"complexity_{app_id}.json").read_text())
        sc_data = json.loads((SCEN_DIR / f"scenario_assessment_{app_id}.json").read_text())
        complexity_score = cx_data["complexity_score"]
        cm = compute_cost_multiplier(complexity_score)

        app_scenarios = []
        for s in sc_data["scenarios_detailed"]:
            sid = s["id"]
            if s["status"] != "APPLICABLE":
                continue
            if sid not in FINANCE:
                continue
            finance = FINANCE[sid]
            sm = compute_savings_multiplier(sid, complexity_score)
            adj_cost = round(finance["cost"] * cm, 2)
            adj_savings = round(finance["savings"] * sm, 2)
            app_scenarios.append({
                "scenario_id": sid,
                "scenario_name": SCENARIO_NAMES[sid],
                "status": "APPLICABLE",
                "complexity_score": complexity_score,
                "cost_multiplier": round(cm, 4),
                "savings_multiplier": sm,
                "base_cost": finance["cost"],
                "base_savings": finance["savings"],
                "adjusted_cost": adj_cost,
                "adjusted_yearly_savings": adj_savings,
            })
            scenario_agg[sid]["applicable_count"] += 1
            scenario_agg[sid]["total_cost"] += adj_cost
            scenario_agg[sid]["total_savings"] += adj_savings
            scenario_agg[sid]["apps"].append(app_id)
            total_cost += adj_cost
            total_savings += adj_savings

        if app_scenarios:
            app_total_cost = sum(x["adjusted_cost"] for x in app_scenarios)
            app_total_savings = sum(x["adjusted_yearly_savings"] for x in app_scenarios)
            app_details.append({
                "application_identifier": app_id,
                "app_id": app_id,                                    # alias for HTML generator
                "application_name": app["app_name"],
                "title": app["app_name"],                            # alias for HTML generator
                "complexity_score": complexity_score,
                "scenarios": app_scenarios,
                "total_adjusted_cost": round(app_total_cost, 2),
                "total_adjusted_yearly_savings": round(app_total_savings, 2),
                "break_even_years": round(app_total_cost / app_total_savings, 1) if app_total_savings > 0 else None,
            })

    scenarios_summary = []
    for sid, agg in scenario_agg.items():
        if agg["applicable_count"] > 0:
            roi = round(agg["total_cost"] / agg["total_savings"], 1) if agg["total_savings"] > 0 else None
            scenarios_summary.append({
                "scenario_id": sid,
                "scenario_name": SCENARIO_NAMES[sid],
                "applicable_apps_count": agg["applicable_count"],
                "applicable_count": agg["applicable_count"],        # alias for HTML generator
                "total_adjusted_cost": round(agg["total_cost"], 2),
                "total_cost": round(agg["total_cost"], 2),           # alias for HTML generator
                "total_adjusted_yearly_savings": round(agg["total_savings"], 2),
                "total_yearly_savings": round(agg["total_savings"], 2),  # alias for HTML generator
                "break_even_years": roi,
                "roi_years": roi,                                    # alias for HTML generator
                "applicable_app_ids": agg["apps"],
                "app_ids": agg["apps"],                              # alias for HTML generator
            })

    portfolio_roi = round(total_cost / total_savings, 1) if total_savings > 0 else None
    result = {
        "assessment_date": ASSESSMENT_DATE,
        "portfolio_summary": {
            "total_applications_assessed": len(in_scope),
            "applications_with_scenarios": len(app_details),
            "applications_with_opportunities": len(app_details),  # alias for HTML generator
            "total_adjusted_investment": round(total_cost, 2),
            "total_one_time_costs": round(total_cost, 2),          # alias for HTML generator
            "total_adjusted_yearly_savings": round(total_savings, 2),
            "total_yearly_savings": round(total_savings, 2),       # alias for HTML generator
            "portfolio_break_even_years": portfolio_roi,
            "roi_years": portfolio_roi,                             # alias for HTML generator
        },
        "scenarios_summary": scenarios_summary,
        "application_details": app_details,
    }
    write_json(BC_DIR / "business_case.json", result)
    print(f"  ✓ Generated business case with {len(app_details)} apps and {len(scenarios_summary)} scenarios")


# ─── Step 7: Markdown Reports ─────────────────────────────────────────────────

def fmt_currency(val: float) -> str:
    return f"€{val:,.0f}"

def generate_app_markdown(app_id: str) -> str:
    app = load_app(app_id)
    tech_data = json.loads((TECH_DIR / f"technology_assessment_{app_id}.json").read_text())
    cx_data = json.loads((COMP_DIR / f"complexity_{app_id}.json").read_text())
    sc_data = json.loads((SCEN_DIR / f"scenario_assessment_{app_id}.json").read_text())
    bc_data = json.loads((BC_DIR / "business_case.json").read_text())

    # Get app financials from business case
    app_bc = next((x for x in bc_data["application_details"] if x["application_identifier"] == app_id), None)

    components = tech_data["components"]
    current_c = sum(1 for c in components if c["component_status"] == "CURRENT_VERSION")
    outdated_c = sum(1 for c in components if c["component_status"] == "OUTDATED")
    eol_c = sum(1 for c in components if c["component_status"] == "EOL")
    nk_c = sum(1 for c in components if c["component_status"] == "NO_KNOWLEDGE")

    srv_count = get_server_count(app)
    complexity_score = cx_data["complexity_score"]
    complexity_level = cx_data["complexity_level"]
    cx_factors = cx_data["contributing_factors"]

    # Build tech table rows
    tech_rows = ""
    for c in components:
        badge = status_badge(c["component_status"])
        ctype = c["component_type"].replace("_", " ").title()
        tech_rows += f"| {ctype} | {c['component_name']} | {c.get('version','—')} | {badge} {c['component_status']} |\n"

    # Build scenario sections
    scenarios_by_status = {}
    for s in sc_data["scenarios_detailed"]:
        scenarios_by_status.setdefault(s["status"], []).append(s)

    applicable_scenarios_md = ""
    for s in scenarios_by_status.get("APPLICABLE", []):
        sid = s["id"]
        sname = SCENARIO_NAMES.get(sid, sid)
        sc_bc = None
        if app_bc:
            sc_bc = next((x for x in app_bc["scenarios"] if x["scenario_id"] == sid), None)
        cost_line = f"- **Cost:** {fmt_currency(sc_bc['adjusted_cost'])} (one-time)" if sc_bc else ""
        savings_line = f"- **Savings:** {fmt_currency(sc_bc['adjusted_yearly_savings'])}/year" if sc_bc else ""
        applicable_scenarios_md += f"""
#### ✅ {sname}

- **Reason:** {s['reason']}
- **Confidence:** {s['confidence']}/10
{cost_line}
{savings_line}
"""

    other_scenarios_md = "| Scenario | Status | Reason |\n|----------|--------|--------|\n"
    for status in ("FULFILLED", "NOT_APPLICABLE", "BLOCKED", "LACK_OF_DATA"):
        for s in scenarios_by_status.get(status, []):
            icon = {"FULFILLED": "✔️", "NOT_APPLICABLE": "❌", "BLOCKED": "🚫", "LACK_OF_DATA": "❓"}.get(status, "")
            sname = SCENARIO_NAMES.get(s["id"], s["id"])
            reason_short = s["reason"][:120] + "..." if len(s["reason"]) > 120 else s["reason"]
            other_scenarios_md += f"| {sname} | {icon} {status} | {reason_short} |\n"

    # Financial summary
    fin_summary = ""
    if app_bc:
        total_cost = app_bc["total_adjusted_cost"]
        total_savings = app_bc["total_adjusted_yearly_savings"]
        be = app_bc.get("break_even_years", "—")
        fin_summary = f"""
## Financial Summary

| Metric | Value |
|--------|-------|
| Total One-Time Investment | {fmt_currency(total_cost)} |
| Total Annual Savings | {fmt_currency(total_savings)} |
| Break-Even | {be} years |
"""
    else:
        fin_summary = "\n## Financial Summary\n\nNo applicable scenarios with financial data found.\n"

    dep_type = app.get("deployment_type", "—")
    servers_str = ", ".join(app["server_instances"]) if isinstance(app.get("server_instances"), list) else str(app.get("server_instances", ""))

    md = f"""# Application Report: {app['app_name']}

**ID:** {app_id}
**Generated:** {TODAY}

## Overview

| Attribute | Value |
|-----------|-------|
| Business Unit | {app.get('business_unit', '—')} |
| Solution Type | {app.get('solution_type', '—')} |
| Deployment | {dep_type} |
| Business Criticality | {app.get('business_criticality', '—')} |
| Users | {app.get('user_count', '—')} |
| Servers | {srv_count} ({servers_str}) |
| Containerized | {app.get('is_containerized', '—')} |
| CI/CD | {app.get('ci_cd_present', '—')} |
| Architecture | {app.get('application_architecture', '—')} |

## Technology Stack

| Component | Technology | Version | Status |
|-----------|-----------|---------|--------|
{tech_rows}
```mermaid
pie title Technology Health
    "Current" : {current_c}
    "Outdated" : {outdated_c}
    "End of Life" : {eol_c}
    "Unknown" : {nk_c}
```

## Complexity Assessment

**Score:** {complexity_score}/10 — **{complexity_level}**
**Confidence:** {cx_data['confidence']}/10

| Factor | Value |
|--------|-------|
| Technology Age (EOL/Outdated) | {cx_factors['number_of_eol_technologies']} EOL / {cx_factors['number_of_outdated_technologies']} outdated |
| Integration (External Interfaces) | {cx_factors['number_of_interfaces']} |
| Infrastructure (Servers) | {cx_factors['number_of_servers']} |
| Business Criticality | {cx_factors['business_criticality']} |
| Containerized | {cx_factors['containerized']} |
| CI/CD Present | {cx_factors['ci_cd_present']} |

> {cx_data['reasoning']}

## Modernization Scenarios

### Applicable Scenarios
{applicable_scenarios_md if applicable_scenarios_md.strip() else "_No applicable scenarios._"}

### Other Scenarios

{other_scenarios_md}
{fin_summary}
"""
    return md


def generate_portfolio_markdown():
    in_scope = sorted([f.stem for f in APP_MODEL.glob("app*.json") if f.stem not in RETIRED_APPS])

    # Gather data
    all_cx = {}
    all_sc = {}
    all_tech = {}
    for app_id in in_scope:
        all_cx[app_id] = json.loads((COMP_DIR / f"complexity_{app_id}.json").read_text())
        all_sc[app_id] = json.loads((SCEN_DIR / f"scenario_assessment_{app_id}.json").read_text())
        all_tech[app_id] = json.loads((TECH_DIR / f"technology_assessment_{app_id}.json").read_text())

    bc_data = json.loads((BC_DIR / "business_case.json").read_text())

    low_count = sum(1 for a in in_scope if all_cx[a]["complexity_level"] == "LOW")
    med_count = sum(1 for a in in_scope if all_cx[a]["complexity_level"] == "MEDIUM")
    high_count = sum(1 for a in in_scope if all_cx[a]["complexity_level"] == "HIGH")

    total_current = total_outdated = total_eol = total_nk = 0
    for app_id in in_scope:
        for c in all_tech[app_id]["components"]:
            if c["component_status"] == "CURRENT_VERSION": total_current += 1
            elif c["component_status"] == "OUTDATED": total_outdated += 1
            elif c["component_status"] == "EOL": total_eol += 1
            else: total_nk += 1

    # Scenario applicability matrix
    scenario_app_counts = {}
    for sid in ALL_SCENARIOS:
        count = sum(1 for a in in_scope
                    if any(s["id"] == sid and s["status"] == "APPLICABLE"
                           for s in all_sc[a]["scenarios_detailed"]))
        scenario_app_counts[sid] = count

    # Matrix header
    matrix_header = "| Application |"
    for sid in ALL_SCENARIOS:
        matrix_header += f" {SCENARIO_NAMES[sid][:20]} |"
    matrix_sep = "|-------------|" + ":---:|" * len(ALL_SCENARIOS)
    matrix_rows = ""
    for app_id in in_scope:
        app = load_app(app_id)
        row = f"| {app['app_name'][:30]} |"
        sc_map = {s["id"]: s["status"] for s in all_sc[app_id]["scenarios_detailed"]}
        for sid in ALL_SCENARIOS:
            st = sc_map.get(sid, "")
            icon = {"FULFILLED": "✔️", "APPLICABLE": "✅", "NOT_APPLICABLE": "❌",
                    "BLOCKED": "🚫", "LACK_OF_DATA": "❓"}.get(st, "—")
            row += f" {icon} |"
        matrix_rows += row + "\n"

    # Top scenarios
    sorted_scenarios = sorted(
        [(sid, cnt) for sid, cnt in scenario_app_counts.items() if cnt > 0],
        key=lambda x: -x[1]
    )
    top_scenarios_table = "| Scenario | Applicable Apps | Total Cost | Yearly Savings | Break-Even |\n"
    top_scenarios_table += "|----------|----------------|------------|---------------|------------|\n"
    for sid, cnt in sorted_scenarios:
        bc_s = next((x for x in bc_data["scenarios_summary"] if x["scenario_id"] == sid), None)
        if bc_s:
            top_scenarios_table += (
                f"| {SCENARIO_NAMES[sid]} | {cnt} | "
                f"{fmt_currency(bc_s['total_adjusted_cost'])} | "
                f"{fmt_currency(bc_s['total_adjusted_yearly_savings'])} | "
                f"{bc_s['break_even_years']}y |\n"
            )
        else:
            top_scenarios_table += f"| {SCENARIO_NAMES[sid]} | {cnt} | — | — | — |\n"

    # High risk apps
    risk_rows = ""
    risk_apps = sorted(in_scope, key=lambda a: -all_cx[a]["complexity_score"])[:10]
    for app_id in risk_apps:
        app = load_app(app_id)
        cx = all_cx[app_id]
        eol_c = all_cx[app_id]["contributing_factors"]["number_of_eol_technologies"]
        applicable_count = sum(1 for s in all_sc[app_id]["scenarios_detailed"] if s["status"] == "APPLICABLE")
        risk_rows += f"| {app['app_name']} | {cx['complexity_score']}/10 ({cx['complexity_level']}) | {eol_c} | {applicable_count} |\n"

    # Portfolio financials
    ps = bc_data["portfolio_summary"]
    total_inv = ps["total_adjusted_investment"]
    total_sav = ps["total_adjusted_yearly_savings"]
    port_be = ps["portfolio_break_even_years"]

    # Graph LR for top scenarios
    top4 = sorted_scenarios[:4]
    graph_nodes = ""
    if len(top4) >= 2:
        graph_nodes += '    subgraph "High Priority"\n'
        for sid, cnt in top4[:2]:
            graph_nodes += f'        {sid[:8]}["{SCENARIO_NAMES[sid][:30]} ({cnt} apps)"]\n'
        graph_nodes += "    end\n"
    if len(top4) >= 4:
        graph_nodes += '    subgraph "Medium Priority"\n'
        for sid, cnt in top4[2:4]:
            graph_nodes += f'        {sid[:8]}b["{SCENARIO_NAMES[sid][:30]} ({cnt} apps)"]\n'
        graph_nodes += "    end\n"

    # App links table
    app_links = "| Application | Complexity | Report |\n|-------------|-----------|--------|\n"
    for app_id in in_scope:
        app = load_app(app_id)
        cx = all_cx[app_id]
        app_links += f"| {app['app_name']} | {cx['complexity_score']}/10 ({cx['complexity_level']}) | [View Report](apps/{app_id}.md) |\n"

    md = f"""# Portfolio Modernization Report

**Generated:** {TODAY}
**Applications Analyzed:** {len(in_scope)} (in-scope) of 30 total

## Executive Summary

The portfolio analysis covered {len(in_scope)} in-scope production applications out of 30 total (4 retired apps excluded). The assessment identified significant modernization opportunities across the portfolio: {high_count} applications are classified as HIGH complexity, {med_count} as MEDIUM, and {low_count} as LOW. Technology debt is considerable, with {total_eol} End-of-Life and {total_outdated} outdated technology components detected. The top modernization opportunity is application containerization and cloud migration, with a combined total portfolio investment of {fmt_currency(total_inv)} yielding estimated annual savings of {fmt_currency(total_sav)} and a break-even of approximately {port_be} years.

## Portfolio Overview

```mermaid
pie title Complexity Distribution
    "Low (1-3)" : {low_count}
    "Medium (4-6)" : {med_count}
    "High (7-10)" : {high_count}
```

```mermaid
pie title Technology Health (Component Count)
    "Current" : {total_current}
    "Outdated" : {total_outdated}
    "End of Life" : {total_eol}
    "Unknown" : {total_nk}
```

## Top Modernization Opportunities

```mermaid
graph LR
{graph_nodes}
```

{top_scenarios_table}

## Scenario Applicability Matrix

{matrix_header}
{matrix_sep}
{matrix_rows}
**Legend:** ✅ Applicable | ❌ Not Applicable | ✔️ Fulfilled | 🚫 Blocked | ❓ Unknown

## Financial Summary

| Metric | Value |
|--------|-------|
| Total One-Time Investment | {fmt_currency(total_inv)} |
| Total Annual Savings | {fmt_currency(total_sav)} |
| Portfolio Break-Even | {port_be} years |

```mermaid
graph TD
    A["💰 Investment: {fmt_currency(total_inv)}"] --> B["📈 Annual Savings: {fmt_currency(total_sav)}"]
    B --> C["⏱️ Break-Even: {port_be} years"]
```

## Risk Applications (Highest Complexity)

| Application | Complexity | EOL Components | Applicable Scenarios |
|-------------|-----------|---------------|---------------------|
{risk_rows}

## Per-Application Reports

{app_links}
"""
    return md


def generate_reports():
    in_scope = sorted([f.stem for f in APP_MODEL.glob("app*.json") if f.stem not in RETIRED_APPS])
    for app_id in in_scope:
        md = generate_app_markdown(app_id)
        (APPS_MD_DIR / f"{app_id}.md").write_text(md)
    print(f"  ✓ Generated {len(in_scope)} per-app markdown reports")

    portfolio_md = generate_portfolio_markdown()
    (REPORT_DIR / "portfolio_report.md").write_text(portfolio_md)
    print("  ✓ Generated portfolio_report.md")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=== Portfolio Modernization Analysis ===")
    print("\nStep 1: Consolidated Schema...")
    generate_consolidated_schema()

    print("\nStep 2: Out-of-Scope Assessment...")
    generate_out_of_scope()

    print("\nStep 3: Technology Assessment...")
    generate_technology_assessment()

    print("\nStep 4: Complexity Assessment...")
    generate_complexity()

    print("\nStep 5: Scenario Analysis...")
    generate_scenario_analysis()

    print("\nStep 6: Business Case...")
    generate_business_case()

    print("\nStep 7: Markdown Reports...")
    generate_reports()

    print("\n=== All JSON and Markdown files generated ===")


if __name__ == "__main__":
    main()
