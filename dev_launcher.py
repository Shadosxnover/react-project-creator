import os
import sys
import subprocess
import tempfile

def create_and_open_terminal(project_path, command):
    """
    Create a launcher script and open it in a new terminal window.
    Returns True if successful, False otherwise.
    """
    try:
        # Check if running on Windows
        if os.name == 'nt':
            # Create a batch file
            launcher_path = os.path.join(project_path, "start-dev-server.bat")
            with open(launcher_path, "w") as f:
                f.write("@echo off\n")
                f.write(f"cd /d \"{project_path}\"\n")  # Explicitly change directory first
                f.write("color 0A\n")  # Green text on black background
                f.write("title React Development Server\n")
                f.write("cls\n")
                f.write("echo =======================================\n")
                f.write("echo   React Development Server Launcher\n")
                f.write("echo =======================================\n")
                f.write("echo.\n")
                f.write("echo Current directory: %cd%\n")
                f.write("echo.\n")
                f.write("echo Press any key to start the development server...\n")
                f.write("pause > nul\n")
                f.write(f"echo Running: {command}\n")
                f.write("echo.\n")
                f.write(f"{command}\n")
                f.write("echo.\n")
                f.write("echo Server stopped. Press any key to exit...\n")
                f.write("pause > nul\n")
                
            # For Windows, use the absolute path and ensure we start in the correct directory
            # Using cmd /k approach with explicit directory change
            os.system(f'start cmd /k "cd /d "{project_path}" && "{launcher_path}""')
            return True
            
        # For Linux/macOS
        elif os.name == 'posix':
            # Create shell script
            launcher_path = os.path.join(project_path, "start-dev-server.sh")
            with open(launcher_path, "w") as f:
                f.write("#!/bin/bash\n")
                f.write(f"cd \"{project_path}\"\n")  # Explicitly change directory first
                f.write("clear\n")
                f.write('echo "======================================="\n')
                f.write('echo "  React Development Server Launcher"\n')
                f.write('echo "======================================="\n')
                f.write('echo ""\n')
                f.write('echo "Current directory: $(pwd)"\n')
                f.write('echo ""\n')
                f.write('echo "Press Enter to start the development server..."\n')
                f.write('read\n')
                f.write(f'echo "Running: {command}"\n')
                f.write('echo ""\n')
                f.write(f'{command}\n')
                f.write('echo ""\n')
                f.write('echo "Server stopped. Press Enter to exit..."\n')
                f.write('read\n')
            
            # Make executable
            os.chmod(launcher_path, 0o755)
            
            # Try to find a terminal emulator
            if os.uname().sysname == "Darwin":  # macOS
                subprocess.Popen(['open', '-a', 'Terminal', launcher_path], cwd=project_path)
            elif os.path.exists("/usr/bin/gnome-terminal"):
                subprocess.Popen(['gnome-terminal', '--working-directory', project_path, '--', launcher_path])
            elif os.path.exists("/usr/bin/xterm"):
                subprocess.Popen(['xterm', '-e', f'cd "{project_path}" && "{launcher_path}"'])
            else:
                # Fallback - display the command that should be run
                return False
                
            return True
    except Exception as e:
        print(f"Error opening terminal: {e}")
        return False
        
# To test this script directly:
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python dev_launcher.py <project_path> <command>")
        sys.exit(1)
    
    success = create_and_open_terminal(sys.argv[1], sys.argv[2])
    print(f"Terminal {'opened successfully' if success else 'could not be opened'}")
