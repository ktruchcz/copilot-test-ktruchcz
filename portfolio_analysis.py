#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import os
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT_ROOT = ROOT / "output"
INTERNAL_APP_DIR = OUTPUT_ROOT / "applications" / "internal_app_model"
CONSOLIDATED_DIR = OUTPUT_ROOT / "applications" / "consolidated_schema"
SCHEMAS_DIR = OUTPUT_ROOT / "schemas"
OUT_OF_SCOPE_DIR = OUTPUT_ROOT / "out_of_scope_results"
TECH_DIR = OUTPUT_ROOT / "technology_assessment"
COMPLEXITY_DIR = OUTPUT_ROOT / "complexity_results"
SCENARIO_DIR = OUTPUT_ROOT / "scenario_applicability_results"
BUSINESS_CASE_DIR = OUTPUT_ROOT / "business_case_results"
REPORTS_DIR = OUTPUT_ROOT / "reports"
APP_REPORTS_DIR = REPORTS_DIR / "apps"
APPLICATION_HTML_DIR = REPORTS_DIR / "application_reports"
MONITORING_DIR = OUTPUT_ROOT / "00_monitoring"
SCENARIOS_PATH = ROOT / ".github" / "skills" / "modernization_scenarios_list.json"
FINANCE_PATH = ROOT / ".github" / "skills" / "modernization_scenarios_finance.json"
ASSESSMENT_DATE = "2025-01-01"
APPLICABLE_STATUSES = {"APPLICABLE", "PARTIALLY_FULFILLED"}


def ensure_directories() -> None:
    for directory in [
        CONSOLIDATED_DIR,
        SCHEMAS_DIR,
        OUT_OF_SCOPE_DIR,
        TECH_DIR,
        COMPLEXITY_DIR,
        SCENARIO_DIR,
        BUSINESS_CASE_DIR,
        APP_REPORTS_DIR,
        APPLICATION_HTML_DIR,
        MONITORING_DIR,
    ]:
        directory.mkdir(parents=True, exist_ok=True)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def safe_text(value) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_text(value) -> str:
    return safe_text(value).lower()


def to_list(value) -> list[str]:
    if isinstance(value, list):
        return [safe_text(item) for item in value if safe_text(item)]
    if safe_text(value):
        return [safe_text(value)]
    return []


def is_yes(value) -> bool:
    return normalize_text(value) in {"yes", "y", "true", "1"}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "item"


def escape_html(value) -> str:
    text = safe_text(value)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def format_currency(value) -> str:
    if value is None:
        return "n/a"
    return f"EUR {float(value):,.2f}"


def format_roi(value) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.2f}%"


def count_servers(app: dict) -> int:
    servers = app.get("server_instances")
    if isinstance(servers, list):
        return len([item for item in servers if safe_text(item)])
    return 1 if safe_text(servers) else 0


def count_dependencies(app: dict) -> int:
    dependencies = app.get("dependencies")
    if isinstance(dependencies, list):
        return len([item for item in dependencies if safe_text(item)])
    if safe_text(dependencies):
        return len([item for item in re.split(r"[,;]", safe_text(dependencies)) if safe_text(item)])
    return int(app.get("external_interface_count") or 0)


def custom_code_indicated(app: dict) -> bool:
    return "custom" in normalize_text(app.get("solution_type"))


def determine_out_of_scope(app: dict) -> dict:
    status = normalize_text(app.get("application_status"))
    name = normalize_text(app.get("app_name"))
    description = normalize_text(app.get("app_description"))
    solution_type = normalize_text(app.get("solution_type"))
    reason = None
    if "retired" in status or "retired" in name:
        reason = "RETIRED"
    elif any(re.search(r"\bsap\b", value) for value in [name, description, solution_type]):
        reason = "SAP"
    return {
        "app_id": safe_text(app.get("app_id")),
        "app_name": safe_text(app.get("app_name")),
        "out_of_scope": reason is not None,
        "reason": reason,
    }


def make_component(component_type: str, name: str, version: str, status: str, notes: str) -> dict:
    return {
        "component_type": component_type,
        "name": name,
        "version": version,
        "status": status,
        "notes": notes,
    }


def assess_operating_system(value) -> dict | None:
    text = safe_text(value)
    lower = text.lower()
    if not text:
        return None
    if match := re.search(r"rhel\s*(7|8|9)\b", lower):
        version = match.group(1)
        status = {"7": "EOL", "8": "CURRENT_VERSION", "9": "CURRENT_VERSION"}[version]
        return make_component("operating_system", "RHEL", version, status, f"Lifecycle rule matched for RHEL {version}.")
    if match := re.search(r"ubuntu\s*(18\.04|20\.04|22\.04)\b", lower):
        version = match.group(1)
        status = {"18.04": "EOL", "20.04": "OUTDATED", "22.04": "CURRENT_VERSION"}[version]
        return make_component("operating_system", "Ubuntu", version, status, f"Lifecycle rule matched for Ubuntu {version}.")
    if "windows server" in lower:
        if "2012r2" in lower or "2012 r2" in lower:
            return make_component("operating_system", "Windows Server", "2012R2", "EOL", "Lifecycle rule matched for Windows Server 2012R2.")
        for version, status in [("2012", "EOL"), ("2016", "OUTDATED"), ("2019", "CURRENT_VERSION"), ("2022", "CURRENT_VERSION")]:
            if version in lower:
                return make_component("operating_system", "Windows Server", version, status, f"Lifecycle rule matched for Windows Server {version}.")
    return make_component("operating_system", text, "unknown", "NO_KNOWLEDGE", "Operating system version is not covered by the provided lifecycle rules.")


