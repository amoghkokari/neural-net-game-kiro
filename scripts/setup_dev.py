#!/usr/bin/env python3
"""
Development environment setup script for Neural Network Adventure RPG
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description, check=True):
    """Run a command and handle errors gracefully"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def setup_virtual_environment():
    """Set up virtual environment"""
    venv_path = Path("navenv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    success = run_command(
        f"{sys.executable} -m venv navenv",
        "Creating virtual environment"
    )
    
    if success:
        print("📝 Virtual environment created at 'navenv/'")
        print("   Activate with:")
        if platform.system() == "Windows":
            print("   navenv\\Scripts\\activate")
        else:
            print("   source navenv/bin/activate")
    
    return success

def install_dependencies():
    """Install development dependencies"""
    # Determine pip command based on platform and virtual environment
    if platform.system() == "Windows":
        pip_cmd = "navenv\\Scripts\\pip"
    else:
        pip_cmd = "navenv/bin/pip"
    
    # Upgrade pip first
    success = run_command(
        f"{pip_cmd} install --upgrade pip",
        "Upgrading pip"
    )
    
    if not success:
        return False
    
    # Install development dependencies
    success = run_command(
        f"{pip_cmd} install -r requirements-dev.txt",
        "Installing development dependencies"
    )
    
    return success

def setup_pre_commit_hooks():
    """Set up pre-commit hooks for code quality"""
    if platform.system() == "Windows":
        pre_commit_cmd = "navenv\\Scripts\\pre-commit"
    else:
        pre_commit_cmd = "navenv/bin/pre-commit"
    
    # Create .pre-commit-config.yaml if it doesn't exist
    pre_commit_config = Path(".pre-commit-config.yaml")
    if not pre_commit_config.exists():
        config_content = """# Pre-commit hooks for Neural Network Adventure RPG
repos:
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
        language_version: python3
        args: [--line-length=88]

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: [--profile=black]

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203,W503]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.6.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--ignore-missing-imports]

  - repo: https://github.com/pycqa/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-r, src/, -f, json]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
"""
        with open(pre_commit_config, 'w') as f:
            f.write(config_content)
        print("✅ Created .pre-commit-config.yaml")
    
    # Install pre-commit hooks
    success = run_command(
        f"{pre_commit_cmd} install",
        "Installing pre-commit hooks"
    )
    
    return success

def create_vscode_settings():
    """Create VS Code settings for the project"""
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)
    
    settings_file = vscode_dir / "settings.json"
    if not settings_file.exists():
        settings_content = """{
    "python.defaultInterpreterPath": "./navenv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length=88"],
    "python.sortImports.args": ["--profile=black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        ".pytest_cache": true,
        ".coverage": true,
        "htmlcov": true,
        "build": true,
        "dist": true,
        "*.egg-info": true
    },
    "python.analysis.typeCheckingMode": "basic"
}"""
        with open(settings_file, 'w') as f:
            f.write(settings_content)
        print("✅ Created VS Code settings")
    
    # Create launch configuration for debugging
    launch_file = vscode_dir / "launch.json"
    if not launch_file.exists():
        launch_content = """{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run Game",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "Run Tests",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/scripts/run_tests.py",
            "args": ["all"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "Debug Current Test",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["${file}", "-v"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}"""
        with open(launch_file, 'w') as f:
            f.write(launch_content)
        print("✅ Created VS Code launch configuration")

def run_initial_tests():
    """Run tests to verify setup"""
    if platform.system() == "Windows":
        python_cmd = "navenv\\Scripts\\python"
    else:
        python_cmd = "navenv/bin/python"
    
    success = run_command(
        f"{python_cmd} scripts/run_tests.py quick",
        "Running initial tests"
    )
    
    return success

def create_development_scripts():
    """Create helpful development scripts"""
    scripts_dir = Path("scripts")
    scripts_dir.mkdir(exist_ok=True)
    
    # Create a quick development launcher
    dev_launcher = scripts_dir / "dev.py"
    if not dev_launcher.exists():
        launcher_content = '''#!/usr/bin/env python3
"""
Quick development launcher for Neural Network Adventure RPG
"""

import sys
import subprocess
import platform

def main():
    """Main development launcher"""
    if len(sys.argv) < 2:
        print("Usage: python scripts/dev.py <command>")
        print("Commands:")
        print("  game     - Run the game")
        print("  test     - Run all tests")
        print("  quick    - Run quick tests")
        print("  format   - Format code")
        print("  lint     - Run linting")
        print("  build    - Build executable")
        return
    
    command = sys.argv[1]
    
    # Determine Python command
    if platform.system() == "Windows":
        python_cmd = "navenv\\\\Scripts\\\\python"
    else:
        python_cmd = "navenv/bin/python"
    
    if command == "game":
        subprocess.run([python_cmd, "main.py"])
    elif command == "test":
        subprocess.run([python_cmd, "scripts/run_tests.py", "all"])
    elif command == "quick":
        subprocess.run([python_cmd, "scripts/run_tests.py", "quick"])
    elif command == "format":
        subprocess.run([python_cmd, "-m", "black", "src/", "tests/"])
        subprocess.run([python_cmd, "-m", "isort", "src/", "tests/"])
    elif command == "lint":
        subprocess.run([python_cmd, "-m", "flake8", "src/", "tests/"])
        subprocess.run([python_cmd, "-m", "mypy", "src/"])
    elif command == "build":
        subprocess.run([python_cmd, "scripts/build_executable.py"])
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
'''
        with open(dev_launcher, 'w') as f:
            f.write(launcher_content)
        print("✅ Created development launcher script")

def print_next_steps():
    """Print next steps for the developer"""
    print("\n🎉 Development environment setup complete!")
    print("\n📋 Next Steps:")
    print("1. Activate virtual environment:")
    if platform.system() == "Windows":
        print("   navenv\\Scripts\\activate")
    else:
        print("   source navenv/bin/activate")
    
    print("\n2. Start developing:")
    print("   python main.py                    # Run the game")
    print("   python scripts/run_tests.py all  # Run all tests")
    print("   python scripts/dev.py game       # Quick game launcher")
    
    print("\n3. Code quality tools:")
    print("   black src/ tests/                # Format code")
    print("   flake8 src/ tests/               # Lint code")
    print("   mypy src/                        # Type checking")
    
    print("\n4. Build executable:")
    print("   python scripts/build_executable.py")
    
    print("\n📚 Documentation:")
    print("   README.md                        # Project overview")
    print("   docs/CONTRIBUTING.md             # Contribution guide")
    print("   PROJECT_ARCHITECTURE.md         # Architecture overview")
    
    print("\n🎮 Happy coding! Your neural network adventure awaits!")

def main():
    """Main setup function"""
    print("🚀 Neural Network Adventure RPG - Development Setup")
    print("=" * 55)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup steps
    steps = [
        ("Virtual Environment", setup_virtual_environment),
        ("Dependencies", install_dependencies),
        ("Pre-commit Hooks", setup_pre_commit_hooks),
        ("VS Code Settings", create_vscode_settings),
        ("Development Scripts", create_development_scripts),
        ("Initial Tests", run_initial_tests),
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        print(f"\n🔧 Setting up {step_name}...")
        if not step_func():
            failed_steps.append(step_name)
            print(f"⚠️  {step_name} setup failed, but continuing...")
    
    if failed_steps:
        print(f"\n⚠️  Some steps failed: {', '.join(failed_steps)}")
        print("You may need to set these up manually.")
    
    print_next_steps()
    
    if not failed_steps:
        print("\n✅ All setup steps completed successfully!")
    
    return len(failed_steps) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)