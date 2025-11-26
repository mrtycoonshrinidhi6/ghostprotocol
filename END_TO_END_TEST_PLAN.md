# 🧪 Ghost Protocol - End-to-End Test Plan

**Version:** 1.0  
**Date:** November 26, 2025

---

## 🎯 TEST OBJECTIVES

1. Verify death detection works with real/mock APIs
2. Validate asset scanning discovers all digital assets
3. Confirm smart contract execution on Polygon testnet
4. Test Memorial Chat with live Gemini
5. Verify observability emits proper logs/traces/metrics
6. Validate frontend displays real backend data

---

## 📋 PRE-TEST SETUP

### Environment Setup
```bash
# 1. Copy environment file
cp .env.example .env

# 2. Add minimum required keys
# GEMINI_API_KEY (for Memorial Chat)
# GOOGLE_SEARCH_API_KEY (optional, can use mock)
# ETHERSCAN_API_KEY (optional, can use mock)

# 3. Install dependencies
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# 4. Verify backend requirements
python -c "import fastapi, uvicorn, google.generativeai; print('✅ All imports successful')"
```

### Start Services
```bash
# Option 1: Automated
python run.py

# Option 2: Manual
# Terminal 1:
cd backend && python api.py

# Terminal 2:
cd frontend && streamlit run app.py
```

**Verify:**
- Backend: http://localhost:8000/health → `{"status": "healthy"}`
- Frontend: http://localhost:8501 → Opens UI
- API Docs: http://localhost:8000/docs → Interactive docs

---

## TEST SUITE 1: DEATH DETECTION

### Test 1.1: Manual Death Detection (Mock Data)

**Steps:**
1. Open frontend: http://localhost:8501
2. Navigate to "⚰️ Death Detection"
3. Select sources: `obituary`, `death_registry`
4. Check "Manual Override"
5. Click "Run Death Detection"

**Expected Output:**
```
Confidence Score: 85-95%
Evidence Found: 2-4 sources
Status: ✓ Death Confirmed
Session ID: Generated UUID
```

**Verify:**
- Evidence cards display obituary + death registry results
- Confidence bar shows visual progress
- "Proceed to Asset Discovery" message appears

**Backend Logs to Check:**
```json
{
  "level": "info",
  "message": "Death detection requested",
  "metadata": {
    "user_id": "user_demo_123",
    "session_id": "<uuid>",
    "sources": ["obituary", "death_registry"]
  }
}
```

**Edge Cases:**
- [ ] Without manual override, confidence < 85% → Warning message
- [ ] No sources selected → Error or default sources
- [ ] Backend offline → Offline banner shown

---

### Test 1.2: Death Detection with Real Google Search

**Prerequisites:**
- `GOOGLE_SEARCH_API_KEY` set in `.env`
- `GOOGLE_SEARCH_ENGINE_ID` configured

**Steps:**
1. Update `agents_realtime.py` line 79-109 with real Google API call
2. Re-run death detection
3. Check actual search results

**Expected:**
- Real Google search results in evidence
- URLs are real (not mock)
- Snippet text from actual search

**Troubleshooting:**
- 403 Error → API key invalid
- 429 Error → Rate limit exceeded
- Empty results → Search engine not configured

---

## TEST SUITE 2: ASSET DISCOVERY

### Test 2.1: Asset Scan (Mock Data)

**Prerequisites:**
- Death must be confirmed first (run Test 1.1)

**Steps:**
1. Navigate to "💼 Asset Discovery"
2. Select all scan types: `email`, `cloud`, `crypto`, `social`
3. Click "Start Asset Scan"
4. Wait 10-30 seconds

**Expected Output:**
```
Total Assets Found: 5-10 assets
Email Accounts: 1 account
Cloud Storage: 2 services (45-60 GB)
Cryptocurrency: 3 wallets ($15,000-$25,000)
Social Media: 0 accounts (mock returns empty)
```

**Verify Tabs:**
- 📧 Email: Table with provider, email, total_emails, last_activity
- ☁️ Cloud: Table with service, file_count, storage_gb
- 🪙 Crypto: Table with chain, address, balance, balance_usd
- 📱 Social: Empty or minimal data

**Backend Logs:**
```json
{
  "level": "info",
  "message": "Asset scan requested",
  "metadata": {
    "scan_types": ["email", "cloud", "crypto", "social"]
  }
}
```

---

### Test 2.2: Asset Scan with Real Blockchain API

**Prerequisites:**
- `ETHERSCAN_API_KEY` in `.env`

**Steps:**
1. Update `realtime_tools.py` BlockchainBalanceTool with real API (see integration guide)
2. Use real wallet address: `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb`
3. Run asset scan

**Expected:**
- Real ETH balance from Etherscan
- Real USD value based on current ETH price
- Token balances if wallet holds ERC-20 tokens

**Verify:**
- Balance matches Etherscan website
- USD conversion is recent (within 5 minutes)
- No mock data indicators

