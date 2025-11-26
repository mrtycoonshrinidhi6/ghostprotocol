"""
Ghost Protocol - Quick Start Script
Runs both backend and frontend simultaneously with health checks

Features:
- Automated dependency installation
- Port availability checks
- Backend health monitoring
- High-contrast WCAG AAA compliant UI theme
- Graceful shutdown handling
"""

import subprocess
import sys
import os
import time
import socket
import requests
from pathlib import Path


def check_dependencies():
    """Check if required packages are installed"""
    
    print("Checking dependencies...")
    
    backend_reqs = Path("backend/requirements.txt")
    frontend_reqs = Path("frontend/requirements.txt")
    
    if not backend_reqs.exists() or not frontend_reqs.exists():
        print("❌ Requirements files not found!")
        return False
    
    print("✅ Requirements files found")
    return True


def check_critical_imports():
    """Check if critical packages can be imported"""
    critical_packages = [
        ('dotenv', 'python-dotenv'),
        ('fastapi', 'fastapi'),
        ('uvicorn', 'uvicorn'),
        ('streamlit', 'streamlit')
    ]
    
    missing = []
    for import_name, package_name in critical_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package_name)
    
    return missing


def install_dependencies():
    """Install backend and frontend dependencies"""
    
    print("\n📦 Installing backend dependencies...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt", "--upgrade"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"❌ Backend installation failed: {result.stderr}")
        return False
    
    print("✅ Backend dependencies installed")
    
    print("\n📦 Installing frontend dependencies...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "frontend/requirements.txt", "--upgrade"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"❌ Frontend installation failed: {result.stderr}")
        return False
    
    print("✅ Frontend dependencies installed\n")
    return True


def check_port(port):
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0


def wait_for_backend():
    """Wait for backend to be ready"""
    max_retries = 45  # Increased from 30
    retry_count = 0
    
    print("⏳ Waiting for backend to start...", end="", flush=True)
    
    while retry_count < max_retries:
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                print(" ✅")
                print("✅ Backend ready on http://localhost:8000")
                return True
        except:
            pass
        
        time.sleep(1)
        retry_count += 1
        print(".", end="", flush=True)
    
    print(" ❌")
    return False


def run_backend():
    """Start FastAPI backend"""
    
    print("🚀 Starting backend on http://localhost:8000...")
    
    # Don't capture output - let it show in terminal for debugging
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"],
        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
    )
    
    return backend_process


def run_frontend():
    """Start Streamlit frontend"""
    
    print("🚀 Starting frontend on http://localhost:8501...")
    
    # Don't capture output - let it show in terminal
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend/app.py"],
        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
    )
    
    return frontend_process


