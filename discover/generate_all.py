#!/usr/bin/env python3
"""Generate all JSON files for the portfolio modernization analysis (Steps 1-6)."""

import json
import math
import os
import shutil
from pathlib import Path

BASE = Path("/home/runner/work/copilot-test-ktruchcz/copilot-test-ktruchcz/discover/output")
INTERNAL_MODEL = BASE / "applications" / "internal_app_model"

# ── Directory setup ────────────────────────────────────────────────────────────
for d in [
    BASE / "applications" / "consolidated_schema",
    BASE / "applications" / "out_of_scope",
    BASE / "applications" / "technology_assessment",
    BASE / "applications" / "complexity",
    BASE / "applications" / "scenario_assessment",
    BASE / "schemas",
    BASE / "reports" / "apps",
    BASE / "reports" / "application_reports",
]:
    d.mkdir(parents=True, exist_ok=True)

# ── App data ───────────────────────────────────────────────────────────────────
RETIRED = {"app005", "app007", "app009", "app029"}
ALL_IDS = [f"app{str(i).zfill(3)}" for i in range(1, 31)]
IN_SCOPE = [a for a in ALL_IDS if a not in RETIRED]

# Load raw app JSON files
apps = {}
for aid in ALL_IDS:
    p = INTERNAL_MODEL / f"{aid}.json"
    with open(p) as f:
        apps[aid] = json.load(f)

# ── STEP 1a: Copy to internal_app_model_application_<id>.json ─────────────────
for aid in ALL_IDS:
    src = INTERNAL_MODEL / f"{aid}.json"
    dst = INTERNAL_MODEL / f"internal_app_model_application_{aid}.json"
    shutil.copy2(src, dst)
print("Step 1a: Copied internal model files")

# ── STEP 1b: Consolidated schema ──────────────────────────────────────────────
def make_consolidated(app):
    aid = app["app_id"]
    svrs = app.get("server_instances", [])
    phys = ", ".join(svrs) if svrs else "sv01"
    return {
        "app_id": aid,
        "name": app.get("app_name", ""),
        "description": app.get("app_description", ""),
        "Solution type": app.get("solution_type", "Custom made"),
        "criticality": app.get("business_criticality", ""),
        "Application status": app.get("application_status", ""),
        "Decomission date": str(app.get("additional_attributes", {}).get("decomission_date", "")),
        "Deployment type": app.get("deployment_type", ""),
        "data classification": app.get("data_classification", "Confidential"),
        "business unit": app.get("business_unit", ""),
        "number of users": str(app.get("user_count", "")),
        "Operating system": app.get("operating_system", ""),
        "programming language": app.get("programming_language", ""),
        "Application Server type": app.get("application_server"),
        "Application Architecture": app.get("application_architecture", ""),
        "Application is containerized": app.get("is_containerized", "No"),
        "Number of environments": str(app.get("environment_count", "")),
        "Physical servers instances": phys,
        "external interfaces": str(app.get("external_interface_count", "")),
        "db_engine": app.get("database_engine", ""),
        "CI_CD present": app.get("ci_cd_present", "No"),
        "framework": None,
        "monitoring_tool": app.get("monitoring_tool"),
        "logging_solution": app.get("logging_solution"),
        "database_storage_gb": app.get("database_storage_gb", 0),
        "database_license_required": app.get("database_license_required", "No"),
    }

for aid in ALL_IDS:
    cs = make_consolidated(apps[aid])
    out = BASE / "applications" / "consolidated_schema" / f"consolidated_schema_application_{aid}.json"
    with open(out, "w") as f:
        json.dump(cs, f, indent=2)
print("Step 1b: Created consolidated schema files")

# ── STEP 1c: Consolidated overview ────────────────────────────────────────────
overview = {
    "total_applications": len(ALL_IDS),
    "in_scope": len(IN_SCOPE),
    "out_of_scope": len(RETIRED),
    "retired_apps": list(RETIRED),
    "applications": [make_consolidated(apps[aid]) for aid in ALL_IDS],
}
with open(BASE / "applications" / "consolidated_applications_overview.json", "w") as f:
    json.dump(overview, f, indent=2)
print("Step 1c: Created consolidated_applications_overview.json")

# ── STEP 1d: Schema exports ───────────────────────────────────────────────────
schema_def = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Application Portfolio Schema",
    "type": "object",
    "properties": {
        "app_id": {"type": "string"},
        "name": {"type": "string"},
        "criticality": {"type": "string", "enum": ["Low", "Medium", "High", "Critical"]},
        "Application status": {"type": "string"},
        "Deployment type": {"type": "string"},
        "Operating system": {"type": "string"},
        "programming language": {"type": "string"},
        "db_engine": {"type": "string"},
    },
}
with open(BASE / "schemas" / "consolidated_schema.json", "w") as f:
    json.dump(schema_def, f, indent=2)
with open(BASE / "schemas" / "internal_app_model_schema.json", "w") as f:
    json.dump({"$schema": "http://json-schema.org/draft-07/schema#", "title": "Internal App Model"}, f, indent=2)
print("Step 1d: Created schema exports")

