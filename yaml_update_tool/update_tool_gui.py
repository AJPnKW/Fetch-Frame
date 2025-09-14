# Version: 1.0.0
# Last Updated: 2025-09-14
# Author: Andrew + Copilot
# Section: GUI Update Tool

import os
import yaml
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

DOCS_DIR = "docs"
HISTORY_DIR = os.path.join(DOCS_DIR, "yaml-history")
LOG_FILE = os.path.join("logs", "update.log")

def list_yaml_files():
    all_files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".yaml")]
    applied = os.listdir(HISTORY_DIR) if os.path.exists(HISTORY_DIR) else []
    return [f for f in all_files if f not in applied], applied

def load_yaml(filename):
    with open(os.path.join(DOCS_DIR, filename), "r") as f:
        return yaml.safe_load(f)

def apply_yaml(filename, data):
    for file in data.get("updated_files", []):
        path = os.path.join(DOCS_DIR, file)
        if os.path.exists(path):
            shutil.copy(path, os.path.join("backups", f"{file}.{datetime.now().strftime('%Y%m%d%H%M')}"))
        with open(path, "a") as f:
            for change in data["changes"].get(file, []):
                f.write(f"\n<!-- Update: {change} -->\n")
    shutil.move(os.path.join(DOCS_DIR, filename), os.path.join(HISTORY_DIR, filename))
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now().isoformat()} - Applied {filename}\n")
    regenerate_index()

def regenerate_index():
    md_files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".md")]
    with open(os.path.join(DOCS_DIR, "index.md"), "w") as index:
        index.write("# index.md\n\n## Documentation Files\n")
        for f in sorted(md_files):
            index.write(f"- [{f}]({f})\n")

class UpdateToolGUI:
    def __init__(self, root):
        root.title("YAML Update Tool")
        root.geometry("800x600")

        self.available_list = tk.Listbox(root, width=40)
        self.available_list.pack(side="left", fill="y", padx=10, pady=10)

        self.preview = tk.Text(root, wrap="word")
        self.preview.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.apply_button = tk.Button(root, text="Apply Selected YAML", command=self.apply_selected)
        self.apply_button.pack(side="bottom", pady=10)

        self.refresh_button = tk.Button(root, text="Refresh List", command=self.refresh)
        self.refresh_button.pack(side="bottom")

        self.refresh()

    def refresh(self):
        self.available_list.delete(0, tk.END)
        available, _ = list_yaml_files()
        for f in available:
            self.available_list.insert(tk.END, f)
        self.available_list.bind("<<ListboxSelect>>", self.preview_yaml)

    def preview_yaml(self, event):
        selection = self.available_list.curselection()
        if selection:
            filename = self.available_list.get(selection[0])
            data = load_yaml(filename)
            self.preview.delete("1.0", tk.END)
            self.preview.insert(tk.END, yaml.dump(data, sort_keys=False))

    def apply_selected(self):
        selection = self.available_list.curselection()
        if selection:
            filename = self.available_list.get(selection[0])
            data = load_yaml(filename)
            apply_yaml(filename, data)
            messagebox.showinfo("Update Applied", f"{filename} has been processed.")
            self.refresh()

if __name__ == "__main__":
    os.makedirs(HISTORY_DIR, exist_ok=True)
    os.makedirs("backups", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    root = tk.Tk()
    app = UpdateToolGUI(root)
    root.mainloop()
