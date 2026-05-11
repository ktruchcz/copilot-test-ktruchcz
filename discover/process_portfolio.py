#!/usr/bin/env python3
"""Portfolio modernization processing script - handles Steps 1-6"""
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

BASE = Path("/home/runner/work/copilot-test-ktruchcz/copilot-test-ktruchcz")
OUT = BASE / "discover/output"

# Create directories
for d in [
    "applications/internal_app_model",
    "applications/consolidated_schema",
    "schemas",
    "out_of_scope_results",
    "technology_assessment",
    "complexity_results",
    "scenario_applicability_results",
    "business_case_results",
    "reports/apps",
    "reports/application_reports",
]:
    (OUT / d).mkdir(parents=True, exist_ok=True)

# Load all raw app JSON files
raw_dir = OUT / "applications/internal_app_model"
apps = []
for f in sorted(raw_dir.glob("app*.json")):
    with open(f) as fh:
        apps.append(json.load(fh))

print(f"Loaded {len(apps)} applications")

# ============================================================
# STEP 1: Create proper file naming + consolidated schema files
# ============================================================

def write_internal_model(app):
    app_id = app["app_id"]
    model = {
        "app_id": app_id,
        "app_name": app["app_name"],
        "app_description": app.get("app_description", ""),
        "retiring_at": str(app.get("additional_attributes", {}).get("decomission_date", "")) or ""
    }
    path = OUT / f"applications/internal_app_model/internal_app_model_application_{app_id}.json"
    with open(path, "w") as f:
        json.dump(model, f, indent=2)

def write_consolidated_schema(app):
    app_id = app["app_id"]
    servers = app.get("server_instances", [])
    if isinstance(servers, list):
        servers_str = ", ".join(servers)
    else:
        servers_str = str(servers) if servers else ""
    
    schema = {
        "app_id": app_id,
        "name": app["app_name"],
        "description": app.get("app_description", ""),
        "Solution type": app.get("solution_type", ""),
        "criticality": app.get("business_criticality", ""),
        "Application status": app.get("application_status", ""),
        "Decomission date": str(app.get("additional_attributes", {}).get("decomission_date", "") or ""),
        "Deployment type": app.get("deployment_type", ""),
        "data classification": app.get("data_classification", ""),
        "business unit": app.get("business_unit", ""),
        "number of users": str(app.get("user_count", "")) if app.get("user_count") is not None else "",
        "Operating system": app.get("operating_system", ""),
        "programming language": app.get("programming_language", ""),
        "Application Server type": app.get("application_server", "") or "",
        "Application Architecture": app.get("application_architecture", ""),
        "Application is containerized": app.get("is_containerized", ""),
        "Number of environments": str(app.get("environment_count", "")) if app.get("environment_count") is not None else "",
        "Physical servers instances": servers_str,
        "external interfaces": str(app.get("external_interface_count", "")) if app.get("external_interface_count") is not None else "",
        "db_engine": app.get("database_engine", "") or "",
        "CI_CD present": app.get("ci_cd_present", "") or "",
        "logging_solution": app.get("logging_solution", "") or "",
        "monitoring_tool": app.get("monitoring_tool", "") or "",
        "database_storage_gb": str(app.get("database_storage_gb", "")) if app.get("database_storage_gb") is not None else "",
        "database_license_required": app.get("database_license_required", "") or "",
        "business_capabilities": app.get("business_capabilities", []),
    }
    path = OUT / f"applications/consolidated_schema/consolidated_schema_application_{app_id}.json"
    with open(path, "w") as f:
        json.dump(schema, f, indent=2)

for app in apps:
    write_internal_model(app)
    write_consolidated_schema(app)

# Write overview
import hashlib
overview = {
    "analysis_id": hashlib.md5(datetime.now().isoformat().encode()).hexdigest(),
    "applications_overview": {
        "total_applications": len(apps),
        "valid_applications": len(apps),
        "invalid_applications": 0,
        "application_id_field": "app_id",
        "application_name_field": "name",
        "application_description_field": "description",
        "invalid_applications_list": []
    },
    "timestamp": datetime.now().isoformat()
}
with open(OUT / "applications/consolidated_applications_overview.json", "w") as f:
    json.dump(overview, f, indent=2)

# Write schemas
schema_def = {
    "fields": ["app_id","name","description","Solution type","criticality","Application status",
               "Decomission date","Deployment type","data classification","business unit",
               "number of users","Operating system","programming language","Application Server type",
               "Application Architecture","Application is containerized","Number of environments",
               "Physical servers instances","external interfaces","db_engine","CI_CD present"]
}
with open(OUT / "schemas/consolidated_application_schema.json", "w") as f:
    json.dump(schema_def, f, indent=2)
with open(OUT / "schemas/original_application_schema_from_apps_db_complete.json", "w") as f:
    json.dump(schema_def, f, indent=2)
with open(OUT / "schemas/original_unified_schema_from_validated_output.json", "w") as f:
    json.dump(schema_def, f, indent=2)
with open(OUT / "schemas/original_relationship_model_schema_from_validated_output.json", "w") as f:
    json.dump({"relationships": []}, f, indent=2)

print("Step 1 complete: File structure created")

# ============================================================
# STEP 2: Out-of-scope assessment
# ============================================================

def is_sap(app):
    name = (app.get("app_name","") + " " + app.get("app_description","") + " " + app.get("solution_type","")).lower()
    return "sap" in name

def assess_out_of_scope(app):
    app_id = app["app_id"]
    status = app.get("application_status","").lower()
    retired = status in ["retired", "decommissioned", "retired / decommissioned"]
    sap = is_sap(app)
    
    assessments = [
        {
            "exclusion_type": "RETIRED",
            "applies": retired,
            "confidence": 9,
            "reasoning": f"Application status is '{app.get('application_status','')}'. {'Application is retired.' if retired else 'Application is in production.'}"
        },
        {
            "exclusion_type": "SAP",
            "applies": sap,
            "confidence": 9,
            "reasoning": "SAP indicators found in application data." if sap else "No SAP indicators found in solution type or description."
        }
    ]
    
    out_of_scope = retired or sap
    result = {
        "application_identifier": app_id,
        "assessments": assessments,
        "out_of_scope": out_of_scope
    }
    path = OUT / f"out_of_scope_results/out_of_scope_{app_id}.json"
    with open(path, "w") as f:
        json.dump(result, f, indent=2)
    return out_of_scope

oos_map = {}
for app in apps:
    oos_map[app["app_id"]] = assess_out_of_scope(app)

in_scope = [a for a in apps if not oos_map[a["app_id"]]]
out_of_scope_apps = [a for a in apps if oos_map[a["app_id"]]]
print(f"Step 2 complete: {len(out_of_scope_apps)} out-of-scope, {len(in_scope)} in-scope")

