#!/usr/bin/env python3
"""
Comprehensive portfolio modernization analysis generator.
Produces all output files for steps 1-7.
"""

import json
import os
import math
from pathlib import Path

BASE = Path("/home/runner/work/copilot-test-ktruchcz/copilot-test-ktruchcz/discover")
OUTPUT = BASE / "output"
APP_MODEL = OUTPUT / "applications" / "internal_app_model"

# ─── Helpers ───────────────────────────────────────────────────────────────────

def mkdir(p):
    Path(p).mkdir(parents=True, exist_ok=True)

def write_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  wrote {path}")

def load_app(app_id):
    with open(APP_MODEL / f"{app_id}.json") as f:
        return json.load(f)

def server_list(app):
    sv = app.get("server_instances", [])
    if isinstance(sv, str):
        return [sv]
    return sv or []

# ─── App IDs ──────────────────────────────────────────────────────────────────

ALL_IDS = [f"app{str(i).zfill(3)}" for i in range(1, 31)]
OUT_OF_SCOPE_IDS = {"app005", "app007", "app009", "app029"}
IN_SCOPE_IDS = [a for a in ALL_IDS if a not in OUT_OF_SCOPE_IDS]

# ─── STEP 1: Consolidated overview + schema files ─────────────────────────────

def step1():
    print("\n=== STEP 1: Consolidated overview & schema ===")

    consolidated = []
    for app_id in ALL_IDS:
        app = load_app(app_id)
        consolidated.append(app)

    write_json(OUTPUT / "applications" / "consolidated_applications_overview.json", consolidated)

    schema_dir = OUTPUT / "applications" / "consolidated_schema"
    mkdir(schema_dir)

    for app in consolidated:
        aid = app["app_id"]
        decomm = app.get("additional_attributes", {}).get("decomission_date") if app.get("additional_attributes") else None
        schema = {
            "app_id": aid,
            "name": app["app_name"],
            "description": app.get("app_description", ""),
            "Solution type": app["solution_type"],
            "criticality": app["business_criticality"],
            "Application status": app["application_status"],
            "Decomission date": str(decomm) if decomm else None,
            "Deployment type": app.get("deployment_type", "On-Premise"),
            "data classification": app.get("data_classification", "Internal"),
            "business unit": app.get("business_unit", "IT"),
            "number of users": str(app.get("user_count", 0)),
            "Operating system": app["operating_system"],
            "programming language": app["programming_language"],
            "Application Server type": app.get("application_server"),
            "Application Architecture": app.get("application_architecture", "unknown"),
            "Application is containerized": app.get("is_containerized", "No"),
            "Number of environments": app.get("environment_count", 1),
            "Physical servers instances": server_list(app),
            "external interfaces": app.get("external_interface_count", 0),
            "db_engine": app["database_engine"]
        }
        write_json(schema_dir / f"consolidated_schema_application_{aid}.json", schema)

    # Schema exports
    schemas_dir = OUTPUT / "schemas"
    mkdir(schemas_dir)

    internal_schema = {
        "schema_name": "internal_app_model",
        "version": "1.0",
        "fields": [
            "app_id","app_name","app_description","solution_type","business_criticality",
            "application_status","deployment_type","data_classification","business_unit",
            "business_capabilities","user_count","operating_system","programming_language",
            "application_server","application_architecture","is_containerized",
            "environment_count","server_instances","cpu_cores","memory_gb",
            "production_environments","ci_cd_present","api_endpoint_count",
            "external_interface_count","database_engine","database_storage_gb",
            "database_license_required","logging_solution","monitoring_tool","additional_attributes"
        ]
    }
    write_json(schemas_dir / "internal_app_model_schema.json", internal_schema)

    consolidated_schema = {
        "schema_name": "consolidated_schema",
        "version": "1.0",
        "fields": [
            "app_id","name","description","Solution type","criticality","Application status",
            "Decomission date","Deployment type","data classification","business unit",
            "number of users","Operating system","programming language",
            "Application Server type","Application Architecture",
            "Application is containerized","Number of environments",
            "Physical servers instances","external interfaces","db_engine"
        ]
    }
    write_json(schemas_dir / "consolidated_schema.json", consolidated_schema)


# ─── STEP 2: Out-of-scope ─────────────────────────────────────────────────────

def step2():
    print("\n=== STEP 2: Out-of-scope assessment ===")
    oos_dir = OUTPUT / "out_of_scope_results"
    mkdir(oos_dir)

    for app_id in ALL_IDS:
        app = load_app(app_id)
        is_retired = app["application_status"] == "Retired"

        desc_lower = (app.get("app_description") or "").lower()
        name_lower = app["app_name"].lower()
        sol_lower = app["solution_type"].lower()
        is_sap = "sap" in desc_lower or "sap" in name_lower or "sap" in sol_lower

        result = {
            "application_identifier": app_id,
            "assessments": [
                {
                    "exclusion_type": "RETIRED",
                    "applies": is_retired,
                    "confidence": 9,
                    "reasoning": f"Application status is {app['application_status']}."
                },
                {
                    "exclusion_type": "SAP",
                    "applies": is_sap,
                    "confidence": 9,
                    "reasoning": "SAP indicators found in name/description." if is_sap else "No SAP indicators found."
                }
            ],
            "out_of_scope": is_retired or is_sap
        }
        write_json(oos_dir / f"out_of_scope_{app_id}.json", result)


# ─── Technology lifecycle reference ───────────────────────────────────────────