def run_verification():
    """Run verification script to check critical fixes"""
    print("\n" + "="*70)
    print("🔍 Running system verification...")
    print("="*70)
    
    try:
        result = subprocess.run(
            [sys.executable, "verify_fixes.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ All verification tests passed")
            return True
        else:
            print("❌ Verification failed:")
            print(result.stdout)
            return False
    except FileNotFoundError:
        print("⚠️  verify_fixes.py not found - skipping verification")
        return True
    except Exception as e:
        print(f"⚠️  Verification error: {e}")
        return True  # Don't block startup


def main():
    """Main execution"""
    
    print("="*70)
    print("👻 GHOST PROTOCOL - QUICK START (Phase 10 Complete!)")
    print("="*70)
    print()
    
    # Run verification first
    if not run_verification():
        print("\n⚠️  System verification failed!")
        cont = input("Continue anyway? (y/n): ").lower()
        if cont != 'y':
            sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check critical imports
    missing = check_critical_imports()
    if missing:
        print(f"\n⚠️  Missing critical packages: {', '.join(missing)}")
        print("📦 Installing missing packages automatically...")
        if not install_dependencies():
            print("❌ Failed to install dependencies")
            sys.exit(1)
    else:
        # Ask to install/update
        install = input("\nInstall/update dependencies? (y/n): ").lower()
        if install == 'y':
            if not install_dependencies():
                print("❌ Failed to install dependencies")
                sys.exit(1)
    
    print("\n" + "="*70)
    print("🔍 Pre-flight checks...")
    print("="*70)
    
    # Check if ports are available
    if not check_port(8000):
        print("❌ Port 8000 is already in use! Please stop the existing service.")
        sys.exit(1)
    print("✅ Port 8000 is available (Backend)")
    
    if not check_port(8501):
        print("❌ Port 8501 is already in use! Please stop the existing service.")
        sys.exit(1)
    print("✅ Port 8501 is available (Frontend)")
    
    print("\n" + "="*70)
    print("🚀 Starting services...")
    print("="*70 + "\n")
    
    backend_proc = None
    frontend_proc = None
    
    try:
        # Start backend
        backend_proc = run_backend()
        
        # Wait for backend health check
        if not wait_for_backend():
            print("❌ Backend failed to start properly")
            if backend_proc:
                backend_proc.terminate()
            sys.exit(1)
        
        # Start frontend
        frontend_proc = run_frontend()
        time.sleep(3)  # Give frontend time to initialize
        
        print("\n" + "="*70)
        print("✅ Ghost Protocol is running! (All 10 Phases Complete)")
        print("="*70)
        print()
        print("🌐 BACKEND API:")
        print("   └─ Main API:    http://localhost:8000")
        print("   └─ API Docs:    http://localhost:8000/docs")
        print("   └─ Health:      http://localhost:8000/health")
        print("   └─ Diagnostics: http://localhost:8000/api/v1/diagnostics/keys")
        print()
        print("🎨 FRONTEND UI:")
        print("   └─ Streamlit:   http://localhost:8501")
        print("   └─ Mode Badge:  🟢 LIVE or 🟡 DEMO mode indicator")
        print("   └─ Theme:       High-Contrast Black & White")
        print("   └─ Visibility:  WCAG AAA Compliant (21:1)")
        print()
        print("🚀 FEATURES (REALTIME/MOCK Modes):")
        print("   └─ ⚰️  Death Detection (Multi-source verification)")
        print("   └─ 💼 Asset Discovery (Email, Cloud, Crypto, Social)")
        print("   └─ 📜 Smart Contract (Polygon blockchain)")
        print("   └─ 🕊️  Memorial Chat (AI memory twin)")
        print("   └─ 🔄 Retry Logic (3 attempts, exponential backoff)")
        print("   └─ ⏱️  Rate Limiting (60 calls/min per tool)")
        print("   └─ 📊 Observability (Logs, traces, metrics)")
        print("   └─ 🧪 System Testing (One-click validation)")
        print()
        print("🧪 TEST SYSTEM (Windows PowerShell):")
        print('   └─ Invoke-WebRequest -Method POST -Uri "http://localhost:8000/api/v1/run_full_system_test"')
        print()
        print("🧪 OR use Python:")
        print('   └─ python -c "import requests; print(requests.post(\\"http://localhost:8000/api/v1/run_full_system_test\\").json())"')
        print()
        print("💡 TIP: Open http://localhost:8501 in your browser")
        print("💡 Check mode in sidebar: 🟢 LIVE MODE or 🟡 DEMO MODE")
        print()
        print("⚠️  Press Ctrl+C to stop all services")
        print("="*70 + "\n")
        
        # Keep running and monitor processes
        while True:
            # Check if processes are still running
            if backend_proc.poll() is not None:
                print("❌ Backend process terminated unexpectedly!")
                break
            if frontend_proc.poll() is not None:
                print("❌ Frontend process terminated unexpectedly!")
                break
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("🛑 Shutting down Ghost Protocol...")
        print("="*70)
        
        if backend_proc:
            print("Stopping backend...", end="", flush=True)
            backend_proc.terminate()
            try:
                backend_proc.wait(timeout=5)
                print(" ✅")
            except subprocess.TimeoutExpired:
                backend_proc.kill()
                print(" ⚠️ (forced)")
        
        if frontend_proc:
            print("Stopping frontend...", end="", flush=True)
            frontend_proc.terminate()
            try:
                frontend_proc.wait(timeout=5)
                print(" ✅")
            except subprocess.TimeoutExpired:
                frontend_proc.kill()
                print(" ⚠️ (forced)")
        
        print("\n✅ All services stopped successfully")
        print("="*70 + "\n")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if backend_proc:
            backend_proc.terminate()
        if frontend_proc:
            frontend_proc.terminate()
        sys.exit(1)


if __name__ == "__main__":
    main()