def assess_programming_language(value) -> dict | None:
    text = safe_text(value)
    lower = text.lower()
    if not text:
        return None
    if match := re.search(r"java\s*(8|11|17|21)\b", lower):
        version = match.group(1)
        status = {"8": "EOL", "11": "OUTDATED", "17": "CURRENT_VERSION", "21": "CURRENT_VERSION"}[version]
        return make_component("programming_language", "Java", version, status, f"Lifecycle rule matched for Java {version}.")
    if ".net" in lower:
        if match := re.search(r"\.net(?:\s+core)?\s*(6|8)\b", lower):
            version = match.group(1)
            status = {"6": "EOL", "8": "CURRENT_VERSION"}[version]
            return make_component("programming_language", ".NET", version, status, f"Lifecycle rule matched for .NET {version}.")
        return make_component("programming_language", ".NET", "unknown", "NO_KNOWLEDGE", "The application uses .NET, but no supported version was provided.")
    if match := re.search(r"python\s*(2(?:\.\d+)?|3\.8|3\.9|3\.10|3\.11|3\.12)\b", lower):
        version = match.group(1)
        if version.startswith("2"):
            status = "EOL"
        else:
            status = {
                "3.8": "EOL",
                "3.9": "OUTDATED",
                "3.10": "OUTDATED",
                "3.11": "CURRENT_VERSION",
                "3.12": "CURRENT_VERSION",
            }.get(version, "NO_KNOWLEDGE")
        return make_component("programming_language", "Python", version, status, f"Lifecycle rule matched for Python {version}.")
    if match := re.search(r"angular\s*(\d+)\b", lower):
        major = int(match.group(1))
        if major <= 15:
            status = "EOL"
        elif major == 16:
            status = "OUTDATED"
        else:
            status = "CURRENT_VERSION"
        return make_component("programming_language", "Angular", str(major), status, f"Lifecycle rule matched for Angular {major}.")
    if match := re.search(r"react\s*(18|17)\b", lower):
        version = match.group(1)
        status = {"17": "OUTDATED", "18": "CURRENT_VERSION"}[version]
        return make_component("programming_language", "React", version, status, f"Lifecycle rule matched for React {version}.")
    if match := re.search(r"node(?:\.js)?\s*(16|18|20|22)\b", lower):
        version = match.group(1)
        status = {"16": "EOL", "18": "OUTDATED", "20": "CURRENT_VERSION", "22": "CURRENT_VERSION"}[version]
        return make_component("programming_language", "Node", version, status, f"Lifecycle rule matched for Node {version}.")
    return make_component("programming_language", text, "unknown", "NO_KNOWLEDGE", "Programming language or runtime version is not covered by the provided lifecycle rules.")


def assess_application_server(value) -> dict | None:
    text = safe_text(value)
    lower = text.lower()
    if not text:
        return None
    if match := re.search(r"spring\s*boot\s*(\d+)", lower):
        major = int(match.group(1))
        status = "EOL" if major == 2 else "CURRENT_VERSION" if major == 3 else "NO_KNOWLEDGE"
        return make_component("application_server", "Spring Boot", str(major), status, f"Lifecycle rule matched for Spring Boot {major}.x.")
    if "tomcat" in lower:
        match = re.search(r"tomcat[^0-9]*([0-9]+(?:\.[0-9]+)?)", lower)
        version = match.group(1) if match else "unknown"
        major = match.group(1).split(".")[0] if match else ""
        if major == "8":
            status = "EOL"
        elif major in {"9", "10"}:
            status = "CURRENT_VERSION"
        else:
            status = "NO_KNOWLEDGE"
        notes = f"Lifecycle rule matched for Tomcat {major}." if status != "NO_KNOWLEDGE" else "Tomcat version is not covered by the provided lifecycle rules."
        return make_component("application_server", "Tomcat", version, status, notes)
    if match := re.search(r"jboss\s*eap[^0-9]*([67])", lower):
        version = match.group(1)
        status = {"6": "EOL", "7": "OUTDATED"}[version]
        return make_component("application_server", "JBoss EAP", version, status, f"Lifecycle rule matched for JBoss EAP {version}.")
    if "weblogic" in lower:
        if "12c" in lower:
            return make_component("application_server", "WebLogic", "12c", "EOL", "Lifecycle rule matched for WebLogic 12c.")
        return make_component("application_server", "WebLogic", "unknown", "NO_KNOWLEDGE", "WebLogic version is not covered by the provided lifecycle rules.")
    if "liberty" in lower:
        return make_component("application_server", "WebSphere Liberty", "Liberty", "CURRENT_VERSION", "Lifecycle rule matched for WebSphere Liberty.")
    if "websphere" in lower:
        match = re.search(r"websphere[^0-9]*([0-9]+(?:\.[0-9]+)?)", lower)
        version = match.group(1) if match else "unknown"
        major = version.split(".")[0] if version != "unknown" else ""
        if major == "8":
            return make_component("application_server", "WebSphere", version, "EOL", "Lifecycle rule matched for WebSphere 8.x.")
        return make_component("application_server", "WebSphere", version, "NO_KNOWLEDGE", "WebSphere version is not covered by the provided lifecycle rules.")
    return make_component("application_server", text, "unknown", "NO_KNOWLEDGE", "Application server technology is not covered by the provided lifecycle rules.")