TECH_LIFECYCLE = {
    # OS
    "AIX 7.2":               ("OUTDATED",        "IBM AIX 7.2 is aging; extended support but limited future roadmap."),
    "AIX 6":                 ("EOL",             "AIX 6 reached end of service in April 2015."),
    "RHEL 7":                ("EOL",             "Red Hat Enterprise Linux 7 reached End of Maintenance in June 2024."),
    "RHEL 8":                ("CURRENT_VERSION", "RHEL 8 is supported until May 2029."),
    "Windows Server 2012":   ("EOL",             "Windows Server 2012 reached End of Support in October 2023."),
    "Windows Server 2016":   ("OUTDATED",        "Windows Server 2016 mainstream support ended Jan 2022; extended to Jan 2027."),
    "Windows Server 2019":   ("CURRENT_VERSION", "Windows Server 2019 is supported until January 2029."),
    "Windows Server 2022":   ("CURRENT_VERSION", "Windows Server 2022 is supported until October 2031."),
    "Debian 6":              ("EOL",             "Debian 6 Squeeze reached end of life in May 2014."),
    "Debian 7":              ("EOL",             "Debian 7 Wheezy reached end of life in May 2018."),
    "CentOS 7":              ("EOL",             "CentOS 7 reached end of life in June 2024."),
    "Ubuntu 14":             ("EOL",             "Ubuntu 14.04 LTS reached end of life in April 2019."),
    # Languages
    "COBOL-2014":            ("OUTDATED",        "COBOL-2014 is a decades-old standard; not EOL but significantly outdated."),
    "Java 8":                ("OUTDATED",        "Java 8 is still receiving patches from some vendors but is an older LTS generation."),
    "Java 11":               ("OUTDATED",        "Java 11 LTS is superseded by Java 17 and 21; approaching end of active support."),
    "Java 17":               ("CURRENT_VERSION", "Java 17 is the current LTS and actively supported."),
    "Python 3.7":            ("EOL",             "Python 3.7 reached end of life in June 2023."),
    "Python 3.8":            ("OUTDATED",        "Python 3.8 reached end of support in October 2024."),
    "Python 3.9":            ("OUTDATED",        "Python 3.9 reaches end of support in October 2025."),
    "Python 3.11":           ("CURRENT_VERSION", "Python 3.11 is actively supported until October 2027."),
    "Node.js 14":            ("EOL",             "Node.js 14 reached end of life in April 2023."),
    "Node.js 18":            ("CURRENT_VERSION", "Node.js 18 is a current LTS version supported until April 2025."),
    "Go 1.16":               ("OUTDATED",        "Go 1.16 is superseded by multiple newer releases."),
    "Go 1.19":               ("OUTDATED",        "Go 1.19 is superseded; only last two releases receive security updates."),
    "Ruby 2.7":              ("EOL",             "Ruby 2.7 reached end of life in March 2023."),
    "Rust 1.70":             ("CURRENT_VERSION", "Rust follows a rolling release; 1.70 is within supported range."),
    "PHP 8.1":               ("CURRENT_VERSION", "PHP 8.1 is supported until November 2025."),
    "C# .NET 6":             ("OUTDATED",        ".NET 6 reached end of support in May 2024."),
    "ASP.NET Core":          ("CURRENT_VERSION", "ASP.NET Core (latest) is actively supported."),
    "VB.NET":                ("OUTDATED",        "VB.NET is in maintenance mode; no new language features are planned."),
    "Angular 15":            ("OUTDATED",        "Angular 15 is superseded by multiple newer major versions."),
    "React Native":          ("CURRENT_VERSION", "React Native is actively maintained with recent releases."),
    "Scala 2.13":            ("OUTDATED",        "Scala 2.13 is stable but superseded by Scala 3."),
    "C++ 17":                ("CURRENT_VERSION", "C++17 is widely supported and still a current standard."),
    "FORTRAN 2018":          ("OUTDATED",        "FORTRAN 2018 is the latest standard but the ecosystem is legacy."),
    "PowerShell":            ("CURRENT_VERSION", "PowerShell 7.x is actively maintained."),
    "Perl":                  ("OUTDATED",        "Perl is actively maintained but declining in industry adoption."),
    ".NET Core":             ("OUTDATED",        ".NET Core 3.x reached end of support; superseded by .NET 5+."),
    # Databases
    "Oracle 19c":            ("CURRENT_VERSION", "Oracle 19c is on extended support through 2027."),
    "Oracle 12c":            ("EOL",             "Oracle 12c reached end of Extended Support in July 2022."),
    "Oracle 11g":            ("EOL",             "Oracle 11g reached end of Extended Support in December 2020."),
    "SQL Server 2014":       ("EOL",             "SQL Server 2014 reached end of Extended Support in July 2024."),
    "SQL Server 2016":       ("OUTDATED",        "SQL Server 2016 mainstream support ended; extended support until July 2026."),
    "SQL Server 2019":       ("CURRENT_VERSION", "SQL Server 2019 is supported until 2030."),
    "SQL Server 2022":       ("CURRENT_VERSION", "SQL Server 2022 is the latest version and actively supported."),
    "PostgreSQL 13":         ("OUTDATED",        "PostgreSQL 13 reaches end of support in November 2025."),
    "PostgreSQL 14":         ("CURRENT_VERSION", "PostgreSQL 14 is supported until November 2026."),
    "PostgreSQL 15":         ("CURRENT_VERSION", "PostgreSQL 15 is actively supported."),
    "MySQL 5.7":             ("EOL",             "MySQL 5.7 reached end of life in October 2023."),
    "MySQL 8.0":             ("CURRENT_VERSION", "MySQL 8.0 is the current GA release."),
    "MongoDB":               ("CURRENT_VERSION", "MongoDB latest versions are actively maintained."),
    "DB2":                   ("OUTDATED",        "IBM Db2 is still supported but considered a legacy platform."),
    "Aurora PostgreSQL":     ("CURRENT_VERSION", "Amazon Aurora PostgreSQL is a managed service with continuous updates."),
    "Amazon RDS MySQL":      ("CURRENT_VERSION", "Amazon RDS MySQL is a managed service with continuous updates."),
}

