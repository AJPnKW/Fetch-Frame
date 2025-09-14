# yaml_update-tool-ui-design.md

## 1. Purpose
Modular GUI tool to apply YAML-based updates to markdown documentation across any project.

## 2. Features
- Select or change target `/docs` folder
- Preview and apply `update.yaml` files
- Log history of applied updates
- Regenerate `index.md` automatically
- First-time setup button to create folders and config
- Config file to store default paths

## 3. Folder Roles
| Folder         | Purpose |
|----------------|---------|
| `/yaml-inbox`  | Holds new YAML files to be processed |
| `/yaml-history`| Stores applied YAML files |
| `/logs`        | Persistent update logs |
| `/backups`     | Previous versions of `.md` files |
| `/config`      | Stores `settings.yaml` with default paths |

## 4. GUI Layout
| Panel | Function |
|-------|----------|
| Left  | List of YAML files in `/yaml-inbox` |
| Center| Preview selected YAML |
| Right | Buttons: Apply, Refresh, Setup |
| Bottom| Log viewer |

## 5. First-Time Setup
- Creates all required folders
- Initializes `settings.yaml`
- Creates empty `index.md` in `/docs` if missing
