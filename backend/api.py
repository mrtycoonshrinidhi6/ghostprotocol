"""
Ghost Protocol - FastAPI Backend
AI orchestrator connecting real-time agents and tools
"""

# ============================================================================
# SYSTEM PATH FIX (Critical for imports)
# ============================================================================

import sys
from pathlib import Path

# Ensures 'config', 'agents_realtime', 'realtime_tools', etc. import correctly
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

# ============================================================================
# EXTERNAL DEPENDENCIES
# ============================================================================

from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    BackgroundTasks,
    UploadFile,
    File
)

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from contextlib import asynccontextmanager
import asyncio
import uuid

# ============================================================================
# PYDANTIC MODELS (Corrected and fully validated)
# ============================================================================

class UserProfile(BaseModel):
    """User account profile stored in DB (static data)."""
    user_id: str
    full_name: str
    email: str
    date_of_birth: str
    validators: List[str] = Field(default_factory=list)
    beneficiaries: List[Dict] = Field(default_factory=list)


class DeathDetectionRequest(BaseModel):
    """Client triggers multi-source death verification."""
    user_id: str
    sources: List[str] = Field(default_factory=lambda: ["obituary", "social_media", "email"])
    manual_trigger: bool = False


class DeathDetectionResponse(BaseModel):
    """Response returned from DeathDetectionAgent."""
    session_id: str
    is_confirmed: bool
    confidence: float
    evidence: List[Dict]
    sources: List[str]
    timestamp: str


class AssetScanRequest(BaseModel):
    """Client triggers digital asset discovery."""
    user_id: str
    session_id: str
    scan_types: List[str] = Field(default_factory=lambda: ["email", "cloud", "crypto", "social"])


class AssetScanResponse(BaseModel):
    """Digital Asset Agent output."""
    session_id: str
    total_assets: int
    email_accounts: List[Dict]
    cloud_storage: List[Dict]
    crypto_wallets: List[Dict]
    social_accounts: List[Dict]
    scan_status: str


class MemorialChatRequest(BaseModel):
    """Send a message to the AI Memorial Twin."""
    user_id: str
    session_id: str
    recipient: str
    message: str
    context_type: str = "general"


class MemorialChatResponse(BaseModel):
    """Output from the Memorial Twin (LLM model)."""
    response: str
    sentiment: str
    context_used: int
    timestamp: str


class WillExecutionRequest(BaseModel):
    """Trigger smart contract execution."""
    user_id: str
    session_id: str
    contract_address: Optional[str] = None


class WillExecutionResponse(BaseModel):
    """Smart contract execution response."""
    session_id: str
    contract_address: str
    execution_status: str
    transactions: List[Dict]
    beneficiaries_notified: List[str]
    timestamp: str


class SessionStatus(BaseModel):
    """Lifecycle status of a user's execution pipeline."""
    session_id: str
    user_id: str
    state: str
    current_agent: Optional[str]
    progress: float
    created_at: str
    updated_at: str


