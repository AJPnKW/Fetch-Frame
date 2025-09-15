# Version: 1.0.0  
# Last Updated: 2025-09-14  
# Author: Andrew  
# Section: Developer Guide

## 1. Onboarding Checklist

- [ ] Clone the FetchFrame repository
- [ ] Install Python 3.11+
- [ ] Run `pip install -r requirements.txt`
- [ ] Launch GUI via `update_tool_gui.py`
- [ ] Review `standards.md` and `architecture.md`

## 2. Environment Setup

| Tool/Library | Purpose |
|--------------|---------|
| PyQt5        | GUI framework |
| PyYAML       | YAML parsing |
| shutil/os    | File operations |
| datetime     | Timestamping updates |

## 3. Folder Conventions

```text
project/
+-- docs/                  # Markdown files
¦   +-- yaml-history/      # Applied YAMLs
+-- yaml_update_tool/      # Tool logic
¦   +-- config/            # settings.yaml
¦   +-- logs/              # update.log
¦   +-- backups/           # .md backups

## 4. Coding Standards

    Use 4 spaces for indentation
    Follow semantic versioning in YAML
    Use descriptive commit messages:
	[gui] added index.html generation to create_index()

## 5.Pull Request Flow

    Fork and branch from main
    Submit PR with clear title and description
    Link affected .md files and YAMLs
    Tag reviewers and assign milestone

## 6. Related Files

