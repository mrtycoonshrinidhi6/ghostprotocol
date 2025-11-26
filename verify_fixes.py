"""
Ghost Protocol - Verification Script
Tests that all critical fixes were applied correctly
"""

import sys

def test_imports():
    """Test that all imports work correctly"""
    print("=" * 70)
    print("TEST 1: Verifying Imports")
    print("=" * 70)
    
    try:
        from config import (
            REALTIME_CONFIDENCE_THRESHOLD,
            MOCK_CONFIDENCE_THRESHOLD,
            MOCK_ASSET_COUNT_BOOST,
            should_use_realtime,
            get_confidence_threshold
        )
        print("✅ All config imports successful")
        print(f"   - REALTIME_CONFIDENCE_THRESHOLD = {REALTIME_CONFIDENCE_THRESHOLD}")
        print(f"   - MOCK_CONFIDENCE_THRESHOLD = {MOCK_CONFIDENCE_THRESHOLD}")
        print(f"   - MOCK_ASSET_COUNT_BOOST = {MOCK_ASSET_COUNT_BOOST}")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_config_functions():
    """Test config helper functions"""
    print("\n" + "=" * 70)
    print("TEST 2: Verifying Config Functions")
    print("=" * 70)
    
    try:
        from config import (
            get_current_mode,
            should_use_realtime,
            get_confidence_threshold,
            get_mock_latency
        )
        
        mode = get_current_mode()
        use_realtime = should_use_realtime()
        threshold = get_confidence_threshold()
        latency = get_mock_latency()
        
        print(f"✅ All config functions work")
        print(f"   - Current mode: {mode}")
        print(f"   - Use realtime: {use_realtime}")
        print(f"   - Confidence threshold: {threshold}")
        print(f"   - Mock latency range: {latency}")
        return True
    except Exception as e:
        print(f"❌ Function test failed: {e}")
        return False


def test_agent_imports():
    """Test that agents can import their dependencies"""
    print("\n" + "=" * 70)
    print("TEST 3: Verifying Agent Dependencies")
    print("=" * 70)
    
    try:
        # Test Death Detection Agent imports
        from config import should_use_realtime, REALTIME_CONFIDENCE_THRESHOLD, MOCK_CONFIDENCE_THRESHOLD
        print("✅ DeathDetectionAgent imports OK")
        
        # Test Digital Asset Agent imports
        from config import MOCK_ASSET_COUNT_BOOST
        print("✅ DigitalAssetAgent imports OK")
        
        # Test Smart Contract Agent imports
        from config import should_use_realtime
        print("✅ SmartContractAgent imports OK")
        
        return True
    except ImportError as e:
        print(f"❌ Agent import failed: {e}")
        return False


def test_agent_initialization():
    """Test that agents can be initialized"""
    print("\n" + "=" * 70)
    print("TEST 4: Verifying Agent Initialization")
    print("=" * 70)
    
    try:
        from agents_realtime import (
            RealtimeDeathDetectionAgent,
            RealtimeDigitalAssetAgent,
            RealtimeSmartContractAgent,
            RealtimeLoopAgent
        )
        from realtime_tools import RealtimeToolRegistry
        
        # Create tool registry
        tools = RealtimeToolRegistry()
        
        # Test each agent
        death_agent = RealtimeDeathDetectionAgent("test-death-1", tools)
        print(f"✅ DeathDetectionAgent initialized")
        print(f"   - Mode: {'REALTIME' if death_agent.is_realtime_mode else 'MOCK'}")
        print(f"   - Confidence threshold: {death_agent.confidence_threshold}")
        
        asset_agent = RealtimeDigitalAssetAgent("test-asset-1", tools)
        print(f"✅ DigitalAssetAgent initialized")
        print(f"   - Mode: {'REALTIME' if asset_agent.is_realtime_mode else 'MOCK'}")
        print(f"   - Asset count boost: {asset_agent.asset_count_boost}")
        
        contract_agent = RealtimeSmartContractAgent("test-contract-1", tools)
        print(f"✅ SmartContractAgent initialized")
        print(f"   - Mode: {'REALTIME' if contract_agent.is_realtime_mode else 'MOCK'}")
        
        loop_agent = RealtimeLoopAgent("test-loop-1", tools)
        print(f"✅ LoopAgent initialized")
        print(f"   - Mode: {'REALTIME' if loop_agent.is_realtime_mode else 'MOCK'}")
        
        return True
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_consistency():
    """Test that values are consistent"""
    print("\n" + "=" * 70)
    print("TEST 5: Verifying Value Consistency")
    print("=" * 70)
    
    try:
        from config import (
            REALTIME_CONFIDENCE_THRESHOLD,
            MOCK_CONFIDENCE_THRESHOLD,
            MOCK_ASSET_COUNT_BOOST,
            get_confidence_threshold,
            should_use_realtime
        )
        
        # Check confidence threshold function matches constants
        expected_threshold = REALTIME_CONFIDENCE_THRESHOLD if should_use_realtime() else MOCK_CONFIDENCE_THRESHOLD
        actual_threshold = get_confidence_threshold()
        
        if expected_threshold == actual_threshold:
            print("✅ Confidence threshold function consistent")
            print(f"   - Expected: {expected_threshold}")
            print(f"   - Actual: {actual_threshold}")
        else:
            print(f"❌ Threshold mismatch: {expected_threshold} != {actual_threshold}")
            return False
        
        # Check types
        if isinstance(REALTIME_CONFIDENCE_THRESHOLD, float):
            print("✅ REALTIME_CONFIDENCE_THRESHOLD is float")
        else:
            print(f"❌ REALTIME_CONFIDENCE_THRESHOLD should be float, got {type(REALTIME_CONFIDENCE_THRESHOLD)}")
            return False
        
        if isinstance(MOCK_CONFIDENCE_THRESHOLD, float):
            print("✅ MOCK_CONFIDENCE_THRESHOLD is float")
        else:
            print(f"❌ MOCK_CONFIDENCE_THRESHOLD should be float, got {type(MOCK_CONFIDENCE_THRESHOLD)}")
            return False
        
        if isinstance(MOCK_ASSET_COUNT_BOOST, int):
            print("✅ MOCK_ASSET_COUNT_BOOST is int")
        else:
            print(f"❌ MOCK_ASSET_COUNT_BOOST should be int, got {type(MOCK_ASSET_COUNT_BOOST)}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Consistency check failed: {e}")
        return False


def main():
    """Run all verification tests"""
    print("\n")
    print("🔍" * 35)
    print("GHOST PROTOCOL - VERIFICATION SCRIPT")
    print("Testing Critical Fixes")
    print("🔍" * 35)
    print("\n")
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Config Functions", test_config_functions()))
    results.append(("Agent Dependencies", test_agent_imports()))
    results.append(("Agent Initialization", test_agent_initialization()))
    results.append(("Value Consistency", test_consistency()))
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("=" * 70)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - SYSTEM IS READY! 🎉\n")
        return 0
    else:
        print(f"\n⚠️  {total - passed} TEST(S) FAILED - REVIEW NEEDED ⚠️\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
