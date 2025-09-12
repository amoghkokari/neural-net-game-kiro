#!/usr/bin/env python3
"""
Test runner script for Neural Network Adventure RPG
"""

import sys
import subprocess
import argparse
import os

def run_unit_tests():
    """Run unit tests only"""
    print("🧪 Running Unit Tests...")
    cmd = ["python3", "-m", "pytest", "tests/unit/", "-v", "--cov=src", "--cov-report=term-missing"]
    return subprocess.run(cmd).returncode

def run_integration_tests():
    """Run integration tests only"""
    print("🔗 Running Integration Tests...")
    cmd = ["python3", "-m", "pytest", "tests/integration/", "-v", "--cov=src", "--cov-report=term-missing"]
    return subprocess.run(cmd).returncode

def run_e2e_tests():
    """Run end-to-end tests only"""
    print("🎮 Running End-to-End Tests...")
    cmd = ["python3", "-m", "pytest", "tests/e2e/", "-v", "--cov=src", "--cov-report=term-missing"]
    return subprocess.run(cmd).returncode

def run_all_tests():
    """Run all tests with coverage"""
    print("🚀 Running All Tests with Coverage...")
    cmd = [
        "python3", "-m", "pytest", 
        "tests/", 
        "-v", 
        "--cov=src", 
        "--cov-report=html", 
        "--cov-report=term-missing",
        "--cov-fail-under=80"
    ]
    return subprocess.run(cmd).returncode

def run_quick_tests():
    """Run quick tests (unit tests only)"""
    print("⚡ Running Quick Tests...")
    cmd = ["python3", "-m", "pytest", "tests/unit/", "-x", "--tb=short"]
    return subprocess.run(cmd).returncode

def run_coverage_report():
    """Generate detailed coverage report"""
    print("📊 Generating Coverage Report...")
    
    # Run tests with coverage
    cmd = [
        "python3", "-m", "pytest", 
        "tests/", 
        "--cov=src", 
        "--cov-report=html",
        "--cov-report=xml",
        "--cov-report=term-missing"
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n✅ Coverage report generated!")
        print("📁 HTML report: htmlcov/index.html")
        print("📄 XML report: coverage.xml")
    
    return result.returncode

def check_code_quality():
    """Run code quality checks"""
    print("🔍 Running Code Quality Checks...")
    
    # Check if flake8 is available
    try:
        subprocess.run(["flake8", "--version"], capture_output=True, check=True)
        flake8_available = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        flake8_available = False
    
    if flake8_available:
        print("Running flake8...")
        cmd = ["flake8", "src/", "--max-line-length=120", "--ignore=E501,W503"]
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print("❌ Code quality issues found!")
            return result.returncode
    else:
        print("⚠️  flake8 not available, skipping code quality check")
    
    print("✅ Code quality check passed!")
    return 0

def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(description="Neural Network Adventure RPG Test Runner")
    parser.add_argument(
        "test_type", 
        choices=["unit", "integration", "e2e", "all", "quick", "coverage", "quality"],
        help="Type of tests to run"
    )
    
    args = parser.parse_args()
    
    # Set environment variable for headless testing
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    
    print("🎮 Neural Network Adventure RPG - Test Runner")
    print("=" * 50)
    
    if args.test_type == "unit":
        return run_unit_tests()
    elif args.test_type == "integration":
        return run_integration_tests()
    elif args.test_type == "e2e":
        return run_e2e_tests()
    elif args.test_type == "all":
        return run_all_tests()
    elif args.test_type == "quick":
        return run_quick_tests()
    elif args.test_type == "coverage":
        return run_coverage_report()
    elif args.test_type == "quality":
        return check_code_quality()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())