---

## TEST SUITE 3: SMART CONTRACT EXECUTION

### Test 3.1: Mock Contract Execution

**Prerequisites:**
- Death confirmed
- Assets scanned

**Steps:**
1. Navigate to "📜 Smart Contract"
2. Enter beneficiary addresses:
   - Beneficiary 1: `0x742d35Cc...` (50%)
   - Beneficiary 2: `0x1A1zP1e...` (50%)
3. Check gas settings
4. Click "Execute Will on Blockchain"

**Expected Output:**
```
✓ Smart Contract Successfully Deployed
Contract Address: 0x1234567890abcdef
Transaction Hash: 0xabc123...
Gas Used: ~150,000
Status: Execution complete
```

**Verify:**
- Transaction details displayed
- Gas cost shown in MATIC and USD
- "Distribution will occur automatically" message

---

### Test 3.2: Real Polygon Mumbai Testnet Deployment

**Prerequisites:**
- MetaMask or Web3 wallet
- Mumbai testnet MATIC (get from faucet)
- Private key in `.env`

**Steps:**
1. Get testnet MATIC: https://faucet.polygon.technology/
2. Add to `.env`:
   ```
   WALLET_PRIVATE_KEY=your_key
   RPC_URL=https://rpc-mumbai.maticvigil.com
   ```
3. Deploy contract: `python contracts/deploy.py`
4. Copy contract address to `.env`
5. Execute will through frontend

**Expected:**
- Real transaction on Mumbai explorer
- Actual gas cost deducted from wallet
- Contract state changes visible on-chain

**Verify on PolygonScan Mumbai:**
- https://mumbai.polygonscan.com/address/YOUR_CONTRACT_ADDRESS
- Check contract creation transaction
- Verify beneficiary additions
- Check will execution

---

## TEST SUITE 4: MEMORIAL CHAT (GEMINI)

### Test 4.1: Memorial Chat with Gemini API

**Prerequisites:**
- `GEMINI_API_KEY` in `.env`
- Valid Google AI Studio account

**Steps:**
1. Navigate to "🕊️ Memorial Chat"
2. Select recipient: "Son - Michael"
3. Type message: "Dad, I miss you. What advice would you give me?"
4. Click "Send Message"

**Expected Output:**
```
AI Twin Response:
- Warm, parental tone
- References synthetic memory nature
- Emotionally supportive content
- No repetition or looping
```

**Verify:**
- Response appears within 2-5 seconds
- Tone matches selected recipient
- No "I'm an AI" generic responses
- Message added to chat history

**Backend Logs:**
```json
{
  "level": "info",
  "message": "Memorial Twin response generated",
  "metadata": {
    "recipient": "Son - Michael",
    "memories_used": 0-5,
    "response_length": 200-500
  }
}
```

---

### Test 4.2: Memorial Chat Fallback (No API Key)

**Steps:**
1. Remove `GEMINI_API_KEY` from `.env`
2. Restart backend
3. Send memorial chat message

**Expected:**
- Fallback rule-based response used
- Warning logged about missing API key
- Response is still emotionally appropriate
- No errors or crashes

---

## TEST SUITE 5: OBSERVABILITY

### Test 5.1: Structured Logging

**Verify Console Output:**
```json
{
  "timestamp": "2025-11-26T03:52:00Z",
  "level": "info",
  "service": "ghost-protocol-api",
  "message": "Death detection requested",
  "agent_id": "death-api-1",
  "session_id": "abc123",
  "trace_id": "trace_001",
  "metadata": {
    "user_id": "user_demo_123"
  }
}
```

**Check:**
- [ ] All logs are JSON format
- [ ] Timestamps in ISO 8601
- [ ] Service name present
- [ ] Metadata includes context
- [ ] Error logs include error details

---

### Test 5.2: Tracing Spans

**Steps:**
1. Run death detection
2. Check logs for span IDs
3. Verify parent-child relationships

**Expected Log Sequence:**
```
[Span started: death_detection] trace_id=001
  [Span started: obituary_lookup] parent=death_detection
  [Span completed: obituary_lookup] duration=250ms
  [Span started: google_search] parent=death_detection
  [Span completed: google_search] duration=180ms
[Span completed: death_detection] duration=850ms
```

**Verify:**
- [ ] Trace ID propagates through all spans
- [ ] Duration calculated correctly
- [ ] Nested spans show parent relationship

---

### Test 5.3: Metrics Collection

**Check Metrics in Backend:**
```python
# After running tests, check metrics
from backend.api import deps

metrics = deps.metrics
print(metrics.get_all_metrics())
```

**Expected Metrics:**
- `death_detection_accuracy`: 0.85-0.95
- `agent_latency_ms`: 500-3000
- `tool_latency_ms`: 100-500
- `asset_discovery_accuracy`: 0.8-1.0
- `contract_execution_success`: True/False

---

## TEST SUITE 6: FRONTEND/BACKEND INTEGRATION