def get_tech(tech_name):
    return TECH_LIFECYCLE.get(tech_name, ("NO_KNOWLEDGE", f"No lifecycle data available for {tech_name}."))


# ─── STEP 3: Technology Assessment ───────────────────────────────────────────

def step3():
    print("\n=== STEP 3: Technology assessment ===")
    ta_dir = OUTPUT / "technology_assessment"
    mkdir(ta_dir)

    for app_id in IN_SCOPE_IDS:
        app = load_app(app_id)
        os_status, os_reason = get_tech(app["operating_system"])
        lang_status, lang_reason = get_tech(app["programming_language"])
        db_status, db_reason = get_tech(app["database_engine"])

        components = [
            {"component_type": "operating_system", "name": app["operating_system"], "status": os_status, "reasoning": os_reason},
            {"component_type": "programming_language", "name": app["programming_language"], "status": lang_status, "reasoning": lang_reason},
            {"component_type": "database", "name": app["database_engine"], "status": db_status, "reasoning": db_reason},
        ]
        if app.get("application_server"):
            asrv_status, asrv_reason = get_tech(app["application_server"])
            components.append({"component_type": "application_server", "name": app["application_server"], "status": asrv_status, "reasoning": asrv_reason})

        statuses = [c["status"] for c in components]
        if "EOL" in statuses:
            overall = "EOL"
        elif "OUTDATED" in statuses:
            overall = "OUTDATED"
        elif all(s == "CURRENT_VERSION" for s in statuses):
            overall = "CURRENT_VERSION"
        else:
            overall = "NO_KNOWLEDGE"

        result = {
            "application_identifier": app_id,
            "application_name": app["app_name"],
            "overall_technology_status": overall,
            "components": components
        }
        write_json(ta_dir / f"technology_assessment_{app_id}.json", result)


# ─── STEP 4: Complexity Assessment ───────────────────────────────────────────

def complexity_score(app):
    # Technology age (25%)
    os_s, _ = get_tech(app["operating_system"])
    lang_s, _ = get_tech(app["programming_language"])
    db_s, _ = get_tech(app["database_engine"])
    status_map = {"EOL": 10, "OUTDATED": 6, "CURRENT_VERSION": 2, "NO_KNOWLEDGE": 5}
    tech_raw = max(status_map[os_s], status_map[lang_s], status_map[db_s])
    tech_score = tech_raw * 0.25

    # Integration complexity (20%)
    ifc = app.get("external_interface_count", 0)
    if ifc >= 20:
        integ_raw = 10
    elif ifc >= 10:
        integ_raw = 7
    elif ifc >= 5:
        integ_raw = 4
    else:
        integ_raw = 2
    integ_score = integ_raw * 0.20

    # Infrastructure scale (15%)
    svs = len(server_list(app))
    envs = app.get("environment_count", 1)
    infra_raw = min(10, svs * 2 + envs)
    infra_score = infra_raw * 0.15

    # Business criticality (15%)
    crit_map = {"Critical": 10, "High": 7, "Medium": 4, "Low": 2}
    crit_raw = crit_map.get(app["business_criticality"], 5)
    crit_score = crit_raw * 0.15

    # Code & architecture (15%)
    arch = app.get("application_architecture", "unknown").lower()
    containerized = app.get("is_containerized", "No")
    ci_cd = app.get("ci_cd_present", "No")
    arch_raw = 7
    if "1-tier" in arch or "monolith" in arch:
        arch_raw = 9
    elif "2-tier" in arch:
        arch_raw = 6
    elif "3-tier" in arch or "microservice" in arch:
        arch_raw = 4
    elif "unknown" in arch:
        arch_raw = 6
    if containerized == "Yes":
        arch_raw = max(1, arch_raw - 2)
    if ci_cd == "Yes":
        arch_raw = max(1, arch_raw - 1)
    arch_score = arch_raw * 0.15

    # Data complexity (10%)
    db_storage = app.get("database_storage_gb", 0)
    if db_storage >= 5000:
        data_raw = 10
    elif db_storage >= 1000:
        data_raw = 7
    elif db_storage >= 100:
        data_raw = 5
    else:
        data_raw = 3
    data_score = data_raw * 0.10

    total = tech_score + integ_score + infra_score + crit_score + arch_score + data_score
    final = max(1, min(10, round(total)))

    if final <= 3:
        classification = "LOW"
    elif final <= 6:
        classification = "MEDIUM"
    else:
        classification = "HIGH"

    return final, classification, {
        "technology_age_eol": round(tech_score, 2),
        "integration_complexity": round(integ_score, 2),
        "infrastructure_scale": round(infra_score, 2),
        "business_criticality": round(crit_score, 2),
        "code_and_architecture": round(arch_score, 2),
        "data_complexity": round(data_score, 2)
    }


