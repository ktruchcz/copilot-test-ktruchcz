---
name: obligatory_java_current_version_update
description: Keep Java source/target/toolchain, CI setup, and docs aligned to the repository's current approved Java version.
---

# Obligatory Java Current Version Update

When Java version requirements are updated:
- update Maven/Gradle Java source/target/release configuration (`pom.xml` / `build.gradle`)
- update CI Java setup version (e.g., `actions/setup-java` `java-version` field in `.github/workflows/`)
- update architecture documentation and user-facing version references (e.g., Arc42 constraints, technology decision tables, deployment requirements)
- update ADRs that reference old build/test/version decisions to reflect superseded status
- update code metrics sections to reflect actual lines-of-code, methods, and test coverage
- update risk registers and technical debt backlogs to mark mitigated/resolved items
- ensure tests pass on the updated Java version
