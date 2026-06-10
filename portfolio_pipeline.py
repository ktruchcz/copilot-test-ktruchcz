#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
OUTPUT_ROOT = ROOT / "output"
INTERNAL_APP_DIR = OUTPUT_ROOT / "applications" / "internal_app_model"
CONSOLIDATED_DIR = OUTPUT_ROOT / "applications" / "consolidated_schema"
SCHEMAS_DIR = OUTPUT_ROOT / "schemas"
OUT_OF_SCOPE_DIR = OUTPUT_ROOT / "out_of_scope_results"
TECH_DIR = OUTPUT_ROOT / "technology_assessment"
COMPLEXITY_DIR = OUTPUT_ROOT / "complexity_results"
SCENARIO_DIR = OUTPUT_ROOT / "scenario_applicability_results"
BUSINESS_DIR = OUTPUT_ROOT / "business_case_results"
REPORTS_DIR = OUTPUT_ROOT / "reports"
APP_MD_DIR = REPORTS_DIR / "apps"
APP_HTML_DIR = REPORTS_DIR / "application_reports"
MONITORING_DIR = OUTPUT_ROOT / "00_monitoring"
SCENARIOS_PATH = ROOT / ".github" / "skills" / "modernization_scenarios_list.json"
FINANCE_PATH = ROOT / ".github" / "skills" / "modernization_scenarios_finance.json"
LOGO_PATH = ROOT / ".github" / "skills" / "logo.svg"
CUSTOMER_NAME = "GenDiscover"
SUBTITLE = "Application modernization with Agentic AI powered by Capgemini GenSuite"
STANDARD_LINUX_FAMILIES = {"rhel", "ubuntu"}
CURRENT_TS = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


TECH_RULES: dict[str, list[dict[str, Any]]] = {
    "os": [
        {"family": "RHEL", "patterns": [r"rhel\s*(7|8|9)"], "versions": {"7": ("EOL", "2024-06-30", "RHEL 7 reached end of maintenance support in June 2024."), "8": ("CURRENT_VERSION", "2029-05-31", "RHEL 8 remains in vendor support until May 2029."), "9": ("CURRENT_VERSION", None, "RHEL 9 is a current supported major release.")}},
        {"family": "Ubuntu", "patterns": [r"ubuntu\s*(14\.04|18\.04|20\.04|22\.04)"], "versions": {"14.04": ("EOL", "2019-04-30", "Ubuntu 14.04 is long past end of standard support."), "18.04": ("EOL", "2023-04-30", "Ubuntu 18.04 reached end of standard support in April 2023."), "20.04": ("OUTDATED", "2025-04-30", "Ubuntu 20.04 is still recognizable LTS but behind newer supported baselines."), "22.04": ("CURRENT_VERSION", "2027-04-30", "Ubuntu 22.04 is within its LTS support window.")}},
        {"family": "Windows Server", "patterns": [r"windows server\s*(2012r2|2012 r2|2012|2016|2019|2022)"], "versions": {"2012r2": ("EOL", "2023-10-10", "Windows Server 2012 R2 reached end of support in October 2023."), "2012 r2": ("EOL", "2023-10-10", "Windows Server 2012 R2 reached end of support in October 2023."), "2012": ("EOL", "2023-10-10", "Windows Server 2012 reached end of support in October 2023."), "2016": ("OUTDATED", None, "Windows Server 2016 is still usable but beyond mainstream support and behind current releases."), "2019": ("CURRENT_VERSION", "2029-01-09", "Windows Server 2019 remains supported in the extended support window until 2029."), "2022": ("CURRENT_VERSION", None, "Windows Server 2022 is a current supported release.")}},
        {"family": "Debian", "patterns": [r"debian\s*(6|7)"], "versions": {"6": ("EOL", "2016-02-29", "Debian 6 is end-of-life."), "7": ("EOL", "2018-05-31", "Debian 7 is end-of-life.")}},
        {"family": "CentOS", "patterns": [r"centos\s*(7)"], "versions": {"7": ("EOL", "2024-06-30", "CentOS 7 reached end of life in June 2024.")}},
    ],
    "database": [
        {"family": "MySQL", "patterns": [r"mysql\s*(5\.7|8(?:\.0)?)"], "versions": {"5.7": ("EOL", "2023-10-31", "MySQL 5.7 reached end of life in October 2023."), "8": ("CURRENT_VERSION", None, "MySQL 8 is the current supported major release."), "8.0": ("CURRENT_VERSION", None, "MySQL 8.0 is the current supported major release.")}},
        {"family": "PostgreSQL", "patterns": [r"postgresql\s*(12|13|14|15|16)"], "versions": {"12": ("EOL", "2024-11-14", "PostgreSQL 12 reached end of life in November 2024."), "13": ("OUTDATED", "2025-11-13", "PostgreSQL 13 is behind the current supported baselines and nearing or beyond its support boundary."), "14": ("CURRENT_VERSION", None, "PostgreSQL 14 remains a current supported release."), "15": ("CURRENT_VERSION", None, "PostgreSQL 15 remains a current supported release."), "16": ("CURRENT_VERSION", None, "PostgreSQL 16 remains a current supported release.")}},
        {"family": "Oracle Database", "patterns": [r"oracle\s*(11g|12c|19c)"], "versions": {"11g": ("EOL", None, "Oracle Database 11g is end-of-life."), "12c": ("EOL", None, "Oracle Database 12c is end-of-life."), "19c": ("CURRENT_VERSION", "2027-04-30", "Oracle Database 19c is the current long-term support release until April 2027.")}},
        {"family": "SQL Server", "patterns": [r"sql server\s*(2014|2016|2019|2022)"], "versions": {"2014": ("EOL", "2024-07-09", "SQL Server 2014 is end-of-life."), "2016": ("OUTDATED", None, "SQL Server 2016 is still usable but well behind current supported releases."), "2019": ("CURRENT_VERSION", None, "SQL Server 2019 remains supported."), "2022": ("CURRENT_VERSION", None, "SQL Server 2022 is a current supported release.")}},
    ],
    "framework": [
        {"family": ".NET", "patterns": [r"\.net(?:\s+core)?\s*(6|8)", r"c#\s+\.net\s*(6|8)"], "versions": {"6": ("EOL", "2024-11-12", ".NET 6 reached end of support in November 2024."), "8": ("CURRENT_VERSION", "2026-11-10", ".NET 8 is the current LTS release until November 2026.")}},
        {"family": "Angular", "patterns": [r"angular\s*(\d+)"], "versions": {"15": ("EOL", None, "Angular 15 is below the currently supported baseline and treated as end-of-life."), "16": ("OUTDATED", None, "Angular 16 is still recognizable but behind current releases."), "17": ("CURRENT_VERSION", None, "Angular 17 and later are treated as current supported baselines."), "18": ("CURRENT_VERSION", None, "Angular 17 and later are treated as current supported baselines."), "19": ("CURRENT_VERSION", None, "Angular 17 and later are treated as current supported baselines.")}},
        {"family": "React", "patterns": [r"react\s*(17|18)"], "versions": {"17": ("OUTDATED", None, "React 17 is behind the current supported baseline."), "18": ("CURRENT_VERSION", None, "React 18 is the current supported baseline.")}},
        {"family": "Node.js", "patterns": [r"node(?:\.js)?\s*(16|18|20|22)"], "versions": {"16": ("EOL", "2023-09-11", "Node.js 16 is end-of-life."), "18": ("OUTDATED", "2025-04-30", "Node.js 18 is still recognizable but behind current long-term support releases."), "20": ("CURRENT_VERSION", "2026-04-30", "Node.js 20 remains in active support."), "22": ("CURRENT_VERSION", None, "Node.js 22 is a current supported release.")}},
        {"family": "Spring Boot", "patterns": [r"spring boot\s*(2|3)"], "versions": {"2": ("EOL", "2023-11-24", "Spring Boot 2.x is end-of-life."), "3": ("CURRENT_VERSION", None, "Spring Boot 3.x is the current supported line.")}},
        {"family": "ASP.NET Core", "patterns": [r"asp\.net core\s*(6|8)"], "versions": {"6": ("EOL", "2024-11-12", "ASP.NET Core 6 follows .NET 6 and is end-of-life."), "8": ("CURRENT_VERSION", "2026-11-10", "ASP.NET Core 8 follows .NET 8 LTS and is current.")}},
    ],
    "application_server": [
        {"family": "Tomcat", "patterns": [r"tomcat[^0-9]*([0-9]+(?:\.[0-9]+)?)"], "versions": {"5": ("EOL", None, "Tomcat 5.x is long end-of-life."), "6": ("EOL", None, "Tomcat 6.x is long end-of-life."), "7": ("EOL", None, "Tomcat 7.x is end-of-life."), "8": ("EOL", None, "Tomcat 8.x is end-of-life."), "9": ("CURRENT_VERSION", None, "Tomcat 9.x remains supported."), "10": ("CURRENT_VERSION", None, "Tomcat 10.x remains supported.")}},
        {"family": "JBoss EAP", "patterns": [r"jboss eap[^0-9]*([67])"], "versions": {"6": ("EOL", None, "JBoss EAP 6.x is end-of-life."), "7": ("OUTDATED", None, "JBoss EAP 7.x is aging and treated as outdated.")}},
        {"family": "WebLogic", "patterns": [r"weblogic[^0-9]*([0-9]+(?:\.[0-9]+)?)", r"weblogic\s*(12c)"], "versions": {"8": ("EOL", None, "WebLogic 8 is long end-of-life."), "9": ("EOL", None, "WebLogic 9 is long end-of-life."), "12c": ("EOL", None, "WebLogic 12c is end-of-life.")}},
        {"family": "WebSphere", "patterns": [r"websphere[^0-9]*([0-9]+(?:\.[0-9]+)?)"], "versions": {"7": ("EOL", None, "WebSphere 7 is end-of-life."), "8": ("EOL", None, "WebSphere 8.x is end-of-life."), "8.5": ("EOL", None, "WebSphere 8.5 is end-of-life."), "9": ("OUTDATED", None, "WebSphere 9 is still maintained in some estates but is behind current cloud-oriented platforms.")}},
        {"family": "WebSphere Liberty", "patterns": [r"liberty"], "versions": {"liberty": ("CURRENT_VERSION", None, "WebSphere Liberty is a current supported platform.")}},
    ],
}