def step4():
    print("\n=== STEP 4: Complexity assessment ===")
    cx_dir = OUTPUT / "complexity_results"
    mkdir(cx_dir)

    scores = {}
    for app_id in IN_SCOPE_IDS:
        app = load_app(app_id)
        score, classification, breakdown = complexity_score(app)
        scores[app_id] = score

        result = {
            "application_identifier": app_id,
            "application_name": app["app_name"],
            "complexity_score": score,
            "complexity_classification": classification,
            "score_breakdown": breakdown,
            "reasoning": (
                f"{app['app_name']} scores {score}/10 ({classification}). "
                f"Key drivers: OS={app['operating_system']}, "
                f"Lang={app['programming_language']}, "
                f"DB={app['database_engine']}, "
                f"Criticality={app['business_criticality']}, "
                f"Interfaces={app.get('external_interface_count',0)}."
            )
        }
        write_json(cx_dir / f"complexity_{app_id}.json", result)

    return scores


# ─── STEP 5: Scenario Analysis ───────────────────────────────────────────────

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
]

def assess_scenarios(app, cx_score):
    os_name = app["operating_system"]
    lang = app["programming_language"]
    db = app["database_engine"]
    sol_type = app["solution_type"]
    is_3rd_party = sol_type == "3rd party software"
    containerized = app.get("is_containerized", "No") == "Yes"
    ci_cd = app.get("ci_cd_present", "No") == "Yes"
    criticality = app["business_criticality"]
    arch = app.get("application_architecture", "unknown").lower()

    os_st, _ = get_tech(os_name)
    lang_st, _ = get_tech(lang)
    db_st, _ = get_tech(db)

    linux_oses = ["RHEL","CentOS","Debian","Ubuntu","AIX"]
    is_linux = any(x.lower() in os_name.lower() for x in linux_oses)
    is_windows = "Windows" in os_name

    proprietary_dbs = ["Oracle", "SQL Server", "DB2"]
    has_proprietary_db = any(p in db for p in proprietary_dbs)
    has_eol_db = db_st == "EOL"
    has_outdated_db = db_st in ("EOL", "OUTDATED")

    results = {}

    # 1. os_update_security_patch
    if os_st == "EOL":
        status = "APPLICABLE"
        reasoning = f"OS {os_name} is EOL; security patch update is needed."
    elif os_st == "OUTDATED":
        status = "APPLICABLE"
        reasoning = f"OS {os_name} is outdated; update recommended."
    else:
        status = "NOT_APPLICABLE"
        reasoning = f"OS {os_name} is current; no immediate patch needed."
    results["os_update_security_patch"] = {"status": status, "reasoning": reasoning}

    # 2. switch_to_standard_linux_os
    if is_windows:
        if is_3rd_party:
            status = "PARTIALLY_FULFILLED"
            reasoning = f"Running on {os_name}; switch to Linux may require vendor support confirmation for 3rd party software."
        else:
            status = "APPLICABLE"
            reasoning = f"Running on {os_name}; migrating to standard Linux would reduce licensing costs."
    elif os_name.startswith("AIX"):
        status = "APPLICABLE"
        reasoning = f"Running on {os_name} (UNIX); migrating to standard Linux would modernize infrastructure."
    else:
        status = "FULFILLED"
        reasoning = f"Already running on standard Linux ({os_name})."
    results["switch_to_standard_linux_os"] = {"status": status, "reasoning": reasoning}

    # 3. switch_to_arm_cpu
    if containerized and not is_3rd_party:
        status = "APPLICABLE"
        reasoning = "Application is containerized; ARM CPU adoption is feasible with image rebuilds."
    elif containerized and is_3rd_party:
        status = "PARTIALLY_FULFILLED"
        reasoning = "Containerized 3rd party app; ARM support depends on vendor."
    elif is_3rd_party:
        status = "BLOCKED"
        reasoning = "3rd party software; ARM support depends on vendor roadmap."
    else:
        status = "APPLICABLE"
        reasoning = "ARM CPU migration is possible with recompilation/containerization effort."
    results["switch_to_arm_cpu"] = {"status": status, "reasoning": reasoning}

    # 4. application_server_replacement
    app_server = app.get("application_server")
    if app_server:
        status = "APPLICABLE"
        reasoning = f"Uses application server {app_server}; replacement/upgrade may be beneficial."
    elif is_3rd_party:
        status = "NOT_APPLICABLE"
        reasoning = "3rd party software; application server is managed by vendor."
    else:
        status = "NOT_APPLICABLE"
        reasoning = "No dedicated application server identified; scenario not applicable."
    results["application_server_replacement"] = {"status": status, "reasoning": reasoning}

    # 5. app_deployment_to_cloud
    if criticality == "Critical" and cx_score >= 7:
        status = "PARTIALLY_FULFILLED"
        reasoning = f"Critical application with high complexity ({cx_score}/10); cloud migration requires careful planning."
    elif is_3rd_party:
        status = "APPLICABLE"
        reasoning = "3rd party software; cloud-hosted or SaaS version likely available."
    else:
        status = "APPLICABLE"
        reasoning = "Application can be migrated to cloud (lift & shift)."
    results["app_deployment_to_cloud"] = {"status": status, "reasoning": reasoning}

    # 6. app_containerization
    if containerized:
        status = "FULFILLED"
        reasoning = "Application is already containerized."
    elif is_3rd_party:
        status = "BLOCKED"
        reasoning = "3rd party software; containerization depends on vendor support."
    elif "1-tier" in arch or "cobol" in lang.lower() or "fortran" in lang.lower():
        status = "PARTIALLY_FULFILLED"
        reasoning = f"Legacy architecture/language ({lang}); containerization is complex but possible with effort."
    else:
        status = "APPLICABLE"
        reasoning = "Application can be containerized to improve portability and scalability."
    results["app_containerization"] = {"status": status, "reasoning": reasoning}

    # 7. app_refactor_decoupling
    if is_3rd_party:
        status = "BLOCKED"
        reasoning = "3rd party software; source code refactoring is not feasible."
    elif "1-tier" in arch or "cobol" in lang.lower() or "fortran" in lang.lower():
        status = "APPLICABLE"
        reasoning = f"Monolithic/legacy architecture with {lang}; refactoring and decoupling recommended."
    elif cx_score >= 7:
        status = "APPLICABLE"
        reasoning = f"High complexity ({cx_score}/10); refactoring would reduce technical debt."
    elif "3-tier" in arch or "microservice" in arch:
        status = "PARTIALLY_FULFILLED"
        reasoning = "Already uses multi-tier architecture; further decomposition may be beneficial."
    else:
        status = "APPLICABLE"
        reasoning = "Refactoring would improve maintainability and reduce technical debt."
    results["app_refactor_decoupling"] = {"status": status, "reasoning": reasoning}

    # 8. upgrade_legacy_databases
    if has_eol_db:
        status = "APPLICABLE"
        reasoning = f"Database {db} is EOL; upgrade is critical for security."
    elif has_outdated_db:
        status = "APPLICABLE"
        reasoning = f"Database {db} is outdated; upgrade recommended."
    elif is_3rd_party and has_outdated_db:
        status = "PARTIALLY_FULFILLED"
        reasoning = f"3rd party software with outdated database {db}; upgrade depends on vendor."
    else:
        status = "NOT_APPLICABLE"
        reasoning = f"Database {db} is current; no immediate upgrade needed."
    results["upgrade_legacy_databases"] = {"status": status, "reasoning": reasoning}

    # 9. switch_db_engine_open_source
    if has_proprietary_db and not is_3rd_party:
        status = "APPLICABLE"
        reasoning = f"Uses proprietary database {db}; switching to PostgreSQL/MySQL would reduce licensing costs."
    elif has_proprietary_db and is_3rd_party:
        status = "PARTIALLY_FULFILLED"
        reasoning = f"3rd party software using proprietary database {db}; switch feasibility depends on vendor."
    else:
        status = "NOT_APPLICABLE"
        reasoning = f"Already using open source or managed database ({db})."
    results["switch_db_engine_open_source"] = {"status": status, "reasoning": reasoning}

    # 10. update_outdated_components
    has_outdated = any(s in ("EOL", "OUTDATED") for s in [os_st, lang_st, db_st])
    if has_outdated and is_3rd_party:
        status = "PARTIALLY_FULFILLED"
        reasoning = "3rd party software with outdated components; updates depend on vendor release schedule."
    elif has_outdated:
        status = "APPLICABLE"
        reasoning = f"Multiple outdated components detected (OS: {os_st}, Lang: {lang_st}, DB: {db_st})."
    else:
        status = "NOT_APPLICABLE"
        reasoning = "All components are current; no immediate updates needed."
    results["update_outdated_components"] = {"status": status, "reasoning": reasoning}

    return results


