# Version: 2.1.0
# Last Updated: 2025-09-14
# Author: Andrew + Copilot
# Section: PyQt5 YAML Update Tool GUI (Project-Aware)

import os
import yaml
import shutil
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QTextEdit, QLabel, QFileDialog, QTabWidget, QMessageBox
)
from PyQt5.QtCore import Qt

TOOL_ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(TOOL_ROOT, "config", "settings.yaml")
LOG_DIR = os.path.join(TOOL_ROOT, "logs")
BACKUP_DIR = os.path.join(TOOL_ROOT, "backups")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)
    return {}

def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(config, f)

class YAMLUpdateTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YAML Update Tool")
        self.setGeometry(100, 100, 1200, 700)

        self.config = load_config()
        self.project_path = self.config.get("project_path", "")
        self.docs_path = os.path.join(self.project_path, "docs") if self.project_path else ""
        self.history_path = os.path.join(self.docs_path, "yaml-history")
        self.log_file = os.path.join(LOG_DIR, "update.log")

        self.status_label = QLabel("Status: Ready")
        self.yaml_list = QListWidget()
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)

        self.tabs = QTabWidget()
        self.yaml_preview = QTextEdit()
        self.diff_view = QTextEdit()
        self.settings_editor = QTextEdit()

        self.tabs.addTab(self.yaml_preview, "YAML Preview")
        self.tabs.addTab(self.diff_view, "Diff View")
        self.tabs.addTab(self.settings_editor, "Settings Editor")

        self.build_ui()
        if self.project_path:
            self.refresh_yaml_list()

    def build_ui(self):
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        center_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        left_layout.addWidget(QLabel("YAML Inbox"))
        left_layout.addWidget(self.yaml_list)
        self.yaml_list.itemClicked.connect(self.preview_yaml)

        center_layout.addWidget(self.tabs)
        
        right_layout.addWidget(QLabel("🟢 First-Time Setup"))
        right_layout.addWidget(QPushButton("Select Project Folder", clicked=self.select_project))
        right_layout.addWidget(QPushButton("Initialize Project Structure", clicked=self.initialize_project_structure))
        right_layout.addWidget(QPushButton("Create Index.md", clicked=self.create_index))
        right_layout.addWidget(QPushButton("Init settings.yaml", clicked=self.init_settings))

        right_layout.addWidget(QLabel("🔄 Update Workflow"))
        right_layout.addWidget(QPushButton("Import YAML", clicked=self.import_yaml))
        right_layout.addWidget(QPushButton("Dry Run", clicked=self.dry_run))
        right_layout.addWidget(QPushButton("Apply Update", clicked=self.apply_update))
        right_layout.addWidget(QPushButton("Undo Last Update", clicked=self.undo_update))

        right_layout.addWidget(QLabel("⚙️ Configuration"))
        right_layout.addWidget(QPushButton("Edit Settings", clicked=self.load_settings))
        right_layout.addWidget(QPushButton("Refresh YAML List", clicked=self.refresh_yaml_list))

        bottom_layout = QVBoxLayout()
        bottom_layout.addWidget(self.status_label)
        bottom_layout.addWidget(QLabel("Log Viewer"))
        bottom_layout.addWidget(self.log_view)

        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(center_layout, 5)
        main_layout.addLayout(right_layout, 2)

        layout = QVBoxLayout()
        layout.addLayout(main_layout)
        layout.addLayout(bottom_layout)
        self.setLayout(layout)

    def set_status(self, message):
        self.status_label.setText(f"Status: {message}")
        self.log_view.append(f"{datetime.now().isoformat()} - {message}")

    def select_project(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder")
        if folder:
            self.project_path = folder
            self.docs_path = os.path.join(folder, "docs")
            self.history_path = os.path.join(self.docs_path, "yaml-history")
            self.config["project_path"] = folder
            save_config(self.config)
            self.set_status(f"Project selected: {folder}")
            self.refresh_yaml_list()
            
    def initialize_project_structure(self):
        if not self.project_path:
            self.set_status("Please select a project folder first.")
            return
    
        os.makedirs(self.docs_path, exist_ok=True)
        os.makedirs(self.history_path, exist_ok=True)
        os.makedirs(BACKUP_DIR, exist_ok=True)
        os.makedirs(LOG_DIR, exist_ok=True)
    
        index_path = os.path.join(self.docs_path, "index.md")
        if not os.path.exists(index_path):
            with open(index_path, "w") as f:
                f.write("# index.md\n\n## Documentation Files\n")
    
        if not os.path.exists(CONFIG_PATH):
            save_config(self.config)
    
        self.set_status("Project structure initialized.")

    def refresh_yaml_list(self):
        self.yaml_list.clear()
        if not os.path.exists(self.docs_path):
            self.set_status("Docs folder not found.")
            return
        all_files = [f for f in os.listdir(self.docs_path) if f.endswith(".yaml")]
        applied = os.listdir(self.history_path) if os.path.exists(self.history_path) else []
        available = [f for f in all_files if f not in applied]
        self.yaml_list.addItems(available)
        self.set_status("YAML list refreshed.")

    def preview_yaml(self):
        item = self.yaml_list.currentItem()
        if item:
            filename = item.text()
            path = os.path.join(self.docs_path, filename)
            with open(path, "r") as f:
                data = yaml.safe_load(f)
            self.yaml_preview.setText(yaml.dump(data, sort_keys=False))
            self.set_status(f"Previewing: {filename}")

    def apply_update(self):
        item = self.yaml_list.currentItem()
        if item:
            filename = item.text()
            path = os.path.join(self.docs_path, filename)
            with open(path, "r") as f:
                data = yaml.safe_load(f)
            for file in data.get("updated_files", []):
                target = os.path.join(self.docs_path, file)
                if os.path.exists(target):
                    os.makedirs(BACKUP_DIR, exist_ok=True)
                    backup_name = f"{file}.{datetime.now().strftime('%Y%m%d%H%M')}"
                    shutil.copy(target, os.path.join(BACKUP_DIR, backup_name))
                    with open(target, "a") as out:
                        for change in data["changes"].get(file, []):
                            out.write(f"\n<!-- Update: {change} -->\n")
            os.makedirs(self.history_path, exist_ok=True)
            shutil.move(path, os.path.join(self.history_path, filename))
            self.log_action(f"Applied {filename}")
            self.create_index()
            self.refresh_yaml_list()

    def dry_run(self):
        item = self.yaml_list.currentItem()
        if item:
            filename = item.text()
            path = os.path.join(self.docs_path, filename)
            with open(path, "r") as f:
                data = yaml.safe_load(f)
            self.set_status(f"Dry run completed for: {filename}")

    def import_yaml(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import YAML", "", "YAML Files (*.yaml)")
        if path:
            dest = os.path.join(self.docs_path, os.path.basename(path))
            shutil.copy(path, dest)
            self.set_status(f"Imported YAML: {os.path.basename(path)}")
            self.refresh_yaml_list()

    def undo_update(self):
        backups = sorted(os.listdir(BACKUP_DIR), reverse=True)
        if not backups:
            self.set_status("No backups found.")
            return
        latest = backups[0]
        original = latest.split(".")[0]
        shutil.copy(os.path.join(BACKUP_DIR, latest), os.path.join(self.docs_path, original))
        self.set_status(f"Restored: {original} from {latest}")

    def create_index(self):
        md_files = [f for f in os.listdir(self.docs_path) if f.endswith(".md")]
        with open(os.path.join(self.docs_path, "index.md"), "w") as index:
            index.write("# index.md\n\n## Documentation Files\n")
            for f in sorted(md_files):
                index.write(f"- [{f}]({f})\n")
        self.set_status("index.md regenerated.")        

        html_path = os.path.join(self.docs_path, "index.html")
        with open(html_path, "w") as html:
            html.write("<html><body><h1>Documentation Files</h1><ul>\n")
            for f in sorted(md_files):
                html.write(f"<li><a href='{f}'>{f}</a></li>\n")
            html.write("</ul></body></html>")



    def init_settings(self):
        save_config(self.config)
        self.set_status("settings.yaml initialized.")

    def load_settings(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                self.settings_editor.setText(f.read())
            self.set_status("Loaded settings.yaml for editing.")
        else:
            self.settings_editor.setText("# settings.yaml not found.")
            self.set_status("settings.yaml missing.")

    def log_action(self, message):
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(self.log_file, "a") as log:
            log.write(f"{datetime.now().isoformat()} - {message}\n")
        self.set_status(message)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = YAMLUpdateTool()
    window.show()
    sys.exit(app.exec_())