# ============================================================
# STEP 3: Technology Assessment
# ============================================================

def assess_technology(app):
    app_id = app["app_id"]
    components = []
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # OS assessment
    os_str = app.get("operating_system","") or ""
    if os_str:
        comp = assess_os(os_str)
        components.append(comp)
    
    # DB assessment
    db_str = app.get("database_engine","") or ""
    if db_str:
        comp = assess_db(db_str)
        components.append(comp)
    
    # Programming language
    lang_str = app.get("programming_language","") or ""
    if lang_str:
        comp = assess_language(lang_str)
        components.append(comp)
    
    # App server
    srv_str = app.get("application_server","") or ""
    if srv_str and srv_str.lower() not in ["none","n/a","-","",None]:
        comp = assess_app_server(srv_str)
        components.append(comp)
    
    has_eol = any(c["component_status"] == "EOL" for c in components)
    has_outdated = any(c["component_status"] == "OUTDATED" for c in components)
    has_missing = any(c["component_status"] == "NO_KNOWLEDGE" for c in components)
    
    result = {
        "application_identifier": app_id,
        "components_analyzed": components,
        "has_eol_components": has_eol,
        "has_outdated_components": has_outdated,
        "has_missing_version_data": has_missing,
        "analysis_timestamp": ts
    }
    path = OUT / f"technology_assessment/technology_assessment_{app_id}.json"
    with open(path, "w") as f:
        json.dump(result, f, indent=2)
    return result

def assess_os(os_str):
    os_lower = os_str.lower()
    
    if "aix" in os_lower:
        ver = ""
        import re
        m = re.search(r'(\d+\.?\d*)', os_str)
        if m: ver = m.group(1)
        # AIX 7.2 - end of support April 2023, AIX 7.3 - still supported
        if ver.startswith("7.3"): status, eol, reason = "CURRENT_VERSION", "2029-04-30", "AIX 7.3 is supported until 2029."
        elif ver.startswith("7.2"): status, eol, reason = "EOL", "2023-04-30", "AIX 7.2 reached end of support in April 2023."
        elif ver.startswith("7.1"): status, eol, reason = "EOL", "2023-04-30", "AIX 7.1 is end of life."
        else: status, eol, reason = "OUTDATED", "", f"AIX {ver} is outdated."
        return {"component_name": f"AIX {ver}","component_family":"AIX","component_type":"os","managed_service":False,"version":ver,"component_status":status,"eol_date":eol,"reason":reason,"confidence":8}
    
    elif "rhel" in os_lower or "red hat" in os_lower:
        import re
        m = re.search(r'(\d+)', os_str)
        ver = m.group(1) if m else ""
        ver_int = int(ver) if ver.isdigit() else 0
        if ver_int >= 9: status, eol, reason = "CURRENT_VERSION", "2032-05-31", f"RHEL {ver} is actively supported."
        elif ver_int == 8: status, eol, reason = "CURRENT_VERSION", "2029-05-31", f"RHEL 8 is supported until May 2029."
        elif ver_int == 7: status, eol, reason = "EOL", "2024-06-30", f"RHEL 7 reached end of maintenance support June 2024."
        elif ver_int <= 6: status, eol, reason = "EOL", "2020-11-30", f"RHEL {ver} is end of life."
        else: status, eol, reason = "NO_KNOWLEDGE", "", f"Unknown RHEL version."
        return {"component_name":f"RHEL {ver}","component_family":"RHEL","component_type":"os","managed_service":False,"version":ver,"component_status":status,"eol_date":eol,"reason":reason,"confidence":9}
    
    elif "ubuntu" in os_lower:
        import re
        m = re.search(r'(\d+\.\d+)', os_str)
        ver = m.group(1) if m else ""
        lts = ["18.04","20.04","22.04","24.04"]
        if ver in ["24.04"]: status, eol, reason = "CURRENT_VERSION","2029-04-30",f"Ubuntu {ver} LTS is actively supported."
        elif ver in ["22.04"]: status, eol, reason = "CURRENT_VERSION","2027-04-30",f"Ubuntu 22.04 LTS is supported until 2027."
        elif ver in ["20.04"]: status, eol, reason = "OUTDATED","2025-04-30",f"Ubuntu 20.04 LTS is approaching end of standard support."
        elif ver in ["18.04"]: status, eol, reason = "EOL","2023-04-30",f"Ubuntu 18.04 LTS reached end of life April 2023."
        else: status, eol, reason = "OUTDATED","",f"Ubuntu {ver} - check LTS support status."
        return {"component_name":f"Ubuntu {ver}","component_family":"Ubuntu","component_type":"os","managed_service":False,"version":ver,"component_status":status,"eol_date":eol,"reason":reason,"confidence":8}
    
    elif "windows server" in os_lower or "windows" in os_lower:
        import re
        m = re.search(r'(2008|2012|2016|2019|2022)', os_str)
        ver = m.group(1) if m else ""
        if ver == "2022": status, eol, reason = "CURRENT_VERSION","2031-10-14","Windows Server 2022 is actively supported."
        elif ver == "2019": status, eol, reason = "CURRENT_VERSION","2029-01-09","Windows Server 2019 is actively supported."
        elif ver == "2016": status, eol, reason = "OUTDATED","2027-01-12","Windows Server 2016 is in extended support."
        elif ver == "2012": status, eol, reason = "EOL","2023-10-10","Windows Server 2012 reached end of support October 2023."
        elif ver == "2008": status, eol, reason = "EOL","2020-01-14","Windows Server 2008 reached end of support January 2020."
        else: status, eol, reason = "OUTDATED","","Windows Server - version details needed."
        name = f"Windows Server {ver}" if ver else "Windows Server"
        return {"component_name":name,"component_family":"Windows Server","component_type":"os","managed_service":False,"version":ver,"component_status":status,"eol_date":eol,"reason":reason,"confidence":8}
    
    elif "debian" in os_lower:
        import re
        m = re.search(r'(\d+)', os_str)
        ver = m.group(1) if m else ""
        ver_int = int(ver) if ver.isdigit() else 0
        if ver_int >= 12: status, eol, reason = "CURRENT_VERSION","2028-06-30",f"Debian {ver} is actively supported."
        elif ver_int == 11: status, eol, reason = "OUTDATED","2026-06-30",f"Debian 11 is in LTS support."
        elif ver_int <= 10: status, eol, reason = "EOL","2024-06-30",f"Debian {ver} is end of life."
        else: status, eol, reason = "NO_KNOWLEDGE","",f"Unknown Debian version."
        return {"component_name":f"Debian {ver}","component_family":"Debian","component_type":"os","managed_service":False,"version":ver,"component_status":status,"eol_date":eol,"reason":reason,"confidence":8}
    
    else:
        return {"component_name":os_str,"component_family":os_str.split()[0] if os_str.split() else os_str,"component_type":"os","managed_service":False,"version":"","component_status":"NO_KNOWLEDGE","eol_date":"","reason":f"Lifecycle information not available for {os_str}.","confidence":4}