def step5():
    print("\n=== STEP 5: Scenario analysis ===")
    sa_dir = OUTPUT / "scenario_applicability_results"
    mkdir(sa_dir)

    all_scenario_results = {}
    for app_id in IN_SCOPE_IDS:
        app = load_app(app_id)
        cx_path = OUTPUT / "complexity_results" / f"complexity_{app_id}.json"
        with open(cx_path) as f:
            cx_data = json.load(f)
        cx_score = cx_data["complexity_score"]

        scenario_results = assess_scenarios(app, cx_score)

        assessments = []
        for sc_name in SCENARIOS:
            sr = scenario_results.get(sc_name, {"status": "NOT_APPLICABLE", "reasoning": "No assessment available."})
            assessments.append({
                "scenario_id": sc_name,
                "status": sr["status"],
                "reasoning": sr["reasoning"]
            })

        result = {
            "application_identifier": app_id,
            "application_name": app["app_name"],
            "scenario_assessments": assessments
        }
        write_json(sa_dir / f"scenario_assessment_{app_id}.json", result)
        all_scenario_results[app_id] = scenario_results

    return all_scenario_results


# ─── STEP 6: Business Case ────────────────────────────────────────────────────

FINANCE_CONFIG = {
    "os_update_security_patch":     {"cost": 1000,   "savings_per_year": 500},
    "switch_to_standard_linux_os":  {"cost": 300,    "savings_per_year": 400},
    "switch_to_arm_cpu":            {"cost": 5000,   "savings_per_year": 1000},
    "application_server_replacement":{"cost": 10000, "savings_per_year": 12000},
    "app_deployment_to_cloud":      {"cost": 5000,   "savings_per_year": 3000},
    "app_containerization":         {"cost": 100000, "savings_per_year": 100000},
    "app_refactor_decoupling":      {"cost": 250000, "savings_per_year": 150000},
    "upgrade_legacy_databases":     {"cost": 10000,  "savings_per_year": 10000},
    "switch_db_engine_open_source": {"cost": 25000,  "savings_per_year": 15000},
    # update_outdated_components: no finance config
}