def assess_database(value) -> dict | None:
    text = safe_text(value)
    lower = text.lower()
    if not text:
        return None
    if "mysql" in lower:
        if "5.7" in lower:
            return make_component("database", "MySQL", "5.7", "EOL", "Lifecycle rule matched for MySQL 5.7.")
        if re.search(r"\b8(?:\.0)?\b", lower):
            return make_component("database", "MySQL", "8", "CURRENT_VERSION", "Lifecycle rule matched for MySQL 8.")
        return make_component("database", "MySQL", "unknown", "NO_KNOWLEDGE", "MySQL is identified, but no supported version is present.")
    if "postgresql" in lower:
        match = re.search(r"postgresql[^0-9]*([0-9]+)", lower)
        version = match.group(1) if match else "unknown"
        if version == "12":
            status = "EOL"
        elif version in {"14", "15", "16"}:
            status = "CURRENT_VERSION"
        else:
            status = "NO_KNOWLEDGE"
        notes = f"Lifecycle rule matched for PostgreSQL {version}." if status != "NO_KNOWLEDGE" else "PostgreSQL version is not covered by the provided lifecycle rules."
        return make_component("database", "PostgreSQL", version, status, notes)
    if "oracle" in lower:
        if "12c" in lower:
            return make_component("database", "Oracle", "12c", "EOL", "Lifecycle rule matched for Oracle 12c.")
        if "19c" in lower:
            return make_component("database", "Oracle", "19c", "CURRENT_VERSION", "Lifecycle rule matched for Oracle 19c.")
        return make_component("database", "Oracle", "unknown", "NO_KNOWLEDGE", "Oracle version is not covered by the provided lifecycle rules.")
    if "sql server" in lower:
        match = re.search(r"sql server[^0-9]*([0-9]{4})", lower)
        version = match.group(1) if match else "unknown"
        status = {
            "2014": "EOL",
            "2016": "OUTDATED",
            "2019": "CURRENT_VERSION",
            "2022": "CURRENT_VERSION",
        }.get(version, "NO_KNOWLEDGE")
        notes = f"Lifecycle rule matched for SQL Server {version}." if status != "NO_KNOWLEDGE" else "SQL Server version is not covered by the provided lifecycle rules."
        return make_component("database", "SQL Server", version, status, notes)
    return make_component("database", text, "unknown", "NO_KNOWLEDGE", "Database engine is not covered by the provided lifecycle rules.")


def technology_assessment(app: dict) -> dict:
    components = []
    for assessor, value in [
        (assess_operating_system, app.get("operating_system")),
        (assess_programming_language, app.get("programming_language")),
        (assess_application_server, app.get("application_server")),
        (assess_database, app.get("database_engine")),
    ]:
        component = assessor(value)
        if component:
            components.append(component)
    eol_count = sum(1 for component in components if component["status"] == "EOL")
    outdated_count = sum(1 for component in components if component["status"] == "OUTDATED")
    current_count = sum(1 for component in components if component["status"] == "CURRENT_VERSION")
    no_knowledge_count = sum(1 for component in components if component["status"] == "NO_KNOWLEDGE")
    if eol_count:
        overall_risk = "CRITICAL"
    elif outdated_count:
        overall_risk = "HIGH"
    elif no_knowledge_count:
        overall_risk = "MEDIUM"
    else:
        overall_risk = "LOW"
    return {
        "app_id": safe_text(app.get("app_id")),
        "app_name": safe_text(app.get("app_name")),
        "assessment_date": ASSESSMENT_DATE,
        "components": components,
        "overall_technology_risk": overall_risk,
        "eol_count": eol_count,
        "outdated_count": outdated_count,
        "current_count": current_count,
    }


def complexity_assessment(app: dict, technology: dict) -> dict:
    score = 3
    criticality = normalize_text(app.get("business_criticality"))
    criticality_adjustment = {"critical": 2, "high": 1, "medium": 0, "low": -1}.get(criticality, 0)
    score += criticality_adjustment
    eol_adjustment = min(technology.get("eol_count", 0), 3)
    score += eol_adjustment
    server_count = count_servers(app)
    server_adjustment = 2 if server_count > 5 else 1 if 2 <= server_count <= 5 else 0
    score += server_adjustment
    dependency_count = count_dependencies(app)
    dependency_adjustment = 2 if dependency_count > 10 else 1 if 5 <= dependency_count <= 10 else 0
    score += dependency_adjustment
    custom_code = custom_code_indicated(app)
    custom_code_adjustment = 1 if custom_code else 0
    score += custom_code_adjustment
    containerized = is_yes(app.get("is_containerized"))
    container_adjustment = -1 if containerized else 0
    score += container_adjustment
    score = max(1, min(10, score))
    if score <= 3:
        label = "Low"
        effort = "1-2 months"
    elif score <= 6:
        label = "Medium"
        effort = "3-6 months"
    elif score <= 9:
        label = "High"
        effort = "6-12 months"
    else:
        label = "Very High"
        effort = "12+ months"
    reasoning = (
        f"Started from base score 3, applied {criticality_adjustment:+d} for {safe_text(app.get('business_criticality')) or 'unknown'} criticality, "
        f"{eol_adjustment:+d} for {technology.get('eol_count', 0)} EOL component(s), {server_adjustment:+d} for {server_count} server(s), "
        f"{dependency_adjustment:+d} using external interfaces as the dependency proxy ({dependency_count}), {custom_code_adjustment:+d} for custom code indication, "
        f"and {container_adjustment:+d} for containerization."
    )
    return {
        "app_id": safe_text(app.get("app_id")),
        "app_name": safe_text(app.get("app_name")),
        "complexity_score": score,
        "complexity_label": label,
        "estimated_effort": effort,
        "factors": {
            "base_score": 3,
            "business_criticality": safe_text(app.get("business_criticality")),
            "criticality_adjustment": criticality_adjustment,
            "eol_components": technology.get("eol_count", 0),
            "eol_adjustment": eol_adjustment,
            "server_count": server_count,
            "server_adjustment": server_adjustment,
            "dependency_proxy": "external_interface_count",
            "dependency_count": dependency_count,
            "dependency_adjustment": dependency_adjustment,
            "custom_code": custom_code,
            "custom_code_adjustment": custom_code_adjustment,
            "containerized": containerized,
            "containerization_adjustment": container_adjustment,
        },
        "reasoning": reasoning,
    }


