#!/usr/bin/env python3
"""
Simple launcher for Neural Network Adventure RPG
Handles virtual environment activation and dependency checking
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher required")
        print(f"   Current version: {sys.version}")
        return False
    return True

def check_virtual_env():
    """Check if virtual environment exists and activate it"""
    venv_paths = ['navenv', 'venv', '.venv']
    
    for venv_path in venv_paths:
        if os.path.exists(venv_path):
            print(f"✅ Found virtual environment: {venv_path}")
            
            # Determine activation script based on platform
            if platform.system() == "Windows":
                activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
                python_exe = os.path.join(venv_path, "Scripts", "python.exe")
            else:
                activate_script = os.path.join(venv_path, "bin", "activate")
                python_exe = os.path.join(venv_path, "bin", "python")
            
            if os.path.exists(python_exe):
                return python_exe
    
    print("⚠️  No virtual environment found, using system Python")
    return sys.executable

def install_dependencies(python_exe):
    """Install required dependencies"""
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found")
        return False
    
    print("📦 Checking dependencies...")
    try:
        result = subprocess.run([
            python_exe, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed/verified")
            return True
        else:
            print("❌ Failed to install dependencies")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def launch_game(python_exe):
    """Launch the main game"""
    if not os.path.exists("main.py"):
        print("❌ main.py not found")
        return False
    
    print("🎮 Launching Neural Network Adventure...")
    try:
        # Launch the game
        subprocess.run([python_exe, "main.py"])
        return True
    except KeyboardInterrupt:
        print("\n👋 Game closed by user")
        return True
    except Exception as e:
        print(f"❌ Error launching game: {e}")
        return False

def main():
    """Main launcher process"""
    print("🧠 Neural Network Adventure RPG Launcher")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Find Python executable (preferably from virtual environment)
    python_exe = check_virtual_env()
    
    # Install dependencies
    if not install_dependencies(python_exe):
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Launch game
    if not launch_game(python_exe):
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()