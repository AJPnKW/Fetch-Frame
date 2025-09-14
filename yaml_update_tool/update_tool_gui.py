# Version: 1.1.1
# Last Updated: 2025-09-14
# Author: Andrew + Copilot
# Section: YAML Update Tool GUI (Refined)

import os
import yaml
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

CONFIG_PATH = "yaml_update_tool/config/settings.yaml"
DEFAULT_DOCS_DIR = "docs"

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)
    return {
        "default_docs_path": DEFAULT_DOCS_DIR,
        "backup_enabled": True,
        "index_autogen": True,
        "log_level": "info"
    }

config = load_config()
DOCS_DIR = config["default_docs_path"]
HISTORY_DIR = os.path.join(DOCS_DIR, "yaml-history")
LOG_FILE = os.path.join("logs", "update.log")
BACKUP_DIR = "backups"

def list_yaml_files():
    all_files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".yaml")]
    applied = os.listdir(HISTORY_DIR) if os.path.exists(HISTORY_DIR) else []
    return [f for f in all_files if f not in applied], applied

def load_yaml(filename):
    with open(os.path.join(DOCS_DIR, filename), "r") as f:
        return yaml.safe_load(f)

def apply_yaml(filename, data, dry_run=False):
    for file in data.get("updated_files", []):
        path = os.path.join(DOCS_DIR, file)
        if os.path.exists(path):
            if config["backup_enabled"]:
                os.makedirs(BACKUP_DIR, exist_ok=True)
                shutil.copy(path, os.path.join(BACKUP_DIR, f"{file}.{datetime.now().strftime('%Y%m%d%H%M')}"))
            if not dry_run:
                with open(path, "a") as f:
                    for change in data["changes"].get(file, []):
                        f.write(f"\n<!-- Update: {change} -->\n")
    if not dry_run:
        shutil.move(os.path.join(DOCS_DIR, filename), os.path.join(HISTORY_DIR, filename))
        with open(LOG_FILE, "a") as log:
            log.write(f"{datetime.now().isoformat()} - Applied {filename}\n")
        if config["index_autogen"]:
            regenerate_index()

def regenerate_index():
    md_files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".md")]
    with open(os.path.join(DOCS_DIR, "index.md"), "w") as index:
        index.write("# index.md\n\n## Documentation Files\n")
        for f in sorted(md_files):
            index.write(f"- [{f}]({f})\n")

def undo_last_update():
    messagebox.showinfo("Undo", "Undo feature not yet implemented.")

class UpdateToolGUI:
    def __init__(self, root):
        root.title("YAML Update Tool")
        root.geometry("1000x720")

        # Panels
        self.left_panel = tk.Frame(root, width=250)
        self.center_panel = tk.Frame(root)
        self.right_panel = tk.Frame(root, width=200)
        self.bottom_panel = tk.Frame(root, height=100)
        self.status_bar = tk.Label(root, text="Status: Ready", anchor="w", bg="#cccccc", font=("Arial", 10))

        self.left_panel.pack(side="left", fill="y")
        self.center_panel.pack(side="left", expand=True, fill="both")
        self.right_panel.pack(side="right", fill="y")
        self.bottom_panel.pack(side="bottom", fill="x")
        self.status_bar.pack(side="bottom", fill="x")

        self.build_left_panel()
        self.build_center_panel()
        self.build_right_panel()
        self.build_bottom_panel()

        self.refresh()

    def build_left_panel(self):
        tk.Label(self.left_panel, text="YAML Inbox", font=("Arial", 12, "bold")).pack(pady=10)
        self.available_list = tk.Listbox(self.left_panel)
        self.available_list.pack(fill="both", expand=True, padx=10)
        self.available_list.bind("<<ListboxSelect>>", self.preview_yaml)

    def build_center_panel(self):
        preview_frame = tk.Frame(self.center_panel)
        preview_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.preview = tk.Text(preview_frame, wrap="word")
        scrollbar = tk.Scrollbar(preview_frame, command=self.preview.yview)
        self.preview.configure(yscrollcommand=scrollbar.set)

        self.preview.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def build_right_panel(self):
        tk.Label(self.right_panel, text="Actions", font=("Arial", 12, "bold")).pack(pady=10)
        actions = [
            ("Apply", self.apply_selected),
            ("Dry Run", self.dry_run_selected),
            ("Refresh", self.refresh),
            ("Import YAML", self.import_yaml),
            ("Undo", undo_last_update),
            ("Setup", self.first_time_setup)
        ]
        for label, command in actions:
            tk.Button(self.right_panel, text=label, command=command, width=18).pack(pady=5)

    def build_bottom_panel(self):
        tk.Label(self.bottom_panel, text="Log Viewer", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
        self.log_text = tk.Text(self.bottom_panel, height=5)
        self.log_text.pack(fill="both", expand=True, padx=10, pady=5)

    def status(self, message):
        clean_msg = message.replace("\n", " ").strip()
        self.status_bar.config(text=f"Status: {clean_msg}")
        self.log_text.insert("end", f"{datetime.now().isoformat()} - {clean_msg}\n")

    def refresh(self):
        self.available_list.delete(0, tk.END)
        available, _ = list_yaml_files()
        for f in available:
            self.available_list.insert(tk.END, f)
        self.status("YAML list refreshed")

    def preview_yaml(self, event):
        selection = self.available_list.curselection()
        if selection:
            filename = self.available_list.get(selection[0])
            data = load_yaml(filename)
            self.preview.delete("1.0", tk.END)
            self.preview.insert(tk.END, yaml.dump(data, sort_keys=False))
            self.status(f"Previewing: {filename}")

    def apply_selected(self):
        selection = self.available_list.curselection()
        if selection:
            filename = self.available_list.get(selection[0])
            data = load_yaml(filename)
            apply_yaml(filename, data)
            messagebox.showinfo("Update Applied", f"{filename} has been processed.")
            self.status(f"Applied: {filename}")
            self.refresh()

    def dry_run_selected(self):
        selection = self.available_list.curselection()
        if selection:
            filename = self.available_list.get(selection[0])
            data = load_yaml(filename)
            apply_yaml(filename, data, dry_run=True)
            self.status(f"Dry run completed for: {filename}")

    def import_yaml(self):
        file_path = filedialog.askopenfilename(filetypes=[("YAML files", "*.yaml")])
        if file_path:
            dest = os.path.join(DOCS_DIR, os.path.basename(file_path))
            shutil.copy(file_path, dest)
            self.status(f"Imported YAML: {os.path.basename(file_path)}")
            self.refresh()

    def first_time_setup(self):
        os.makedirs(DOCS_DIR, exist_ok=True)
        os.makedirs(HISTORY_DIR, exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        os.makedirs("backups", exist_ok=True)
        if not os.path.exists(os.path.join(DOCS_DIR, "index.md")):
            with open(os.path.join(DOCS_DIR, "index.md"), "w") as f:
                f.write("# index.md\n\n## Documentation Files\n")
        self.status("First-time setup complete")

# Launch
if __name__ == "__main__":
    root = tk.Tk()
    app = UpdateToolGUI(root)
    root.mainloop()