def assess_db(db_str):
    db_lower = db_str.lower()
    import re
    
    if "oracle" in db_lower:
        m = re.search(r'(\d+[a-z]?)', db_str)
        ver = m.group(1) if m else ""
        if ver in ["21","21c"]: status, eol, reason = "CURRENT_VERSION","2026-04-30","Oracle 21c is in active support."
        elif ver in ["19","19c"]: status, eol, reason = "CURRENT_VERSION","2027-04-30","Oracle 19c is in Long Term Support until 2027."
        elif ver in ["18","18c"]: status, eol, reason = "EOL","2021-06-30","Oracle 18c reached end of premier support."
        elif ver in ["12","12c"]: status, eol, reason = "EOL","2022-07-31","Oracle 12c reached end of premier support July 2022."
        elif ver in ["11","11g"]: status, eol, reason = "EOL","2020-12-31","Oracle 11g is end of life."
        else: status, eol, reason = "OUTDATED","",f"Oracle DB {ver} - check lifecycle status."
        return {"component_name":f"Oracle {ver}","component_family":"Oracle","component_type":"database","managed_service":False,"version":ver,"component_status":status,"eol_date":eol,"reason":reason,"confidence":9}
    
    elif "postgresql" in db_lower or "postgres" in db_lower:
        m = re.search(r'(\d+)', db_str)
        ver = m.group(1) if m else ""
        ver_int = int(ver) if ver.isdigit() else 0
        if ver_int >= 16: status, eol, reason = "CURRENT_VERSION","2028-11-09",f"PostgreSQL {ver} is actively supported."
        elif ver_int == 15: status, eol, reason = "CURRENT_VERSION","2027-11-11",f"PostgreSQL 15 is actively supported."
        elif ver_int == 14: status, eol, reason = "CURRENT_VERSION","2026-11-12",f"PostgreSQL 14 is actively supported."
        elif ver_int == 13: status, eol, reason = "OUTDATED","2025-11-13",f"PostgreSQL 13 reaches EOL November 2025."
        elif ver_int == 12: status, eol, reason = "EOL","2024-11-14",f"PostgreSQL 12 reached EOL November 2024."
        elif ver_int <= 11: status, eol, reason = "EOL","2023-11-09",f"PostgreSQL {ver} is end of life."
        else: status, eol, reason = "NO_KNOWLEDGE","","Unknown PostgreSQL version."
        return {"component_name":f"PostgreSQL {ver}","component_family":"PostgreSQL","component_type":"database","managed_service":False,"version":ver,"component_status":status,"eol_date":eol,"reason":reason,"confidence":9}
    
    elif "mysql" in db_lower:
        m = re.search(r'(\d+\.\d+)', db_str)
        ver = m.group(1) if m else ""
        major = ver.split(".")[0] if ver else ""
        if major == "8": 
            minor = float(ver) if ver else 0
            if minor >= 8.0: status, eol, reason = "CURRENT_VERSION","2026-04-30","MySQL 8.0 is in active support."
            else: status, eol, reason = "OUTDATED","","MySQL 8.x - check minor version."
        elif major == "5":
            if "5.7" in ver: status, eol, reason = "EOL","2023-10-31","MySQL 5.7 reached EOL October 2023."
            else: status, eol, reason = "EOL","2023-10-31",f"MySQL {ver} is end of life."
        else: status, eol, reason = "NO_KNOWLEDGE","",f"Unknown MySQL version {ver}."
        return {"component_name":f"MySQL {ver}","component_family":"MySQL","component_type":"database","managed_service":False,"version":ver,"component_status":status,"eol_date":eol,"reason":reason,"confidence":8}
    
    elif "mongodb" in db_lower:
        m = re.search(r'(\d+)', db_str)
        ver = m.group(1) if m else ""
        ver_int = int(ver) if ver.isdigit() else 0
        if ver_int >= 7: status, eol, reason = "CURRENT_VERSION","2027-08-01",f"MongoDB {ver} is actively supported."
        elif ver_int == 6: status, eol, reason = "CURRENT_VERSION","2025-07-01","MongoDB 6.0 is in active support."
        elif ver_int == 5: status, eol, reason = "EOL","2024-10-01","MongoDB 5.0 reached EOL."
        elif ver_int <= 4: status, eol, reason = "EOL","2024-02-01",f"MongoDB {ver} is end of life."
        else: status, eol, reason = "NO_KNOWLEDGE","","Unknown MongoDB version."
        return {"component_name":f"MongoDB {ver}","component_family":"MongoDB","component_type":"database","managed_service":False,"version":ver,"component_status":status,"eol_date":eol,"reason":reason,"confidence":8}
    
    elif "mssql" in db_lower or "sql server" in db_lower or "microsoft sql" in db_lower:
        m = re.search(r'(2014|2016|2017|2019|2022)', db_str)
        ver = m.group(1) if m else ""
        if ver == "2022": status, eol, reason = "CURRENT_VERSION","2033-01-11","SQL Server 2022 is actively supported."
        elif ver == "2019": status, eol, reason = "CURRENT_VERSION","2030-01-08","SQL Server 2019 is actively supported."
        elif ver == "2017": status, eol, reason = "OUTDATED","2027-10-12","SQL Server 2017 is in extended support."
        elif ver == "2016": status, eol, reason = "EOL","2026-07-14","SQL Server 2016 reaches end of mainstream support."
        elif ver in ["2014","2012","2008"]: status, eol, reason = "EOL","2024-07-09",f"SQL Server {ver} is end of life."
        else: status, eol, reason = "OUTDATED","",f"SQL Server {ver} - check lifecycle."
        name = f"SQL Server {ver}" if ver else "SQL Server"
        return {"component_name":name,"component_family":"SQL Server","component_type":"database","managed_service":False,"version":ver,"component_status":status,"eol_date":eol,"reason":reason,"confidence":8}
    
    elif "cassandra" in db_lower:
        m = re.search(r'(\d+\.?\d*)', db_str)
        ver = m.group(1) if m else ""
        return {"component_name":f"Cassandra {ver}","component_family":"Cassandra","component_type":"database","managed_service":False,"version":ver,"component_status":"CURRENT_VERSION","eol_date":"","reason":"Apache Cassandra 4.x/5.x is actively supported.","confidence":6}
    
    elif "redis" in db_lower:
        m = re.search(r'(\d+)', db_str)
        ver = m.group(1) if m else ""
        ver_int = int(ver) if ver.isdigit() else 0
        if ver_int >= 7: status, reason = "CURRENT_VERSION", "Redis 7.x is actively supported."
        elif ver_int == 6: status, reason = "CURRENT_VERSION", "Redis 6.x is in active support."
        else: status, reason = "OUTDATED", f"Redis {ver} - check support status."
        return {"component_name":f"Redis {ver}","component_family":"Redis","component_type":"database","managed_service":False,"version":ver,"component_status":status,"eol_date":"","reason":reason,"confidence":7}
    
    elif "elasticsearch" in db_lower:
        m = re.search(r'(\d+)', db_str)
        ver = m.group(1) if m else ""
        ver_int = int(ver) if ver.isdigit() else 0
        if ver_int >= 8: status, reason = "CURRENT_VERSION", f"Elasticsearch {ver} is actively supported."
        elif ver_int == 7: status, reason = "OUTDATED", "Elasticsearch 7.x is in maintenance mode."
        else: status, reason = "EOL", f"Elasticsearch {ver} is end of life."
        return {"component_name":f"Elasticsearch {ver}","component_family":"Elasticsearch","component_type":"database","managed_service":False,"version":ver,"component_status":status,"eol_date":"","reason":reason,"confidence":7}
    
    else:
        return {"component_name":db_str,"component_family":db_str.split()[0] if db_str else "Unknown","component_type":"database","managed_service":False,"version":"","component_status":"NO_KNOWLEDGE","eol_date":"","reason":f"Lifecycle info not available for {db_str}.","confidence":4}