def step6(scenario_results):
    print("\n=== STEP 6: Business case ===")
    bc_dir = OUTPUT / "business_case_results"
    mkdir(bc_dir)

    portfolio_entries = []
    total_cost = 0
    total_savings = 0

    crit_savings_mult = {"Low": 1.0, "Medium": 0.9, "High": 0.8, "Critical": 0.8}

    for app_id in IN_SCOPE_IDS:
        app = load_app(app_id)
        cx_path = OUTPUT / "complexity_results" / f"complexity_{app_id}.json"
        with open(cx_path) as f:
            cx_data = json.load(f)
        cx_score = cx_data["complexity_score"]
        criticality = app["business_criticality"]

        cost_multiplier = 0.5 * (1.15 ** cx_score)
        savings_mult = crit_savings_mult.get(criticality, 0.9)

        sc_results = scenario_results.get(app_id, {})
        app_scenarios = []
        app_total_cost = 0
        app_total_savings = 0

        for sc_name, fc in FINANCE_CONFIG.items():
            sc = sc_results.get(sc_name, {})
            status = sc.get("status", "NOT_APPLICABLE")
            if status != "APPLICABLE":
                continue

            impl_cost = round(fc["cost"] * cost_multiplier, 2)
            ann_savings = round(fc["savings_per_year"] * savings_mult, 2)
            roi_3yr = round((ann_savings * 3 - impl_cost) / impl_cost * 100, 1) if impl_cost > 0 else 0
            payback_months = round(impl_cost / (ann_savings / 12), 1) if ann_savings > 0 else None

            app_scenarios.append({
                "scenario_id": sc_name,
                "implementation_cost": impl_cost,
                "annual_savings": ann_savings,
                "roi_3_year_pct": roi_3yr,
                "payback_months": payback_months
            })
            app_total_cost += impl_cost
            app_total_savings += ann_savings

        portfolio_entries.append({
            "application_identifier": app_id,
            "application_name": app["app_name"],
            "complexity_score": cx_score,
            "cost_multiplier": round(cost_multiplier, 4),
            "total_implementation_cost": round(app_total_cost, 2),
            "total_annual_savings": round(app_total_savings, 2),
            "roi_3_year_pct": round((app_total_savings * 3 - app_total_cost) / app_total_cost * 100, 1) if app_total_cost > 0 else 0,
            "scenarios": app_scenarios
        })
        total_cost += app_total_cost
        total_savings += app_total_savings

    business_case = {
        "portfolio_summary": {
            "total_applications_analyzed": len(IN_SCOPE_IDS),
            "total_implementation_cost": round(total_cost, 2),
            "total_annual_savings": round(total_savings, 2),
            "portfolio_roi_3_year_pct": round((total_savings * 3 - total_cost) / total_cost * 100, 1) if total_cost > 0 else 0
        },
        "applications": portfolio_entries
    }
    write_json(bc_dir / "business_case.json", business_case)
    return business_case


# ─── STEP 7: Reports ──────────────────────────────────────────────────────────

STATUS_EMOJI = {
    "CURRENT_VERSION": "✅",
    "OUTDATED": "⚠️",
    "EOL": "🔴",
    "NO_KNOWLEDGE": "❓"
}

SCENARIO_LABELS = {
    "os_update_security_patch": "OS Update / Security Patch",
    "switch_to_standard_linux_os": "Switch to Standard Linux OS",
    "switch_to_arm_cpu": "Switch to ARM CPU",
    "application_server_replacement": "Application Server Replacement",
    "app_deployment_to_cloud": "Cloud Migration (Lift & Shift)",
    "app_containerization": "Containerization",
    "app_refactor_decoupling": "Refactoring & Decoupling",
    "upgrade_legacy_databases": "Upgrade Legacy Databases",
    "switch_db_engine_open_source": "Switch to Open Source DB",
    "update_outdated_components": "Update Outdated Components",
}

