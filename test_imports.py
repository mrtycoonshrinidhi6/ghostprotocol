"""
Ghost Protocol - Import Test Script
Quick check to verify all critical imports work
"""

import sys

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"✅ {package_name}")
        return True
    except ImportError as e:
        print(f"❌ {package_name} - {e}")
        return False


def main():
    """Test all critical imports"""
    
    print("=" * 70)
    print("🔍 GHOST PROTOCOL - IMPORT TEST")
    print("=" * 70)
    print()
    
    print("Python Version:", sys.version)
    print("Python Path:", sys.executable)
    print()
    
    print("=" * 70)
    print("CRITICAL PACKAGES:")
    print("=" * 70)
    
    critical = [
        ('dotenv', 'python-dotenv'),
        ('fastapi', 'fastapi'),
        ('uvicorn', 'uvicorn'),
        ('pydantic', 'pydantic'),
        ('requests', 'requests'),
        ('streamlit', 'streamlit'),
    ]
    
    results = []
    for module, package in critical:
        results.append(test_import(module, package))
    
    print()
    print("=" * 70)
    print("PROJECT MODULES:")
    print("=" * 70)
    
    project = [
        'config',
        'load_env',
        'mock_generators',
        'retry_handler',
        'observability',
        'realtime_tools',
        'agents_realtime',
    ]
    
    for module in project:
        results.append(test_import(module))
    
    print()
    print("=" * 70)
    print("SUMMARY:")
    print("=" * 70)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL IMPORTS SUCCESSFUL!")
        print("✅ System is ready to run")
        return 0
    else:
        print(f"\n❌ {total - passed} IMPORT(S) FAILED")
        print("\n💡 To fix:")
        print("   pip install -r backend/requirements.txt")
        print("   pip install -r frontend/requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