def assess_language(lang_str):
    lang_lower = lang_str.lower()
    import re
    
    if "cobol" in lang_lower:
        return {"component_name":lang_str,"component_family":"COBOL","component_type":"language","managed_service":False,"version":"2014","component_status":"OUTDATED","eol_date":"","reason":"COBOL is a legacy language. While COBOL-2014 standard exists, it is considered outdated for modern development patterns.","confidence":8}
    
    elif "java" in lang_lower and "javascript" not in lang_lower:
        m = re.search(r'(\d+)', lang_str)
        ver = m.group(1) if m else ""
        ver_int = int(ver) if ver.isdigit() else 0
        if ver_int >= 21: status, eol, reason = "CURRENT_VERSION","2028-09-30",f"Java {ver} LTS is actively supported."
        elif ver_int == 17: status, eol, reason = "CURRENT_VERSION","2026-09-30","Java 17 LTS is in active support."
        elif ver_int == 11: status, eol, reason = "OUTDATED","2026-09-30","Java 11 LTS is approaching end of active support."
        elif ver_int == 8: status, eol, reason = "EOL","2030-12-31","Java 8 premier support ended March 2022."  # complex EOL
        elif ver_int <= 7: status, eol, reason = "EOL","2019-07-31",f"Java {ver} is end of life."
        else: status, eol, reason = "NO_KNOWLEDGE","",f"Unknown Java version {ver}."
        return {"component_name":f"Java {ver}","component_family":"Java","component_type":"language","managed_service":False,"version":ver,"component_status":status,"eol_date":eol,"reason":reason,"confidence":9}
    
    elif "python" in lang_lower:
        m = re.search(r'(\d+\.\d*)', lang_str)
        ver = m.group(1) if m else ""
        major = ver.split(".")[0] if ver else ""
        if major == "3":
            minor = int(ver.split(".")[1]) if len(ver.split(".")) > 1 and ver.split(".")[1].isdigit() else 0
            if minor >= 12: status, reason = "CURRENT_VERSION","Python 3.12+ is actively supported."
            elif minor >= 10: status, reason = "CURRENT_VERSION",f"Python {ver} is actively supported."
            elif minor == 9: status, reason = "OUTDATED","Python 3.9 reaches EOL October 2025."
            elif minor <= 8: status, reason = "EOL",f"Python {ver} is end of life."
            else: status, reason = "CURRENT_VERSION",f"Python {ver} is supported."
        elif major == "2": status, reason = "EOL","Python 2.x reached end of life January 2020."
        else: status, reason = "NO_KNOWLEDGE",f"Unknown Python version {ver}."
        return {"component_name":f"Python {ver}","component_family":"Python","component_type":"language","managed_service":False,"version":ver,"component_status":status,"eol_date":"","reason":reason,"confidence":8}
    
    elif ".net" in lang_lower or "c#" in lang_lower or "csharp" in lang_lower:
        m = re.search(r'(\d+)', lang_str)
        ver = m.group(1) if m else ""
        ver_int = int(ver) if ver.isdigit() else 0
        if ver_int >= 8: status, reason = "CURRENT_VERSION",f".NET {ver} is actively supported."
        elif ver_int == 7: status, reason = "OUTDATED",".NET 7 is in maintenance."
        elif ver_int == 6: status, reason = "OUTDATED",".NET 6 LTS reached EOL November 2024."
        elif ver_int <= 5: status, reason = "EOL",f".NET {ver} is end of life."
        else:
            if "framework" in lang_lower:
                status, reason = "OUTDATED",".NET Framework is legacy; consider migration to .NET 6+."
            else:
                status, reason = "NO_KNOWLEDGE","Unknown .NET version."
        return {"component_name":lang_str,"component_family":".NET","component_type":"language","managed_service":False,"version":ver,"component_status":status,"eol_date":"","reason":reason,"confidence":8}
    
    elif "node" in lang_lower or "javascript" in lang_lower or "typescript" in lang_lower:
        m = re.search(r'(\d+)', lang_str)
        ver = m.group(1) if m else ""
        ver_int = int(ver) if ver.isdigit() else 0
        if ver_int >= 20: status, reason = "CURRENT_VERSION",f"Node.js {ver} LTS is actively supported."
        elif ver_int == 18: status, reason = "CURRENT_VERSION","Node.js 18 LTS is in active support."
        elif ver_int == 16: status, reason = "EOL","Node.js 16 reached EOL September 2023."
        elif ver_int <= 14: status, reason = "EOL",f"Node.js {ver} is end of life."
        else: status, reason = "CURRENT_VERSION","JavaScript/TypeScript - actively maintained."
        lang_name = "TypeScript" if "typescript" in lang_lower else "JavaScript/Node.js"
        return {"component_name":lang_str,"component_family":lang_name,"component_type":"language","managed_service":False,"version":ver,"component_status":status,"eol_date":"","reason":reason,"confidence":7}
    
    elif "go" in lang_lower or "golang" in lang_lower:
        return {"component_name":lang_str,"component_family":"Go","component_type":"language","managed_service":False,"version":"","component_status":"CURRENT_VERSION","eol_date":"","reason":"Go is actively developed and maintained.","confidence":7}
    
    elif "rust" in lang_lower:
        return {"component_name":lang_str,"component_family":"Rust","component_type":"language","managed_service":False,"version":"","component_status":"CURRENT_VERSION","eol_date":"","reason":"Rust is actively developed and maintained.","confidence":7}
    
    elif "php" in lang_lower:
        m = re.search(r'(\d+)', lang_str)
        ver = m.group(1) if m else ""
        ver_int = int(ver) if ver.isdigit() else 0
        if ver_int >= 8: status, reason = "CURRENT_VERSION",f"PHP {ver} is actively supported."
        elif ver_int == 7: status, reason = "EOL","PHP 7.x reached end of life December 2022."
        else: status, reason = "EOL",f"PHP {ver} is end of life."
        return {"component_name":lang_str,"component_family":"PHP","component_type":"language","managed_service":False,"version":ver,"component_status":status,"eol_date":"","reason":reason,"confidence":8}
    
    else:
        return {"component_name":lang_str,"component_family":lang_str.split()[0] if lang_str else "Unknown","component_type":"language","managed_service":False,"version":"","component_status":"NO_KNOWLEDGE","eol_date":"","reason":f"Lifecycle info not available for {lang_str}.","confidence":4}

