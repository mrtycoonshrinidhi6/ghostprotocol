"""
Ghost Protocol - System Test Script
Quick way to test all 7 tools from command line (Windows compatible)
"""

import requests
import json
import sys
from datetime import datetime


def test_system():
    """Run full system test"""
    
    print("=" * 70)
    print("🧪 GHOST PROTOCOL - SYSTEM TEST")
    print("=" * 70)
    print()
    
    # Check if backend is running
    print("📡 Checking backend connection...", end="", flush=True)
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print(" ✅ Backend online")
        else:
            print(f" ❌ Backend returned {response.status_code}")
            return False
    except requests.ConnectionError:
        print(" ❌ Backend not running!")
        print("\n💡 Start backend first:")
        print("   python backend/api.py")
        print("   OR")
        print("   python run.py")
        return False
    except Exception as e:
        print(f" ❌ Error: {e}")
        return False
    
    # Run system test
    print("\n🔍 Testing all 7 tools...\n")
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/run_full_system_test",
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        # Display results
        print("=" * 70)
        print(f"OVERALL STATUS: {result['overall_status']}")
        print("=" * 70)
        print()
        print(f"📊 Results: {result['tests_passed']}/{result['tests_total']} passed ({result['pass_rate']}%)")
        print(f"⏱️  Duration: {result['duration_seconds']}s")
        print(f"🔧 Mode: {result['mode']}")
        print()
        
        # Show individual results
        print("=" * 70)
        print("INDIVIDUAL TOOL RESULTS:")
        print("=" * 70)
        
        for tool_name, tool_result in result['results'].items():
            status_icon = "✅" if tool_result['status'] == "PASS" else "❌"
            mode = tool_result.get('mode', 'N/A')
            
            print(f"\n{status_icon} {tool_name.upper().replace('_', ' ')}")
            print(f"   Status: {tool_result['status']}")
            print(f"   Mode:   {mode}")
            
            if tool_result['status'] == "PASS":
                # Show success details
                if 'sources_searched' in tool_result:
                    print(f"   Sources: {tool_result['sources_searched']}")
                if 'total_found' in tool_result:
                    print(f"   Found: {tool_result['total_found']}")
                if 'chains_checked' in tool_result:
                    print(f"   Chains: {tool_result['chains_checked']}")
                if 'total_count' in tool_result:
                    print(f"   Count: {tool_result['total_count']}")
                if 'prices_fetched' in tool_result:
                    print(f"   Prices: {tool_result['prices_fetched']}")
                if 'safe' in tool_result:
                    print(f"   Gas: {tool_result['safe']}/{tool_result['standard']}/{tool_result['fast']} gwei")
            else:
                # Show error
                if 'error' in tool_result:
                    print(f"   Error: {tool_result['error']}")
        
        # Summary
        print("\n" + "=" * 70)
        print("SUMMARY BY TYPE:")
        print("=" * 70)
        print(f"MCP Tools:    {result['summary']['mcp_tools']['passed']}/{result['summary']['mcp_tools']['tested']} passed")
        print(f"OpenAPI Tools: {result['summary']['openapi_tools']['passed']}/{result['summary']['openapi_tools']['tested']} passed")
        print()
        
        # Final verdict
        if result['overall_status'] == "PASS":
            print("🎉 ALL TESTS PASSED - SYSTEM IS HEALTHY! 🎉")
            return True
        elif result['overall_status'] == "PARTIAL":
            print("⚠️  PARTIAL SUCCESS - SOME TOOLS FAILED")
            print("\n💡 This is normal if:")
            print("   - Running in MOCK mode (all should pass)")
            print("   - Running in REALTIME mode without all API keys (expected)")
            return True
        else:
            print("❌ ALL TESTS FAILED - SYSTEM ISSUES DETECTED")
            return False
    
    except requests.Timeout:
        print("❌ Request timed out after 30s")
        print("\n💡 System may be overloaded or stuck")
        return False
    except requests.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_diagnostics():
    """Get system diagnostics"""
    
    print("\n" + "=" * 70)
    print("🔧 SYSTEM DIAGNOSTICS")
    print("=" * 70)
    print()
    
    try:
        response = requests.get("http://localhost:8000/api/v1/diagnostics/keys", timeout=5)
        response.raise_for_status()
        diag = response.json()
        
        print(f"Mode: {diag['mode']}")
        print(f"Realtime Enabled: {diag['realtime_mode_enabled']}")
        print(f"Can Use Realtime: {diag['can_use_realtime']}")
        print()
        
        api_keys = diag['api_keys']
        print(f"API Keys: {api_keys['total_loaded']}/{api_keys['total_loaded'] + api_keys['total_missing']}")
        print()
        
        # Critical keys
        print("Critical Keys:")
        for key_name, status in api_keys.get('critical', {}).items():
            icon = "✅" if status['available'] else "❌"
            print(f"  {icon} {key_name}")
        
        # Agents
        print("\nAgents:")
        for agent_name, agent_info in diag['agents'].items():
            icon = "✅" if agent_info['initialized'] else "❌"
            mode = agent_info.get('mode', 'N/A')
            print(f"  {icon} {agent_name} (Mode: {mode})")
        
        return True
    
    except Exception as e:
        print(f"❌ Could not fetch diagnostics: {e}")
        return False


def main():
    """Main execution"""
    
    # Run system test
    test_passed = test_system()
    
    # Show diagnostics
    test_diagnostics()
    
    print("\n" + "=" * 70)
    
    if test_passed:
        print("✅ System test completed successfully")
        print("=" * 70)
        print()
        return 0
    else:
        print("❌ System test completed with issues")
        print("=" * 70)
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