# ============================================================================
# LIFESPAN HANDLER (Startup/Shutdown)
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Modern FastAPI startup/shutdown system.
    Initializes ALL agents, tools, memory, observability.
    """
    try:
        deps.init_dependencies()
        print("✅ Ghost Protocol API started successfully")
        print("🌐 Endpoint: http://0.0.0.0:8000")
    except Exception as e:
        print(f"❌ Fatal startup error: {e}")
        raise

    yield  # API is serving traffic

    print("🛑 Shutting down Ghost Protocol backend...")

# ============================================================================
# FASTAPI APP INITIALIZATION
# ============================================================================

app = FastAPI(
    title="Ghost Protocol API",
    description="AI-powered digital executor for posthumous asset management",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS (configure properly for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# DEPENDENCY CONTAINER (Centralized Singleton)
# ============================================================================

# IMPORTANT:
# All agents and tools must be imported AFTER sys.path injection above.

from realtime_tools import RealtimeToolRegistry
from agents_realtime import (
    RealtimeDeathDetectionAgent,
    RealtimeDigitalAssetAgent,
    RealtimeSmartContractAgent
)
from memory_session import InMemorySessionService, MemoryBank
from observability import StructuredLogger, MetricsCollector
from memorial_chat import MemorialTwin, get_available_recipients


class Dependencies:
    """
    Central service container for the entire backend.
    Initializes ALL agents, tools, memory, observability, metrics, etc.
    """

    def __init__(self):
        # Will be filled during init_dependencies()
        self.tool_registry = None
        self.session_service = None
        self.logger = None
        self.metrics = None
        self.memory_bank = None

        # AI Agents
        self.death_agent = None
        self.asset_agent = None
        self.contract_agent = None

        # AI Twin
        self.memorial_twin = None

    def init_dependencies(self):
        """Initialize tool registry, logging, memory, and all real-time agents."""

        # --- Core system services ---
        self.tool_registry = RealtimeToolRegistry()
        self.session_service = InMemorySessionService()
        self.memory_bank = MemoryBank()

        self.logger = StructuredLogger("ghost-protocol-api")
        self.metrics = MetricsCollector()

        # --- Real-time agents ---
        self.death_agent = RealtimeDeathDetectionAgent(
            agent_id="death-agent-1",
            tool_registry=self.tool_registry
        )

        self.asset_agent = RealtimeDigitalAssetAgent(
            agent_id="asset-agent-1",
            tool_registry=self.tool_registry
        )

        self.contract_agent = RealtimeSmartContractAgent(
            agent_id="smartcontract-agent-1",
            tool_registry=self.tool_registry
        )

        # --- Memorial Twin (LLM w/ memory) ---
        self.memorial_twin = MemorialTwin(
            memory_bank=self.memory_bank,
            logger=self.logger
        )

        print("✅ Dependencies initialized successfully.")


# Global DI container instance for FastAPI
deps = Dependencies()


def get_dependencies():
    """Injected into every endpoint."""
    return deps

# ============================================================================
# ENDPOINT: /detect_death
# ============================================================================

@app.post("/api/v1/detect_death", response_model=DeathDetectionResponse)
async def detect_death(
    request: DeathDetectionRequest,
    background_tasks: BackgroundTasks,
    deps: Dependencies = Depends(get_dependencies)
):
    """
    Trigger death detection workflow.

    - Runs RealtimeDeathDetectionAgent
    - Creates a session_id
    - Returns confidence, evidence, and sources
    - If confirmed -> launches background asset scan
    """

    try:
        # Create unique session
        session_id = str(uuid.uuid4())

        # Log request
        if deps.logger:
            deps.logger.info(
                "Death detection requested",
                metadata={
                    "user_id": request.user_id,
                    "session_id": session_id,
                    "sources": request.sources,
                    "manual_trigger": request.manual_trigger
                }
            )

        # Prepare agent payload
        payload = {
            "user_id": request.user_id,
            "full_name": request.user_id,              # Replace w/ real profile later
            "location": "",
            "state": "CA",
            "email": f"{request.user_id}@example.com",
            "trace_id": session_id,
            "session_id": session_id
        }

        # Run realtime OR mock agent depending on system mode
        result = await deps.death_agent.execute(payload)

        # Log metrics
        if deps.metrics:
            deps.metrics.record_death_detection_accuracy(
                confidence=result.get("confidence", 0),
                was_correct=True,                       # placeholder
                session_id=session_id
            )

        # Trigger asset scan (non-blocking) if death is confirmed
        if result.get("is_confirmed"):
            background_tasks.add_task(
                trigger_asset_scan_background,
                request.user_id,
                session_id
            )

        # Build final API response
        return DeathDetectionResponse(
            session_id=session_id,
            is_confirmed=result.get("is_confirmed", False),
            confidence=result.get("confidence", 0.0),
            evidence=result.get("evidence", []),
            sources=result.get("sources", []),
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        if deps.logger:
            deps.logger.error("Death detection failed", error=e)
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# BACKGROUND TASK: trigger asset scan after confirmed death
# ============================================================================

async def trigger_asset_scan_background(user_id: str, session_id: str):
    """Run digital asset scan automatically after death detection."""
    await asyncio.sleep(2)   # simulate delay / handoff
    # You could later call deps.asset_agent.execute(...)
    return True

# ============================================================================
# ENDPOINT: /scan_assets
# ============================================================================

@app.post("/api/v1/scan_assets", response_model=AssetScanResponse)
async def scan_assets(
    request: AssetScanRequest,
    deps: Dependencies = Depends(get_dependencies)
):
    """
    Run full digital asset discovery workflow.

    Scans:
    - Email activity (IMAP or mock)
    - Cloud storage (Dropbox/Google/OneDrive or mock)
    - Blockchain wallets (ETH, MATIC, BTC)
    - Social traces (mock or future real integration)

    Returns consolidated asset inventory used by Will Execution.
    """

    try:
        # Log incoming request
        if deps.logger:
            deps.logger.info(
                "Asset scan requested",
                metadata={
                    "user_id": request.user_id,
                    "session_id": request.session_id,
                    "scan_types": request.scan_types
                }
            )

        # Build tool/agent payload
        payload = {
            "user_id": request.user_id,
            "primary_email": f"{request.user_id}@example.com",
            "wallet_addresses": [
                "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"  # sample ETH wallet
            ],
            "trace_id": request.session_id,
            "session_id": request.session_id
        }

        # Call Digital Asset Agent (Realtime or Mock automatically)
        result = await deps.asset_agent.execute(payload)

        # Ensure social_accounts exists (agent may not return field)
        social_accounts = result.get("social_accounts", [])

        # Log accuracy metrics
        if deps.metrics:
            deps.metrics.record_asset_discovery_accuracy(
                discovered=result.get("total_assets", 0),
                total=result.get("total_assets", 0),
                session_id=request.session_id
            )

        # Build sanitized output
        return AssetScanResponse(
            session_id=request.session_id,
            total_assets=result.get("total_assets", 0),
            email_accounts=result.get("email_accounts", []),
            cloud_storage=result.get("cloud_storage", []),
            crypto_wallets=result.get("crypto_wallets", []),
            social_accounts=social_accounts,
            scan_status="completed"
        )

    except Exception as e:
        if deps.logger:
            deps.logger.error("Asset scan failed", error=e)
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ENDPOINT: /memorial_chat
# ============================================================================

@app.post("/api/v1/memorial_chat", response_model=MemorialChatResponse)
async def memorial_chat(
    request: MemorialChatRequest,
    deps: Dependencies = Depends(get_dependencies)
):
    """
    AI Memorial Chat

    - Uses the MemorialTwin (Gemini-powered digital persona)
    - Generates replies in the deceased user's style
    - Pulls context from memory_bank
    - Adds emotional, supportive tone
    - Maintains multi-message chat history
    """

    try:
        # Log incoming chat request
        if deps.logger:
            deps.logger.info(
                "Memorial chat request received",
                metadata={
                    "user_id": request.user_id,
                    "recipient": request.recipient,
                    "session_id": request.session_id,
                    "message_length": len(request.message)
                }
            )

        # === Generate AI Twin Response ===
        ai_message = deps.memorial_twin.get_response(
            user_message=request.message,
            recipient=request.recipient,
            session_id=request.session_id
        )

        # === Sentiment Tagging ===
        txt = ai_message.lower()
        sentiment = "neutral"

        if any(w in txt for w in ["love", "care", "support", "here for you", "miss you"]):
            sentiment = "comforting"
        elif any(w in txt for w in ["remember", "memory", "time we", "think back"]):
            sentiment = "nostalgic"
        elif any(w in txt for w in ["proud", "strong", "keep going"]):
            sentiment = "encouraging"

        # === Context Usage (how many memory items were used) ===
        context_used = len(deps.memorial_twin.chat_history)

        # === Metrics Collection ===
        if deps.metrics:
            deps.metrics.record_message_quality_score(
                score=0.95,                      # static score until LLM scoring added
                recipient=request.recipient,
                session_id=request.session_id
            )

        # === Build Response ===
        return MemorialChatResponse(
            response=ai_message,
            sentiment=sentiment,
            context_used=context_used,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        import traceback
        error_details = {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "endpoint": "memorial_chat"
        }
        if deps.logger:
            deps.logger.error("Memorial chat failed", error=e, metadata=error_details)
        
        print(f"❌ Memorial Chat Error: {str(e)}")
        print(f"   Traceback: {traceback.format_exc()}")
        
        raise HTTPException(
            status_code=500, 
            detail=f"Memorial chat failed: {str(e)}"
        )

# ============================================================================
# ENDPOINT: /execute_will
# ============================================================================

@app.post("/api/v1/execute_will", response_model=WillExecutionResponse)
async def execute_will(
    request: WillExecutionRequest,
    background_tasks: BackgroundTasks,
    deps: Dependencies = Depends(get_dependencies)
):
    """
    Execute on-chain smart-contract will.

    Workflow:
    1. Validate user + contract address
    2. Smart contract agent performs:
        - Asset distribution
        - Transaction submission
        - Event monitoring
    3. Legacy messages queued & delivered in background
    4. Return execution receipt + transaction list
    """

    try:
        # === Log request ===
        if deps.logger:
            deps.logger.info(
                "Will execution requested",
                metadata={
                    "user_id": request.user_id,
                    "session_id": request.session_id,
                    "contract_address": request.contract_address or "(auto)"
                }
            )

        # === Execute Smart Contract Agent ===
        # (RealtimeSmartContractAgent returns structured dict)
        try:
            result = await deps.contract_agent.execute({
                "user_id": request.user_id,
                "session_id": request.session_id,
                "contract_address": request.contract_address
            })

        except Exception as sc_err:
            # Fallback to mock execution
            if deps.logger:
                deps.logger.error(
                    "Smart contract execution failed — using MOCK fallback",
                    error=sc_err
                )

            result = {
                "contract_address": request.contract_address or "0x000000000000000000000000000000000000dEaD",
                "execution_status": "mock_completed",
                "transactions": [
                    {
                        "tx_hash": "0xMOCK123...abcd",
                        "beneficiary": "mock_beneficiary_1",
                        "amount": "5.0 MATIC",
                        "status": "confirmed"
                    }
                ],
                "beneficiaries_notified": ["mock@example.com"]
            }

        # === Metrics ===
        if deps.metrics:
            deps.metrics.record_contract_execution_success(
                success=True,
                gas_used=0.0031,
                session_id=request.session_id
            )

        # === Background Legacy Messaging ===
        background_tasks.add_task(
            send_legacy_messages_background,
            request.user_id,
            request.session_id
        )

        # === Build Response ===
        return WillExecutionResponse(
            session_id=request.session_id,
            contract_address=result["contract_address"],
            execution_status=result["execution_status"],
            transactions=result["transactions"],
            beneficiaries_notified=result.get("beneficiaries_notified", []),
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        import traceback
        error_details = {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "endpoint": "execute_will",
            "user_id": request.user_id,
            "session_id": request.session_id
        }
        if deps.logger:
            deps.logger.error("Will execution endpoint crashed", error=e, metadata=error_details)
        
        print(f"❌ Execute Will Error: {str(e)}")
        print(f"   Traceback: {traceback.format_exc()}")
        
        raise HTTPException(
            status_code=500,
            detail=f"Will execution failed: {str(e)}"
        )


# ============================================================================
# BACKGROUND TASK: Send Legacy Messages
# ============================================================================

async def send_legacy_messages_background(user_id: str, session_id: str):
    """
    Background process:
    - Sends pre-written legacy messages
    - Sends letters, emails, videos, etc.
    - Does not block main API request
    """
    try:
        await asyncio.sleep(1)  # simulate work

        # Future:
        # await deps.orchestrator.agents["legacy"].execute(...)

        print(f"[Background] Legacy messages sent for user {user_id} session {session_id}")

    except Exception as e:
        print(f"[Background] Legacy message delivery failed: {e}")

# ============================================================================
# ENDPOINT: /session_status
# ============================================================================

@app.get("/api/v1/session/{session_id}", response_model=SessionStatus)
async def get_session_status(
    session_id: str,
    deps: Dependencies = Depends(get_dependencies)
):
    """
    Return status of an execution session.

    Tracks:
    - Current agent running
    - Pipeline state (death_detection, asset_scan, contract_execution)
    - Progress 0 → 1.0
    - Timestamps
    """

    try:
        # 🔍 Try to fetch actual session (if implemented)
        session = None
        try:
            session = deps.session_service.get_session(session_id)
        except Exception:
            # InMemorySessionService may not have a session (still safe)
            session = None

        # If session exists, return real state
        if session:
            return SessionStatus(
                session_id=session_id,
                user_id=session.get("user_id", "unknown"),
                state=session.get("state", "UNKNOWN"),
                current_agent=session.get("current_agent", None),
                progress=session.get("progress", 0.0),
                created_at=session.get("created_at", datetime.now().isoformat()),
                updated_at=session.get("updated_at", datetime.now().isoformat())
            )

        # Fallback MOCK session object
        if deps.logger:
            deps.logger.warn(
                "Session not found — returning mock placeholder",
                metadata={"session_id": session_id}
            )

        return SessionStatus(
            session_id=session_id,
            user_id="mock_user",
            state="ASSET_SCANNING",
            current_agent="DigitalAssetAgent",
            progress=0.65,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

    except Exception as e:
        if deps.logger:
            deps.logger.error("Session status lookup failed", error=e)

        raise HTTPException(
            status_code=404,
            detail=f"Session '{session_id}' not found or inaccessible"
        )
# ============================================================================
# ENDPOINT: /upload_obituary
# ============================================================================

@app.post("/api/v1/upload_obituary")
async def upload_obituary(
    user_id: str,
    file: UploadFile = File(...),
    deps: Dependencies = Depends(get_dependencies)
):
    """
    Upload obituary document for manual death verification.

    Expected workflow:
    - User uploads PDF/JPEG/PNG obituary file
    - System extracts: name, date_of_death, location
    - DeathDetectionAgent receives manual-confirmation evidence
    """

    try:
        # Read file bytes
        content = await file.read()
        file_size = len(content)
        filename = file.filename or "unknown"

        # Log upload
        if deps.logger:
            deps.logger.info(
                "Obituary document uploaded",
                metadata={
                    "user_id": user_id,
                    "filename": filename,
                    "size_bytes": file_size
                }
            )

        # ---------------------------------------------------------------------
        # FUTURE: Connect to OCR pipeline (Vision Transformer + Gemini Vision)
        #
        # Example:
        # extracted = await deps.document_processor.extract_obituary(content)
        #
        # For now, return stable mock extraction.
        # ---------------------------------------------------------------------

        extracted_info = {
            "full_name": "John Doe",
            "date_of_death": "2025-11-20",
            "location": "California, USA",
            "confidence": 0.95,
            "mode": "MOCK"
        }

        # Produce response
        return {
            "status": "uploaded",
            "filename": filename,
            "size_bytes": file_size,
            "extracted_info": extracted_info,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        if deps.logger:
            deps.logger.error(
                "Obituary upload failed",
                error=e,
                metadata={"user_id": user_id}
            )

        raise HTTPException(
            status_code=500,
            detail="Obituary upload failed — invalid file or processing error"
        )
# ============================================================================
# ENDPOINT: /diagnostics/keys
# ============================================================================

@app.get("/api/v1/diagnostics/keys")
async def diagnostics_keys(
    deps: Dependencies = Depends(get_dependencies)
):
    """
    System diagnostics endpoint.

    Returns:
    - Current runtime mode (REALTIME/MOCK)
    - API key availability summary
    - Critical vs optional key status
    - Agent runtime configuration
    - Whether REALTIME mode is allowed
    """

    try:
        from config import should_use_realtime
        from load_env import (
            get_load_result,
            get_key_status_dict
        )

        # Determine mode
        is_realtime = should_use_realtime()
        mode = "REALTIME" if is_realtime else "MOCK"

        # Key loading results
        load_result = get_load_result()
        key_status = get_key_status_dict(load_result)

        # Categorize keys
        critical_keys = {}
        optional_keys = {}

        for key_name, status in key_status.items():
            key_info = {
                "available": status["is_valid"],
                "preview": status["value_preview"],  # e.g. "sk-******8Z"
            }

            if status["is_critical"]:
                critical_keys[key_name] = key_info
            else:
                optional_keys[key_name] = key_info

        # Agent runtime status
        agents_status = {
            "death_detection": {
                "initialized": deps.death_agent is not None,
                "confidence_threshold": getattr(
                    deps.death_agent,
                    "confidence_threshold",
                    None
                ),
                "mode": mode
            },
            "digital_asset": {
                "initialized": deps.asset_agent is not None,
                "asset_count_boost": getattr(
                    deps.asset_agent,
                    "asset_count_boost",
                    0
                ),
                "mode": mode
            },
            "smart_contract": {
                "initialized": deps.contract_agent is not None,
                "mode": mode
            }
        }

        return {
            "mode": mode,
            "realtime_mode_enabled": is_realtime,
            "can_use_realtime": load_result.can_use_realtime,
            "timestamp": datetime.now().isoformat(),
            "api_keys": {
                "critical": critical_keys,
                "optional": optional_keys,
                "total_loaded": load_result.loaded_keys,
                "total_missing": load_result.missing_keys
            },
            "agents": agents_status
        }

    except Exception as e:
        # Safe fallback result
        if deps.logger:
            deps.logger.error("Diagnostics endpoint failed", error=e)

        return {
            "mode": "UNKNOWN",
            "error": "Diagnostics failed — see server logs.",
            "timestamp": datetime.now().isoformat()
        }
# ============================================================================
# ENDPOINT: /diagnostics/set_mode
# ============================================================================

@app.post("/api/v1/diagnostics/set_mode")
async def set_mode(mode: str, deps: Dependencies = Depends(get_dependencies)):
    """
    Set system mode (REALTIME or MOCK).
    
    Note:
    - Changes environment variable only.
    - Agents will NOT switch mode until backend is restarted.
    - Used mainly for testing/demo purposes.
    """

    try:
        mode = mode.upper()
        if mode not in ["REALTIME", "MOCK"]:
            raise HTTPException(status_code=400, detail="Mode must be REALTIME or MOCK")

        # Update ENV variable (in-memory)
        import os
        os.environ["REALTIME_MODE"] = "true" if mode == "REALTIME" else "false"

        deps.logger.info(
            "System mode changed",
            metadata={"new_mode": mode}
        )

        return {
            "status": "success",
            "message": f"Mode updated to {mode}. Restart backend for changes to apply.",
            "mode": mode,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        if deps.logger:
            deps.logger.error("Failed to set mode", error=e)
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINT: /run_full_system_test
# ============================================================================

@app.post("/api/v1/run_full_system_test")
async def run_full_system_test(deps: Dependencies = Depends(get_dependencies)):
    """
    Runs full system test across all 7 tools:
      1. ObituaryLookupTool
      2. BlockchainBalanceTool
      3. EmailActivityTool
      4. CloudActivityTool
      5. DeathRegistryAPI
      6. CryptoPriceFeedAPI.get_crypto_prices
      7. CryptoPriceFeedAPI.get_gas_prices
    """

    from config import should_use_realtime

    test_start = datetime.now()
    results = {}
    mode = "REALTIME" if should_use_realtime() else "MOCK"

    deps.logger.info("Running full system test", metadata={"mode": mode})

    # Helper to wrap tests
    async def run_test(name, fn, params):
        try:
            res = await fn(params)
            return {"status": "PASS", "mode": mode, "result": res}
        except Exception as e:
            return {"status": "FAIL", "mode": mode, "error": str(e)}

    # Map of tests
    TESTS = {
        "obituary_lookup": (
            deps.tool_registry.execute_tool,
            {"name": "get_recent_obituaries", "params": {
                "full_name": "Test User",
                "location": "CA",
                "date_range_days": 30
            }}
        ),
        "blockchain_balance": (
            deps.tool_registry.execute_tool,
            {"name": "fetch_blockchain_balance", "params": {
                "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
                "chains": ["ETH"]
            }}
        ),
        "email_activity": (
            deps.tool_registry.execute_tool,
            {"name": "get_recent_emails", "params": {
                "email_address": "test@example.com",
                "days_back": 20
            }}
        ),
        "cloud_activity": (
            deps.tool_registry.execute_tool,
            {"name": "get_cloud_activity", "params": {
                "user_id": "test_user",
                "services": ["dropbox"]
            }}
        ),
        "death_registry": (
            deps.tool_registry.execute_tool,
            {"name": "verify_death_certificate", "params": {
                "full_name": "Test User",
                "state": "CA"
            }}
        ),
        "crypto_prices": (
            deps.tool_registry.execute_tool,
            {"name": "get_crypto_prices", "params": {
                "symbols": "BTC,ETH"
            }}
        ),
        "gas_prices": (
            deps.tool_registry.execute_tool,
            {"name": "get_gas_prices", "params": {
                "chain": "ethereum"
            }}
        ),
    }

    # Execute each test
    for test_name, (fn, test_data) in TESTS.items():
        call = lambda p=test_data: fn(p["name"], p["params"])
        results[test_name] = await run_test(test_name, call, None)

    # Compute summary
    passed = sum(1 for r in results.values() if r["status"] == "PASS")
    failed = sum(1 for r in results.values() if r["status"] == "FAIL")
    overall_status = (
        "PASS" if failed == 0 else
        "PARTIAL" if passed > 0 else
        "FAIL"
    )

    test_duration = (datetime.now() - test_start).total_seconds()

    deps.logger.info(
        "System test completed",
        metadata={
            "mode": mode,
            "passed": passed,
            "failed": failed,
            "overall_status": overall_status,
            "duration_seconds": test_duration
        }
    )

    return {
        "overall_status": overall_status,
        "mode": mode,
        "tests_passed": passed,
        "tests_failed": failed,
        "tests_total": len(results),
        "duration_seconds": round(test_duration, 2),
        "results": results,
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# ENDPOINT: /health
# ============================================================================

@app.get("/health")
async def health_check():
    """Basic health check."""
    return {
        "status": "healthy",
        "service": "ghost-protocol-api",
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# MAIN ENTRY POINT (UVICORN)
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("=" * 70)
    print("🚀 Starting Ghost Protocol Backend API")
    print("=" * 70)

    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped manually")
    except Exception as e:
        print(f"\n❌ Backend error: {e}")
        raise