def step7(business_case):
    print("\n=== STEP 7: Reports ===")
    apps_rpt = OUTPUT / "reports" / "apps"
    mkdir(apps_rpt)

    bc_by_app = {e["application_identifier"]: e for e in business_case["applications"]}

    for app_id in IN_SCOPE_IDS:
        app = load_app(app_id)
        name = app["app_name"]

        # Load sub-results
        with open(OUTPUT / "technology_assessment" / f"technology_assessment_{app_id}.json") as f:
            ta = json.load(f)
        with open(OUTPUT / "complexity_results" / f"complexity_{app_id}.json") as f:
            cx = json.load(f)
        with open(OUTPUT / "scenario_applicability_results" / f"scenario_assessment_{app_id}.json") as f:
            sa = json.load(f)

        bc_entry = bc_by_app.get(app_id, {})
        cx_score = cx["complexity_score"]
        cx_class = cx["complexity_classification"]

        lines = []
        lines.append(f"# {name} ({app_id})")
        lines.append("")
        lines.append(f"**Status:** {app['application_status']} | **Criticality:** {app['business_criticality']} | **Solution Type:** {app['solution_type']}")
        lines.append("")

        # Overview
        lines.append("## Overview")
        lines.append("")
        lines.append(f"| Field | Value |")
        lines.append(f"|-------|-------|")
        lines.append(f"| Description | {app.get('app_description','')} |")
        lines.append(f"| Business Unit | {app.get('business_unit','N/A')} |")
        lines.append(f"| Operating System | {app['operating_system']} |")
        lines.append(f"| Programming Language | {app['programming_language']} |")
        lines.append(f"| Database | {app['database_engine']} |")
        lines.append(f"| Architecture | {app.get('application_architecture','unknown')} |")
        lines.append(f"| Containerized | {app.get('is_containerized','No')} |")
        lines.append(f"| CI/CD Present | {app.get('ci_cd_present','No')} |")
        lines.append(f"| Environments | {app.get('environment_count',1)} |")
        lines.append(f"| Server Instances | {', '.join(server_list(app))} |")
        lines.append(f"| External Interfaces | {app.get('external_interface_count',0)} |")
        lines.append(f"| Users | {app.get('user_count',0)} |")
        lines.append("")

        # Technology
        lines.append("## Technology Assessment")
        lines.append("")
        lines.append(f"**Overall Status:** {STATUS_EMOJI.get(ta['overall_technology_status'],'')} {ta['overall_technology_status']}")
        lines.append("")
        lines.append("| Component | Name | Status |")
        lines.append("|-----------|------|--------|")
        for comp in ta["components"]:
            emoji = STATUS_EMOJI.get(comp["status"], "")
            lines.append(f"| {comp['component_type']} | {comp['name']} | {emoji} {comp['status']} |")
        lines.append("")

        # Complexity
        lines.append("## Complexity Assessment")
        lines.append("")
        lines.append(f"**Score:** {cx_score}/10 — **Classification:** {cx_class}")
        lines.append("")
        lines.append("| Factor | Score |")
        lines.append("|--------|-------|")
        for k, v in cx["score_breakdown"].items():
            lines.append(f"| {k.replace('_',' ').title()} | {v} |")
        lines.append("")

        # Scenarios
        lines.append("## Scenario Analysis")
        lines.append("")
        lines.append("| Scenario | Status | Reasoning |")
        lines.append("|----------|--------|-----------|")
        for sa_item in sa["scenario_assessments"]:
            sc_label = SCENARIO_LABELS.get(sa_item["scenario_id"], sa_item["scenario_id"])
            lines.append(f"| {sc_label} | {sa_item['status']} | {sa_item['reasoning']} |")
        lines.append("")

        # Business case
        if bc_entry and bc_entry.get("scenarios"):
            lines.append("## Business Case")
            lines.append("")
            lines.append(f"**Total Implementation Cost:** ${bc_entry['total_implementation_cost']:,.2f}")
            lines.append(f"**Total Annual Savings:** ${bc_entry['total_annual_savings']:,.2f}")
            lines.append(f"**3-Year ROI:** {bc_entry['roi_3_year_pct']}%")
            lines.append("")
            lines.append("| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |")
            lines.append("|----------|------------|----------------|----------|--------------|")
            for sc in bc_entry["scenarios"]:
                sc_label = SCENARIO_LABELS.get(sc["scenario_id"], sc["scenario_id"])
                lines.append(f"| {sc_label} | ${sc['implementation_cost']:,.2f} | ${sc['annual_savings']:,.2f} | {sc['roi_3_year_pct']}% | {sc['payback_months']} |")
            lines.append("")

        rpt_path = apps_rpt / f"report_{app_id}.md"
        with open(rpt_path, "w") as f:
            f.write("\n".join(lines))
        print(f"  wrote {rpt_path}")

    # ── Out-of-scope app stubs ──
    for app_id in OUT_OF_SCOPE_IDS:
        app = load_app(app_id)
        name = app["app_name"]
        lines = [
            f"# {name} ({app_id}) — OUT OF SCOPE",
            "",
            f"**Status:** {app['application_status']} | **Criticality:** {app['business_criticality']}",
            "",
            "This application has been excluded from modernization analysis.",
            "",
            f"**Reason:** Application status is `{app['application_status']}`.",
            "",
        ]
        rpt_path = apps_rpt / f"report_{app_id}.md"
        with open(rpt_path, "w") as f:
            f.write("\n".join(lines))
        print(f"  wrote {rpt_path}")

    # ── Portfolio report ──
    generate_portfolio_report(business_case)