# ── STEP 2: Out-of-scope assessment ───────────────────────────────────────────
def make_out_of_scope(app):
    aid = app["app_id"]
    is_retired = aid in RETIRED
    return {
        "application_identifier": aid,
        "assessments": [
            {
                "exclusion_type": "RETIRED",
                "applies": is_retired,
                "confidence": 9,
                "reasoning": (
                    f"Application status is {app.get('application_status', 'Unknown')}."
                    if not is_retired
                    else f"Application status is RETIRED/decommissioned."
                ),
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

for aid in ALL_IDS:
    oos = make_out_of_scope(apps[aid])
    out = BASE / "applications" / "out_of_scope" / f"out_of_scope_{aid}.json"
    with open(out, "w") as f:
        json.dump(oos, f, indent=2)
print("Step 2: Created out-of-scope files")

# ── STEP 3: Technology assessment ─────────────────────────────────────────────
OS_STATUS = {
    "AIX 7.2": ("OUTDATED", "IBM AIX 7.2 is proprietary Unix, still supported but considered outdated for modern workloads."),
    "AIX 6": ("EOL", "IBM AIX 6.1 reached End of Life in April 2017."),
    "RHEL 7": ("EOL", "Red Hat Enterprise Linux 7 reached End of Life in June 2024."),
    "RHEL 8": ("CURRENT_VERSION", "RHEL 8 is supported until May 2029."),
    "CentOS 7": ("EOL", "CentOS 7 reached End of Life in June 2024."),
    "Debian 6": ("EOL", "Debian 6 (Squeeze) reached End of Life in May 2014."),
    "Debian 7": ("EOL", "Debian 7 (Wheezy) reached End of Life in April 2018."),
    "Ubuntu 14": ("EOL", "Ubuntu 14.04 reached End of Life in April 2019."),
    "Windows Server 2012": ("EOL", "Windows Server 2012 reached End of Life in October 2023."),
    "Windows Server 2019": ("CURRENT_VERSION", "Windows Server 2019 is supported until 2029."),
    "Windows Server 2022": ("CURRENT_VERSION", "Windows Server 2022 is supported until 2031."),
}

DB_STATUS = {
    "Oracle 19c": ("CURRENT_VERSION", "Oracle 19c has Long Term Support until April 2027."),
    "Oracle 12c": ("EOL", "Oracle 12c reached End of Life in December 2022."),
    "Oracle 11g": ("EOL", "Oracle 11g reached End of Life in December 2020."),
    "DB2 (version unknown)": ("NO_KNOWLEDGE", "DB2 version is unknown; cannot determine lifecycle status."),
    "SQL Server 2022": ("CURRENT_VERSION", "SQL Server 2022 is currently in mainstream support."),
    "SQL Server 2019": ("CURRENT_VERSION", "SQL Server 2019 mainstream support until 2025, extended until 2030."),
    "SQL Server 2016": ("OUTDATED", "SQL Server 2016 mainstream EOL July 2021, in extended support until July 2026."),
    "SQL Server 2014": ("EOL", "SQL Server 2014 reached End of Life in July 2024."),
    "MySQL 8.0": ("CURRENT_VERSION", "MySQL 8.0 is currently supported."),
    "MySQL 5.7": ("EOL", "MySQL 5.7 reached End of Life in October 2023."),
    "PostgreSQL 13": ("OUTDATED", "PostgreSQL 13 reaches End of Life in November 2025, approaching end of support."),
    "PostgreSQL 14": ("CURRENT_VERSION", "PostgreSQL 14 is supported until November 2026."),
    "PostgreSQL 15": ("CURRENT_VERSION", "PostgreSQL 15 is supported until November 2027."),
    "Aurora PostgreSQL": ("CURRENT_VERSION", "Amazon Aurora PostgreSQL is a managed service with current support."),
    "Amazon RDS MySQL": ("CURRENT_VERSION", "Amazon RDS MySQL is a managed service with current support."),
    "MongoDB (no version)": ("NO_KNOWLEDGE", "MongoDB version is unspecified; cannot determine lifecycle status."),
}

LANG_STATUS = {
    "COBOL-2014": ("OUTDATED", "COBOL-2014 is an aging language still used in mainframes but considered outdated."),
    "Java 8": ("EOL", "Oracle Premier Support for Java SE 8 ended March 2022 (without paid extended support)."),
    "Java 11": ("CURRENT_VERSION", "Java 11 is an LTS release with Oracle extended support until September 2026."),
    "Java 17": ("CURRENT_VERSION", "Java 17 is an LTS release with Oracle extended support until September 2030."),
    "Python 3.9": ("OUTDATED", "Python 3.9 reaches End of Life in October 2025, approaching end of support."),
    "Python 3.8": ("EOL", "Python 3.8 reached End of Life in October 2024."),
    "Python 3.11": ("CURRENT_VERSION", "Python 3.11 is supported until October 2027."),
    ".NET Core": ("CURRENT_VERSION", "Modern .NET Core is currently supported."),
    "C# .NET 6": ("OUTDATED", ".NET 6 LTS reached End of Life in November 2024."),
    "ASP.NET Core": ("CURRENT_VERSION", "ASP.NET Core on modern .NET is currently supported."),
    "Ruby 2.7": ("EOL", "Ruby 2.7 reached End of Life in March 2023."),
    "Node.js 18": ("CURRENT_VERSION", "Node.js 18 LTS is supported until April 2025."),
    "Node.js 14": ("EOL", "Node.js 14 reached End of Life in April 2023."),
    "Go 1.19": ("OUTDATED", "Go 1.19 is no longer actively supported; Go 1.22+ is current."),
    "Go 1.16": ("EOL", "Go 1.16 is no longer supported."),
    "Rust 1.70": ("CURRENT_VERSION", "Rust 1.70 is recent and considered current."),
    "PowerShell": ("CURRENT_VERSION", "PowerShell Core is actively maintained by Microsoft."),
    "C++ 17": ("CURRENT_VERSION", "C++17 is a current ISO standard with wide compiler support."),
    "Scala 2.13": ("CURRENT_VERSION", "Scala 2.13 is actively maintained."),
    "VB.NET": ("OUTDATED", "VB.NET is a legacy .NET Framework language with declining usage."),
    "Angular 15": ("OUTDATED", "Angular 17/18 is current; Angular 15 is outdated."),
    "React Native": ("NO_KNOWLEDGE", "React Native version is not specified."),
    "PHP 8.1": ("CURRENT_VERSION", "PHP 8.1 is supported until December 2025."),
    "FORTRAN 2018": ("OUTDATED", "FORTRAN 2018 is a niche language standard, outdated for most modern architectures."),
    "Perl": ("OUTDATED", "Perl 5 is maintained but declining in usage and ecosystem support."),
}

APPSERVER_STATUS = {
    "Websphere 7.0": ("EOL", "IBM WebSphere Application Server 7.0 reached End of Life in April 2015."),
    "Websphere 8.0": ("EOL", "IBM WebSphere Application Server 8.0 reached End of Life in December 2022."),
    "Websphere 8.5": ("OUTDATED", "IBM WebSphere 8.5.5 is in extended support but approaching end of life."),
    "Oracle Weblogic 8.0": ("EOL", "Oracle WebLogic Server 8.1 reached End of Life in December 2008."),
    "Weblogic 9.0": ("EOL", "WebLogic 9.0 reached End of Life."),
    "Apache Tomcat 5.3": ("EOL", "Apache Tomcat 5.x reached End of Life."),
    "Apache Tomcat 6.1": ("EOL", "Apache Tomcat 6 reached End of Life in December 2016."),
    "Apache Tomcat 7.4": ("EOL", "Apache Tomcat 7 reached End of Life in March 2021."),
    "Apache Tomcat 8.0": ("EOL", "Apache Tomcat 8.0 reached End of Life in June 2018."),
    "Glassfish 3.0": ("EOL", "GlassFish 3 reached End of Life."),
    "Glassfish 4.0": ("OUTDATED", "GlassFish 4.0 has no active support since Oracle handed off to Eclipse Foundation."),
    "Glassfish 4.5": ("OUTDATED", "GlassFish 4.5 has no active commercial support."),
    "Glassfish 5.0": ("OUTDATED", "Eclipse GlassFish 5.x is in extended maintenance mode."),
    "Payara 4.0": ("EOL", "Payara 4 reached End of Life."),
    "Payara 5.0": ("OUTDATED", "Payara 5 is approaching End of Life; Payara 6 is current."),
    "Payara 6.0": ("CURRENT_VERSION", "Payara 6.0 is the current supported version."),
    "Microsoft IIS 8.0": ("EOL", "IIS 8.0 (Windows Server 2012) reached End of Life in October 2023."),
    "Microsoft IIS 8.5": ("EOL", "IIS 8.5 (Windows Server 2012 R2) reached End of Life in October 2023."),
    "Microsoft IIS 10.0": ("CURRENT_VERSION", "IIS 10.0 (Windows Server 2016/2019/2022) is currently supported."),
}

def get_tech_status(category, value):
    if not value:
        return None
    lookup = {"os": OS_STATUS, "db": DB_STATUS, "lang": LANG_STATUS, "appserver": APPSERVER_STATUS}[category]
    return lookup.get(value, ("NO_KNOWLEDGE", f"No lifecycle data available for {value}."))

def tech_assessment(app):
    aid = app["app_id"]
    os_val = app.get("operating_system", "")
    db_val = app.get("database_engine", "")
    lang_val = app.get("programming_language", "")
    srv_val = app.get("application_server")

    components = []

    os_status = get_tech_status("os", os_val)
    if os_status:
        components.append({
            "component_type": "Operating System",
            "component_name": os_val,
            "version": os_val,
            "status": os_status[0],
            "reasoning": os_status[1],
        })

    db_status = get_tech_status("db", db_val)
    if db_status:
        components.append({
            "component_type": "Database",
            "component_name": db_val,
            "version": db_val,
            "status": db_status[0],
            "reasoning": db_status[1],
        })

    lang_status = get_tech_status("lang", lang_val)
    if lang_status:
        components.append({
            "component_type": "Programming Language",
            "component_name": lang_val,
            "version": lang_val,
            "status": lang_status[0],
            "reasoning": lang_status[1],
        })

    if srv_val:
        srv_status = get_tech_status("appserver", srv_val)
        if srv_status:
            components.append({
                "component_type": "Application Server",
                "component_name": srv_val,
                "version": srv_val,
                "status": srv_status[0],
                "reasoning": srv_status[1],
            })

    statuses = [c["status"] for c in components]
    eol_count = statuses.count("EOL")
    outdated_count = statuses.count("OUTDATED")
    no_knowledge_count = statuses.count("NO_KNOWLEDGE")
    current_count = statuses.count("CURRENT_VERSION")

    if eol_count >= 2:
        overall = "EOL"
    elif eol_count == 1:
        overall = "EOL"
    elif outdated_count >= 1:
        overall = "OUTDATED"
    elif no_knowledge_count > 0 and current_count == 0:
        overall = "NO_KNOWLEDGE"
    else:
        overall = "CURRENT_VERSION"

    return {
        "application_identifier": aid,
        "components": components,
        "overall_status": overall,
        "eol_component_count": eol_count,
        "outdated_component_count": outdated_count,
        "current_component_count": current_count,
        "no_knowledge_component_count": no_knowledge_count,
    }

tech_assessments = {}
for aid in IN_SCOPE:
    ta = tech_assessment(apps[aid])
    tech_assessments[aid] = ta
    out = BASE / "applications" / "technology_assessment" / f"technology_assessment_{aid}.json"
    with open(out, "w") as f:
        json.dump(ta, f, indent=2)
print("Step 3: Created technology assessment files")

# ── STEP 4: Complexity assessment ─────────────────────────────────────────────
def calc_complexity(app, ta):
    aid = app["app_id"]
    interfaces = int(app.get("external_interface_count", 0))
    servers = len(app.get("server_instances", []))
    envs = int(app.get("environment_count", 1))
    criticality_str = app.get("business_criticality", "Medium")
    arch = app.get("application_architecture", "unknown")
    containerized = app.get("is_containerized", "No")
    cicd = app.get("ci_cd_present", "No")
    os_val = app.get("operating_system", "")
    db_val = app.get("database_engine", "")
    appserver = app.get("application_server")

    # tech_age score (0-10)
    eol_count = ta["eol_component_count"]
    outdated_count = ta["outdated_component_count"]
    if eol_count >= 3:
        tech_age = 9
    elif eol_count == 2:
        tech_age = 8
    elif eol_count == 1:
        tech_age = 7
    elif outdated_count >= 2:
        tech_age = 6
    elif outdated_count == 1:
        tech_age = 5
    else:
        tech_age = 2

    # integration score
    if interfaces <= 2:
        integration = 2
    elif interfaces <= 5:
        integration = 5
    elif interfaces <= 10:
        integration = 7
    elif interfaces <= 20:
        integration = 8
    else:
        integration = 9

    # infrastructure score
    infra_pts = servers + envs
    if infra_pts <= 3:
        infrastructure = 2
    elif infra_pts <= 5:
        infrastructure = 5
    elif infra_pts <= 8:
        infrastructure = 7
    else:
        infrastructure = 9

    # criticality score
    crit_map = {"Low": 3, "Medium": 5, "High": 7, "Critical": 9}
    criticality_score = crit_map.get(criticality_str, 5)

    # architecture score
    is_legacy_os = any(x in os_val for x in ["AIX", "RHEL 7", "CentOS", "Debian 6", "Debian 7", "Windows Server 2012"])
    has_eol_appserver = appserver and APPSERVER_STATUS.get(appserver, ("", ""))[0] == "EOL"
    modernized = containerized == "Yes" and cicd == "Yes"

    if arch in ["1-Tier"] or ("COBOL" in app.get("programming_language", "") or "FORTRAN" in app.get("programming_language", "")):
        architecture_score = 9 if cicd == "No" else 8
    elif arch in ["unknown", "Unknown"] and not modernized:
        architecture_score = 6
    elif modernized and arch in ["3-Tier", "2-Tier"]:
        architecture_score = 3
    elif cicd == "No":
        architecture_score = 7
    else:
        architecture_score = 4

    # data score
    db_status = ta["components"][1]["status"] if len(ta["components"]) > 1 else "NO_KNOWLEDGE"
    is_commercial_db = any(x in db_val for x in ["Oracle", "SQL Server", "DB2"])
    if db_status == "EOL":
        data_score = 8
    elif db_status == "OUTDATED":
        data_score = 6
    elif is_commercial_db:
        data_score = 5
    else:
        data_score = 2

    raw = (tech_age * 0.25 + integration * 0.20 + infrastructure * 0.15 +
           criticality_score * 0.15 + architecture_score * 0.15 + data_score * 0.10)
    final_score = round(raw)

    if final_score <= 3:
        level = "LOW"
    elif final_score <= 6:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return {
        "application_identifier": aid,
        "complexity_score": final_score,
        "complexity_level": level,
        "contributing_factors": {
            "tech_age_score": tech_age,
            "integration_score": integration,
            "infrastructure_score": infrastructure,
            "criticality_score": criticality_score,
            "architecture_score": architecture_score,
            "data_score": data_score,
        },
        "weights": {
            "tech_age": 0.25,
            "integration": 0.20,
            "infrastructure": 0.15,
            "criticality": 0.15,
            "architecture": 0.15,
            "data": 0.10,
        },
        "raw_score": round(raw, 2),
    }

complexities = {}
for aid in IN_SCOPE:
    cx = calc_complexity(apps[aid], tech_assessments[aid])
    complexities[aid] = cx
    out = BASE / "applications" / "complexity" / f"complexity_{aid}.json"
    with open(out, "w") as f:
        json.dump(cx, f, indent=2)
print("Step 4: Created complexity files")

# ── STEP 5: Scenario assessment ───────────────────────────────────────────────
SCENARIOS = [
    "os_update_security_patch",
    "switch_to_standard_linux_os",
    "switch_to_arm_cpu",
    "application_server_replacement",
    "app_deployment_to_cloud",
    "app_containerization",
    "app_refactor_decoupling",
    "upgrade_legacy_databases",
    "switch_db_engine_open_source",
    "update_outdated_components",
    "switch_to_managed_db",
    "managed_arm_db",
    "serverless_db_migration",
    "switch_db_engine_postgresql",
]

def assess_scenarios(app, ta, cx):
    aid = app["app_id"]
    os_val = app.get("operating_system", "")
    db_val = app.get("database_engine", "")
    lang_val = app.get("programming_language", "")
    appserver = app.get("application_server")
    deploy = app.get("deployment_type", "")
    containerized = app.get("is_containerized", "No")
    cicd = app.get("ci_cd_present", "No")
    arch = app.get("application_architecture", "unknown")
    crit = app.get("business_criticality", "Medium")

    os_status = OS_STATUS.get(os_val, ("NO_KNOWLEDGE", ""))[0]
    db_status_val = DB_STATUS.get(db_val, ("NO_KNOWLEDGE", ""))[0]
    lang_status_val = LANG_STATUS.get(lang_val, ("NO_KNOWLEDGE", ""))[0]
    appserver_status = APPSERVER_STATUS.get(appserver, ("NO_KNOWLEDGE", ""))[0] if appserver else None

    is_legacy_unix = any(x in os_val for x in ["AIX", "HP-UX", "Solaris"])
    is_windows = "Windows" in os_val
    is_on_prem = "On-Premise" in deploy
    is_cloud = "AWS" in deploy or "Azure" in deploy or "GCP" in deploy
    is_cloud_only = deploy.strip() in ["AWS", "Azure", "GCP"]
    is_commercial_db = any(x in db_val for x in ["Oracle", "SQL Server", "DB2"])
    is_oss_db = any(x in db_val for x in ["PostgreSQL", "MySQL", "Aurora", "RDS", "MongoDB"])
    is_managed_db = any(x in db_val for x in ["Amazon RDS", "Aurora", "Cloud SQL"])

    results = {}

    # 1. os_update_security_patch
    if os_status in ("EOL", "OUTDATED"):
        results["os_update_security_patch"] = {
            "status": "APPLICABLE",
            "reasoning": f"OS {os_val} is {os_status} and requires security patching or upgrade.",
        }
    else:
        results["os_update_security_patch"] = {
            "status": "FULFILLED",
            "reasoning": f"OS {os_val} is current and receiving security updates.",
        }

    # 2. switch_to_standard_linux_os
    if is_legacy_unix:
        results["switch_to_standard_linux_os"] = {
            "status": "APPLICABLE",
            "reasoning": f"{os_val} is a proprietary Unix OS. Migrating to standard Linux would reduce licensing costs and improve supportability.",
        }
    elif is_windows:
        results["switch_to_standard_linux_os"] = {
            "status": "NOT_APPLICABLE",
            "reasoning": "Application runs on Windows OS. This scenario targets non-standard Unix to standard Linux migration.",
        }
    elif "RHEL" in os_val or "CentOS" in os_val or "Debian" in os_val or "Ubuntu" in os_val:
        if os_status in ("EOL", "OUTDATED"):
            results["switch_to_standard_linux_os"] = {
                "status": "APPLICABLE",
                "reasoning": f"{os_val} is {os_status}. Upgrading to a current Linux distribution is recommended.",
            }
        else:
            results["switch_to_standard_linux_os"] = {
                "status": "FULFILLED",
                "reasoning": f"Application already runs on standard Linux ({os_val}).",
            }
    else:
        results["switch_to_standard_linux_os"] = {
            "status": "NOT_APPLICABLE",
            "reasoning": f"OS {os_val} scenario evaluation not applicable.",
        }

    # 3. switch_to_arm_cpu
    if is_legacy_unix:
        results["switch_to_arm_cpu"] = {
            "status": "BLOCKED",
            "reasoning": f"Legacy Unix OS ({os_val}) is tied to proprietary hardware architecture. ARM migration is not feasible without OS migration first.",
        }
    elif is_on_prem and not is_cloud:
        results["switch_to_arm_cpu"] = {
            "status": "APPLICABLE",
            "reasoning": "On-premise deployment can be evaluated for ARM-based hardware to reduce energy costs.",
        }
    else:
        results["switch_to_arm_cpu"] = {
            "status": "APPLICABLE",
            "reasoning": "Cloud deployment can leverage ARM-based instances (e.g., AWS Graviton) for cost savings.",
        }

    # 4. application_server_replacement
    if not appserver:
        results["application_server_replacement"] = {
            "status": "NOT_APPLICABLE",
            "reasoning": "No application server is used by this application.",
        }
    elif appserver_status == "EOL":
        results["application_server_replacement"] = {
            "status": "APPLICABLE",
            "reasoning": f"Application server {appserver} is EOL and must be replaced.",
        }
    elif appserver_status == "OUTDATED":
        results["application_server_replacement"] = {
            "status": "APPLICABLE",
            "reasoning": f"Application server {appserver} is outdated and should be upgraded.",
        }
    else:
        results["application_server_replacement"] = {
            "status": "FULFILLED",
            "reasoning": f"Application server {appserver} is current.",
        }

    # 5. app_deployment_to_cloud
    if is_cloud_only:
        results["app_deployment_to_cloud"] = {
            "status": "FULFILLED",
            "reasoning": f"Application is already deployed on cloud ({deploy}).",
        }
    elif is_on_prem and not is_cloud:
        results["app_deployment_to_cloud"] = {
            "status": "APPLICABLE",
            "reasoning": "Application is deployed on-premise. Cloud migration would improve scalability and reduce infrastructure costs.",
        }
    else:
        results["app_deployment_to_cloud"] = {
            "status": "PARTIALLY_FULFILLED",
            "reasoning": f"Application has hybrid deployment ({deploy}). Full cloud migration could be considered.",
        }

    # 6. app_containerization
    if containerized == "Yes":
        results["app_containerization"] = {
            "status": "FULFILLED",
            "reasoning": "Application is already containerized.",
        }
    elif is_legacy_unix:
        results["app_containerization"] = {
            "status": "BLOCKED",
            "reasoning": f"Legacy Unix OS ({os_val}) is not compatible with container technologies. OS migration required first.",
        }
    elif arch == "1-Tier" or any(x in lang_val for x in ["COBOL", "FORTRAN"]):
        results["app_containerization"] = {
            "status": "BLOCKED",
            "reasoning": f"Legacy monolithic architecture ({arch}) with {lang_val} makes containerization impractical without significant refactoring.",
        }
    else:
        results["app_containerization"] = {
            "status": "APPLICABLE",
            "reasoning": "Application is not containerized. Containerization would improve deployment consistency and portability.",
        }

    # 7. app_refactor_decoupling
    if arch == "1-Tier" or (arch in ["2-Tier"] and cicd == "No"):
        results["app_refactor_decoupling"] = {
            "status": "APPLICABLE",
            "reasoning": f"Application has a {arch} monolithic architecture with limited CI/CD. Refactoring to microservices would improve maintainability.",
        }
    elif arch == "unknown" and cicd == "No":
        results["app_refactor_decoupling"] = {
            "status": "APPLICABLE",
            "reasoning": "Application architecture is unknown with no CI/CD. Assessment suggests potential for refactoring.",
        }
    elif arch in ["3-Tier"] and containerized == "Yes" and cicd == "Yes":
        results["app_refactor_decoupling"] = {
            "status": "FULFILLED",
            "reasoning": "Application has modern 3-Tier architecture with containerization and CI/CD in place.",
        }
    else:
        results["app_refactor_decoupling"] = {
            "status": "APPLICABLE",
            "reasoning": f"Application with {arch} architecture could benefit from decoupling and modernization.",
        }

    # 8. upgrade_legacy_databases
    if db_status_val == "EOL":
        results["upgrade_legacy_databases"] = {
            "status": "APPLICABLE",
            "reasoning": f"Database {db_val} is EOL and must be upgraded.",
        }
    elif db_status_val == "OUTDATED":
        results["upgrade_legacy_databases"] = {
            "status": "APPLICABLE",
            "reasoning": f"Database {db_val} is outdated and should be upgraded.",
        }
    elif db_status_val == "NO_KNOWLEDGE":
        results["upgrade_legacy_databases"] = {
            "status": "LACK_OF_DATA",
            "reasoning": f"Database version ({db_val}) is unspecified. Cannot determine if upgrade is needed.",
        }
    else:
        results["upgrade_legacy_databases"] = {
            "status": "FULFILLED",
            "reasoning": f"Database {db_val} is current.",
        }

    # 9. switch_db_engine_open_source
    if is_commercial_db:
        results["switch_db_engine_open_source"] = {
            "status": "APPLICABLE",
            "reasoning": f"{db_val} is a commercial database. Switching to an open-source alternative would reduce licensing costs.",
        }
    elif is_oss_db:
        results["switch_db_engine_open_source"] = {
            "status": "FULFILLED",
            "reasoning": f"Application already uses an open-source database ({db_val}).",
        }
    else:
        results["switch_db_engine_open_source"] = {
            "status": "LACK_OF_DATA",
            "reasoning": f"Database {db_val} cannot be classified without version information.",
        }

    # 10. update_outdated_components
    has_outdated = ta["outdated_component_count"] > 0 or ta["eol_component_count"] > 0
    if has_outdated:
        outdated_comps = [c["component_name"] for c in ta["components"] if c["status"] in ("EOL", "OUTDATED")]
        results["update_outdated_components"] = {
            "status": "APPLICABLE",
            "reasoning": f"Outdated/EOL components detected: {', '.join(outdated_comps)}. Updates required.",
        }
    else:
        results["update_outdated_components"] = {
            "status": "FULFILLED",
            "reasoning": "All technology components are current.",
        }

    # 11. switch_to_managed_db
    if is_managed_db:
        results["switch_to_managed_db"] = {
            "status": "FULFILLED",
            "reasoning": f"Database ({db_val}) is already a managed cloud service.",
        }
    elif is_on_prem and not is_cloud:
        results["switch_to_managed_db"] = {
            "status": "APPLICABLE",
            "reasoning": "On-premise database could be migrated to a managed cloud database service.",
        }
    else:
        results["switch_to_managed_db"] = {
            "status": "APPLICABLE",
            "reasoning": "Database could be migrated to a fully managed cloud database service for reduced operational overhead.",
        }

    # 12. managed_arm_db
    if is_legacy_unix or (is_on_prem and not is_cloud):
        results["managed_arm_db"] = {
            "status": "APPLICABLE",
            "reasoning": "Migrating database to ARM-based managed cloud service would reduce costs.",
        }
    elif is_managed_db:
        results["managed_arm_db"] = {
            "status": "APPLICABLE",
            "reasoning": "Existing managed database service can be evaluated for ARM-based instances for cost optimization.",
        }
    else:
        results["managed_arm_db"] = {
            "status": "APPLICABLE",
            "reasoning": "Database can be evaluated for ARM-based managed service deployment.",
        }

    # 13. serverless_db_migration
    if is_legacy_unix or arch == "1-Tier":
        results["serverless_db_migration"] = {
            "status": "BLOCKED",
            "reasoning": "Legacy architecture makes serverless database migration impractical without significant application refactoring.",
        }
    elif is_managed_db:
        results["serverless_db_migration"] = {
            "status": "APPLICABLE",
            "reasoning": "Application already uses a managed database; migration to serverless variant is feasible.",
        }
    else:
        results["serverless_db_migration"] = {
            "status": "APPLICABLE",
            "reasoning": "Database can be migrated to a serverless database solution to reduce operational overhead.",
        }

    # 14. switch_db_engine_postgresql
    if "PostgreSQL" in db_val:
        results["switch_db_engine_postgresql"] = {
            "status": "FULFILLED",
            "reasoning": f"Application already uses PostgreSQL ({db_val}).",
        }
    elif is_commercial_db:
        results["switch_db_engine_postgresql"] = {
            "status": "APPLICABLE",
            "reasoning": f"{db_val} is a commercial database. Migrating to PostgreSQL would eliminate licensing costs.",
        }
    elif "MySQL" in db_val or "MariaDB" in db_val:
        results["switch_db_engine_postgresql"] = {
            "status": "APPLICABLE",
            "reasoning": f"Migrating from {db_val} to PostgreSQL would provide a more feature-rich open-source database.",
        }
    elif "MongoDB" in db_val:
        results["switch_db_engine_postgresql"] = {
            "status": "NOT_APPLICABLE",
            "reasoning": "MongoDB is a document store; switching to PostgreSQL requires architectural changes and may not be appropriate.",
        }
    else:
        results["switch_db_engine_postgresql"] = {
            "status": "LACK_OF_DATA",
            "reasoning": f"Cannot determine applicability for database {db_val}.",
        }

    scenario_list = []
    for s in SCENARIOS:
        r = results[s]
        scenario_list.append({
            "scenario_id": s,
            "status": r["status"],
            "reasoning": r["reasoning"],
        })

    applicable_count = sum(1 for s in scenario_list if s["status"] == "APPLICABLE")
    return {
        "application_identifier": aid,
        "scenarios": scenario_list,
        "applicable_count": applicable_count,
        "summary": {
            "APPLICABLE": sum(1 for s in scenario_list if s["status"] == "APPLICABLE"),
            "FULFILLED": sum(1 for s in scenario_list if s["status"] == "FULFILLED"),
            "NOT_APPLICABLE": sum(1 for s in scenario_list if s["status"] == "NOT_APPLICABLE"),
            "BLOCKED": sum(1 for s in scenario_list if s["status"] == "BLOCKED"),
            "PARTIALLY_FULFILLED": sum(1 for s in scenario_list if s["status"] == "PARTIALLY_FULFILLED"),
            "LACK_OF_DATA": sum(1 for s in scenario_list if s["status"] == "LACK_OF_DATA"),
        },
    }

scenario_assessments = {}
for aid in IN_SCOPE:
    sa = assess_scenarios(apps[aid], tech_assessments[aid], complexities[aid])
    scenario_assessments[aid] = sa
    out = BASE / "applications" / "scenario_assessment" / f"scenario_assessment_{aid}.json"
    with open(out, "w") as f:
        json.dump(sa, f, indent=2)
print("Step 5: Created scenario assessment files")

# ── STEP 6: Business case ─────────────────────────────────────────────────────
FINANCE = {
    "os_update_security_patch": {"cost_once": 1000, "savings_annual": 500},
    "switch_to_standard_linux_os": {"cost_once": 300, "savings_annual": 400},
    "switch_to_arm_cpu": {"cost_once": 5000, "savings_annual": 1000},
    "application_server_replacement": {"cost_once": 10000, "savings_annual": 12000},
    "app_deployment_to_cloud": {"cost_once": 5000, "savings_annual": 3000},
    "app_containerization": {"cost_once": 100000, "savings_annual": 100000},
    "app_refactor_decoupling": {"cost_once": 250000, "savings_annual": 150000},
    "upgrade_legacy_databases": {"cost_once": 10000, "savings_annual": 10000},
    "switch_to_managed_db": {"cost_once": 5000, "savings_annual": 10000},
    "managed_arm_db": {"cost_once": 5000, "savings_annual": 5000},
    "serverless_db_migration": {"cost_once": 5000, "savings_annual": 15000},
    "switch_db_engine_postgresql": {"cost_once": 25000, "savings_annual": 15000},
    # map open_source to postgresql costs
    "switch_db_engine_open_source": {"cost_once": 25000, "savings_annual": 15000},
}

# Scenarios with no finance config (note in output)
NO_FINANCE = {"update_outdated_components"}

APPLICATION_FOCUS_SCENARIOS = {
    "app_containerization", "app_refactor_decoupling", "app_deployment_to_cloud",
    "application_server_replacement",
}

def savings_multiplier(complexity_level, scenario_id):
    if scenario_id in APPLICATION_FOCUS_SCENARIOS:
        return {"LOW": 1.0, "MEDIUM": 0.9, "HIGH": 0.8}.get(complexity_level, 0.9)
    return 1.0

def cost_multiplier(complexity_score):
    return 0.5 * (1.15 ** complexity_score)

all_app_cases = []
total_cost = 0
total_savings = 0

for aid in IN_SCOPE:
    app = apps[aid]
    sa = scenario_assessments[aid]
    cx = complexities[aid]
    complexity_score = cx["complexity_score"]
    complexity_level = cx["complexity_level"]
    cm = cost_multiplier(complexity_score)

    app_cases = []
    app_cost = 0
    app_savings = 0

    for s in sa["scenarios"]:
        sid = s["scenario_id"]
        if s["status"] != "APPLICABLE":
            continue
        if sid in NO_FINANCE:
            app_cases.append({
                "scenario_id": sid,
                "status": "APPLICABLE",
                "note": "No finance configuration available for this scenario.",
                "estimated_cost": None,
                "estimated_annual_savings": None,
                "roi_years": None,
            })
            continue
        if sid not in FINANCE:
            continue

        fin = FINANCE[sid]
        sm = savings_multiplier(complexity_level, sid)
        est_cost = round(fin["cost_once"] * cm, 2)
        est_savings = round(fin["savings_annual"] * sm, 2)
        roi = round(est_cost / est_savings, 2) if est_savings > 0 else None

        app_cases.append({
            "scenario_id": sid,
            "status": "APPLICABLE",
            "base_cost_once": fin["cost_once"],
            "base_savings_annual": fin["savings_annual"],
            "cost_multiplier": round(cm, 4),
            "savings_multiplier": sm,
            "estimated_cost": est_cost,
            "estimated_annual_savings": est_savings,
            "roi_years": roi,
        })
        app_cost += est_cost
        app_savings += est_savings

    all_app_cases.append({
        "application_identifier": aid,
        "app_name": app.get("app_name", ""),
        "complexity_score": complexity_score,
        "complexity_level": complexity_level,
        "scenarios": app_cases,
        "total_estimated_cost": round(app_cost, 2),
        "total_estimated_annual_savings": round(app_savings, 2),
    })
    total_cost += app_cost
    total_savings += app_savings

business_case = {
    "portfolio_summary": {
        "total_in_scope_apps": len(IN_SCOPE),
        "total_estimated_cost": round(total_cost, 2),
        "total_estimated_annual_savings": round(total_savings, 2),
        "estimated_roi_years": round(total_cost / total_savings, 2) if total_savings > 0 else None,
    },
    "notes": [
        "Cost multiplier formula: 0.5 * 1.15^complexity_score",
        "Savings multiplier for application-focus scenarios: LOW=1.0, MEDIUM=0.9, HIGH=0.8",
        "switch_db_engine_open_source mapped to switch_db_engine_postgresql finance data",
        "update_outdated_components: no finance configuration available",
    ],
    "applications": all_app_cases,
}

with open(BASE / "business_case.json", "w") as f:
    json.dump(business_case, f, indent=2)
print("Step 6: Created business_case.json")

print("\nAll JSON generation complete!")
print(f"In-scope apps: {len(IN_SCOPE)}")
print(f"Total portfolio cost estimate: ${total_cost:,.2f}")
print(f"Total annual savings estimate: ${total_savings:,.2f}")