### Test 6.1: Full Pipeline Integration

**End-to-End Flow:**
1. Death Detection → Confirmed
2. Asset Discovery → Finds assets
3. Memorial Chat → Responds
4. Smart Contract → Executes

**Session State Tracking:**
- [ ] Session ID persists across pages
- [ ] death_confirmed flag enables Asset Discovery
- [ ] death_confirmed flag enables Memorial Chat
- [ ] All API calls include session_id

**Verify State Transitions:**
```
CREATED → MONITORING → DEATH_DETECTED → ASSET_SCANNING → COMPLETED
```

---

### Test 6.2: Error Handling

**Backend Offline Test:**
1. Stop backend: Ctrl+C in backend terminal
2. Try to run death detection from frontend
3. Verify error handling

**Expected:**
- Red "Backend Offline" banner
- Error message: "Backend not reachable"
- No crashes or white screens
- Retry instructions shown

**Backend Error Test:**
1. Start backend
2. Trigger API error (invalid input)
3. Check frontend displays error gracefully

---

### Test 6.3: CORS Validation

**Steps:**
1. Open browser dev tools (F12)
2. Network tab
3. Run death detection
4. Check response headers

**Verify Headers:**
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: POST, GET, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

**No CORS Errors:**
- Check console for CORS-related errors
- All API calls should succeed
- No preflight request failures

---

## 🔧 TROUBLESHOOTING GUIDE

### Issue: Death Detection Confidence Too Low

**Solution:**
- Enable "Manual Override" checkbox
- Add more evidence sources
- Check if mock data is being returned

### Issue: Asset Scan Returns 0 Assets

**Cause:** APIs returning mock empty data

**Solution:**
- Verify wallet addresses are correct
- Check API keys are set
- Review backend logs for errors

### Issue: Memorial Chat No Response

**Causes:**
- Missing GEMINI_API_KEY
- API quota exceeded
- Network timeout

**Solution:**
```bash
# Check API key
echo $GEMINI_API_KEY

# Test Gemini directly
python -c "import google.generativeai as genai; genai.configure(api_key='YOUR_KEY'); print(genai.GenerativeModel('gemini-pro').generate_content('test').text)"
```

### Issue: Frontend Won't Connect to Backend

**Checklist:**
- [ ] Backend running on port 8000
- [ ] Frontend API_BASE_URL correct
- [ ] No firewall blocking localhost
- [ ] CORS enabled in backend
- [ ] Both use same host (localhost vs 127.0.0.1)

---

## ✅ ACCEPTANCE CRITERIA

### Minimum Viable Test Pass

- [ ] Death detection completes without errors
- [ ] Asset scan returns at least mock data
- [ ] Memorial chat responds (Gemini or fallback)
- [ ] Frontend displays all backend responses
- [ ] Logs emit to console in JSON format
- [ ] No crashes or unhandled exceptions

### Production-Ready Test Pass

- [ ] All above + real APIs integrated
- [ ] Gemini API working for Memorial Chat
- [ ] At least one blockchain API (Etherscan) working
- [ ] Google Search API providing real results
- [ ] Smart contract deployed on Mumbai testnet
- [ ] All observability metrics collected
- [ ] Error handling graceful for all failures

---

## 📊 TEST EXECUTION CHECKLIST

**Automated Tests (Future):**
- [ ] Unit tests for each tool
- [ ] Integration tests for each agent
- [ ] E2E tests for full pipeline
- [ ] Performance tests (latency < 5s per agent)
- [ ] Load tests (10 concurrent users)

**Manual Tests (Current):**
- [x] Test 1.1: Death Detection (Mock)
- [ ] Test 1.2: Death Detection (Real Google)
- [x] Test 2.1: Asset Scan (Mock)
- [ ] Test 2.2: Asset Scan (Real Blockchain)
- [x] Test 3.1: Contract (Mock)
- [ ] Test 3.2: Contract (Mumbai)
- [ ] Test 4.1: Memorial Chat (Gemini)
- [x] Test 4.2: Memorial Chat (Fallback)
- [x] Test 5.1: Logging
- [x] Test 5.2: Tracing
- [ ] Test 5.3: Metrics
- [x] Test 6.1: Full Pipeline
- [x] Test 6.2: Error Handling
- [x] Test 6.3: CORS

**Status:** 9/15 tests passing with mock data

---

## 🎯 NEXT STEPS

1. **Immediate (1 hour):**
   - Add Gemini API key
   - Test Memorial Chat with real AI
   - Verify all mock flows work

2. **Short-term (2-4 hours):**
   - Integrate Etherscan API
   - Add CoinGecko for prices
   - Deploy contract to Mumbai

3. **Medium-term (1-2 days):**
   - Add Gmail API for emails
   - Integrate Google Drive
   - Set up automated tests

4. **Production (1 week):**
   - Security audit
   - Rate limiting
   - Production deployment
   - Monitoring dashboard

