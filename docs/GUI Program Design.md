# Version: 1.0.0  
# Last Updated: 2025-09-14  
# Author: Andrew  
# Section: GUI Program Design

## 1. Layout Overview

The GUI is built with PyQt5 and structured into three main panels:

- **Left**: YAML Inbox (list of available update.yaml files)
- **Center**: Tabbed view (Preview, Diff, Settings)
- **Right**: Workflow buttons (Setup, Update, Config)

## 2. Workflow Buttons

| Group              | Buttons |
|--------------------|---------|
| First-Time Setup   | Select Project, Initialize Structure, Create Index, Init Settings |
| Update Workflow    | Import YAML, Dry Run, Apply Update, Undo |
| Configuration      | Edit Settings, Refresh YAML List |

## 3. Tabbed Center Panel

- **YAML Preview**: Shows parsed YAML content
- **Diff View**: Placeholder for future diff engine
- **Settings Editor**: Editable view of `settings.yaml`

## 4. Event Flow

```text
User selects YAML → Preview → Dry Run → Apply → Backup → Archive → Regenerate Index

## 5. PyQt5 Components
	Component	Role
	QListWidget	YAML file list
	QTextEdit	Preview, logs, settings
	QPushButton	Action triggers
	QTabWidget	Center panel tabs
	QFileDialog	File/folder selection

## 6. Related Files


## 🖥️ GUI Program Design

### Features

| Feature | Description |
|--------|-------------|
| YAML List | Shows available and applied YAML files |
| Preview | Displays contents of selected YAML |
| Apply | Button to process selected YAML |
| Log Viewer | Shows history of applied updates |
| Auto Index | Regenerates `index.md` after update |
| Backup | Archives previous `.md` versions |

### Layout

- **Left Panel**: YAML file list (available + applied)
- **Center Panel**: YAML preview
- **Right Panel**: Action buttons (Apply, View Log, Refresh Index)
- **Bottom Panel**: Persistent log viewer

### Tech Stack

| Component | Choice |
|----------|--------|
| Language | Python |
| GUI      | Tkinter or PyQt |
| File Ops | `os`, `shutil`, `yaml`, `markdown` |
| Logging  | `logging` module with persistent file

---

## 🚀 Launcher & .bat File

### launcher.py

```python
import subprocess
subprocess.run(["python", "gui/update_tool.py"])