def component_by_type(technology: dict) -> dict:
    return {component["component_type"]: component for component in technology.get("components", [])}


def assess_scenario(app: dict, technology: dict, complexity: dict, scenario: dict) -> dict:
    scenario_id = safe_text(scenario.get("scenario_id"))
    scenario_name = safe_text(scenario.get("scenario_name"))
    comp = component_by_type(technology)
    os_component = comp.get("operating_system", {})
    app_server_component = comp.get("application_server", {})
    db_component = comp.get("database", {})
    deployment = normalize_text(app.get("deployment_type"))
    solution_type = normalize_text(app.get("solution_type"))
    os_text = normalize_text(app.get("operating_system"))
    language_text = normalize_text(app.get("programming_language"))
    app_server_text = normalize_text(app.get("application_server"))
    db_text = normalize_text(app.get("database_engine"))
    description = normalize_text(app.get("app_description"))
    containerized = is_yes(app.get("is_containerized"))
    in_cloud = any(marker in deployment for marker in ["aws", "azure", "gcp", "cloud"])
    on_prem = "on-prem" in deployment or "on premise" in deployment
    standard_linux = any(marker in os_text for marker in ["rhel", "ubuntu"])
    linux_nonstandard = any(marker in os_text for marker in ["debian", "centos"])
    windows_stack = "windows" in os_text or "iis" in app_server_text or ".net" in language_text or "vb.net" in language_text
    legacy_stack = any(marker in os_text for marker in ["aix", "debian 6", "debian 7"]) or any(marker in language_text for marker in ["cobol", "fortran"]) or any(marker in app_server_text for marker in ["websphere", "weblogic"])
    modern_portable_stack = any(marker in language_text for marker in ["java", "python", "node", "go", "rust", "php", "scala"]) and not legacy_stack
    third_party = "3rd" in solution_type or "third" in solution_type
    open_source_db = any(marker in db_text for marker in ["postgresql", "mysql", "mongodb"])
    proprietary_db = any(marker in db_text for marker in ["oracle", "sql server", "db2"])
    integration_heavy = int(app.get("external_interface_count") or 0) >= 10 or int(app.get("api_endpoint_count") or 0) >= 20
    microservice_hint = any(marker in description for marker in ["microservice", "service mesh"])

    status = "LACK_OF_DATA"
    rationale = "Insufficient data was available to assess this scenario."

    if scenario_id == "os_update_security_patch":
        os_status = os_component.get("status")
        if os_status == "CURRENT_VERSION":
            status = "FULFILLED"
            rationale = f"The operating system ({safe_text(app.get('operating_system'))}) is already on a current version per the provided lifecycle rules."
        elif os_status in {"OUTDATED", "EOL"}:
            status = "APPLICABLE"
            rationale = f"The operating system ({safe_text(app.get('operating_system'))}) is assessed as {os_status}, so patching or upgrading is recommended."
        else:
            rationale = f"The operating system ({safe_text(app.get('operating_system'))}) is not covered by the provided lifecycle rules."
    elif scenario_id == "switch_to_standard_linux_os":
        if standard_linux:
            status = "FULFILLED"
            rationale = f"The application already runs on a standard Linux distribution ({safe_text(app.get('operating_system'))})."
        elif linux_nonstandard:
            status = "PARTIALLY_FULFILLED"
            rationale = f"The workload already runs on Linux ({safe_text(app.get('operating_system'))}), but not on the target standard Linux distributions highlighted in the rules."
        elif any(marker in os_text for marker in ["windows", "aix"]):
            if windows_stack:
                status = "BLOCKED"
                rationale = f"The current stack ({safe_text(app.get('operating_system'))}, {safe_text(app.get('programming_language'))}, {safe_text(app.get('application_server'))}) shows platform coupling that blocks a simple move to standard Linux."
            else:
                status = "APPLICABLE"
                rationale = f"The application runs on {safe_text(app.get('operating_system'))}, so moving to standard Linux is a viable modernization path."
        else:
            rationale = f"The current operating system ({safe_text(app.get('operating_system'))}) does not provide enough evidence for a Linux standardization decision."
    elif scenario_id == "switch_to_arm_cpu":
        if legacy_stack:
            status = "BLOCKED"
            rationale = f"The current stack ({safe_text(app.get('operating_system'))}, {safe_text(app.get('programming_language'))}, {safe_text(app.get('application_server'))}) is legacy and would make an ARM migration high risk."
        elif in_cloud and (containerized or modern_portable_stack):
            status = "APPLICABLE"
            rationale = f"The application is already deployed on {safe_text(app.get('deployment_type'))} and uses a portable stack, so ARM-based hosting is a credible optimization option."
        elif containerized:
            status = "PARTIALLY_FULFILLED"
            rationale = "Containerization reduces infrastructure coupling, but the current deployment model does not confirm ARM readiness end-to-end."
        else:
            rationale = "The available data does not confirm whether the current workload and hosting model are suitable for ARM adoption."
    elif scenario_id == "application_server_replacement":
        app_server_status = app_server_component.get("status")
        if not safe_text(app.get("application_server")) or "iis" in app_server_text:
            status = "NOT_APPLICABLE"
            rationale = f"The recorded server technology ({safe_text(app.get('application_server')) or 'none'}) is not a target application server replacement candidate in the provided rules."
        elif app_server_status in {"EOL", "OUTDATED"}:
            status = "APPLICABLE"
            rationale = f"The current application server ({safe_text(app.get('application_server'))}) is assessed as {app_server_status}, which makes replacement relevant."
        elif app_server_status == "CURRENT_VERSION":
            status = "FULFILLED"
            rationale = f"The current application server ({safe_text(app.get('application_server'))}) is already on a current version per the provided rules."
        elif any(marker in app_server_text for marker in ["websphere", "weblogic", "glassfish", "payara", "tomcat"]):
            status = "APPLICABLE"
            rationale = f"The application uses {safe_text(app.get('application_server'))}, which is a legacy-style middleware component worth evaluating for replacement."
        else:
            rationale = f"The current application server ({safe_text(app.get('application_server'))}) is not covered clearly enough for a definitive recommendation."
    elif scenario_id == "app_deployment_to_cloud":
        if in_cloud:
            status = "FULFILLED"
            rationale = f"The application is already deployed in {safe_text(app.get('deployment_type'))}."
        elif on_prem and containerized:
            status = "PARTIALLY_FULFILLED"
            rationale = "The application is still on-premise, but containerization improves portability for a future cloud move."
        elif on_prem or safe_text(app.get("deployment_type")):
            status = "APPLICABLE"
            rationale = f"The application is currently deployed as {safe_text(app.get('deployment_type'))}, so lift-and-shift to cloud remains a valid option."
    elif scenario_id == "app_containerization":
        if containerized:
            status = "FULFILLED"
            rationale = "The application is already marked as containerized."
        elif legacy_stack:
            status = "BLOCKED"
            rationale = f"The legacy stack ({safe_text(app.get('operating_system'))}, {safe_text(app.get('programming_language'))}) makes near-term containerization difficult."
        elif in_cloud:
            status = "PARTIALLY_FULFILLED"
            rationale = "The application is already cloud-hosted, but the source data does not show containerization yet."
        else:
            status = "APPLICABLE"
            rationale = "The application is not containerized today, so containerization remains a relevant modernization option."
    elif scenario_id == "app_refactor_decoupling":
        if third_party:
            status = "NOT_APPLICABLE"
            rationale = f"The solution type ({safe_text(app.get('solution_type'))}) suggests packaged software, which limits custom refactoring opportunities."
        elif microservice_hint:
            status = "FULFILLED"
            rationale = "The available description already points to microservice-oriented architecture or service mesh characteristics."
        elif custom_code_indicated(app) and (integration_heavy or complexity.get("complexity_score", 0) >= 7):
            status = "APPLICABLE"
            rationale = "The application is custom-built and integration-heavy, so decoupling and refactoring would likely improve modernization outcomes."
        elif custom_code_indicated(app):
            status = "PARTIALLY_FULFILLED"
            rationale = "The application is custom-built, but the current data shows only moderate integration pressure for deeper refactoring."
        else:
            status = "NOT_APPLICABLE"
            rationale = "The available application data does not show a strong need for structural refactoring."
    elif scenario_id == "upgrade_legacy_databases":
        db_status = db_component.get("status")
        if db_status == "CURRENT_VERSION":
            status = "FULFILLED"
            rationale = f"The database ({safe_text(app.get('database_engine'))}) is already current according to the provided lifecycle rules."
        elif db_status in {"OUTDATED", "EOL"}:
            status = "APPLICABLE"
            rationale = f"The database ({safe_text(app.get('database_engine'))}) is assessed as {db_status}, so an upgrade is justified."
        else:
            rationale = f"The database version for {safe_text(app.get('database_engine'))} is not covered by the supplied lifecycle rules."
    elif scenario_id == "switch_db_engine_open_source":
        if open_source_db:
            status = "FULFILLED"
            rationale = f"The application already uses an open-source or open-source-based database engine ({safe_text(app.get('database_engine'))})."
        elif proprietary_db and third_party:
            status = "BLOCKED"
            rationale = f"The database ({safe_text(app.get('database_engine'))}) is proprietary and the application is packaged software, so switching engines may not be vendor-supported."
        elif proprietary_db:
            status = "APPLICABLE"
            rationale = f"The application uses a proprietary database ({safe_text(app.get('database_engine'))}), so an open-source alternative could reduce cost and lock-in."
        else:
            rationale = f"The current database engine ({safe_text(app.get('database_engine'))}) does not provide enough information for an open-source migration decision."
    elif scenario_id == "update_outdated_components":
        has_unknown = any(component.get("status") == "NO_KNOWLEDGE" for component in technology.get("components", []))
        if technology.get("eol_count", 0) or technology.get("outdated_count", 0):
            status = "APPLICABLE"
            rationale = f"The technology assessment found {technology.get('eol_count', 0)} EOL and {technology.get('outdated_count', 0)} outdated component(s)."
        elif has_unknown:
            status = "PARTIALLY_FULFILLED"
            rationale = "Known components are current, but some technologies could not be dated from the available application data."
        elif technology.get("current_count", 0):
            status = "FULFILLED"
            rationale = "All assessed components are on current versions according to the provided lifecycle rules."
    return {
        "scenario_id": scenario_id,
        "scenario_name": scenario_name,
        "status": status,
        "rationale": rationale,
    }


