"""
Quick Start Script - Auto-starts Ghost Protocol backend and frontend
Bypasses interactive prompts for fast startup
"""

import subprocess
import sys
import time
import requests
import socket

def check_port(port):
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0

def wait_for_backend():
    """Wait for backend to be ready"""
    max_retries = 45
    retry_count = 0
    
    print("⏳ Waiting for backend to start...", end="", flush=True)
    
    while retry_count < max_retries:
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                print(" ✅")
                return True
        except:
            pass
        
        time.sleep(1)
        retry_count += 1
        print(".", end="", flush=True)
    
    print(" ❌")
    return False

def main():
    print("=" * 70)
    print("👻 GHOST PROTOCOL - QUICK START")
    print("=" * 70)
    print()
    
    # Check ports
    if not check_port(8000):
        print("❌ Port 8000 is already in use!")
        print("💡 Run: taskkill /F /IM python.exe")
        sys.exit(1)
    
    if not check_port(8501):
        print("❌ Port 8501 is already in use!")
        print("💡 Run: taskkill /F /IM python.exe")
        sys.exit(1)
    
    print("✅ Ports 8000 and 8501 are available")
    print()
    
    # Start backend
    print("🚀 Starting backend...")
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"],
        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
    )
    
    # Wait for backend
    if not wait_for_backend():
        print("❌ Backend failed to start")
        backend.terminate()
        sys.exit(1)
    
    print("✅ Backend ready on http://localhost:8000")
    print()
    
    # Start frontend
    print("🚀 Starting frontend...")
    frontend = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend/app.py"],
        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
    )
    
    time.sleep(3)
    print("✅ Frontend ready on http://localhost:8501")
    print()
    
    print("=" * 70)
    print("✅ GHOST PROTOCOL IS RUNNING!")
    print("=" * 70)
    print()
    print("🌐 BACKEND:  http://localhost:8000")
    print("   └─ Docs:  http://localhost:8000/docs")
    print("   └─ Health: http://localhost:8000/health")
    print()
    print("🎨 FRONTEND: http://localhost:8501")
    print()
    print("💡 Open http://localhost:8501 in your browser")
    print()
    print("⚠️  Press Ctrl+C to stop (close this window when done)")
    print("=" * 70)
    print()
    
    try:
        while True:
            if backend.poll() is not None:
                print("❌ Backend stopped!")
                break
            if frontend.poll() is not None:
                print("❌ Frontend stopped!")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        backend.terminate()
        frontend.terminate()
        print("✅ Stopped")

if __name__ == "__main__":
    main()
