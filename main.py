import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess
import threading
import shutil
import sys
import os.path as osp
import tempfile

try:
    from dev_launcher import create_and_open_terminal
except ImportError:
    def create_and_open_terminal(project_path, command):
        if os.name == 'nt':
            launcher_path = os.path.join(project_path, "start-dev-server.bat")
            with open(launcher_path, "w") as f:
                f.write("@echo off\n")
                f.write(f"echo Starting development server...\n")
                f.write(f"echo Command: {command}\n")
                f.write(f"pause\n")
                f.write(f"{command}\n")
                f.write("pause\n")
            os.system(f'start cmd /k "{launcher_path}"')
            return True
        return False

class ReactProjectCreator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("React Project Creator v1.0.0")
        self.geometry("600x700")
        self.resizable(False, False)
        
        self.common_dependencies = [
            "react-router-dom", 
            "axios",
            "react-icons",
            "lucide-react",
            "react-query",
            "swr",
            "@emotion/react",
            "@emotion/styled",
            "@mui/material",
            "@chakra-ui/react",
            "react-bootstrap",
            "bootstrap",
            "date-fns",
            "lodash",
            "uuid",
            "react-toastify",
            "react-hook-form",
            "yup",
            "formik",
            "react-modal"
        ]
        
        self.npm_path = self.find_npm_path()
        
        self.setup_ui()
    
    def find_npm_path(self):
        npm_cmd = "npm.cmd" if os.name == 'nt' else "npm"
        path = shutil.which(npm_cmd)
        if not path:
            if os.name == 'nt':
                path = shutil.which("npm")
        return path
    
    def setup_ui(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Project Type:").grid(row=0, column=0, sticky="w", pady=(0, 10))
        self.project_type = tk.StringVar(value="vite")
        ttk.Radiobutton(main_frame, text="Vite", variable=self.project_type, value="vite").grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(main_frame, text="Create React App", variable=self.project_type, value="cra").grid(row=0, column=2, sticky="w")
        
        ttk.Label(main_frame, text="Project Name:").grid(row=1, column=0, sticky="w", pady=(0, 10))
        self.project_name = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.project_name, width=40).grid(row=1, column=1, columnspan=2, sticky="w")
        
        ttk.Label(main_frame, text="Project Path:").grid(row=2, column=0, sticky="w", pady=(0, 10))
        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=2, column=1, columnspan=2, sticky="w")
        
        self.project_path = tk.StringVar()
        ttk.Entry(path_frame, textvariable=self.project_path, width=30).pack(side=tk.LEFT)
        ttk.Button(path_frame, text="Browse", command=self.browse_path).pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Label(main_frame, text="Language:").grid(row=3, column=0, sticky="w", pady=(0, 10))
        self.language = tk.StringVar(value="javascript")
        ttk.Radiobutton(main_frame, text="JavaScript", variable=self.language, value="javascript").grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(main_frame, text="TypeScript", variable=self.language, value="typescript").grid(row=3, column=2, sticky="w")
        
        ttk.Label(main_frame, text="Select Libraries to Install:").grid(row=4, column=0, sticky="nw", pady=(0, 10))
        
        dependencies_frame = ttk.LabelFrame(main_frame, text="Ready-to-use Libraries")
        dependencies_frame.grid(row=4, column=1, columnspan=2, rowspan=2, sticky="nw", pady=(0, 10))
        
        dependencies_canvas = tk.Canvas(dependencies_frame, width=300, height=200)
        scrollbar = ttk.Scrollbar(dependencies_frame, orient="vertical", command=dependencies_canvas.yview)
        scrollable_frame = ttk.Frame(dependencies_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: dependencies_canvas.configure(
                scrollregion=dependencies_canvas.bbox("all")
            )
        )
        
        dependencies_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        dependencies_canvas.configure(yscrollcommand=scrollbar.set)
        
        dependencies_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.dependency_vars = {}
        for i, dep in enumerate(self.common_dependencies):
            var = tk.BooleanVar(value=False)
            self.dependency_vars[dep] = var
            ttk.Checkbutton(scrollable_frame, text=dep, variable=var).grid(
                row=i//2, column=i%2, sticky="w", padx=5, pady=2
            )
        
        self.auto_run = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Open terminal with dev command after creation", 
                        variable=self.auto_run).grid(row=6, column=0, columnspan=3, sticky="w", pady=(10, 10))
        
        ttk.Label(main_frame, text="Console Output:").grid(row=7, column=0, sticky="nw", pady=(10, 0))
        self.console = tk.Text(main_frame, height=10, width=60)
        self.console.grid(row=8, column=0, columnspan=3, sticky="w")
        self.console.config(state=tk.DISABLED)
        
        ttk.Button(main_frame, text="Create Project", command=self.create_project).grid(row=9, column=0, columnspan=3, pady=(10, 0))
        
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)
    
    def browse_path(self):
        directory = filedialog.askdirectory()
        if directory:
            self.project_path.set(directory)
    
    def update_console(self, text):
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)
        self.update()
    
    def validate_inputs(self):
        if not self.project_name.get().strip():
            messagebox.showerror("Error", "Project name is required!")
            return False
        
        if not self.project_path.get().strip():
            messagebox.showerror("Error", "Project path is required!")
            return False
            
        if not os.path.exists(self.project_path.get()):
            messagebox.showerror("Error", "Project path doesn't exist!")
            return False
        
        if not self.npm_path:
            messagebox.showerror("Error", "npm executable could not be found! Please make sure Node.js is installed and in your PATH.")
            return False
            
        return True
    
    def get_selected_dependencies(self):
        dependencies = []
        
        for dep, var in self.dependency_vars.items():
            if var.get():
                dependencies.append(dep)
        
        return dependencies
        
    def execute_command(self, cmd, cwd=None):
        if cmd[0] == "npm" and self.npm_path:
            cmd[0] = self.npm_path
        elif cmd[0] == "npx" and self.npm_path:
            npx_path = self.npm_path.replace("npm", "npx")
            if os.path.exists(npx_path):
                cmd[0] = npx_path
            else:
                npx_cmd = cmd[1:]
                cmd = [self.npm_path, "exec"]
                cmd.extend(npx_cmd)
        
        self.update_console(f"Executing: {' '.join(cmd)}")
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=cwd,
                shell=True if os.name == 'nt' else False
            )
            
            for line in process.stdout:
                self.update_console(line.strip())
            
            process.wait()
            return process.returncode == 0
        except Exception as e:
            self.update_console(f"Error: {str(e)}")
            return False
    
    def create_project(self):
        if not self.validate_inputs():
            return
        
        threading.Thread(target=self._create_project_thread, daemon=True).start()
    
    def _create_project_thread(self):
        self.status_var.set("Creating project...")
        project_type = self.project_type.get()
        project_name = self.project_name.get().strip()
        project_path = self.project_path.get().strip()
        is_typescript = self.language.get() == "typescript"
        dependencies = self.get_selected_dependencies()
        
        full_project_path = os.path.join(project_path, project_name)
        
        if project_type == "vite":
            if os.name == 'nt':
                cmd = [self.npm_path, "init", "vite@latest", project_name]
            else:
                cmd = [self.npm_path, "create", "vite@latest", project_name]
                
            if is_typescript:
                cmd.extend(["--", "--template", "react-ts"])
            else:
                cmd.extend(["--", "--template", "react"])
                
            if not self.execute_command(cmd, project_path):
                self.status_var.set("Failed to create Vite project!")
                return
        else:
            cmd = ["npx", "create-react-app", project_name]
            if is_typescript:
                cmd.append("--template typescript")
                
            if not self.execute_command(cmd, project_path):
                self.status_var.set("Failed to create React App project!")
                return
        
        self.update_console("\nRunning npm install...")
        install_cmd = ["npm", "install"]
        if not self.execute_command(install_cmd, full_project_path):
            self.status_var.set("Failed to run npm install!")
            return
            
        if dependencies:
            self.update_console("\nInstalling additional dependencies...")
            install_dep_cmd = ["npm", "install"]
            install_dep_cmd.extend(dependencies)
            
            if not self.execute_command(install_dep_cmd, full_project_path):
                self.status_var.set("Failed to install dependencies!")
                return
        
        if self.auto_run.get():
            dev_command = "npm run dev" if project_type == "vite" else "npm start"
            self.update_console(f"\nOpening terminal with '{dev_command}' command...")
            
            success = create_and_open_terminal(full_project_path, dev_command)
            
            if success:
                self.update_console("Development server terminal opened successfully!")
            else:
                self.update_console("Failed to open terminal automatically.")
                messagebox.showinfo("Manual Action Required", 
                                  f"Could not open terminal automatically.\n\n"
                                  f"A start-dev-server script has been created in your project.\n"
                                  f"Navigate to: {full_project_path}\n"
                                  f"And run the start-dev-server file to start the development server.")
        
        self.update_console("\nProject created successfully!")
        self.status_var.set(f"Project created at {full_project_path}")
        
        if not self.auto_run.get():
            if os.name == 'nt':
                os.startfile(full_project_path)
            elif os.name == 'posix':
                subprocess.call(('open' if os.uname().sysname == 'Darwin' else 'xdg-open', full_project_path))
    
    def _get_startupinfo(self):
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 1
            return startupinfo
        return None


if __name__ == "__main__":
    app = ReactProjectCreator()
    app.mainloop()