def finance_lookup(finance_data: list[dict]) -> dict:
    lookup = {item.get("scenario_id"): item for item in finance_data}
    if "switch_db_engine_postgresql" in lookup and "switch_db_engine_open_source" not in lookup:
        lookup["switch_db_engine_open_source"] = lookup["switch_db_engine_postgresql"]
    return lookup


def scenario_recommendation(scenario_name: str, scenario_id: str) -> str:
    mapping = {
        "os_update_security_patch": "Prioritize OS remediation to restore vendor support and security patch eligibility.",
        "switch_to_standard_linux_os": "Standardize the platform on supported Linux distributions where stack constraints allow.",
        "switch_to_arm_cpu": "Pilot ARM on portable workloads to validate performance and cost savings before broad adoption.",
        "application_server_replacement": "Replace legacy middleware with a supported application platform or simplify the hosting stack.",
        "app_deployment_to_cloud": "Evaluate lift-and-shift migration to reduce infrastructure management effort.",
        "app_containerization": "Containerize the workload to improve portability, release consistency, and scaling options.",
        "app_refactor_decoupling": "Refactor tightly coupled functionality to reduce change risk and improve modernization flexibility.",
        "upgrade_legacy_databases": "Upgrade the database platform to remove lifecycle risk and improve supportability.",
        "switch_db_engine_open_source": "Assess a move to an open-source database to reduce licensing costs and lock-in.",
        "update_outdated_components": "Bundle outdated component upgrades into a coordinated remediation plan.",
    }
    return mapping.get(scenario_id, f"Evaluate {scenario_name} based on the current technology and hosting profile.")


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(safe_text(cell).replace("\n", "<br>") for cell in row) + " |")
    return "\n".join(lines)


