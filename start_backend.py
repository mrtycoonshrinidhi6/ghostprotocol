"""
Ghost Protocol - Robust Backend Starter
Starts backend with automatic restart on crash
"""

import subprocess
import sys
import time
import requests
from datetime import datetime


def check_backend_health():
    """Check if backend is responding"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def start_backend():
    """Start the backend process"""
    print("=" * 70)
    print(f"🚀 Starting Ghost Protocol Backend - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 70)
    
    process = subprocess.Popen(
        [sys.executable, "backend/api.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    return process


def monitor_backend(process):
    """Monitor backend output and health"""
    startup_complete = False
    last_health_check = time.time()
    
    try:
        while True:
            # Check if process is still running
            if process.poll() is not None:
                print(f"\n❌ Backend process terminated with code {process.returncode}")
                return False
            
            # Read output line by line
            line = process.stdout.readline()
            if line:
                print(line.rstrip())
                
                # Detect successful startup
                if "Backend ready" in line or "Application startup complete" in line:
                    startup_complete = True
                    print("\n✅ Backend startup complete!")
                    print("✅ Backend is now accepting requests")
                    print("=" * 70)
            
            # Periodic health check (every 10 seconds after startup)
            if startup_complete and time.time() - last_health_check > 10:
                if not check_backend_health():
                    print("\n⚠️  Health check failed - backend may be unresponsive")
                last_health_check = time.time()
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping backend...")
        process.terminate()
        try:
            process.wait(timeout=5)
            print("✅ Backend stopped cleanly")
        except subprocess.TimeoutExpired:
            process.kill()
            print("⚠️  Backend force killed")
        return None


def main():
    """Main execution with auto-restart"""
    
    print("\n")
    print("🕊️" * 35)
    print("GHOST PROTOCOL - ROBUST BACKEND STARTER")
    print("🕊️" * 35)
    print()
    print("Features:")
    print("✅ Automatic restart on crash")
    print("✅ Health monitoring")
    print("✅ Output logging")
    print("✅ Clean shutdown (Ctrl+C)")
    print()
    
    restart_count = 0
    max_restarts = 5
    
    while restart_count < max_restarts:
        # Start backend
        process = start_backend()
        
        # Monitor it
        result = monitor_backend(process)
        
        # If None, user stopped it (Ctrl+C)
        if result is None:
            print("\n👋 Backend stopped by user")
            break
        
        # If False, it crashed
        if result is False:
            restart_count += 1
            print(f"\n⚠️  Backend crashed! Restart {restart_count}/{max_restarts}")
            
            if restart_count < max_restarts:
                print("⏳ Restarting in 3 seconds...")
                time.sleep(3)
            else:
                print("\n❌ Maximum restart attempts reached!")
                print("💡 Check logs for errors")
                print("💡 Try: python verify_fixes.py")
                return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
