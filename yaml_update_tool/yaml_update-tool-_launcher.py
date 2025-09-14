# Version: 1.0.0
# Last Updated: 2025-09-14
# Author: Andrew + Copilot
# Section: YAML GUI Launcher

import subprocess
import os

def launch_yaml_gui():
    gui_path = os.path.join("yaml_update_tool", "update_tool_gui.py")
    if os.path.exists(gui_path):
        subprocess.run(["python", gui_path])
    else:
        print("GUI tool not found at:", gui_path)

if __name__ == "__main__":
    launch_yaml_gui()