FRAMEWORK_ALIAS_PATTERNS = [
    (r"angular\s*(\d+)", "Angular"),
    (r"react\s*(17|18)", "React"),
    (r"node(?:\.js)?\s*(16|18|20|22)", "Node.js"),
    (r"spring boot\s*(2|3)", "Spring Boot"),
    (r"asp\.net core\s*(6|8)", "ASP.NET Core"),
    (r"c#\s+\.net\s*(6|8)", ".NET"),
    (r"\.net(?:\s+core)?\s*(6|8)", ".NET"),
]


LANGUAGE_VERSION_RULES = {
    "java": {"8": ("EOL", "2022-03-31", "Java 8 premier support ended in March 2022."), "11": ("OUTDATED", "2026-09-30", "Java 11 remains supported but is behind newer LTS releases."), "17": ("CURRENT_VERSION", "2026-09-30", "Java 17 is a current LTS release."), "21": ("CURRENT_VERSION", "2031-09-30", "Java 21 is a current LTS release.")},
    "python": {"2": ("EOL", "2020-01-01", "Python 2 is end-of-life."), "3.7": ("EOL", "2023-06-27", "Python 3.7 is end-of-life."), "3.8": ("EOL", "2024-10-07", "Python 3.8 is end-of-life."), "3.9": ("OUTDATED", "2025-10-31", "Python 3.9 is behind current supported baselines."), "3.10": ("OUTDATED", "2026-10-31", "Python 3.10 is behind the current target baseline."), "3.11": ("CURRENT_VERSION", None, "Python 3.11 is a current supported release."), "3.12": ("CURRENT_VERSION", None, "Python 3.12 is a current supported release.")},
    "go": {"1.19": ("EOL", None, "Go 1.19 is no longer within the two-release support window.")},
    "ruby": {"2.7": ("EOL", None, "Ruby 2.7 is end-of-life.")},
    "php": {"8.1": ("OUTDATED", None, "PHP 8.1 is behind the latest supported baselines and nearing or beyond support boundaries.")},
    "node.js": {"16": ("EOL", "2023-09-11", "Node.js 16 is end-of-life."), "18": ("OUTDATED", "2025-04-30", "Node.js 18 is behind current support baselines."), "20": ("CURRENT_VERSION", "2026-04-30", "Node.js 20 is a current LTS release."), "22": ("CURRENT_VERSION", None, "Node.js 22 is a current supported release.")},
}


PRIORITY_ORDER = {"EOL": 3, "OUTDATED": 2, "CURRENT_VERSION": 1, "NO_KNOWLEDGE": 0}


def safe(value: Any) -> str:
    return "" if value is None else str(value).strip()