def build_app_markdown(app: dict, technology: dict, complexity: dict, scenario_assessment: dict, business_case_entry: dict) -> str:
    overview_rows = [
        ["App ID", safe_text(app.get("app_id"))],
        ["Name", safe_text(app.get("app_name"))],
        ["Status", safe_text(app.get("application_status"))],
        ["Solution Type", safe_text(app.get("solution_type"))],
        ["Deployment Type", safe_text(app.get("deployment_type"))],
        ["Business Criticality", safe_text(app.get("business_criticality"))],
        ["Operating System", safe_text(app.get("operating_system"))],
        ["Programming Language", safe_text(app.get("programming_language"))],
        ["Application Server", safe_text(app.get("application_server"))],
        ["Database Engine", safe_text(app.get("database_engine"))],
    ]
    technology_rows = [
        [component["component_type"], component["name"], component["version"], component["status"], component["notes"]]
        for component in technology.get("components", [])
    ]
    complexity_rows = [[key.replace("_", " ").title(), value] for key, value in complexity.get("factors", {}).items()]
    applicable = [scenario for scenario in scenario_assessment.get("scenarios", []) if scenario["status"] in APPLICABLE_STATUSES]
    scenario_rows = [
        [
            item["scenario_name"],
            item["status"],
            item["rationale"],
            scenario_recommendation(item["scenario_name"], item["scenario_id"]),
        ]
        for item in applicable
    ]
    business_rows = [
        [
            entry["scenario_name"],
            format_currency(entry.get("adjusted_cost")),
            format_currency(entry.get("annual_savings")),
            format_roi(entry.get("roi_3year")),
        ]
        for entry in business_case_entry.get("scenarios", [])
    ]
    if not scenario_rows:
        scenario_rows = [["No applicable scenarios identified", "n/a", "No modernization scenario met the APPLICABLE or PARTIALLY_FULFILLED threshold.", "Continue to monitor technology lifecycle data."]]
    if not business_rows:
        business_rows = [["No quantified scenario", "EUR 0.00", "EUR 0.00", "n/a"]]
    parts = [
        f"# Application Report - {safe_text(app.get('app_name'))}",
        f"Application {safe_text(app.get('app_id'))} assessment generated from the extracted portfolio dataset.",
        "",
        "## App Overview",
        markdown_table(["Field", "Value"], overview_rows),
        "",
        "## Technology Assessment",
        markdown_table(["Component Type", "Name", "Version", "Status", "Notes"], technology_rows),
        "",
        f"Overall technology risk: **{technology.get('overall_technology_risk')}**.",
        "",
        "## Complexity Assessment",
        f"Complexity score: **{complexity.get('complexity_score')}** ({complexity.get('complexity_label')}) — estimated effort **{complexity.get('estimated_effort')}**.",
        "",
        markdown_table(["Factor", "Value"], complexity_rows),
        "",
        complexity.get("reasoning", ""),
        "",
        "## Scenario Analysis",
        markdown_table(["Scenario", "Status", "Rationale", "Recommendation"], scenario_rows),
        "",
        "## Business Case",
        markdown_table(["Scenario", "Adjusted Cost", "Annual Savings", "3-Year ROI"], business_rows),
        "",
        f"Total investment: **{format_currency(business_case_entry.get('total_investment'))}**  ",
        f"Total annual savings: **{format_currency(business_case_entry.get('total_annual_savings'))}**",
    ]
    return "\n".join(parts).strip() + "\n"