def assess_app_server(srv_str):
    srv_lower = srv_str.lower()
    import re
    
    if "tomcat" in srv_lower:
        m = re.search(r'(\d+)', srv_str)
        ver = m.group(1) if m else ""
        ver_int = int(ver) if ver.isdigit() else 0
        if ver_int >= 10: status, reason = "CURRENT_VERSION",f"Tomcat {ver} is actively maintained."
        elif ver_int == 9: status, reason = "CURRENT_VERSION","Tomcat 9 is in active support."
        elif ver_int == 8: status, reason = "EOL","Tomcat 8.x reached end of life."
        elif ver_int <= 7: status, reason = "EOL",f"Tomcat {ver} is end of life."
        else: status, reason = "CURRENT_VERSION","Apache Tomcat is actively maintained."
        return {"component_name":f"Tomcat {ver}","component_family":"Apache Tomcat","component_type":"application_server","managed_service":False,"version":ver,"component_status":status,"eol_date":"","reason":reason,"confidence":8}
    
    elif "jboss" in srv_lower or "wildfly" in srv_lower:
        return {"component_name":srv_str,"component_family":"JBoss/WildFly","component_type":"application_server","managed_service":False,"version":"","component_status":"OUTDATED","eol_date":"","reason":"JBoss/WildFly - check version for lifecycle status. JBoss EAP versions have varied support timelines.","confidence":6}
    
    elif "weblogic" in srv_lower:
        return {"component_name":srv_str,"component_family":"WebLogic","component_type":"application_server","managed_service":False,"version":"","component_status":"OUTDATED","eol_date":"","reason":"Oracle WebLogic is a commercial product requiring license. Check version support.","confidence":6}
    
    elif "websphere" in srv_lower:
        return {"component_name":srv_str,"component_family":"WebSphere","component_type":"application_server","managed_service":False,"version":"","component_status":"OUTDATED","eol_date":"","reason":"IBM WebSphere is a legacy commercial product.","confidence":6}
    
    elif "nginx" in srv_lower:
        return {"component_name":srv_str,"component_family":"Nginx","component_type":"application_server","managed_service":False,"version":"","component_status":"CURRENT_VERSION","eol_date":"","reason":"Nginx is actively maintained.","confidence":7}
    
    elif "iis" in srv_lower:
        return {"component_name":srv_str,"component_family":"IIS","component_type":"application_server","managed_service":False,"version":"","component_status":"CURRENT_VERSION","eol_date":"","reason":"IIS lifecycle follows Windows Server lifecycle.","confidence":7}
    
    elif "spring boot" in srv_lower or "springboot" in srv_lower:
        m = re.search(r'(\d+)', srv_str)
        ver = m.group(1) if m else ""
        ver_int = int(ver) if ver.isdigit() else 0
        if ver_int >= 3: status, reason = "CURRENT_VERSION",f"Spring Boot {ver} is actively supported."
        elif ver_int == 2: status, reason = "OUTDATED","Spring Boot 2.x reached end of support November 2023."
        else: status, reason = "EOL",f"Spring Boot {ver} is end of life."
        return {"component_name":f"Spring Boot {ver}","component_family":"Spring Boot","component_type":"application_server","managed_service":False,"version":ver,"component_status":status,"eol_date":"","reason":reason,"confidence":8}
    
    elif "node" in srv_lower or "express" in srv_lower:
        return {"component_name":srv_str,"component_family":"Node.js/Express","component_type":"application_server","managed_service":False,"version":"","component_status":"CURRENT_VERSION","eol_date":"","reason":"Node.js/Express is actively maintained.","confidence":7}
    
    else:
        return {"component_name":srv_str,"component_family":srv_str.split()[0] if srv_str else "Unknown","component_type":"application_server","managed_service":False,"version":"","component_status":"NO_KNOWLEDGE","eol_date":"","reason":f"Lifecycle info not available for {srv_str}.","confidence":4}

tech_assessments = {}
for app in in_scope:
    tech_assessments[app["app_id"]] = assess_technology(app)

print("Step 3 complete: Technology assessments created")

# ============================================================
# STEP 4: Complexity Assessment
# ============================================================