def lower(value: Any) -> str:
    return safe(value).lower()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def escape_html(value: Any) -> str:
    return (
        safe(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def json_script(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", lower(value)).strip("-") or "item"


def ensure_dirs() -> None:
    for path in [
        INTERNAL_APP_DIR,
        CONSOLIDATED_DIR,
        SCHEMAS_DIR,
        OUT_OF_SCOPE_DIR,
        TECH_DIR,
        COMPLEXITY_DIR,
        SCENARIO_DIR,
        BUSINESS_DIR,
        APP_MD_DIR,
        APP_HTML_DIR,
        MONITORING_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def analysis_id(*parts: str) -> str:
    digest = hashlib.sha256()
    for part in parts:
        digest.update(part.encode("utf-8"))
    return digest.hexdigest()[:16]


def count_servers(app: dict[str, Any]) -> int:
    instances = app.get("server_instances")
    if isinstance(instances, list):
        count = len([x for x in instances if safe(x)])
        if count:
            return count
    return 1 if safe(instances) else 0


def dependency_count(app: dict[str, Any]) -> int:
    deps = app.get("dependencies")
    if isinstance(deps, list):
        count = len([x for x in deps if safe(x)])
        if count:
            return count
    if safe(deps):
        return len([x for x in re.split(r"[,;]", safe(deps)) if safe(x)])
    return int(app.get("external_interface_count") or 0)


def custom_code(app: dict[str, Any]) -> bool:
    return "custom" in lower(app.get("solution_type"))


def is_containerized(app: dict[str, Any]) -> bool:
    return lower(app.get("is_containerized")) in {"yes", "true", "1", "y"}


def parse_rule(dimension: str, raw_value: str) -> tuple[str, str | None, str, str | None, int, str] | None:
    text = lower(raw_value)
    for rule in TECH_RULES.get(dimension, []):
        for pattern in rule["patterns"]:
            match = re.search(pattern, text)
            if not match:
                continue
            version = match.group(1).lower()
            if dimension in {"application_server", "framework"} and version.isdigit() and version not in rule["versions"]:
                if version in {"5", "6", "7", "8", "9", "10"}:
                    version_key = version
                else:
                    version_key = version.split(".")[0]
            else:
                version_key = version if version in rule["versions"] else version.split(".")[0]
            if version_key not in rule["versions"]:
                continue
            status, eol_date, reason = rule["versions"][version_key]
            normalized_version = match.group(1)
            if rule["family"] == "Angular" and int(normalized_version) >= 17:
                status, eol_date, reason = ("CURRENT_VERSION", None, "Angular 17 and later are treated as current supported baselines.")
            return rule["family"], normalized_version, status, eol_date, 9, reason
    return None


def component(component_name: str, family: str, component_type: str, managed_service: bool, version: str | None, status: str, eol_date: str | None, reason: str, confidence: int) -> dict[str, Any]:
    return {
        "component_name": component_name,
        "component_family": family,
        "component_type": component_type,
        "managed_service": managed_service,
        "version": version,
        "component_status": status,
        "eol_date": eol_date,
        "reason": reason,
        "confidence": confidence,
    }


def unknown_component(component_name: str, family: str, component_type: str, raw_value: str, reason: str, confidence: int = 3) -> dict[str, Any]:
    version_match = re.search(r"(\d+(?:\.\d+)?(?:r2|c|g)?)", lower(raw_value))
    return component(component_name, family, component_type, False, version_match.group(1) if version_match else None, "NO_KNOWLEDGE", None, reason, confidence)


def assess_os(raw_value: str) -> dict[str, Any]:
    if not safe(raw_value):
        return component("Unknown operating system", "Unknown", "os", False, None, "NO_KNOWLEDGE", None, "No operating system value was provided in the application inventory.", 1)
    parsed = parse_rule("os", raw_value)
    if parsed:
        family, version, status, eol_date, confidence, reason = parsed
        return component(family, family, "os", False, version, status, eol_date, reason, confidence)
    raw = safe(raw_value)
    if lower(raw).startswith("aix"):
        return unknown_component("AIX", "AIX", "os", raw, "AIX lifecycle data was not part of the supplied rule set, so support status cannot be assessed confidently from the inventory alone.", 4)
    return unknown_component(raw, raw.split()[0], "os", raw, "Operating system version could not be mapped to a reliable lifecycle rule.")


def assess_database(raw_value: str) -> dict[str, Any]:
    raw = safe(raw_value)
    if not raw:
        return component("Unknown database", "Unknown", "database", False, None, "NO_KNOWLEDGE", None, "No database engine value was provided in the application inventory.", 1)
    managed = any(x in lower(raw) for x in ["amazon rds", "aurora", "managed"])
    parsed = parse_rule("database", raw)
    if parsed:
        family, version, status, eol_date, confidence, reason = parsed
        return component(family, family, "database", managed, version, status, eol_date, reason, confidence)
    if "mongodb" in lower(raw):
        return unknown_component("MongoDB", "MongoDB", "database", raw, "The inventory lists MongoDB but does not provide a version, so lifecycle support cannot be assessed.", 4)
    if "db2" in lower(raw):
        return unknown_component("DB2", "DB2", "database", raw, "The inventory lists DB2 without a version, so lifecycle support cannot be assessed.", 4)
    if managed and ("mysql" in lower(raw) or "postgres" in lower(raw)):
        family = "MySQL" if "mysql" in lower(raw) else "PostgreSQL"
        return unknown_component(family, family, "database", raw, f"The workload uses a managed {family} service, but the service version is not recorded in the inventory.", 5)
    return unknown_component(raw, raw.split()[0], "database", raw, "Database engine could not be mapped to a reliable lifecycle rule.")


def assess_language(raw_value: str) -> dict[str, Any]:
    raw = safe(raw_value)
    if not raw:
        return component("Unknown programming language", "Unknown", "language", False, None, "NO_KNOWLEDGE", None, "No programming language value was provided in the application inventory.", 1)
    text = lower(raw)
    if match := re.search(r"java\s*(8|11|17|21)", text):
        version = match.group(1)
        status, eol_date, reason = LANGUAGE_VERSION_RULES["java"][version]
        return component("Java", "Java", "language", False, version, status, eol_date, reason, 9)
    if match := re.search(r"python\s*(2(?:\.\d+)?|3\.7|3\.8|3\.9|3\.10|3\.11|3\.12)", text):
        version = match.group(1)
        key = "2" if version.startswith("2") else version
        status, eol_date, reason = LANGUAGE_VERSION_RULES["python"][key]
        return component("Python", "Python", "language", False, version, status, eol_date, reason, 9)
    if match := re.search(r"go\s*(1\.19)", text):
        version = match.group(1)
        status, eol_date, reason = LANGUAGE_VERSION_RULES["go"][version]
        return component("Go", "Go", "language", False, version, status, eol_date, reason, 7)
    if match := re.search(r"ruby\s*(2\.7)", text):
        version = match.group(1)
        status, eol_date, reason = LANGUAGE_VERSION_RULES["ruby"][version]
        return component("Ruby", "Ruby", "language", False, version, status, eol_date, reason, 7)
    if match := re.search(r"php\s*(8\.1)", text):
        version = match.group(1)
        status, eol_date, reason = LANGUAGE_VERSION_RULES["php"][version]
        return component("PHP", "PHP", "language", False, version, status, eol_date, reason, 6)
    if match := re.search(r"node(?:\.js)?\s*(16|18|20|22)", text):
        version = match.group(1)
        status, eol_date, reason = LANGUAGE_VERSION_RULES["node.js"][version]
        return component("Node.js", "Node.js", "language", False, version, status, eol_date, reason, 8)
    if any(x in text for x in ["angular", "react native", "asp.net core", ".net core", "c# .net"]):
        return unknown_component(raw, raw.split()[0], "language", raw, "The inventory entry represents a framework or runtime rather than an explicit language version, so language lifecycle support cannot be assessed directly.", 4)
    return unknown_component(raw, raw.split()[0], "language", raw, "Programming language lifecycle support could not be mapped confidently from the recorded value.", 3)


def assess_framework(raw_value: str) -> dict[str, Any]:
    raw = safe(raw_value)
    if not raw:
        return component("Unknown framework/runtime", "Unknown", "framework", False, None, "NO_KNOWLEDGE", None, "No framework or runtime value could be inferred from the inventory record.", 1)
    parsed = parse_rule("framework", raw)
    if parsed:
        family, version, status, eol_date, confidence, reason = parsed
        return component(family, family, "framework", False, version, status, eol_date, reason, confidence)
    if "react native" in lower(raw):
        return unknown_component("React Native", "React Native", "framework", raw, "React Native is listed without a version, so lifecycle support cannot be assessed.", 4)
    if "asp.net core" in lower(raw):
        return unknown_component("ASP.NET Core", "ASP.NET Core", "framework", raw, "ASP.NET Core is listed without a version, so lifecycle support cannot be assessed.", 4)
    if ".net core" in lower(raw):
        return unknown_component(".NET", ".NET", "framework", raw, "The workload uses .NET Core but no version is captured in the inventory.", 4)
    return component("Unknown framework/runtime", "Unknown", "framework", False, None, "NO_KNOWLEDGE", None, "No framework or runtime value could be inferred from the inventory record.", 1)


def assess_application_server(raw_value: str) -> dict[str, Any]:
    raw = safe(raw_value)
    if not raw:
        return component("Unknown application server", "Unknown", "application_server", False, None, "NO_KNOWLEDGE", None, "No application server value was provided in the application inventory.", 1)
    parsed = parse_rule("application_server", raw)
    if parsed:
        family, version, status, eol_date, confidence, reason = parsed
        return component(family, family, "application_server", False, version, status, eol_date, reason, confidence)
    text = lower(raw)
    if "iis" in text:
        return unknown_component("Microsoft IIS", "Microsoft IIS", "application_server", raw, "Microsoft IIS is recorded, but the modernization rule set does not provide lifecycle guidance for IIS versions.", 4)
    if any(x in text for x in ["glassfish", "payara"]):
        family = "GlassFish" if "glassfish" in text else "Payara"
        return unknown_component(family, family, "application_server", raw, f"{family} is recorded, but the inventory does not map it to an agreed lifecycle rule in this assessment baseline.", 4)
    return unknown_component(raw, raw.split()[0], "application_server", raw, "Application server lifecycle support could not be mapped confidently from the recorded value.", 3)


def technology_assessment(app: dict[str, Any]) -> dict[str, Any]:
    components = [
        assess_os(app.get("operating_system")),
        assess_database(app.get("database_engine")),
        assess_language(app.get("programming_language")),
        assess_framework(app.get("programming_language")),
        assess_application_server(app.get("application_server")),
    ]
    return {
        "application_identifier": safe(app.get("app_id")),
        "components_analyzed": components,
        "has_eol_components": any(c["component_status"] == "EOL" for c in components),
        "has_outdated_components": any(c["component_status"] == "OUTDATED" for c in components),
        "has_missing_version_data": any(c["component_status"] == "NO_KNOWLEDGE" or not c.get("version") for c in components),
        "analysis_timestamp": CURRENT_TS,
    }


def out_of_scope_assessment(app: dict[str, Any]) -> dict[str, Any]:
    status = lower(app.get("application_status"))
    name = lower(app.get("app_name"))
    description = lower(app.get("app_description"))
    solution_type = lower(app.get("solution_type"))
    reason = None
    notes = "Application is in-scope for modernization assessment."
    if status == "retired":
        reason = "RETIRED"
        notes = "Application is marked as retired in the source inventory and is out of scope."
    elif any(re.search(r"\bsap\b", value) for value in [name, description, solution_type]):
        reason = "SAP"
        notes = "Application appears to be SAP-related based on the source inventory and is out of scope."
    return {
        "application_id": safe(app.get("app_id")),
        "app_name": safe(app.get("app_name")),
        "out_of_scope": reason is not None,
        "reason": reason,
        "evaluation_notes": notes,
    }


def component_lookup(technology: dict[str, Any], component_type: str) -> dict[str, Any]:
    for item in technology["components_analyzed"]:
        if item["component_type"] == component_type:
            return item
    return {}


def modernization_status_label(app_id: str, out_scope: dict[str, Any], tech: dict[str, Any] | None, scenario_result: dict[str, Any] | None) -> str:
    if out_scope.get("out_of_scope"):
        return "Out of Scope"
    if tech and tech.get("has_eol_components"):
        return "Immediate Modernization"
    if tech and tech.get("has_outdated_components"):
        return "Modernization Planned"
    applicable = 0
    if scenario_result:
        applicable = sum(1 for s in scenario_result["scenario_assessments"] if s["status"] == "APPLICABLE")
    return "Optimization Candidate" if applicable else "Maintain / Monitor"


def complexity_assessment(app: dict[str, Any], technology: dict[str, Any]) -> dict[str, Any]:
    score = 3
    factors: list[str] = ["Base score of 3 applied."]
    criticality = lower(app.get("business_criticality"))
    crit_add = {"critical": 2, "high": 1, "medium": 0, "low": -1}.get(criticality, 0)
    score += crit_add
    factors.append(f"Business criticality '{safe(app.get('business_criticality'))}' adjusted score by {crit_add:+d}.")
    eol_count = sum(1 for c in technology["components_analyzed"] if c["component_status"] == "EOL")
    eol_add = min(eol_count, 3)
    score += eol_add
    factors.append(f"{eol_count} EOL component(s) contributed {eol_add:+d} points (capped at +3).")
    servers = count_servers(app)
    server_add = 2 if servers > 5 else 1 if 2 <= servers <= 5 else 0
    score += server_add
    factors.append(f"Server count of {servers} contributed {server_add:+d} points.")
    deps = dependency_count(app)
    dep_add = 2 if deps > 10 else 1 if 5 <= deps <= 10 else 0
    score += dep_add
    dep_basis = "dependencies field" if app.get("dependencies") else "external_interface_count proxy"
    factors.append(f"Dependency count of {deps} using {dep_basis} contributed {dep_add:+d} points.")
    custom_add = 1 if custom_code(app) else 0
    score += custom_add
    factors.append(f"Solution type '{safe(app.get('solution_type'))}' contributed {custom_add:+d} points for custom code." if custom_add else f"Solution type '{safe(app.get('solution_type'))}' contributed +0 points for custom code.")
    container_add = -1 if is_containerized(app) else 0
    score += container_add
    factors.append(f"Containerized='{safe(app.get('is_containerized'))}' adjusted score by {container_add:+d}.")
    score = max(1, min(10, score))
    if score <= 3:
        label, months, effort_range = "Low", 1, "1-2 months"
    elif score <= 6:
        label, months, effort_range = "Medium", 3, "3-6 months"
    elif score <= 9:
        label, months, effort_range = "High", 6, "6-12 months"
    else:
        label, months, effort_range = "Very high", 12, "12+ months"
    return {
        "application_id": safe(app.get("app_id")),
        "app_name": safe(app.get("app_name")),
        "complexity_score": score,
        "complexity_label": label,
        "scoring_factors": factors,
        "migration_effort_months": months,
        "migration_effort_range": effort_range,
        "analysis_timestamp": CURRENT_TS,
    }


def determine_scenario_status(app: dict[str, Any], technology: dict[str, Any], complexity: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    scenario_id = safe(scenario.get("scenario_id"))
    os_comp = component_lookup(technology, "os")
    db_comp = component_lookup(technology, "database")
    framework_comp = component_lookup(technology, "framework")
    server_comp = component_lookup(technology, "application_server")
    deployment = lower(app.get("deployment_type"))
    os_text = lower(app.get("operating_system"))
    lang_text = lower(app.get("programming_language"))
    server_text = lower(app.get("application_server"))
    db_text = lower(app.get("database_engine"))
    architecture = lower(app.get("application_architecture"))
    is_custom = custom_code(app)
    is_third_party = "3rd" in lower(app.get("solution_type")) or "third" in lower(app.get("solution_type"))
    in_cloud = any(x in deployment for x in ["aws", "azure", "gcp", "public cloud"]) and "on-prem" not in deployment
    hybrid = "aws" in deployment and "on-prem" in deployment
    on_prem_only = "on-prem" in deployment and not any(x in deployment for x in ["aws", "azure", "gcp"])
    standard_linux = any(fam in os_text for fam in STANDARD_LINUX_FAMILIES)
    proprietary_os = any(x in os_text for x in ["aix", "hp-ux", "solaris"])
    legacy_stack = proprietary_os or any(x in lang_text for x in ["cobol", "fortran"]) or architecture == "1-tier"
    middleware_like = any(x in server_text for x in ["weblogic", "websphere", "glassfish", "payara", "tomcat", "jboss"])
    portable_runtime = any(x in lang_text for x in ["java", "python", "go", "node", "php", "scala", "rust"]) or framework_comp.get("component_status") in {"CURRENT_VERSION", "OUTDATED"}
    open_source_db = any(x in db_text for x in ["postgres", "mysql", "mongodb"])
    proprietary_db = any(x in db_text for x in ["oracle", "sql server", "db2"])
    dependency_pressure = dependency_count(app) >= 5

    status = "LACK_OF_DATA"
    rationale = "Not enough source data was available to assess this scenario confidently."

    if scenario_id == "os_update_security_patch":
        if os_comp.get("component_status") == "CURRENT_VERSION":
            status = "FULFILLED"
            rationale = f"The operating system {safe(app.get('operating_system'))} is already on a current supported version."
        elif os_comp.get("component_status") in {"OUTDATED", "EOL"}:
            status = "APPLICABLE"
            rationale = f"The operating system {safe(app.get('operating_system'))} is assessed as {os_comp.get('component_status')}, so remediation is recommended."
        else:
            rationale = f"The operating system {safe(app.get('operating_system'))} could not be mapped to a support status."
    elif scenario_id == "switch_to_standard_linux_os":
        if standard_linux:
            status = "FULFILLED"
            rationale = f"The application already runs on a standard Linux distribution ({safe(app.get('operating_system'))})."
        elif proprietary_os or "debian" in os_text or "centos" in os_text:
            status = "APPLICABLE"
            rationale = f"The current operating system ({safe(app.get('operating_system'))}) is not aligned with the standard Linux target baseline."
        elif "windows" in os_text:
            status = "NOT_APPLICABLE"
            rationale = "The recorded Windows-based stack does not indicate a straightforward move to standard Linux without broader platform redesign."
    elif scenario_id == "switch_to_arm_cpu":
        if legacy_stack or is_third_party:
            status = "BLOCKED"
            rationale = "The current stack is legacy or packaged in a way that blocks a low-risk ARM migration."
        elif in_cloud and (portable_runtime or is_containerized(app)):
            status = "APPLICABLE"
            rationale = "The application already runs in cloud and uses a portable stack, so ARM-based infrastructure is a viable optimization path."
        elif hybrid and portable_runtime:
            status = "PARTIALLY_FULFILLED"
            rationale = "The application has some cloud presence and a portable stack, but the hybrid deployment means ARM adoption would be incremental."
    elif scenario_id == "application_server_replacement":
        if not safe(app.get("application_server")) or "iis" in server_text:
            status = "NOT_APPLICABLE"
            rationale = "The inventory does not show a replaceable standalone application server platform for this scenario."
        elif server_comp.get("component_status") in {"EOL", "OUTDATED"}:
            status = "APPLICABLE"
            rationale = f"The application server {safe(app.get('application_server'))} is assessed as {server_comp.get('component_status')}."
        elif server_comp.get("component_status") == "CURRENT_VERSION":
            status = "FULFILLED"
            rationale = f"The application server {safe(app.get('application_server'))} is already current."
        elif middleware_like:
            status = "APPLICABLE"
            rationale = f"The application uses legacy-style middleware ({safe(app.get('application_server'))}), so replacement remains relevant even though exact support status is unknown."
    elif scenario_id == "app_deployment_to_cloud":
        if in_cloud:
            status = "FULFILLED"
            rationale = f"The application is already hosted in cloud ({safe(app.get('deployment_type'))})."
        elif hybrid:
            status = "PARTIALLY_FULFILLED"
            rationale = "The application is already partly cloud-hosted, but still retains on-premise deployment dependencies."
        elif on_prem_only:
            status = "APPLICABLE"
            rationale = "The application is currently on-premise, so lift-and-shift cloud migration is applicable."
    elif scenario_id == "app_containerization":
        if is_containerized(app):
            status = "FULFILLED"
            rationale = "The application is already marked as containerized in the inventory."
        elif legacy_stack:
            status = "BLOCKED"
            rationale = "The current architecture and legacy stack indicate low near-term container readiness."
        elif in_cloud or hybrid:
            status = "PARTIALLY_FULFILLED"
            rationale = "The application already has cloud deployment characteristics, but the inventory does not show containerization yet."
        else:
            status = "APPLICABLE"
            rationale = "The application is not containerized and no blocking constraint is explicitly recorded in the inventory."
    elif scenario_id == "app_refactor_decoupling":
        if is_third_party:
            status = "NOT_APPLICABLE"
            rationale = "The application is recorded as packaged software, limiting refactoring options."
        elif is_custom and (legacy_stack or dependency_pressure or complexity["complexity_score"] >= 7):
            status = "APPLICABLE"
            rationale = "The application is custom-built and shows legacy or integration complexity that makes decoupling valuable."
        elif is_custom:
            status = "PARTIALLY_FULFILLED"
            rationale = "The application is custom-built, but the current record does not show strong integration pressure demanding deep refactoring."
        else:
            status = "NOT_APPLICABLE"
            rationale = "The source record does not indicate a strong need for codebase refactoring."
    elif scenario_id == "upgrade_legacy_databases":
        if db_comp.get("component_status") == "CURRENT_VERSION":
            status = "FULFILLED"
            rationale = f"The database {safe(app.get('database_engine'))} is already on a current supported baseline."
        elif db_comp.get("component_status") in {"OUTDATED", "EOL"}:
            status = "APPLICABLE"
            rationale = f"The database {safe(app.get('database_engine'))} is assessed as {db_comp.get('component_status')}."
        else:
            rationale = f"The database {safe(app.get('database_engine'))} could not be mapped to a support status."
    elif scenario_id == "switch_db_engine_open_source":
        if open_source_db:
            status = "FULFILLED"
            rationale = f"The application already uses an open-source database family ({safe(app.get('database_engine'))})."
        elif proprietary_db and is_third_party:
            status = "BLOCKED"
            rationale = "The application uses a proprietary database inside packaged software, so a database engine switch is likely vendor-constrained."
        elif proprietary_db:
            status = "APPLICABLE"
            rationale = f"The application uses a proprietary database ({safe(app.get('database_engine'))}), so an open-source alternative is relevant."
    elif scenario_id == "update_outdated_components":
        eol_or_outdated = [c for c in technology["components_analyzed"] if c["component_status"] in {"EOL", "OUTDATED"}]
        unknowns = [c for c in technology["components_analyzed"] if c["component_status"] == "NO_KNOWLEDGE"]
        if eol_or_outdated:
            status = "APPLICABLE"
            rationale = f"The technology assessment found {len(eol_or_outdated)} component(s) that are EOL or outdated."
        elif unknowns:
            status = "PARTIALLY_FULFILLED"
            rationale = "Known components are current, but some technologies could not be dated from the available inventory data."
        else:
            status = "FULFILLED"
            rationale = "All assessed components are on current supported baselines."

    return {
        "scenario_id": scenario_id,
        "scenario_name": safe(scenario.get("scenario_name")),
        "status": status,
        "rationale": rationale,
        "recommendation": safe(scenario.get("modernization_suggestion")),
        "priority": safe(scenario.get("priority")),
    }


def finance_lookup() -> dict[str, dict[str, Any]]:
    items = read_json(FINANCE_PATH)
    lookup = {item["scenario_id"]: item for item in items}
    if "switch_db_engine_open_source" not in lookup and "switch_db_engine_postgresql" in lookup:
        lookup["switch_db_engine_open_source"] = lookup["switch_db_engine_postgresql"]
    return lookup


def format_currency(value: float | int | None) -> str:
    if value is None:
        return "n/a"
    return f"EUR {float(value):,.2f}"


def format_roi(value: float | int | None) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.2f}%"


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(safe(cell).replace("\n", "<br>") for cell in row) + " |")
    return "\n".join(lines)


def tech_summary_rows(tech: dict[str, Any]) -> list[list[str]]:
    return [[c["component_type"], c["component_family"], c.get("version") or "unknown", c["component_status"], c["reason"]] for c in tech["components_analyzed"]]


def build_app_markdown(app: dict[str, Any], tech: dict[str, Any], complexity: dict[str, Any], scenario_result: dict[str, Any], business_entry: dict[str, Any]) -> str:
    applicable = [s for s in scenario_result["scenario_assessments"] if s["status"] == "APPLICABLE"]
    top_business = sorted(business_entry["applicable_scenarios"], key=lambda item: ((item.get("roi_3year") or -99999), item.get("annual_savings", 0)), reverse=True)[:5]
    lines = [
        f"# Application Report - {safe(app.get('app_name'))}",
        "",
        "## App overview",
        markdown_table(["Field", "Value"], [
            ["Application ID", safe(app.get("app_id"))],
            ["Name", safe(app.get("app_name"))],
            ["Description", safe(app.get("app_description"))],
            ["Status", safe(app.get("application_status"))],
            ["Criticality", safe(app.get("business_criticality"))],
            ["Deployment", safe(app.get("deployment_type"))],
            ["Solution type", safe(app.get("solution_type"))],
        ]),
        "",
        "## Technology assessment summary",
        markdown_table(["Dimension", "Family", "Version", "Status", "Reason"], tech_summary_rows(tech)),
        "",
        "## Complexity score and label",
        f"- Complexity score: **{complexity['complexity_score']}**",
        f"- Complexity label: **{complexity['complexity_label']}**",
        f"- Indicative migration effort: **{complexity['migration_effort_range']}**",
        "",
        "Scoring factors:",
    ]
    lines.extend([f"- {factor}" for factor in complexity["scoring_factors"]])
    lines.extend(["", "## Applicable scenarios with recommendations"])
    if applicable:
        lines.append(markdown_table(["Scenario", "Priority", "Rationale", "Recommendation"], [[s["scenario_name"], s["priority"], s["rationale"], s["recommendation"]] for s in applicable]))
    else:
        lines.append("No APPLICABLE modernization scenarios were identified from the available source data.")
    lines.extend(["", "## Business case for top scenarios"])
    if top_business:
        lines.append(markdown_table(["Scenario", "Base Cost", "Adjusted Cost", "Annual Savings", "3-Year ROI"], [[s["scenario_name"], format_currency(s["base_cost"]), format_currency(s["adjusted_cost"]), format_currency(s["annual_savings"]), format_roi(s["roi_3year"])] for s in top_business]))
    else:
        lines.append("No quantified APPLICABLE scenarios were available in the finance model.")
    return "\n".join(lines).strip() + "\n"


def status_badge(text: str) -> str:
    slug = slugify(text).replace("-", "_")
    return f'<span class="badge badge-{escape_html(slug)}">{escape_html(text)}</span>'


def render_table_html(headers: list[str], rows: list[list[str]]) -> str:
    thead = "".join(f"<th>{escape_html(h)}</th>" for h in headers)
    tbody = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    return f"<table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table>"


def page_shell(title: str, body: str, payload: dict[str, Any], logo_svg: str) -> str:
    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>{escape_html(title)}</title>
  <style>
    :root {{
      --primary-dark: #081722;
      --report-background: #102737;
      --section-background: #163244;
      --accent: #1ec8d7;
      --accent-rgb: 30, 200, 215;
      --report-text-font-primary: #e9f7ff;
      --report-text-font-secondary-rgb: 184, 216, 232;
      --text-light-blue-rgb: 154, 198, 220;
      --danger: #ff6b81;
      --warning: #ffb347;
      --success: #58d68d;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Arial, Helvetica, sans-serif; color: var(--report-text-font-primary); background: radial-gradient(circle at top, #143243 0%, var(--primary-dark) 58%); }}
    a {{ color: var(--accent); text-decoration: none; }}
    .page {{ max-width: 1360px; margin: 0 auto; padding: 24px 16px; }}
    .shell {{ background: var(--report-background); border: 1px solid rgba(var(--accent-rgb), .18); border-radius: 18px; overflow: hidden; box-shadow: 0 30px 70px rgba(0,0,0,.35); }}
    .header, .footer {{ display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 20px 24px; }}
    .header {{ border-bottom: 1px solid rgba(255,255,255,.08); }}
    .footer {{ border-top: 1px solid rgba(255,255,255,.08); }}
    .logo svg {{ width: auto; height: 44px; }}
    .logo path {{ fill: white; }}
    [data-testid=\"customer-name\"] {{ font-weight: 700; font-size: 1.1rem; margin-bottom: 4px; }}
    .subtitle {{ color: rgba(var(--report-text-font-secondary-rgb), .95); font-size: .95rem; }}
    .content {{ padding: 24px; }}
    .card, details {{ background: var(--section-background); border: 1px solid rgba(var(--accent-rgb), .16); border-radius: 14px; box-shadow: 0 10px 28px rgba(0,0,0,.18); margin-bottom: 18px; }}
    .title-card {{ padding: 20px; }}
    .title-card h1 {{ margin: 0; font-size: 2.2rem; text-shadow: 0 0 18px rgba(var(--accent-rgb), .36); }}
    .lead {{ margin: 10px 0 0; line-height: 1.6; color: rgba(var(--report-text-font-secondary-rgb), .95); }}
    details summary {{ list-style: none; cursor: pointer; padding: 18px 20px; display: flex; justify-content: space-between; align-items: center; }}
    details summary::-webkit-details-marker {{ display: none; }}
    details h2 {{ margin: 0; font-size: 1.3rem; }}
    .section-body {{ padding: 0 20px 20px; color: rgba(var(--report-text-font-secondary-rgb), .96); line-height: 1.6; }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; margin-bottom: 16px; }}
    .metric {{ background: rgba(255,255,255,.04); border: 1px solid rgba(var(--accent-rgb), .14); border-radius: 12px; padding: 16px; }}
    .metric .value {{ font-size: 2rem; font-weight: 800; color: var(--accent); text-shadow: 0 0 18px rgba(var(--accent-rgb), .55); }}
    .metric .label {{ margin-top: 6px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
    th, td {{ padding: 10px 12px; text-align: left; vertical-align: top; border-bottom: 1px solid rgba(var(--accent-rgb), .12); }}
    th {{ color: var(--report-text-font-primary); }}
    ul {{ margin: 0; padding-left: 20px; }}
    .badge {{ display: inline-block; padding: 4px 8px; border-radius: 999px; font-size: .78rem; font-weight: 700; }}
    .badge-eol, .badge-blocked, .badge-immediate_modernization {{ background: rgba(255,107,129,.18); color: #ffd8e0; }}
    .badge-outdated, .badge-partially_fulfilled, .badge-modernization_planned {{ background: rgba(255,179,71,.18); color: #ffe8b8; }}
    .badge-current_version, .badge-fulfilled, .badge-maintain_monitor {{ background: rgba(88,214,141,.18); color: #dbffe6; }}
    .badge-applicable, .badge-optimization_candidate {{ background: rgba(var(--accent-rgb), .18); color: #dcfcff; }}
    .badge-no_knowledge, .badge-lack_of_data, .badge-not_applicable, .badge-out_of_scope {{ background: rgba(255,255,255,.1); color: #eff9ff; }}
    .link-list {{ display: grid; gap: 10px; }}
    .link-card {{ display: flex; justify-content: space-between; gap: 12px; align-items: center; padding: 12px 14px; border-radius: 10px; background: rgba(255,255,255,.05); border: 1px solid rgba(var(--accent-rgb), .12); }}
    .footer p {{ margin: 2px 0; }}
    .footer .primary {{ color: var(--accent); font-weight: 700; }}
    @media (max-width: 800px) {{ .header, .footer {{ flex-direction: column; align-items: flex-start; }} .content {{ padding: 16px; }} }}
  </style>
</head>
<body>
  <div class=\"page\">
    <div class=\"shell\">
      <div class=\"header\">
        <div>
          <div data-testid=\"customer-name\">{escape_html(CUSTOMER_NAME)}</div>
          <div class=\"subtitle\">{escape_html(SUBTITLE)}</div>
        </div>
        <div class=\"logo\">{logo_svg}</div>
      </div>
      <div class=\"content\">{body}</div>
      <div class=\"footer\">
        <div>
          <p class=\"primary\">Generated by GenDiscover</p>
          <p>{escape_html(payload['generated_timestamp'])}</p>
          <p>Analysis ID: {escape_html(payload['analysis_id'])}</p>
        </div>
        <div class=\"logo\">{logo_svg}</div>
      </div>
    </div>
  </div>
  <script type=\"application/json\" id=\"report-data\">{json_script(payload)}</script>
</body>
</html>
"""


def detail_section(test_id: str, title: str, body: str) -> str:
    return f'<details open data-testid="{escape_html(test_id)}"><summary><h2>{escape_html(title)}</h2><span>▾</span></summary><div class="section-body">{body}</div></details>'


def build_app_html(app: dict[str, Any], tech: dict[str, Any], complexity: dict[str, Any], scenario_result: dict[str, Any], business_entry: dict[str, Any], logo_svg: str) -> str:
    title = f"Application Report - {safe(app.get('app_name'))}"
    tech_rows = [[escape_html(c['component_type']), escape_html(c['component_family']), escape_html(c.get('version') or 'unknown'), status_badge(c['component_status']), escape_html(c['reason'])] for c in tech['components_analyzed']]
    complexity_html = "<div class='metrics'>" + "".join([
        f"<div class='metric'><div class='value'>{complexity['complexity_score']}</div><div class='label'>Complexity score</div></div>",
        f"<div class='metric'><div class='value'>{escape_html(complexity['complexity_label'])}</div><div class='label'>Complexity label</div></div>",
        f"<div class='metric'><div class='value'>{escape_html(complexity['migration_effort_range'])}</div><div class='label'>Indicative effort</div></div>",
    ]) + "</div><ul>" + "".join(f"<li>{escape_html(item)}</li>" for item in complexity['scoring_factors']) + "</ul>"
    scenario_rows = [[escape_html(s['scenario_name']), status_badge(s['status']), escape_html(s['rationale']), escape_html(s['recommendation'])] for s in scenario_result['scenario_assessments']]
    business_rows = [[escape_html(s['scenario_name']), escape_html(format_currency(s['base_cost'])), escape_html(format_currency(s['adjusted_cost'])), escape_html(format_currency(s['annual_savings'])), escape_html(format_roi(s['roi_3year']))] for s in business_entry['applicable_scenarios']] or [["No quantified scenario", "EUR 0.00", "EUR 0.00", "EUR 0.00", "n/a"]]
    payload = {
        "app_id": safe(app.get("app_id")),
        "report_title": title,
        "lead_text": safe(app.get("app_description")),
        "sections": [
            {"id": "technology-assessment", "title": "Technology Assessment"},
            {"id": "complexity-assessment", "title": "Complexity Assessment"},
            {"id": "scenario-analysis", "title": "Scenario Analysis"},
            {"id": "business-case", "title": "Business Case"},
        ],
        "generated_timestamp": CURRENT_TS,
        "analysis_id": analysis_id(safe(app.get("app_id")), safe(app.get("app_name"))),
        "application": app,
        "technology": tech,
        "complexity": complexity,
        "scenarios": scenario_result,
        "business_case": business_entry,
    }
    body = "".join([
        f'<section class="card title-card" data-testid="app-report-title"><h1>{escape_html(title)}</h1><p class="lead">{escape_html(safe(app.get("app_description")) or "Modernization assessment generated from the source application inventory.")}</p></section>',
        detail_section("technology-assessment", "Technology Assessment", render_table_html(["Dimension", "Family", "Version", "Status", "Reason"], tech_rows)),
        detail_section("complexity-assessment", "Complexity Assessment", complexity_html),
        detail_section("scenario-analysis", "Scenario Analysis", render_table_html(["Scenario", "Status", "Rationale", "Recommendation"], scenario_rows)),
        detail_section("business-case", "Business Case", "<div class='metrics'>" + f"<div class='metric'><div class='value'>{escape_html(format_currency(business_entry['total_investment']))}</div><div class='label'>Total investment</div></div>" + f"<div class='metric'><div class='value'>{escape_html(format_currency(business_entry['total_annual_savings']))}</div><div class='label'>Annual savings</div></div>" + "</div>" + render_table_html(["Scenario", "Base Cost", "Adjusted Cost", "Annual Savings", "3-Year ROI"], business_rows)),
    ])
    return page_shell(f"{title} - GenDiscover", body, payload, logo_svg)


def build_portfolio_markdown(apps: list[dict[str, Any]], out_scope: dict[str, Any], tech_by_id: dict[str, Any], complexity_by_id: dict[str, Any], scenario_by_id: dict[str, Any], business_case: dict[str, Any]) -> str:
    status_counts = Counter()
    scenario_counts = Counter()
    summary_rows = []
    all_recommendations = []
    for app in apps:
        app_id = safe(app.get("app_id"))
        status_label = modernization_status_label(app_id, out_scope[app_id], tech_by_id.get(app_id), scenario_by_id.get(app_id))
        status_counts[status_label] += 1
    for app_entry in business_case["applications"]:
        app_id = app_entry["application_id"]
        tech = tech_by_id[app_id]
        complexity = complexity_by_id[app_id]
        app_status = modernization_status_label(app_id, out_scope[app_id], tech, scenario_by_id[app_id])
        scenario_count = sum(1 for s in scenario_by_id[app_id]["scenario_assessments"] if s["status"] == "APPLICABLE")
        summary_rows.append([
            app_id,
            app_entry["app_name"],
            app_status,
            str(complexity["complexity_score"]),
            complexity["complexity_label"],
            str(scenario_count),
            format_currency(app_entry["total_investment"]),
            format_currency(app_entry["total_annual_savings"]),
        ])
        for scenario in scenario_by_id[app_id]["scenario_assessments"]:
            if scenario["status"] == "APPLICABLE":
                scenario_counts[scenario["scenario_name"]] += 1
        for item in app_entry["applicable_scenarios"]:
            all_recommendations.append((item.get("roi_3year") if item.get("roi_3year") is not None else -99999, item.get("annual_savings", 0), app_entry["app_name"], item["scenario_name"]))
    all_recommendations.sort(reverse=True)
    pie_lines = ["```mermaid", "pie showData"]
    for label in ["Out of Scope", "Immediate Modernization", "Modernization Planned", "Optimization Candidate", "Maintain / Monitor"]:
        pie_lines.append(f'    "{label}" : {status_counts.get(label, 0)}')
    pie_lines.append("```")
    ordered_scenarios = sorted(scenario_counts.items(), key=lambda item: (-item[1], item[0]))
    bar_lines = ["```mermaid", 'xychart-beta', '    title "Scenario applicability counts"', f"    x-axis [{', '.join(json.dumps(name) for name, _ in ordered_scenarios)}]", f'    y-axis "Apps" 0 --> {max([count for _, count in ordered_scenarios] + [1])}', f"    bar [{', '.join(str(count) for _, count in ordered_scenarios)}]", "```"]
    lines = [
        "# Portfolio Modernization Report",
        "",
        "## Executive summary",
        f"- Total applications: **{business_case['portfolio_summary']['total_applications']}**",
        f"- In-scope applications: **{business_case['portfolio_summary']['in_scope_applications']}**",
        f"- Total investment: **{format_currency(business_case['portfolio_summary']['total_investment'])}**",
        f"- Total annual savings: **{format_currency(business_case['portfolio_summary']['total_annual_savings'])}**",
        f"- Portfolio 3-year ROI: **{format_roi(business_case['portfolio_summary']['portfolio_roi_3year'])}**",
        "",
        "## Application distribution by modernization status",
        "\n".join(pie_lines),
        "",
        "## Scenario applicability counts",
        "\n".join(bar_lines),
        "",
        "## Per-application summary table",
        markdown_table(["App ID", "Application", "Modernization Status", "Complexity Score", "Complexity Label", "Applicable Scenarios", "Investment", "Annual Savings"], summary_rows),
        "",
        "## Top 5 recommendations",
    ]
    if all_recommendations:
        for roi, savings, app_name, scenario_name in all_recommendations[:5]:
            lines.append(f"- Prioritize **{app_name}** for **{scenario_name}**; annual savings {format_currency(savings)} and 3-year ROI {format_roi(roi)}.")
    else:
        lines.append("- No quantified APPLICABLE scenarios were identified in the finance model.")
    return "\n".join(lines).strip() + "\n"


def build_portfolio_html(apps: list[dict[str, Any]], out_scope: dict[str, Any], scenario_by_id: dict[str, Any], business_case: dict[str, Any], logo_svg: str) -> str:
    status_counts = Counter()
    scenario_counts = Counter()
    phase1, phase2, phase3 = [], [], []
    link_cards = []
    for app in apps:
        app_id = safe(app.get("app_id"))
        if out_scope[app_id]["out_of_scope"]:
            status_counts["Out of Scope"] += 1
            continue
        scenario_result = scenario_by_id[app_id]
        app_entry = next(item for item in business_case["applications"] if item["application_id"] == app_id)
        mod_status = app_entry["modernization_status"]
        status_counts[mod_status] += 1
        for s in scenario_result["scenario_assessments"]:
            if s["status"] == "APPLICABLE":
                scenario_counts[s["scenario_name"]] += 1
        link_cards.append(f'<a class="link-card" href="application_reports/application_report_{escape_html(app_id)}.html"><span>{escape_html(app.get("app_name"))} ({escape_html(app_id)})</span><span>Open report ↗</span></a>')
        line = f"{safe(app.get('app_name'))} ({app_entry['modernization_status']}, complexity {app_entry['complexity_score']})"
        if app_entry["modernization_status"] == "Immediate Modernization":
            phase1.append(line)
        elif app_entry["modernization_status"] == "Modernization Planned":
            phase2.append(line)
        else:
            phase3.append(line)
    summary_html = "<div class='metrics'>" + "".join([
        f"<div class='metric'><div class='value'>{business_case['portfolio_summary']['total_applications']}</div><div class='label'>Total apps</div></div>",
        f"<div class='metric'><div class='value'>{business_case['portfolio_summary']['in_scope_applications']}</div><div class='label'>In scope</div></div>",
        f"<div class='metric'><div class='value'>{sum(1 for item in out_scope.values() if item['out_of_scope'])}</div><div class='label'>Out of scope</div></div>",
        f"<div class='metric'><div class='value'>{escape_html(format_currency(business_case['portfolio_summary']['total_investment']))}</div><div class='label'>Total investment</div></div>",
        f"<div class='metric'><div class='value'>{escape_html(format_currency(business_case['portfolio_summary']['total_annual_savings']))}</div><div class='label'>Annual savings</div></div>",
        f"<div class='metric'><div class='value'>{escape_html(format_roi(business_case['portfolio_summary']['portfolio_roi_3year']))}</div><div class='label'>3-year ROI</div></div>",
    ]) + "</div>"
    opp_rows = [[escape_html(name), escape_html(str(count))] for name, count in sorted(scenario_counts.items(), key=lambda item: (-item[1], item[0]))]
    roadmap_html = "<div class='metrics'>" + "".join([
        f"<div class='metric'><div class='value'>Phase 1</div><div class='label'>Immediate modernization</div><ul>{''.join(f'<li>{escape_html(x)}</li>' for x in phase1) or '<li>No apps</li>'}</ul></div>",
        f"<div class='metric'><div class='value'>Phase 2</div><div class='label'>Planned remediation</div><ul>{''.join(f'<li>{escape_html(x)}</li>' for x in phase2) or '<li>No apps</li>'}</ul></div>",
        f"<div class='metric'><div class='value'>Phase 3</div><div class='label'>Optimization and maintain</div><ul>{''.join(f'<li>{escape_html(x)}</li>' for x in phase3) or '<li>No apps</li>'}</ul></div>",
    ]) + "</div>"
    scenario_overview = render_table_html(["Scenario", "Applicable apps"], opp_rows or [["No applicable scenarios", "0"]]) + f"<div class='link-list' style='margin-top:16px'>{''.join(link_cards)}</div>"
    payload = {
        "report_title": "Portfolio Modernization Report",
        "lead_text": "Portfolio-wide summary of technology risk, complexity, scenario applicability, and business case.",
        "section_list": [
            {"id": "section-summary", "title": "Summary"},
            {"id": "section-modernization-opportunities", "title": "Modernization Opportunities"},
            {"id": "section-roadmap-proposal", "title": "Roadmap Proposal"},
            {"id": "section-scenario-overview", "title": "Scenario Overview"},
        ],
        "app_link_list": [{"app_id": item["application_id"], "href": f"application_reports/application_report_{item['application_id']}.html"} for item in business_case["applications"]],
        "generated_timestamp": CURRENT_TS,
        "analysis_id": analysis_id("portfolio", str(business_case['portfolio_summary']['total_applications'])),
        "portfolio": business_case,
    }
    body = "".join([
        '<section class="card title-card" data-testid="app-report-title"><h1>Portfolio Modernization Report</h1><p class="lead">Portfolio-wide summary of technology risk, complexity, modernization scenarios, and business case.</p></section>',
        detail_section("section-summary", "Summary", summary_html),
        detail_section("section-modernization-opportunities", "Modernization Opportunities", render_table_html(["Scenario", "Applicable apps"], opp_rows or [["No applicable scenarios", "0"]])),
        detail_section("section-roadmap-proposal", "Roadmap Proposal", roadmap_html),
        detail_section("section-scenario-overview", "Scenario Overview", scenario_overview),
    ])
    return page_shell("Portfolio Modernization Report - GenDiscover", body, payload, logo_svg)


def build_schema_export(apps: list[dict[str, Any]]) -> dict[str, Any]:
    field_types: dict[str, set[str]] = {}
    field_counts: Counter[str] = Counter()
    for app in apps:
        for key, value in app.items():
            field_counts[key] += 1
            field_types.setdefault(key, set()).add(type(value).__name__)
    return {
        "generated_timestamp": CURRENT_TS,
        "application_count": len(apps),
        "fields": [
            {"field_name": name, "observed_types": sorted(field_types[name]), "present_in_applications": field_counts[name]}
            for name in sorted(field_counts)
        ],
    }


def main() -> None:
    ensure_dirs()
    apps = [read_json(path) for path in sorted(INTERNAL_APP_DIR.glob("app*.json"))]
    scenarios = read_json(SCENARIOS_PATH)
    finance = finance_lookup()
    logo_svg = LOGO_PATH.read_text(encoding="utf-8").strip()

    for app in apps:
        app_id = safe(app.get("app_id"))
        shutil.copyfile(INTERNAL_APP_DIR / f"{app_id}.json", CONSOLIDATED_DIR / f"consolidated_schema_application_{app_id}.json")

    write_json(OUTPUT_ROOT / "applications" / "consolidated_applications_overview.json", [{"id": safe(app.get("app_id")), "name": safe(app.get("app_name")), "status": safe(app.get("application_status"))} for app in apps])
    write_json(SCHEMAS_DIR / "schema_export.json", build_schema_export(apps))

    out_scope: dict[str, Any] = {}
    in_scope_apps: list[dict[str, Any]] = []
    for app in apps:
        result = out_of_scope_assessment(app)
        out_scope[result["application_id"]] = result
        write_json(OUT_OF_SCOPE_DIR / f"out_of_scope_{result['application_id']}.json", result)
        if not result["out_of_scope"]:
            in_scope_apps.append(app)

    tech_by_id: dict[str, Any] = {}
    complexity_by_id: dict[str, Any] = {}
    scenario_by_id: dict[str, Any] = {}
    for app in in_scope_apps:
        app_id = safe(app.get("app_id"))
        tech = technology_assessment(app)
        complexity = complexity_assessment(app, tech)
        scenario_result = {
            "application_id": app_id,
            "app_name": safe(app.get("app_name")),
            "scenario_assessments": [determine_scenario_status(app, tech, complexity, scenario) for scenario in scenarios],
            "analysis_timestamp": CURRENT_TS,
        }
        tech_by_id[app_id] = tech
        complexity_by_id[app_id] = complexity
        scenario_by_id[app_id] = scenario_result
        write_json(TECH_DIR / f"technology_assessment_{app_id}.json", tech)
        write_json(COMPLEXITY_DIR / f"complexity_{app_id}.json", complexity)
        write_json(SCENARIO_DIR / f"scenario_assessment_{app_id}.json", scenario_result)

    business_apps = []
    scenario_portfolio_totals: Counter[str] = Counter()
    total_investment = 0.0
    total_annual_savings = 0.0
    for app in in_scope_apps:
        app_id = safe(app.get("app_id"))
        complexity_score = complexity_by_id[app_id]["complexity_score"]
        app_scenarios = []
        app_investment = 0.0
        app_savings = 0.0
        for scenario in scenario_by_id[app_id]["scenario_assessments"]:
            if scenario["status"] != "APPLICABLE":
                continue
            finance_entry = finance.get(scenario["scenario_id"], {})
            base_cost = round(sum(float(item.get("amount", 0)) for item in finance_entry.get("costs", [])), 2)
            adjusted_cost = round(base_cost * (complexity_score / 5.0), 2)
            annual_savings = round(sum(float(item.get("amount", 0)) for item in finance_entry.get("savings", [])), 2)
            roi = round(((annual_savings * 3 - adjusted_cost) / adjusted_cost) * 100, 2) if adjusted_cost else None
            app_scenarios.append({
                "scenario_id": scenario["scenario_id"],
                "scenario_name": scenario["scenario_name"],
                "base_cost": base_cost,
                "adjusted_cost": adjusted_cost,
                "annual_savings": annual_savings,
                "roi_3year": roi,
            })
            app_investment += adjusted_cost
            app_savings += annual_savings
            scenario_portfolio_totals[scenario["scenario_name"]] += 1
        mod_status = modernization_status_label(app_id, out_scope[app_id], tech_by_id[app_id], scenario_by_id[app_id])
        business_apps.append({
            "application_id": app_id,
            "app_name": safe(app.get("app_name")),
            "complexity_score": complexity_score,
            "modernization_status": mod_status,
            "applicable_scenarios": app_scenarios,
            "total_investment": round(app_investment, 2),
            "total_annual_savings": round(app_savings, 2),
        })
        total_investment += app_investment
        total_annual_savings += app_savings
    portfolio_roi = round(((total_annual_savings * 3 - total_investment) / total_investment) * 100, 2) if total_investment else None
    business_case = {
        "portfolio_summary": {
            "total_applications": len(apps),
            "in_scope_applications": len(in_scope_apps),
            "out_of_scope_applications": sum(1 for item in out_scope.values() if item["out_of_scope"]),
            "total_investment": round(total_investment, 2),
            "total_annual_savings": round(total_annual_savings, 2),
            "portfolio_roi_3year": portfolio_roi,
        },
        "portfolio_scenario_counts": dict(sorted(scenario_portfolio_totals.items())),
        "applications": business_apps,
        "analysis_timestamp": CURRENT_TS,
    }
    write_json(BUSINESS_DIR / "business_case.json", business_case)

    business_lookup = {item["application_id"]: item for item in business_apps}
    for app in in_scope_apps:
        app_id = safe(app.get("app_id"))
        (APP_MD_DIR / f"app_report_{app_id}.md").write_text(build_app_markdown(app, tech_by_id[app_id], complexity_by_id[app_id], scenario_by_id[app_id], business_lookup[app_id]), encoding="utf-8")
        (APP_HTML_DIR / f"application_report_{app_id}.html").write_text(build_app_html(app, tech_by_id[app_id], complexity_by_id[app_id], scenario_by_id[app_id], business_lookup[app_id], logo_svg), encoding="utf-8")

    (REPORTS_DIR / "portfolio_report.md").write_text(build_portfolio_markdown(apps, out_scope, tech_by_id, complexity_by_id, scenario_by_id, business_case), encoding="utf-8")
    (REPORTS_DIR / "portfolio_modernization_report.html").write_text(build_portfolio_html(apps, out_scope, scenario_by_id, business_case, logo_svg), encoding="utf-8")

    write_json(MONITORING_DIR / "analysis_summary.json", {
        "generated_timestamp": CURRENT_TS,
        "total_applications": len(apps),
        "in_scope_applications": len(in_scope_apps),
        "out_of_scope_applications": sum(1 for item in out_scope.values() if item["out_of_scope"]),
        "analysis_id": analysis_id("portfolio", str(len(apps))),
    })


if __name__ == "__main__":
    main()