def mermaid_pie(label_counts: Counter) -> str:
    lines = ["```mermaid", "pie showData"]
    for label in ["Low", "Medium", "High", "Very High"]:
        lines.append(f'    "{label}" : {int(label_counts.get(label, 0))}')
    lines.append("```")
    return "\n".join(lines)


def mermaid_bar(scenario_counts: Counter) -> str:
    ordered = sorted(scenario_counts.items(), key=lambda item: (-item[1], item[0]))
    labels = [name for name, _ in ordered] or ["No scenarios"]
    values = [count for _, count in ordered] or [0]
    ymax = max(values + [1])
    return "\n".join([
        "```mermaid",
        "xychart-beta",
        '    title "Applicable modernization scenarios"',
        f"    x-axis [{', '.join(json.dumps(label) for label in labels)}]",
        f'    y-axis "Apps" 0 --> {ymax}',
        f"    bar [{', '.join(str(value) for value in values)}]",
        "```",
    ])


def build_portfolio_markdown(apps: list[dict], in_scope_apps: list[dict], tech_results: dict, complexity_results: dict, scenario_results: dict, business_case: dict) -> str:
    label_counts = Counter(complexity_results[app_id]["complexity_label"] for app_id in complexity_results)
    scenario_counts = Counter()
    summary_rows = []
    recommendations = []
    for entry in business_case.get("applications", []):
        app_id = entry["app_id"]
        app_name = entry["app_name"]
        tech = tech_results[app_id]
        complexity = complexity_results[app_id]
        applicable_count = len(entry.get("scenarios", []))
        summary_rows.append([
            app_id,
            app_name,
            tech.get("overall_technology_risk"),
            complexity.get("complexity_label"),
            str(applicable_count),
            format_currency(entry.get("total_investment")),
            format_currency(entry.get("total_annual_savings")),
        ])
        for scenario in entry.get("scenarios", []):
            scenario_counts[scenario["scenario_name"]] += 1
            risk_weight = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}.get(tech.get("overall_technology_risk"), 0)
            recommendations.append((risk_weight, scenario.get("roi_3year") or -9999, scenario.get("annual_savings") or 0, app_name, scenario))
    recommendations.sort(reverse=True)
    top_recommendations = recommendations[:5]
    lines = [
        "# Portfolio Modernization Report",
        f"The portfolio contains {len(apps)} applications, of which {len(in_scope_apps)} are in scope for modernization analysis.",
        "",
        "## Executive Summary",
        f"- Total applications: **{business_case['portfolio_summary']['total_apps']}**",
        f"- In-scope applications: **{business_case['portfolio_summary']['in_scope_apps']}**",
        f"- Total investment: **{format_currency(business_case['portfolio_summary']['total_investment'])}**",
        f"- Total annual savings: **{format_currency(business_case['portfolio_summary']['total_annual_savings'])}**",
        f"- Portfolio 3-year ROI: **{format_roi(business_case['portfolio_summary']['portfolio_roi_3year'])}**",
        "",
        "## Complexity Distribution",
        mermaid_pie(label_counts),
        "",
        "## Scenario Overview",
        mermaid_bar(scenario_counts),
        "",
        "## Per-App Summary",
        markdown_table(["App ID", "Application", "Technology Risk", "Complexity", "Applicable Scenarios", "Investment", "Annual Savings"], summary_rows),
        "",
        "## Top 5 Recommendations",
    ]
    if top_recommendations:
        for _, roi, savings, app_name, scenario in top_recommendations:
            lines.append(
                f"- Prioritize **{app_name}** for **{scenario['scenario_name']}**; projected annual savings {format_currency(savings)} and 3-year ROI {format_roi(roi)}."
            )
    else:
        lines.append("- No quantified modernization recommendations were generated from the current dataset.")
    return "\n".join(lines).strip() + "\n"


def build_schema_export(apps: list[dict]) -> dict:
    field_types: dict[str, set[str]] = {}
    field_counts: Counter = Counter()
    for app in apps:
        for key, value in app.items():
            field_counts[key] += 1
            field_types.setdefault(key, set()).add(type(value).__name__)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "application_count": len(apps),
        "fields": [
            {
                "name": key,
                "observed_types": sorted(field_types[key]),
                "present_in_applications": field_counts[key],
            }
            for key in sorted(field_counts)
        ],
    }