def generate_portfolio_report(business_case):
    print("  generating portfolio_report.md ...")
    psumm = business_case["portfolio_summary"]
    bc_apps = {e["application_identifier"]: e for e in business_case["applications"]}

    # Gather stats
    total_apps = 30
    oos_count = len(OUT_OF_SCOPE_IDS)
    in_scope = len(IN_SCOPE_IDS)

    # Technology overview
    tech_counts = {"CURRENT_VERSION": 0, "OUTDATED": 0, "EOL": 0, "NO_KNOWLEDGE": 0}
    cx_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
    all_cx = []

    for app_id in IN_SCOPE_IDS:
        with open(OUTPUT / "technology_assessment" / f"technology_assessment_{app_id}.json") as f:
            ta = json.load(f)
        tech_counts[ta["overall_technology_status"]] = tech_counts.get(ta["overall_technology_status"], 0) + 1

        with open(OUTPUT / "complexity_results" / f"complexity_{app_id}.json") as f:
            cx = json.load(f)
        cx_counts[cx["complexity_classification"]] += 1
        all_cx.append(cx["complexity_score"])

    avg_cx = round(sum(all_cx) / len(all_cx), 1) if all_cx else 0

    lines = []
    lines.append("# Portfolio Modernization Report")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(f"This report covers the modernization analysis of **{total_apps} applications** across the enterprise portfolio.")
    lines.append(f"Of these, **{oos_count} are out-of-scope** (Retired), leaving **{in_scope} applications** for detailed assessment.")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Total Applications | {total_apps} |")
    lines.append(f"| In-Scope Applications | {in_scope} |")
    lines.append(f"| Out-of-Scope (Retired) | {oos_count} |")
    lines.append(f"| Average Complexity Score | {avg_cx}/10 |")
    lines.append(f"| Total Portfolio Implementation Cost | ${psumm['total_implementation_cost']:,.2f} |")
    lines.append(f"| Total Annual Savings | ${psumm['total_annual_savings']:,.2f} |")
    lines.append(f"| Portfolio 3-Year ROI | {psumm['portfolio_roi_3_year_pct']}% |")
    lines.append("")

    lines.append("## Technology Health Overview")
    lines.append("")
    lines.append("```mermaid")
    lines.append("pie title Technology Status Distribution")
    for k, v in tech_counts.items():
        if v > 0:
            lines.append(f'    "{k}" : {v}')
    lines.append("```")
    lines.append("")
    lines.append("| Status | Count |")
    lines.append("|--------|-------|")
    for k, v in tech_counts.items():
        lines.append(f"| {STATUS_EMOJI.get(k,'')} {k} | {v} |")
    lines.append("")

    lines.append("## Complexity Distribution")
    lines.append("")
    lines.append("```mermaid")
    lines.append("pie title Complexity Classification")
    for k, v in cx_counts.items():
        if v > 0:
            lines.append(f'    "{k}" : {v}')
    lines.append("```")
    lines.append("")
    lines.append("| Classification | Count |")
    lines.append("|----------------|-------|")
    for k, v in cx_counts.items():
        lines.append(f"| {k} | {v} |")
    lines.append("")

    lines.append("## Application Portfolio Overview")
    lines.append("")
    lines.append("| App ID | Name | Status | Criticality | OS Tech | Complexity | Impl. Cost | Annual Savings |")
    lines.append("|--------|------|--------|-------------|---------|------------|------------|----------------|")

    for app_id in ALL_IDS:
        app = load_app(app_id)
        name = app["app_name"]
        status = app["application_status"]
        crit = app["business_criticality"]

        if app_id in OUT_OF_SCOPE_IDS:
            lines.append(f"| {app_id} | {name} | ⚫ {status} | {crit} | — | — | — | — |")
            continue

        with open(OUTPUT / "technology_assessment" / f"technology_assessment_{app_id}.json") as f:
            ta = json.load(f)
        with open(OUTPUT / "complexity_results" / f"complexity_{app_id}.json") as f:
            cx = json.load(f)

        os_st = next((c["status"] for c in ta["components"] if c["component_type"] == "operating_system"), "NO_KNOWLEDGE")
        bc_e = bc_apps.get(app_id, {})
        impl_cost = f"${bc_e.get('total_implementation_cost',0):,.0f}" if bc_e else "—"
        ann_sav = f"${bc_e.get('total_annual_savings',0):,.0f}" if bc_e else "—"
        lines.append(f"| {app_id} | {name} | {status} | {crit} | {STATUS_EMOJI.get(os_st,'')} {os_st} | {cx['complexity_score']}/10 ({cx['complexity_classification']}) | {impl_cost} | {ann_sav} |")

    lines.append("")

    lines.append("## Top Modernization Scenarios by Portfolio Impact")
    lines.append("")

    scenario_totals = {}
    for app_id in IN_SCOPE_IDS:
        bc_e = bc_apps.get(app_id, {})
        for sc in bc_e.get("scenarios", []):
            sid = sc["scenario_id"]
            if sid not in scenario_totals:
                scenario_totals[sid] = {"cost": 0, "savings": 0, "apps": 0}
            scenario_totals[sid]["cost"] += sc["implementation_cost"]
            scenario_totals[sid]["savings"] += sc["annual_savings"]
            scenario_totals[sid]["apps"] += 1

    sorted_scenarios = sorted(scenario_totals.items(), key=lambda x: x[1]["savings"] * 3 - x[1]["cost"], reverse=True)
    lines.append("| Scenario | Apps | Total Cost | Annual Savings | 3-Yr Net Value |")
    lines.append("|----------|------|------------|----------------|----------------|")
    for sc_id, vals in sorted_scenarios:
        label = SCENARIO_LABELS.get(sc_id, sc_id)
        net = vals["savings"] * 3 - vals["cost"]
        lines.append(f"| {label} | {vals['apps']} | ${vals['cost']:,.0f} | ${vals['savings']:,.0f} | ${net:,.0f} |")
    lines.append("")

    lines.append("## Out-of-Scope Applications")
    lines.append("")
    lines.append("| App ID | Name | Reason |")
    lines.append("|--------|------|--------|")
    for app_id in sorted(OUT_OF_SCOPE_IDS):
        app = load_app(app_id)
        lines.append(f"| {app_id} | {app['app_name']} | Retired |")
    lines.append("")

    lines.append("## Recommendations")
    lines.append("")
    lines.append("1. **Prioritize EOL OS remediation**: Multiple applications run on EOL operating systems (AIX 6, Debian 6/7, Windows Server 2012, CentOS 7). Immediate patching or migration is required.")
    lines.append("2. **Database upgrades**: Oracle 11g/12c and MySQL 5.7 are EOL; SQL Server 2014 reached EOL. These databases require urgent upgrades.")
    lines.append("3. **Containerization**: Containerizing eligible custom applications will enable cloud portability and reduce infrastructure costs.")
    lines.append("4. **Cloud migration**: Lift-and-shift cloud migration offers a positive ROI for most applications and reduces on-premise infrastructure burden.")
    lines.append("5. **Legacy language modernization**: COBOL, FORTRAN, and other legacy language applications (app001, app008, app026) require long-term modernization roadmaps.")
    lines.append("")

    rpt_path = OUTPUT / "reports" / "portfolio_report.md"
    with open(rpt_path, "w") as f:
        f.write("\n".join(lines))
    print(f"  wrote {rpt_path}")


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    step1()
    step2()
    step3()
    cx_scores = step4()
    scenario_results = step5()
    bc = step6(scenario_results)
    step7(bc)
    print("\n✅ All steps complete.")
