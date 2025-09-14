## 📘 Updated: yaml_standards+requirements.md

```markdown
# yaml_standards+requirements.md

## 1. Purpose

Defines the structure, formatting, and usage of `update.yaml` files used to apply changes to `.md` documentation files. Ensures updates are consistent, traceable, and aligned with project standards.

---

## 2. YAML File Format

```yaml
version: 1.0.0
timestamp: 2025-09-14T16:00:00-04:00
updated_files:
  - standards.md
changes:
  standards.md:
    - Added AI Response Standards
    - Merged previous content
    - Structured with tables and bullets
```

---

## 3. Naming Convention

| Element | Format |
|--------|--------|
| File Name | `update_YYYY-MM-DD_HHMM_version-X.Y.Z.yaml` |
| Example   | `update_2025-09-14_1600_version-1.0.0.yaml` |

---

## 4. Processing Rules

- Only one YAML file processed at a time
- Applied YAMLs moved to `/docs/yaml-history/`
- Log entry created in `/logs/update.log`
- `index.md` regenerated after each update
- Previous `.md` versions backed up to `/backups/docs/YYYY-MM-DD/`

---

## 5. Markdown Update Logic

| Step | Action |
|------|--------|
| 1 | Parse `updated_files` and `changes` |
| 2 | Apply changes to each `.md` file |
| 3 | Backup original files |
| 4 | Move YAML to history folder |
| 5 | Log update |
| 6 | Regenerate `index.md` |

---

## 6. Markdown Formatting Standards

### 6.1 Header Structure

```markdown
# File Title

## 1. Overview
## 2. Section Title
### 2.1 Subsection
```

### 6.2 Required Header Block

```markdown
# Version: 1.0.0
# Last Updated: YYYY-MM-DD
# Author: Name
# Section: [Module/Feature Name]
```

### 6.3 Content Rules

- Use numbered sections
- Use tables for structured data
- Use bullet points for clarity
- Avoid fluff, repetition, and nested instructions
- Use consistent tone: direct, functional, user-focused

---

## 7. Templates for Common Files

### 7.1 changelog.md

```markdown
# changelog.md

## Version History

| Version | Date       | Changes Summary |
|---------|------------|------------------|
| 1.0.0   | 2025-09-14 | Initial release |
```

### 7.2 decision_log.md

```markdown
# decision_log.md

## 1. Architecture Decisions

| Date       | Decision | Rationale | Impact |
|------------|----------|-----------|--------|
| 2025-09-14 | Use SQLite | Lightweight, portable | Simplifies setup |
```

### 7.3 glossary.md

```markdown
# glossary.md

| Term       | Definition |
|------------|------------|
| Dry-run    | Simulated execution without writes |
| NDJSON     | Newline-delimited JSON format |
```

---

## 8. AI Prompt Template - 🧠 Elevated Prompt to Generate a YAML Update File

```text
Generate an update.yaml file for a documentation update process.

Use the standards defined in:
- standards.md
- yaml_standards+requirements.md

The YAML should:
- Include a semantic version number and timestamp
- List only the `.md` files that need updates based on current project complexity
- Summarize the changes for each file in clear bullet points
- Follow the naming convention: update_YYYY-MM-DD_HHMM_version-X.Y.Z.yaml

Reference files that may be included:
- binder_index.md
- changelog.md
- decision_log.md
- folder_structure.md
- glossary.md
- hld.md
- open_questions.md
- progress_tracker.md
- Project_Binder.md
- standards.md

Only include files that are relevant to the current phase of the project. If the project is small or early-stage, include fewer files. If the project is complex or mature, include more.

Ensure the YAML is formatted for use in an automated GUI tool that:
- Applies updates to `.md` files
- Logs the update
- Archives previous versions
- Regenerates index.md

Do not include explanations or summaries. Just generate the YAML file content.

```

---