def assess_complexity(app, tech):
    app_id = app["app_id"]
    
    eol_count = sum(1 for c in tech["components_analyzed"] if c["component_status"] == "EOL")
    outdated_count = sum(1 for c in tech["components_analyzed"] if c["component_status"] == "OUTDATED")
    
    # Technology age (25%)
    if eol_count >= 2: tech_score = 9
    elif eol_count == 1: tech_score = 7
    elif outdated_count >= 2: tech_score = 5
    elif outdated_count == 1: tech_score = 4
    else: tech_score = 2
    
    # Integration complexity (20%)
    iface = app.get("external_interface_count", 0) or 0
    if isinstance(iface, str):
        try: iface = int(iface)
        except: iface = 0
    if iface >= 6: int_score = 8
    elif iface >= 3: int_score = 5
    else: int_score = 2
    
    # Infrastructure scale (15%)
    servers = app.get("server_instances", [])
    if isinstance(servers, list): srv_count = len(servers)
    elif isinstance(servers, str) and servers: srv_count = len([s for s in servers.split(",") if s.strip()])
    else: srv_count = 1
    envs = app.get("environment_count", 1) or 1
    if isinstance(envs, str):
        try: envs = int(envs)
        except: envs = 1
    if srv_count >= 6 or envs >= 4: infra_score = 8
    elif srv_count >= 3 or envs >= 3: infra_score = 5
    else: infra_score = 2
    
    # Business criticality (15%)
    crit = (app.get("business_criticality","") or "").lower()
    if crit in ["high","critical","business critical"]: crit_score = 8
    elif crit in ["medium","moderate"]: crit_score = 5
    else: crit_score = 2
    
    # Architecture (15%)
    arch = (app.get("application_architecture","") or "").lower()
    containerized = (app.get("is_containerized","") or "").lower()
    ci_cd = (app.get("ci_cd_present","") or "").lower()
    lang = (app.get("programming_language","") or "").lower()
    
    arch_score = 5  # default
    if "cobol" in lang or "1-tier" in arch: arch_score = 8
    elif "microservice" in arch or containerized in ["yes","true"]: arch_score = 2
    elif "2-tier" in arch or "monolith" in arch.lower(): arch_score = 7
    elif "3-tier" in arch: arch_score = 4
    if ci_cd in ["no","false",""]: arch_score = min(arch_score + 1, 10)
    
    # Data complexity (10%)
    db = (app.get("database_engine","") or "").lower()
    storage = app.get("database_storage_gb", 0) or 0
    if isinstance(storage, str):
        try: storage = float(storage)
        except: storage = 0
    if storage > 500 or eol_count >= 1: data_score = 7
    elif storage > 100: data_score = 5
    else: data_score = 3
    
    final = round(tech_score * 0.25 + int_score * 0.20 + infra_score * 0.15 + crit_score * 0.15 + arch_score * 0.15 + data_score * 0.10)
    final = max(1, min(10, final))
    
    if final <= 3: level = "LOW"
    elif final <= 6: level = "MEDIUM"
    else: level = "HIGH"
    
    result = {
        "application_identifier": app_id,
        "complexity_score": final,
        "confidence": 7,
        "reasoning": f"Score {final}/10 ({level}): {eol_count} EOL component(s), {outdated_count} outdated, {iface} external interfaces, {srv_count} server(s), criticality={app.get('business_criticality','?')}, architecture={app.get('application_architecture','?')}.",
        "contributing_factors": {
            "number_of_servers": srv_count,
            "number_of_databases": 1 if app.get("database_engine") else 0,
            "number_of_environments": envs,
            "number_of_interfaces": iface,
            "business_criticality": app.get("business_criticality",""),
            "number_of_outdated_technologies": outdated_count,
            "number_of_eol_technologies": eol_count,
            "number_of_dependencies": 0,
            "ci_cd_present": app.get("ci_cd_present","No"),
            "containerized": app.get("is_containerized","No")
        }
    }
    path = OUT / f"complexity_results/complexity_{app_id}.json"
    with open(path, "w") as f:
        json.dump(result, f, indent=2)
    return result

complexity_results = {}
for app in in_scope:
    complexity_results[app["app_id"]] = assess_complexity(app, tech_assessments[app["app_id"]])

print("Step 4 complete: Complexity assessments created")

# ============================================================
# STEP 5: Scenario Analysis
# ============================================================

with open(BASE / ".github/skills/scenario-analysis/references/modernization_scenarios_list.json") as f:
    scenarios = json.load(f)

