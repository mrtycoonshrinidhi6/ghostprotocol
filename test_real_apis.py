"""
Test script for real API integrations
Run this to verify your API keys are working correctly
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 70)
print("🔍 Ghost Protocol - API Integration Test")
print("=" * 70)
print()


# ============================================================================
# TEST 1: Gemini AI (Memorial Chat)
# ============================================================================

async def test_gemini():
    """Test Gemini AI API"""
    print("TEST 1: Gemini AI")
    print("-" * 70)
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env")
        print("   Get your key from: https://makersuite.google.com/app/apikey")
        return False
    
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")
        
        response = model.generate_content("Say 'Hello from Ghost Protocol!' in a warm, comforting tone.")
        
        print(f"✅ Gemini API is working!")
        print(f"   Response: {response.text[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return False


# ============================================================================
# TEST 2: CoinGecko (Crypto Prices) - FREE, NO KEY NEEDED
# ============================================================================

async def test_coingecko():
    """Test CoinGecko API (free, no key required)"""
    print("\nTEST 2: CoinGecko (Crypto Prices)")
    print("-" * 70)
    
    try:
        import httpx
        
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,ethereum,matic-network",
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                print("✅ CoinGecko API is working!")
                print(f"   BTC Price: ${data['bitcoin']['usd']:,.2f}")
                print(f"   ETH Price: ${data['ethereum']['usd']:,.2f}")
                print(f"   MATIC Price: ${data['matic-network']['usd']:.4f}")
                return True
            else:
                print(f"❌ CoinGecko API returned status {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ CoinGecko API error: {e}")
        return False


# ============================================================================
# TEST 3: Etherscan (Blockchain Balance)
# ============================================================================

async def test_etherscan():
    """Test Etherscan API"""
    print("\nTEST 3: Etherscan (Blockchain Balance)")
    print("-" * 70)
    
    api_key = os.getenv("ETHERSCAN_API_KEY")
    
    if not api_key:
        print("⚠️  ETHERSCAN_API_KEY not found in .env (optional)")
        print("   Get your key from: https://etherscan.io/myapikey")
        print("   Skipping test...")
        return None
    
    try:
        import httpx
        
        # Test with Ethereum Foundation address
        test_address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
        
        url = "https://api.etherscan.io/api"
        params = {
            "module": "account",
            "action": "balance",
            "address": test_address,
            "tag": "latest",
            "apikey": api_key
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            if data["status"] == "1":
                balance_wei = int(data["result"])
                balance_eth = balance_wei / 1e18
                
                print("✅ Etherscan API is working!")
                print(f"   Test Address: {test_address[:10]}...")
                print(f"   Balance: {balance_eth:.6f} ETH")
                return True
            else:
                print(f"❌ Etherscan API error: {data.get('message', 'Unknown error')}")
                return False
                
    except Exception as e:
        print(f"❌ Etherscan API error: {e}")
        return False


# ============================================================================
# TEST 4: Google Custom Search
# ============================================================================

async def test_google_search():
    """Test Google Custom Search API"""
    print("\nTEST 4: Google Custom Search")
    print("-" * 70)
    
    api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
    engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    
    if not api_key or not engine_id:
        print("⚠️  GOOGLE_SEARCH_API_KEY or ENGINE_ID not found (optional)")
        print("   Setup: https://console.cloud.google.com/")
        print("   Engine: https://programmablesearchengine.google.com/")
        print("   Skipping test...")
        return None
    
    try:
        import httpx
        
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": engine_id,
            "q": "obituary test search",
            "num": 3
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            if "items" in data:
                print("✅ Google Search API is working!")
                print(f"   Found {len(data['items'])} results")
                print(f"   First result: {data['items'][0]['title'][:50]}...")
                return True
            else:
                print(f"❌ Google Search API error: {data.get('error', {}).get('message', 'Unknown error')}")
                return False
                
    except Exception as e:
        print(f"❌ Google Search API error: {e}")
        return False


# ============================================================================
# TEST 5: Backend Health Check
# ============================================================================

async def test_backend():
    """Test if backend is running"""
    print("\nTEST 5: Backend Health Check")
    print("-" * 70)
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8000/health")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Backend is running!")
                print(f"   Status: {data.get('status', 'unknown')}")
                print(f"   Service: {data.get('service', 'unknown')}")
                return True
            else:
                print(f"❌ Backend returned status {response.status_code}")
                return False
                
    except Exception as e:
        print("❌ Backend is not running")
        print("   Start it with: python run.py")
        return False


# ============================================================================
# RUN ALL TESTS
# ============================================================================

async def run_all_tests():
    """Run all API tests"""
    
    results = {
        "Gemini AI": await test_gemini(),
        "CoinGecko": await test_coingecko(),
        "Etherscan": await test_etherscan(),
        "Google Search": await test_google_search(),
        "Backend": await test_backend()
    }
    
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    skipped = sum(1 for r in results.values() if r is None)
    
    for name, result in results.items():
        if result is True:
            print(f"✅ {name:<20} PASS")
        elif result is False:
            print(f"❌ {name:<20} FAIL")
        else:
            print(f"⚠️  {name:<20} SKIPPED (optional)")
    
    print()
    print(f"Passed: {passed}/5")
    print(f"Failed: {failed}/5")
    print(f"Skipped: {skipped}/5 (optional)")
    print()
    
    if passed >= 2:  # Gemini + CoinGecko minimum
        print("🎉 MINIMUM APIs are working! You can run the demo.")
        print("   Memorial Chat will work with real AI responses.")
        print("   Crypto prices will be real-time.")
    elif passed >= 1:
        print("⚠️  Some APIs are working, but add more for full functionality.")
        print("   Priority: Add GEMINI_API_KEY for Memorial Chat")
    else:
        print("❌ Critical APIs not configured.")
        print("   Action: Add GEMINI_API_KEY to .env")
    
    print()
    print("Next steps:")
    print("1. Fix any failed tests (add API keys to .env)")
    print("2. Run: python run.py")
    print("3. Open: http://localhost:8501")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
