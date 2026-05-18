---
name: excel-ingestion
description: >
  Reads Excel files containing application portfolio data, determines column semantics
  without assuming fixed column names, and extracts structured JSON records per application.
  Use when ingesting Excel/XLSX files with application landscape data, mapping spreadsheet
  columns to application attributes, or extracting application metadata from tabular data.
---

# Excel Ingestion

Read an Excel file where each row describes one application. Column names are NOT fixed —
determine their meaning through semantic analysis. Output must follow the
`example_output/applications/` and `example_output/schemas/` structure.

## Extraction script

A ready-made Python script is bundled at [scripts/extract_applications.py](scripts/extract_applications.py).
Run it to extract applications:

```bash
python .github/skills/excel-ingestion/scripts/extract_applications.py <excel_file> \
  --output-dir output/applications/internal_app_model
```

The script:
- Reads any Excel file with one application per row
- Maps column headers to canonical field names via regex patterns (supports English and German headers)
- Auto-detects list values (comma/semicolon-separated) while preserving free-text fields
- Writes **one JSON file per application** to `output/applications/internal_app_model/`
- Writes overview and schema artifacts needed by downstream steps

If the script does not cover a particular Excel format, you can also do the ingestion manually
following the process below.

## Manual process (when the script is insufficient)

### 1. Read the Excel file

```python
import openpyxl

wb = openpyxl.load_workbook("path/to/file.xlsx", data_only=True)
ws = wb.active
headers = [cell.value for cell in ws[1]]
rows = [[cell.value for cell in row] for row in ws.iter_rows(min_row=2)]
```

### 2. Analyze column semantics

For each column header, classify it into one of these categories:

| Category | Examples of column names | Maps to field |
|----------|------------------------|---------------|
| Application ID | `ID`, `App-ID`, `Application Number`, `#` | `app_id` |
| Application Name | `Name`, `Application`, `App Name`, `System` | `app_name` |
| Description | `Description`, `Purpose`, `Function`, `Desc` | `app_description` |
| Solution Type | `Solution type`, `App Type`, `Software Type` | `solution_type` |
| Programming Language | `Language`, `Tech`, `Dev Language` | `programming_language` |
| Framework | `Framework`, `Platform`, `Runtime` | `framework` |
| Application Server | `App Server`, `Server Type`, `Middleware` | `application_server` |
| Application Architecture | `Architecture`, `App Architecture` | `application_architecture` |
| Database Engine | `DB`, `Database`, `DBMS`, `db_engine` | `database_engine` |
| Operating System | `OS`, `Operating System`, `Platform OS` | `operating_system` |
| Server Instances | `Physical servers`, `Server instances` | `server_instances` |
| Environment Type | `Deployment type`, `Hosting`, `Environment` | `deployment_type` |
| Environment Count | `Number of environments` | `environment_count` |
| Business Criticality | `Criticality`, `Priority`, `Business Impact` | `business_criticality` |
| Number of Users | `Users`, `# Users`, `User Count` | `user_count` |
| External Interface Count | `External interfaces`, `Interfaces` | `external_interface_count` |
| Is Containerized | `Containerized`, `Docker`, `Kubernetes` | `is_containerized` |
| CI/CD Present | `CI_CD`, `Pipeline`, `Continuous` | `ci_cd_present` |
| Decommission Date | `Retire`, `EOL`, `Decommission`, `Sunset` | `decommission_date` |
| Dependencies | `Dependencies`, `Depends On`, `Upstream` | `dependencies` |
| Owner / Team | `Owner`, `Team`, `Responsible`, `Contact` | `owner` |
| Business Unit | `Business unit`, `Department` | `business_unit` |
| Data Classification | `Data classification`, `Classification` | `data_classification` |
| Database Storage | `DB storage`, `Storage in GB` | `database_storage_gb` |
| Logging Solution | `Logging`, `Log solution` | `logging_solution` |
| Monitoring Tool | `Monitoring`, `Monitor tool` | `monitoring_tool` |

**Rules for classification:**
- Match by semantic meaning, not exact string. Column `Betriebssystem` (German) maps to `operating_system`.
- If the language is not English, translate the header to understand it.
- If a column does not fit any category, store it as `additional_attributes.<original_header>`.
- A single column may contain composite data (e.g., "Java 11 / Spring Boot 3"). Parse it into separate fields.
- If no clear Application ID column exists, generate sequential IDs: `APP_001`, `APP_002`, ...

### 3. Build and save application records

For each row, produce these JSON files:

- `output/applications/internal_app_model/internal_app_model_application_<app_id>.json`
- `output/applications/consolidated_schema/consolidated_schema_application_<app_id>.json`

The internal model file should stay minimal and stable:

```json
{
  "app_id": "app001",
  "app_name": "ERPApp-001",
  "app_description": "Core ERP system handling financial transactions",
  "retiring_at": ""
}
```

The consolidated schema file should preserve normalized application fields used by the pipeline:

```json
{
  "app_id": "app001",
  "name": "ERPApp-001",
  "description": "Core ERP system handling financial transactions",
  "Solution type": "Custom made",
  "criticality": "High",
  "Application status": "Production",
  "Decomission date": "2027",
  "Deployment type": "On-Premise",
  "data classification": "Confidential",
  "business unit": "Finance",
  "number of users": "350",
  "Operating system": "AIX 7.2",
  "programming language": "COBOL-2014",
  "Application Server type": "None",
  "Application Architecture": "1-Tier",
  "Application is containerized": "No",
  "Number of environments": "2",
  "Physical servers instances": "sv01, sv02",
  "external interfaces": "5",
  "db_engine": "Oracle 19c"
}
```

### 4. Save metadata

Write overview metadata to `output/applications/consolidated_applications_overview.json`:

```json
{
  "analysis_id": "03f967118873a7e05edc457ccbf494e4",
  "applications_overview": {
    "total_applications": 30,
    "valid_applications": 30,
    "invalid_applications": 0,
    "application_id_field": "app_id",
    "application_name_field": "name",
    "application_description_field": "description",
    "invalid_applications_list": []
  },
  "timestamp": "2026-04-22T13:13:47.709047"
}
```

Also write schema exports under `output/schemas/`:

- `consolidated_application_schema.json`
- `original_application_schema_from_<source>.json`
- `original_unified_schema_from_validated_output.json`
- `original_relationship_model_schema_from_validated_output.json`

## Output structure

```
output/
├── applications/
│   ├── consolidated_applications_overview.json
│   ├── consolidated_schema/
│   │   ├── consolidated_schema_application_app001.json
│   │   └── ...
│   └── internal_app_model/
│       ├── apps_metadata.json
│       ├── internal_app_model_application_app001.json
│       └── ...
└── schemas/
    ├── consolidated_application_schema.json
    ├── original_application_schema_from_<source>.json
    ├── original_unified_schema_from_validated_output.json
    └── original_relationship_model_schema_from_validated_output.json
```

## Edge cases

- **Empty rows**: Skip rows where all cells are empty.
- **Merged cells**: Treat merged cells as belonging to the first row/column of the merge.
- **Multiple sheets**: If the workbook has multiple sheets, analyze the first sheet unless the user specifies otherwise.
- **Missing mandatory fields**: If `app_name` cannot be determined for a row, use `app_id` as fallback.
- **Numeric strings**: Values like `"14.0"` in a version column should remain as strings, not become floats.
- **Free-text fields**: Description, name, and similar fields must NOT be split into lists even if they contain commas.
