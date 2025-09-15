
---

## 📁 `user-guide.md`

```markdown
# Version: 1.0.0  
# Last Updated: 2025-09-14  
# Author: Andrew  
# Section: User Guide

## 1. Launching the Tool

```bash
python yaml_update_tool/update_tool_gui.py


##2. First-Time Setup

    Select your project folder
    Click “Initialize Project Structure”
    Create index.md and index.html
    Initialize settings.yaml

## 3. Update Workflow
Step	Action
Import YAML	Load
file
Preview	View parsed content
Dry Run	Simulate update
Apply	Write changes, backup originals
Undo	Restore from backup

## 4. Troubleshooting
Issue	Solution
GUI doesn’t launch	Check PyQt5 install and final lines in script
YAML not listed	Ensure it’s in /docs and not in /yaml-history
Undo not working	Check /backups folder for latest file

## 5. Related Files
