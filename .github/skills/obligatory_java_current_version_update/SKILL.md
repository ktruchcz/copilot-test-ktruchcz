---
name: obligatory_java_current_version_update
description: Keep Java source/target/toolchain, CI setup, and docs aligned to the repository's current approved Java version.
---

# Obligatory Java Current Version Update

When Java version requirements are updated:
- update Maven/Gradle Java source/target/release configuration
- update CI Java setup version
- update documentation and user-facing version references
- ensure tests pass on the updated Java version
