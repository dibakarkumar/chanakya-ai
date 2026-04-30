#!/usr/bin/env python3
"""
Week 1 Setup Verification Script
Verifies all installations are correct before proceeding
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python():
    """Verify Python version"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} — Good!")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} — Need 3.10+")
        return False

def check_pip():
    """Verify pip is installed"""
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ pip — {result.stdout.strip()}")
            return True
    except:
        pass
    print("❌ pip not found")
    return False

def check_git():
    """Verify Git is installed"""
    try:
        result = subprocess.run(["git", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git — {result.stdout.strip()}")
            return True
    except:
        pass
    print("❌ Git not found")
    return False

def check_ollama():
    """Verify Ollama is installed and running"""
    try:
        result = subprocess.run(["ollama", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama — {result.stdout.strip()}")
            return True
    except:
        pass
    print("❌ Ollama not found or not in PATH")
    print("   → Download from ollama.com and install")
    return False

def check_ollama_running():
    """Check if Ollama server is running"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            print("✅ Ollama server is running on localhost:11434")
            return True
    except:
        pass
    print("⚠️  Ollama server not running")
    print("   → Run: ollama serve")
    return False

def check_models():
    """Check what models are available"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            if models:
                print(f"✅ Available models:")
                for model in models:
                    print(f"   • {model.get('name')}")
                return True
            else:
                print("⚠️  No models downloaded yet")
                print("   → Run: ollama pull llama3.2")
                return False
    except:
        pass
    return False

def main():
    """Run all checks"""
    print("\n" + "="*50)
    print("  CHANAKYA WEEK 1 SETUP VERIFICATION")
    print("="*50 + "\n")
    
    checks = [
        ("Python Version", check_python),
        ("pip", check_pip),
        ("Git", check_git),
        ("Ollama Installation", check_ollama),
        ("Ollama Server", check_ollama_running),
        ("Ollama Models", check_models),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append(False)
    
    print("\n" + "="*50)
    passed = sum(results)
    total = len(results)
    print(f"\nResult: {passed}/{total} checks passed")
    print("="*50 + "\n")
    
    if passed == total:
        print("✅ ALL CHECKS PASSED! Ready for Week 2.\n")
        return 0
    else:
        print("❌ Some checks failed. Fix the issues above and re-run.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
