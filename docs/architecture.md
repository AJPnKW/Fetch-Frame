# Version: 1.0.0  
# Last Updated: 2025-09-14  
# Author: Andrew  
# Section: System Architecture

## 1. Overview

FetchFrame is a modular documentation and update automation tool designed to streamline YAML-driven content updates across markdown files. The architecture prioritizes clarity, traceability, and extensibility.

## 2. Component Breakdown

| Component        | Description |
|------------------|-------------|
| GUI Frontend     | Built with PyQt5, provides workflow-aligned interface for YAML import, preview, dry-run, and apply |
| YAML Processor   | Parses update.yaml files, applies changes to `.md` files, manages backups and history |
| Config Manager   | Loads and saves `settings.yaml`, resolves project paths and flags |
| Index Generator  | Regenerates `index.md` and `index.html` based on current `.md` files |
| Undo Engine      | Restores previous `.md` states using timestamped backups |

## 3. Folder Structure

```text
project/
+-- docs/
¦   +-- *.md
¦   +-- yaml-history/
¦   +-- index.md / index.html
+-- yaml_update_tool/
¦   +-- config/
¦   +-- logs/
¦   +-- backups/
