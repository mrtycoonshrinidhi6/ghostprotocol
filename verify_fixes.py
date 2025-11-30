import asyncio
import os
import json
import time
from datetime import datetime
from memory_session import InMemorySessionService, SessionState
from agents_realtime import RealtimeDigitalAssetAgent
from realtime_tools import RealtimeToolRegistry

async def verify_memory_persistence():
    print("\n--- Verifying Memory Persistence ---")
    service = InMemorySessionService("test_sessions.json")
    
    # 1. Create Session
    session_id = service.create_session("test_user")
    print(f"Created session: {session_id}")
    
    # 2. Check file existence
    if os.path.exists("test_sessions.json"):
        print("✅ Persistence file created.")
    else:
        print("❌ Persistence file NOT created.")
        return

    # 3. Update State
    service.update_state(session_id, SessionState.MONITORING)
    print("Updated state to MONITORING")
    
    # 4. Load new service instance
    service2 = InMemorySessionService("test_sessions.json")
    session2 = service2.get_session(session_id)
    
    if session2 and session2.state == SessionState.MONITORING:
        print("✅ State persisted and loaded correctly.")
    else:
        print(f"❌ State persistence failed. Got {session2.state if session2 else 'None'}")

    # Cleanup
    os.remove("test_sessions.json")

async def verify_parallelism():
    print("\n--- Verifying DigitalAssetAgent Parallelism ---")
    registry = RealtimeToolRegistry()
    agent = RealtimeDigitalAssetAgent("test-asset-agent", registry)
    
    payload = {
        "user_id": "test_user",
        "wallet_addresses": ["0x123"],
        "primary_email": "test@example.com"
    }
    
    start_time = time.time()
    # Mock tools are fast, but we check if it runs without error and returns expected structure
    result = await agent.execute(payload)
    duration = time.time() - start_time
    
    print(f"Execution time: {duration:.4f}s")
    print(f"Result keys: {result.keys()}")
    
    if "crypto_wallets" in result and "email_accounts" in result:
        print("✅ Agent executed successfully and returned assets.")
    else:
        print("❌ Agent execution failed or returned empty assets.")

async def main():
    await verify_memory_persistence()
    await verify_parallelism()
    print("\nVerification Complete.")

if __name__ == "__main__":
    asyncio.run(main())