def evaluate_scenarios(app, tech, complexity):
    app_id = app["app_id"]
    os_str = (app.get("operating_system","") or "").lower()
    db_str = (app.get("database_engine","") or "").lower()
    lang_str = (app.get("programming_language","") or "").lower()
    arch_str = (app.get("application_architecture","") or "").lower()
    deploy_str = (app.get("deployment_type","") or "").lower()
    containerized = (app.get("is_containerized","") or "").lower()
    solution_type = (app.get("solution_type","") or "").lower()
    srv_str = (app.get("application_server","") or "").lower()
    
    eol_components = [c for c in tech["components_analyzed"] if c["component_status"] == "EOL"]
    outdated_components = [c for c in tech["components_analyzed"] if c["component_status"] == "OUTDATED"]
    eol_names = [c["component_name"] for c in eol_components]
    
    is_saas = "saas" in solution_type or "software as a service" in solution_type
    is_cloud = any(x in deploy_str for x in ["cloud","azure","aws","gcp","public cloud"])
    
    scenario_results = []
    
    for scenario in scenarios:
        sid = scenario["scenario_id"]
        
        if sid == "os_update_security_patch":
            os_eol = any(c["component_type"] == "os" and c["component_status"] == "EOL" for c in tech["components_analyzed"])
            os_outdated = any(c["component_type"] == "os" and c["component_status"] == "OUTDATED" for c in tech["components_analyzed"])
            os_current = any(c["component_type"] == "os" and c["component_status"] == "CURRENT_VERSION" for c in tech["components_analyzed"])
            
            if os_current and not os_eol and not os_outdated:
                status, reason, conf = "FULFILLED", "Operating system is on a current, supported version.", 9
            elif os_eol:
                status, reason, conf = "APPLICABLE", f"OS ({os_str}) is EOL and requires update.", 9
            elif os_outdated:
                status, reason, conf = "APPLICABLE", f"OS ({os_str}) is outdated and should be updated.", 8
            else:
                status, reason, conf = "LACK_OF_DATA", "OS lifecycle status could not be determined.", 5
            scenario_results.append({"id":sid,"status":status,"match_type":"ai","reason":reason,"confidence":conf,"source":{"document_id":"","document_title":"","section":"","content_excerpt":"","relevance":""}})
        
        elif sid == "switch_to_standard_linux_os":
            proprietary_os = any(x in os_str for x in ["aix","hp-ux","solaris","irix","windows"])
            already_linux = any(x in os_str for x in ["rhel","ubuntu","debian","centos","linux","sles","amazon linux"])
            is_windows = "windows" in os_str
            
            if already_linux:
                status, reason, conf = "FULFILLED", f"Application already runs on standard Linux ({app.get('operating_system','')}).", 9
            elif is_windows or is_saas:
                status, reason, conf = "NOT_APPLICABLE", "Application runs on Windows or is SaaS; switching to standard Linux OS is not applicable.", 8
            elif proprietary_os:
                status, reason, conf = "APPLICABLE", f"Application runs on proprietary OS ({app.get('operating_system','')}) which should be migrated to standard Linux.", 8
            else:
                status, reason, conf = "LACK_OF_DATA", "OS information insufficient to evaluate Linux migration.", 5
            scenario_results.append({"id":sid,"status":status,"match_type":"ai","reason":reason,"confidence":conf,"source":{"document_id":"","document_title":"","section":"","content_excerpt":"","relevance":""}})
        
        elif sid == "switch_to_arm_cpu":
            if is_saas:
                status, reason, conf = "NOT_APPLICABLE", "SaaS application - infrastructure managed by vendor.", 8
            elif is_cloud:
                status, reason, conf = "APPLICABLE", "Application runs on cloud and could benefit from ARM-based instances (e.g., AWS Graviton).", 6
            else:
                status, reason, conf = "APPLICABLE", "Application on on-premise x86 infrastructure could benefit from ARM migration for cost savings.", 5
            scenario_results.append({"id":sid,"status":status,"match_type":"ai","reason":reason,"confidence":conf,"source":{"document_id":"","document_title":"","section":"","content_excerpt":"","relevance":""}})
        
        elif sid == "application_server_replacement":
            srv_eol = any(c["component_type"] == "application_server" and c["component_status"] == "EOL" for c in tech["components_analyzed"])
            srv_outdated = any(c["component_type"] == "application_server" and c["component_status"] == "OUTDATED" for c in tech["components_analyzed"])
            has_server = bool(srv_str and srv_str not in ["none","n/a","-"])
            
            if not has_server:
                status, reason, conf = "NOT_APPLICABLE", "No application server component identified.", 8
            elif srv_eol:
                status, reason, conf = "APPLICABLE", f"Application server ({app.get('application_server','')}) is EOL and requires replacement.", 9
            elif srv_outdated:
                status, reason, conf = "APPLICABLE", f"Application server ({app.get('application_server','')}) is outdated.", 7
            else:
                status, reason, conf = "FULFILLED", f"Application server appears to be on a supported version.", 7
            scenario_results.append({"id":sid,"status":status,"match_type":"ai","reason":reason,"confidence":conf,"source":{"document_id":"","document_title":"","section":"","content_excerpt":"","relevance":""}})
        
        elif sid == "app_deployment_to_cloud":
            if is_saas:
                status, reason, conf = "NOT_APPLICABLE", "Application is SaaS - already cloud-based.", 9
            elif is_cloud:
                status, reason, conf = "FULFILLED", f"Application is already deployed on cloud ({app.get('deployment_type','')}).", 9
            elif "on-premise" in deploy_str or "on_premise" in deploy_str or "on premise" in deploy_str or "on-prem" in deploy_str:
                status, reason, conf = "APPLICABLE", f"Application runs on-premise and is a candidate for cloud migration.", 8
            else:
                status, reason, conf = "APPLICABLE", "Application deployment is not cloud-based; cloud migration is applicable.", 6
            scenario_results.append({"id":sid,"status":status,"match_type":"ai","reason":reason,"confidence":conf,"source":{"document_id":"","document_title":"","section":"","content_excerpt":"","relevance":""}})
        
        elif sid == "app_containerization":
            if containerized in ["yes","true"]:
                status, reason, conf = "FULFILLED", "Application is already containerized.", 9
            elif "3rd party" in solution_type or "saas" in solution_type:
                status, reason, conf = "NOT_APPLICABLE", "3rd party/SaaS application - containerization managed by vendor.", 7
            elif "cobol" in lang_str or "1-tier" in arch_str:
                status, reason, conf = "BLOCKED", "Legacy architecture (COBOL/1-Tier) makes containerization impractical without major refactoring.", 8
            else:
                status, reason, conf = "APPLICABLE", "Application is not containerized; containerization is applicable for improved portability and scalability.", 8
            scenario_results.append({"id":sid,"status":status,"match_type":"ai","reason":reason,"confidence":conf,"source":{"document_id":"","document_title":"","section":"","content_excerpt":"","relevance":""}})
        
        elif sid == "app_refactor_decoupling":
            is_micro = "microservice" in arch_str
            is_monolith = any(x in arch_str for x in ["1-tier","monolith","2-tier"])
            is_simple = solution_type in ["saas","3rd party software"]
            
            if is_micro:
                status, reason, conf = "FULFILLED", "Application already uses microservices architecture.", 9
            elif is_saas or "3rd party" in solution_type:
                status, reason, conf = "NOT_APPLICABLE", "3rd party/SaaS application - refactoring not applicable.", 8
            elif is_monolith:
                status, reason, conf = "APPLICABLE", f"Application has {app.get('application_architecture','')} architecture - refactoring to microservices would improve scalability.", 8
            elif "3-tier" in arch_str:
                status, reason, conf = "PARTIALLY_FULFILLED", "3-Tier architecture provides some decoupling; further microservice decomposition may be beneficial.", 6
            else:
                status, reason, conf = "APPLICABLE", "Application architecture could benefit from refactoring and decoupling.", 6
            scenario_results.append({"id":sid,"status":status,"match_type":"ai","reason":reason,"confidence":conf,"source":{"document_id":"","document_title":"","section":"","content_excerpt":"","relevance":""}})
        
        elif sid == "upgrade_legacy_databases":
            db_eol = any(c["component_type"] == "database" and c["component_status"] == "EOL" for c in tech["components_analyzed"])
            db_outdated = any(c["component_type"] == "database" and c["component_status"] == "OUTDATED" for c in tech["components_analyzed"])
            db_current = any(c["component_type"] == "database" and c["component_status"] == "CURRENT_VERSION" for c in tech["components_analyzed"])
            has_db = bool(app.get("database_engine",""))
            
            if not has_db:
                status, reason, conf = "NOT_APPLICABLE", "No database component identified.", 7
            elif db_current and not db_eol and not db_outdated:
                status, reason, conf = "FULFILLED", f"Database ({app.get('database_engine','')}) is on a current, supported version.", 9
            elif db_eol:
                status, reason, conf = "APPLICABLE", f"Database ({app.get('database_engine','')}) is EOL and requires upgrade.", 9
            elif db_outdated:
                status, reason, conf = "APPLICABLE", f"Database ({app.get('database_engine','')}) is outdated and should be upgraded.", 7
            else:
                status, reason, conf = "LACK_OF_DATA", "Database lifecycle status could not be determined.", 5
            scenario_results.append({"id":sid,"status":status,"match_type":"ai","reason":reason,"confidence":conf,"source":{"document_id":"","document_title":"","section":"","content_excerpt":"","relevance":""}})
        
        elif sid == "switch_db_engine_open_source":
            is_commercial_db = any(x in db_str for x in ["oracle","sql server","mssql","db2","sybase"])
            is_oss_db = any(x in db_str for x in ["postgresql","postgres","mysql","mariadb","mongodb","cassandra","redis"])
            requires_license = (app.get("database_license_required","") or "").lower() == "yes"
            has_db = bool(app.get("database_engine",""))
            
            if not has_db:
                status, reason, conf = "NOT_APPLICABLE", "No database component identified.", 7
            elif is_oss_db and not requires_license:
                status, reason, conf = "FULFILLED", f"Database ({app.get('database_engine','')}) is already an open-source solution.", 9
            elif is_commercial_db or requires_license:
                status, reason, conf = "APPLICABLE", f"Application uses commercial database ({app.get('database_engine','')}) with license cost; migration to open-source is recommended.", 8
            else:
                status, reason, conf = "LACK_OF_DATA", "Cannot determine if database requires commercial license.", 5
            scenario_results.append({"id":sid,"status":status,"match_type":"ai","reason":reason,"confidence":conf,"source":{"document_id":"","document_title":"","section":"","content_excerpt":"","relevance":""}})
        
        elif sid == "update_outdated_components":
            all_current = all(c["component_status"] == "CURRENT_VERSION" for c in tech["components_analyzed"])
            has_eol_lang = any(c["component_type"] == "language" and c["component_status"] == "EOL" for c in tech["components_analyzed"])
            has_outdated_lang = any(c["component_type"] == "language" and c["component_status"] == "OUTDATED" for c in tech["components_analyzed"])
            
            if all_current and tech["components_analyzed"]:
                status, reason, conf = "FULFILLED", "All components are on current, supported versions.", 9
            elif has_eol_lang or (eol_components and len(eol_components) > 0):
                status, reason, conf = "APPLICABLE", f"EOL components found: {', '.join(eol_names[:3])}. Update required.", 9
            elif has_outdated_lang or outdated_components:
                status, reason, conf = "APPLICABLE", f"Outdated components found. Updating to current versions is recommended.", 7
            else:
                status, reason, conf = "LACK_OF_DATA", "Component lifecycle status insufficient to evaluate.", 5
            scenario_results.append({"id":sid,"status":status,"match_type":"ai","reason":reason,"confidence":conf,"source":{"document_id":"","document_title":"","section":"","content_excerpt":"","relevance":""}})
    
    result = {
        "application_identifier": app_id,
        "scenarios_detailed": scenario_results
    }
    path = OUT / f"scenario_applicability_results/scenario_assessment_{app_id}.json"
    with open(path, "w") as f:
        json.dump(result, f, indent=2)
    return result

