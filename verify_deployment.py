#!/usr/bin/env python3
"""
Deployment Verification Script
Checks if the project is ready for deployment
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - MISSING")
        return False

def check_file_content(filepath, search_text, description):
    """Check if file contains specific text"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if search_text in content:
                print(f"✅ {description}")
                return True
            else:
                print(f"❌ {description} - Not found in {filepath}")
                return False
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return False

def main():
    print("=" * 70)
    print("🚀 Deployment Readiness Verification")
    print("=" * 70)
    print()
    
    checks_passed = 0
    checks_total = 0
    
    # Check critical files
    print("📁 Checking Critical Files:")
    print("-" * 70)
    
    checks_total += 1
    if check_file_exists("Procfile", "Procfile"):
        checks_passed += 1
    
    checks_total += 1
    if check_file_exists("render.yaml", "render.yaml"):
        checks_passed += 1
    
    checks_total += 1
    if check_file_exists("runtime.txt", "runtime.txt"):
        checks_passed += 1
    
    checks_total += 1
    if check_file_exists("platform/requirements.txt", "Platform requirements.txt"):
        checks_passed += 1
    
    checks_total += 1
    if check_file_exists("platform/simple_server.py", "Server file"):
        checks_passed += 1
    
    checks_total += 1
    if check_file_exists("platform/frontend/index.html", "Frontend HTML"):
        checks_passed += 1
    
    checks_total += 1
    if check_file_exists(".gitignore", ".gitignore"):
        checks_passed += 1
    
    print()
    print("🔍 Checking Configuration:")
    print("-" * 70)
    
    # Check Procfile content
    checks_total += 1
    if check_file_content("Procfile", "cd platform && python simple_server.py", 
                         "Procfile has correct start command"):
        checks_passed += 1
    
    # Check render.yaml build command
    checks_total += 1
    if check_file_content("render.yaml", "platform/requirements.txt", 
                         "render.yaml uses platform/requirements.txt"):
        checks_passed += 1
    
    # Check runtime.txt
    checks_total += 1
    if check_file_content("runtime.txt", "python-3.11.0", 
                         "runtime.txt specifies Python 3.11.0"):
        checks_passed += 1
    
    # Check server binds to 0.0.0.0
    checks_total += 1
    if check_file_content("platform/simple_server.py", "0.0.0.0", 
                         "Server binds to 0.0.0.0 (production-ready)"):
        checks_passed += 1
    
    # Check server uses PORT env var
    checks_total += 1
    if check_file_content("platform/simple_server.py", "os.getenv('PORT'", 
                         "Server uses PORT environment variable"):
        checks_passed += 1
    
    # Check frontend uses dynamic API URL
    checks_total += 1
    if check_file_content("platform/frontend/index.html", "window.location.origin", 
                         "Frontend uses dynamic API URL"):
        checks_passed += 1
    
    # Check .gitignore excludes .env
    checks_total += 1
    if check_file_content(".gitignore", ".env", 
                         ".gitignore excludes .env file"):
        checks_passed += 1
    
    print()
    print("=" * 70)
    print(f"📊 Results: {checks_passed}/{checks_total} checks passed")
    print("=" * 70)
    
    if checks_passed == checks_total:
        print("✅ ALL CHECKS PASSED - Ready for deployment!")
        print()
        print("Next steps:")
        print("1. Push code to Git repository")
        print("2. Create Render service and connect repository")
        print("3. Set OPENAI_API_KEY environment variable")
        print("4. Deploy!")
        return 0
    else:
        print("❌ Some checks failed - Review the issues above")
        return 1

if __name__ == "__main__":
    sys.exit(main())