def main() -> None:
    ensure_directories()
    apps = []
    for path in sorted(INTERNAL_APP_DIR.glob("*.json")):
        if path.name.startswith("_"):
            continue
        apps.append(read_json(path))
    scenarios = read_json(SCENARIOS_PATH)
    finance = finance_lookup(read_json(FINANCE_PATH))

    for app in apps:
        app_id = safe_text(app.get("app_id"))
        write_json(CONSOLIDATED_DIR / f"consolidated_schema_application_{app_id}.json", app)

    write_json(OUTPUT_ROOT / "applications" / "consolidated_applications_overview.json", [
        {"id": safe_text(app.get("app_id")), "name": safe_text(app.get("app_name")), "status": safe_text(app.get("application_status"))}
        for app in apps
    ])
    write_json(SCHEMAS_DIR / "schema_export.json", build_schema_export(apps))

    out_of_scope_by_id = {}
    for app in apps:
        result = determine_out_of_scope(app)
        out_of_scope_by_id[result["app_id"]] = result
        write_json(OUT_OF_SCOPE_DIR / f"out_of_scope_{result['app_id']}.json", result)

    tech_results = {}
    complexity_results = {}
    scenario_results = {}
    in_scope_apps = []
    for app in apps:
        app_id = safe_text(app.get("app_id"))
        if out_of_scope_by_id[app_id]["out_of_scope"]:
            continue
        in_scope_apps.append(app)
        technology = technology_assessment(app)
        complexity = complexity_assessment(app, technology)
        scenario_assessment = {
            "app_id": app_id,
            "app_name": safe_text(app.get("app_name")),
            "scenarios": [assess_scenario(app, technology, complexity, scenario) for scenario in scenarios],
        }
        tech_results[app_id] = technology
        complexity_results[app_id] = complexity
        scenario_results[app_id] = scenario_assessment
        write_json(TECH_DIR / f"technology_assessment_{app_id}.json", technology)
        write_json(COMPLEXITY_DIR / f"complexity_{app_id}.json", complexity)
        write_json(SCENARIO_DIR / f"scenario_assessment_{app_id}.json", scenario_assessment)

    business_applications = []
    total_investment = 0.0
    total_annual_savings = 0.0
    for app in in_scope_apps:
        app_id = safe_text(app.get("app_id"))
        complexity_score = complexity_results[app_id]["complexity_score"]
        entries = []
        app_investment = 0.0
        app_annual_savings = 0.0
        for scenario in scenario_results[app_id]["scenarios"]:
            if scenario["status"] not in APPLICABLE_STATUSES:
                continue
            finance_entry = finance.get(scenario["scenario_id"], {})
            base_cost = sum(float(item.get("amount", 0)) for item in finance_entry.get("costs", []))
            annual_savings = sum(float(item.get("amount", 0)) for item in finance_entry.get("savings", []) if item.get("occurrence") == "yearly")
            adjusted_cost = round(base_cost * (complexity_score / 5.0), 2)
            roi_3year = round(((annual_savings * 3 - adjusted_cost) / adjusted_cost) * 100, 2) if adjusted_cost else None
            app_investment += adjusted_cost
            app_annual_savings += annual_savings
            entries.append({
                "scenario_id": scenario["scenario_id"],
                "scenario_name": scenario["scenario_name"],
                "adjusted_cost": adjusted_cost,
                "annual_savings": round(annual_savings, 2),
                "roi_3year": roi_3year,
            })
        app_entry = {
            "app_id": app_id,
            "app_name": safe_text(app.get("app_name")),
            "complexity_score": complexity_score,
            "scenarios": entries,
            "total_investment": round(app_investment, 2),
            "total_annual_savings": round(app_annual_savings, 2),
        }
        total_investment += app_investment
        total_annual_savings += app_annual_savings
        business_applications.append(app_entry)

    portfolio_roi = round(((total_annual_savings * 3 - total_investment) / total_investment) * 100, 2) if total_investment else None
    business_case = {
        "portfolio_summary": {
            "total_apps": len(apps),
            "in_scope_apps": len(in_scope_apps),
            "total_investment": round(total_investment, 2),
            "total_annual_savings": round(total_annual_savings, 2),
            "portfolio_roi_3year": portfolio_roi,
        },
        "applications": business_applications,
    }
    write_json(BUSINESS_CASE_DIR / "business_case.json", business_case)

    business_by_app = {entry["app_id"]: entry for entry in business_applications}
    for app in in_scope_apps:
        app_id = safe_text(app.get("app_id"))
        markdown = build_app_markdown(app, tech_results[app_id], complexity_results[app_id], scenario_results[app_id], business_by_app[app_id])
        (APP_REPORTS_DIR / f"app_report_{app_id}.md").write_text(markdown, encoding="utf-8")

    portfolio_markdown = build_portfolio_markdown(apps, in_scope_apps, tech_results, complexity_results, scenario_results, business_case)
    (REPORTS_DIR / "portfolio_report.md").write_text(portfolio_markdown, encoding="utf-8")

    monitoring = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "applications_processed": len(apps),
        "in_scope_processed": len(in_scope_apps),
        "out_of_scope": sum(1 for item in out_of_scope_by_id.values() if item["out_of_scope"]),
        "reports_generated": len(in_scope_apps) + 1,
        "cwd": os.getcwd(),
        "rounded_up": math.ceil(len(in_scope_apps) / 5) if in_scope_apps else 0,
    }
    write_json(MONITORING_DIR / "analysis_summary.json", monitoring)


if __name__ == "__main__":
    main()