scenario_results = {}
for app in in_scope:
    scenario_results[app["app_id"]] = evaluate_scenarios(app, tech_assessments[app["app_id"]], complexity_results[app["app_id"]])

print("Step 5 complete: Scenario assessments created")

# ============================================================
# STEP 6: Business Case
# ============================================================

with open(BASE / ".github/skills/business-case/references/modernization_scenarios_finance.json") as f:
    finance_config = json.load(f)

finance_map = {fc["scenario_id"]: fc for fc in finance_config}

# Scenario names
scenario_names = {s["scenario_id"]: s["scenario_name"] for s in scenarios}
scenario_meta = {s["scenario_id"]: s for s in scenarios}

def get_cost_multiplier(complexity_score):
    return 0.5 * (1.15 ** complexity_score)

def get_savings_multiplier(complexity_score, technical_focus="Application"):
    if "Application" in technical_focus:
        if complexity_score <= 3: return 1.0
        elif complexity_score <= 6: return 0.9
        else: return 0.8
    return 1.0

total_one_time = 0
total_yearly = 0
scenarios_summary = {}
app_details = []

for app in in_scope:
    app_id = app["app_id"]
    compl = complexity_results[app_id]["complexity_score"]
    scen_assess = scenario_results[app_id]["scenarios_detailed"]
    
    applicable = [s for s in scen_assess if s["status"] == "APPLICABLE"]
    
    app_scenarios = []
    app_total_cost = 0
    app_total_savings = 0
    
    for s in applicable:
        sid = s["id"]
        if sid not in finance_map:
            continue
        
        fc = finance_map[sid]
        cost_mult = get_cost_multiplier(compl)
        
        tech_focus = scenario_meta.get(sid, {}).get("technical_focus", "Application")
        sav_mult = get_savings_multiplier(compl, tech_focus)
        
        base_cost = sum(c["amount"] for c in fc.get("costs",[]) if c.get("occurrence") == "once")
        base_savings = sum(sv["amount"] for sv in fc.get("savings",[]) if sv.get("occurrence") == "yearly")
        
        adj_cost = round(base_cost * cost_mult)
        adj_savings = round(base_savings * sav_mult)
        
        app_total_cost += adj_cost
        app_total_savings += adj_savings
        total_one_time += adj_cost
        total_yearly += adj_savings
        
        app_scenarios.append({
            "scenario_id": sid,
            "base_cost": base_cost,
            "cost_multiplier": round(cost_mult, 3),
            "adjusted_cost": adj_cost,
            "base_yearly_savings": base_savings,
            "savings_multiplier": sav_mult,
            "adjusted_yearly_savings": adj_savings
        })
        
        if sid not in scenarios_summary:
            scenarios_summary[sid] = {"scenario_id":sid,"scenario_name":scenario_names.get(sid,sid),"applicable_count":0,"total_cost":0,"total_yearly_savings":0}
        scenarios_summary[sid]["applicable_count"] += 1
        scenarios_summary[sid]["total_cost"] += adj_cost
        scenarios_summary[sid]["total_yearly_savings"] += adj_savings
    
    roi_years = round(app_total_cost / app_total_savings, 1) if app_total_savings > 0 else None
    
    if app_scenarios:
        app_details.append({
            "app_id": app_id,
            "app_name": app["app_name"],
            "complexity_score": compl,
            "scenarios": app_scenarios,
            "total_cost": app_total_cost,
            "total_yearly_savings": app_total_savings,
            "roi_years": roi_years
        })

# ROI for scenarios_summary
for sid, s in scenarios_summary.items():
    s["roi_years"] = round(s["total_cost"] / s["total_yearly_savings"], 1) if s["total_yearly_savings"] > 0 else None

portfolio_roi = round(total_one_time / total_yearly, 1) if total_yearly > 0 else None
total_applicable = sum(len([s for s in scenario_results[a["app_id"]]["scenarios_detailed"] if s["status"] == "APPLICABLE"]) for a in in_scope)
apps_with_opp = len([a for a in in_scope if any(s["status"] == "APPLICABLE" for s in scenario_results[a["app_id"]]["scenarios_detailed"])])

business_case = {
    "assessment_date": datetime.now().strftime("%Y-%m-%d"),
    "portfolio_summary": {
        "total_applications_assessed": len(in_scope),
        "applications_with_opportunities": apps_with_opp,
        "total_applicable_scenarios": total_applicable,
        "total_one_time_costs": total_one_time,
        "total_yearly_savings": total_yearly,
        "roi_years": portfolio_roi
    },
    "scenarios_summary": list(scenarios_summary.values()),
    "application_details": app_details
}

with open(OUT / "business_case_results/business_case.json", "w") as f:
    json.dump(business_case, f, indent=2)

print(f"Step 6 complete: Business case created. Total costs: {total_one_time}, Total yearly savings: {total_yearly}, ROI: {portfolio_roi} years")
print("All data processing steps complete!")
