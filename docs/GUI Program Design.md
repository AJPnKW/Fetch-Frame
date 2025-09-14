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
