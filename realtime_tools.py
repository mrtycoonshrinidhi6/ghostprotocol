"""
Ghost Protocol - Real-Time Data Tools (ACTIVE REGISTRY)

This is the ACTIVE tool registry used by agents_realtime.py
Contains MCP, OpenAPI, and Built-in tool definitions.

DO NOT USE tools_layer.py - that is legacy/deprecated.
All new tools should be added here.
All agents use RealtimeToolRegistry from this file.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio
import os
import httpx

# Load environment variables (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# ============================================================================
# MCP TOOLS (Model Context Protocol)
# ============================================================================

@dataclass
class MCPToolSchema:
    """Standard MCP tool schema"""
    name: str
    description: str
    parameters: Dict[str, Any]
    returns: Dict[str, Any]


# ----------------------------------------------------------------------------
# OBITUARY LOOKUP TOOL
# ----------------------------------------------------------------------------

class ObituaryLookupTool:
    """MCP Tool: Real-time obituary search"""

    schema = MCPToolSchema(
        name="get_recent_obituaries",
        description="Search recent obituaries from multiple sources (Legacy.com, Tributes.com, newspapers)",
        parameters={
            "full_name": {"type": "string", "required": True},
            "location": {"type": "string", "required": False},
            "date_range_days": {"type": "integer", "default": 30},
            "sources": {"type": "array", "items": "string", "default": ["legacy", "tributes", "newspapers"]},
        },
        returns={
            "obituaries": {"type": "array"},
            "total_found": {"type": "integer"},
            "sources_searched": {"type": "array"},
        }
    )

    async def execute(self, params: Dict) -> Dict:
        """Execute obituary lookup with REALTIME/MOCK mode support"""
        from config import should_use_realtime, EMIT_TOOL_TRACES
        from load_env import is_key_available, get_api_key
        from mock_generators import mock_obituary
        import time

        start_time = time.time()
        mode = "REALTIME" if should_use_realtime() else "MOCK"

        # REALTIME PATH
        if should_use_realtime() and is_key_available("NEWS_API_KEY"):
            try:
                api_key = get_api_key("NEWS_API_KEY")
                full_name = params["full_name"]

                url = "https://newsapi.org/v2/everything"
                api_params = {
                    "q": f"obituary {full_name}",
                    "apiKey": api_key,
                    "pageSize": 10,
                    "sortBy": "relevancy",
                }

                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.get(url, params=api_params)

                    if response.status_code == 200:
                        data = response.json()
                        obituaries = []

                        # Transform into Ghost Protocol unified format
                        for article in data.get("articles", [])[:5]:
                            obituaries.append({
                                "source": article.get("source", {}).get("name", "news"),
                                "url": article.get("url", ""),
                                "full_name": full_name,
                                "date_of_death": article.get("publishedAt", "")[:10],
                                "location": params.get("location", "Unknown"),
                                "confidence": 0.75,
                                "snippet": article.get("description", "")[:250],
                            })

                        elapsed_ms = int((time.time() - start_time) * 1000)
                        if EMIT_TOOL_TRACES:
                            print(f"  [REALTIME] obituary_lookup: {elapsed_ms}ms, found={len(obituaries)}")

                        return {
                            "obituaries": obituaries,
                            "total_found": len(obituaries),
                            "search_query": full_name,
                            "location_filter": params.get("location", ""),
                            "mode": "REALTIME",
                            "timestamp": datetime.now().isoformat(),
                        }

            except Exception as e:
                if os.getenv("LOG_REALTIME_ERRORS", "true").lower() == "true":
                    print(f"[ERROR] Obituary lookup failed: {e}")
                    print("[FALLBACK] Switching to mock")

                mode = "MOCK_FALLBACK"

        # MOCK PATH
        result = await mock_obituary(
            full_name=params["full_name"],
            location=params.get("location", "CA")
        )
        result["mode"] = mode

        elapsed_ms = int((time.time() - start_time) * 1000)
        if EMIT_TOOL_TRACES:
            print(f"  [{mode}] obituary_lookup: {elapsed_ms}ms")

        return result


# ----------------------------------------------------------------------------
# BLOCKCHAIN BALANCE TOOL
# ----------------------------------------------------------------------------

class BlockchainBalanceTool:
    """MCP Tool: Fetch real-time blockchain balances"""

    schema = MCPToolSchema(
        name="fetch_blockchain_balance",
        description="Get real-time cryptocurrency balance for a wallet address",
        parameters={
            "address": {"type": "string", "required": True},
            "chains": {"type": "array", "items": "string", "default": ["ETH", "BTC", "MATIC"]},
            "include_tokens": {"type": "boolean", "default": True},
        },
        returns={
            "balances": {"type": "array"},
            "total_usd": {"type": "float"},
            "block_height": {"type": "integer"},
        }
    )

    async def execute(self, params: Dict) -> Dict:
        """Execute blockchain balance check with REALTIME/MOCK mode support"""
        from config import should_use_realtime, EMIT_TOOL_TRACES
        from load_env import is_key_available, get_api_key
        from mock_generators import mock_blockchain_balance
        import time

        start_time = time.time()
        mode = "REALTIME" if should_use_realtime() else "MOCK"

        address = params["address"]
        chains = params.get("chains", ["ETH", "MATIC"])

        # REALTIME PATH
        if should_use_realtime() and "ETH" in chains and is_key_available("ETHERSCAN_API_KEY"):
            try:
                etherscan_key = get_api_key("ETHERSCAN_API_KEY")
                url = "https://api.etherscan.io/api"

                api_params = {
                    "module": "account",
                    "action": "balance",
                    "address": address,
                    "tag": "latest",
                    "apikey": etherscan_key,
                }

                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.get(url, params=api_params)

                    if response.status_code == 200:
                        data = response.json()

                        if data["status"] == "1":
                            balance_wei = int(data["result"])
                            balance_eth = balance_wei / 1e18

                            # Fetch ETH price from CoinGecko (no key required)
                            price_url = "https://api.coingecko.com/api/v3/simple/price"
                            price_params = {"ids": "ethereum", "vs_currencies": "usd"}

                            price_response = await client.get(price_url, params=price_params)
                            eth_price = price_response.json()["ethereum"]["usd"]

                            balances = [{
                                "chain": "ETH",
                                "address": address,
                                "balance": balance_eth,
                                "balance_usd": balance_eth * eth_price,
                                "tokens": [],
                            }]

                            elapsed_ms = int((time.time() - start_time) * 1000)
                            if EMIT_TOOL_TRACES:
                                print(f"  [REALTIME] blockchain_balance: {elapsed_ms}ms, ETH={balance_eth:.4f}")

                            return {
                                "balances": balances,
                                "total_usd": balance_eth * eth_price,
                                "chains_scanned": ["ETH"],
                                "mode": "REALTIME",
                                "timestamp": datetime.now().isoformat(),
                            }

            except Exception as e:
                if os.getenv("LOG_REALTIME_ERRORS", "true").lower() == "true":
                    print(f"[ERROR] Blockchain balance failed: {e}")
                    print("[FALLBACK] Switching to mock")

                mode = "MOCK_FALLBACK"

        # MOCK PATH
        result = await mock_blockchain_balance(address=address, chains=chains)
        result["mode"] = mode

        elapsed_ms = int((time.time() - start_time) * 1000)
        if EMIT_TOOL_TRACES:
            print(f"  [{mode}] blockchain_balance: {elapsed_ms}ms")

        return result

# ----------------------------------------------------------------------------
# EMAIL ACTIVITY TOOL
# ----------------------------------------------------------------------------

class EmailActivityTool:
    """MCP Tool: Get recent email activity"""

    schema = MCPToolSchema(
        name="get_recent_emails",
        description="Fetch recent email activity from user's inbox",
        parameters={
            "email_address": {"type": "string", "required": True},
            "days_back": {"type": "integer", "default": 7},
            "filter_keywords": {"type": "array", "items": "string", "default": []},
            "include_sentiment": {"type": "boolean", "default": True},
        },
        returns={
            "emails": {"type": "array"},
            "total_count": {"type": "integer"},
            "sentiment_analysis": {"type": "object"},
        }
    )

    async def execute(self, params: Dict) -> Dict:
        """Execute email activity fetch with REALTIME/MOCK mode support"""
        from config import should_use_realtime, EMIT_TOOL_TRACES
        from load_env import is_key_available, get_api_key
        from mock_generators import mock_email_activity
        import time

        start_time = time.time()
        mode = "REALTIME" if should_use_realtime() else "MOCK"

        days_back = params.get("days_back", 7)
        email_addr = params.get("email_address")
        filter_keywords = params.get("filter_keywords", ["funeral", "condolence", "sympathy"])

        # REALTIME PATH (IMAP)
        if should_use_realtime() and is_key_available("IMAP_EMAIL") and is_key_available("IMAP_PASSWORD"):
            try:
                import imaplib
                import email as email_lib
                from email.header import decode_header

                imap_email = get_api_key("IMAP_EMAIL")
                imap_password = get_api_key("IMAP_PASSWORD")

                imap_server = os.getenv("IMAP_SERVER", "imap.gmail.com")

                # Connect to IMAP server
                mail = imaplib.IMAP4_SSL(imap_server)
                mail.login(imap_email, imap_password)
                mail.select("inbox")

                _, message_numbers = mail.search(None, "ALL")
                emails = []
                condolence_count = 0

                # Fetch up to 50 most recent emails
                for num in message_numbers[0].split()[-50:]:
                    _, msg_data = mail.fetch(num, "(RFC822)")
                    msg_raw = msg_data[0][1]

                    message = email_lib.message_from_bytes(msg_raw)

                    # Decode subject
                    subject_raw = decode_header(message["Subject"])[0][0]
                    if isinstance(subject_raw, bytes):
                        subject = subject_raw.decode()
                    else:
                        subject = subject_raw

                    subject_lower = subject.lower()
                    matched = [kw for kw in filter_keywords if kw in subject_lower]

                    sentiment = "sad" if matched else "neutral"
                    if matched:
                        condolence_count += 1

                    emails.append({
                        "from": message["From"],
                        "subject": subject,
                        "date": message["Date"],
                        "snippet": subject[:150],
                        "sentiment": sentiment,
                        "keywords_matched": matched,
                    })

                mail.logout()

                elapsed_ms = int((time.time() - start_time) * 1000)
                if EMIT_TOOL_TRACES:
                    print(f"  [REALTIME] email_activity: {elapsed_ms}ms, total={len(emails)}")

                return {
                    "emails": emails[:20],
                    "total_count": len(emails),
                    "condolence_email_count": condolence_count,
                    "days_scanned": days_back,
                    "mode": "REALTIME",
                    "timestamp": datetime.now().isoformat(),
                }

            except Exception as e:
                if os.getenv("LOG_REALTIME_ERRORS", "true").lower() == "true":
                    print(f"[ERROR] Email IMAP failed: {e}")
                    print("[FALLBACK] Switching to mock")

                mode = "MOCK_FALLBACK"

        # MOCK PATH
        result = await mock_email_activity(days_back=days_back, filter_keywords=filter_keywords)
        result["mode"] = mode

        elapsed_ms = int((time.time() - start_time) * 1000)
        if EMIT_TOOL_TRACES:
            print(f"  [{mode}] email_activity: {elapsed_ms}ms")

        return result


# ----------------------------------------------------------------------------
# CLOUD STORAGE ACTIVITY TOOL
# ----------------------------------------------------------------------------

class CloudActivityTool:
    """MCP Tool: Monitor cloud storage activity"""

    schema = MCPToolSchema(
        name="get_cloud_activity",
        description="Get recent cloud storage activity (Drive, Dropbox, OneDrive)",
        parameters={
            "user_id": {"type": "string", "required": True},
            "services": {"type": "array", "items": "string", "default": ["gdrive", "dropbox", "onedrive"]},
            "days_back": {"type": "integer", "default": 30},
        },
        returns={
            "activity": {"type": "array"},
            "total_files": {"type": "integer"},
            "storage_used_gb": {"type": "float"},
        }
    )

    async def execute(self, params: Dict) -> Dict:
        """Execute cloud activity check with REALTIME/MOCK mode support"""
        from config import should_use_realtime, EMIT_TOOL_TRACES
        from load_env import is_key_available, get_api_key
        from mock_generators import mock_cloud_activity
        import time

        start_time = time.time()
        mode = "REALTIME" if should_use_realtime() else "MOCK"

        services = params.get("services", ["dropbox", "gdrive"])
        days_back = params.get("days_back", 30)

        # REALTIME PATH (DROPBOX)
        if should_use_realtime() and "dropbox" in services and is_key_available("DROPBOX_ACCESS_TOKEN"):
            try:
                token = get_api_key("DROPBOX_ACCESS_TOKEN")

                url = "https://api.dropboxapi.com/2/files/list_folder"
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }
                body = {"path": "", "recursive": False, "limit": 100}

                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(url, headers=headers, json=body)

                    if response.status_code == 200:
                        payload = response.json()
                        entries = payload.get("entries", [])

                        total_size = sum(
                            e.get("size", 0) for e in entries if e.get(".tag") == "file"
                        )
                        size_gb = total_size / (1024 ** 3)

                        recent_files = []
                        for entry in entries[:10]:
                            if entry.get(".tag") == "file":
                                recent_files.append({
                                    "name": entry["name"],
                                    "modified": entry.get("client_modified", ""),
                                    "size_mb": entry.get("size", 0) / (1024 ** 2),
                                })

                        activity = [{
                            "service": "dropbox",
                            "file_count": len(entries),
                            "storage_used_gb": round(size_gb, 2),
                            "recent_files": recent_files,
                            "last_modified": entries[0].get("client_modified", "") if entries else "",
                        }]

                        elapsed_ms = int((time.time() - start_time) * 1000)
                        if EMIT_TOOL_TRACES:
                            print(f"  [REALTIME] cloud_activity: {elapsed_ms}ms, files={len(entries)}")

                        return {
                            "activity": activity,
                            "total_files": len(entries),
                            "total_storage_gb": round(size_gb, 2),
                            "services_scanned": ["dropbox"],
                            "mode": "REALTIME",
                            "timestamp": datetime.now().isoformat(),
                        }

            except Exception as e:
                if os.getenv("LOG_REALTIME_ERRORS", "true").lower() == "true":
                    print(f"[ERROR] Dropbox API failed: {e}")
                    print("[FALLBACK] Switching to mock")

                mode = "MOCK_FALLBACK"

        # MOCK PATH
        result = await mock_cloud_activity(services=services)
        result["mode"] = mode

        elapsed_ms = int((time.time() - start_time) * 1000)
        if EMIT_TOOL_TRACES:
            print(f"  [{mode}] cloud_activity: {elapsed_ms}ms")

        return result


# ============================================================================
# OPENAPI TOOLS
# ============================================================================

class DeathRegistryAPI:
    """OpenAPI Tool: Government death registry verification"""

    openapi_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Death Registry Verification API",
            "version": "1.0.0",
            "description": "Official government death certificate verification",
        },
        "servers": [{"url": "https://api.deathregistry.gov/v1"}],
        "paths": {
            "/verify": {
                "post": {
                    "operationId": "verify_death_certificate",
                    "summary": "Verify death certificate",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "ssn": {"type": "string"},
                                        "full_name": {"type": "string"},
                                        "date_of_birth": {"type": "string"},
                                        "state": {"type": "string"},
                                    },
                                    "required": ["full_name", "state"],
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Verification result",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "verified": {"type": "boolean"},
                                            "certificate_number": {"type": "string"},
                                            "date_of_death": {"type": "string"},
                                            "issuing_authority": {"type": "string"},
                                            "confidence": {"type": "number"},
                                        }
                                    }
                                }
                            },
                        }
                    },
                }
            }
        }
    }

    async def verify_death_certificate(self, **kwargs) -> Dict:
        """Call death registry API with REALTIME/MOCK mode support"""
        from config import should_use_realtime, EMIT_TOOL_TRACES
        from load_env import is_key_available, get_api_key
        from mock_generators import mock_death_registry
        import time

        start_time = time.time()
        mode = "REALTIME" if should_use_realtime() else "MOCK"

        full_name = kwargs.get("full_name", "")

        # REALTIME PATH (GOV API)
        # Requires DEATH_REGISTRY_API_KEY
        if should_use_realtime() and is_key_available("DEATH_REGISTRY_API_KEY"):
            try:
                api_key = get_api_key("DEATH_REGISTRY_API_KEY")
                base_url = os.getenv(
                    "DEATH_REGISTRY_BASE_URL", "https://api.deathregistry.gov/v1"
                )

                url = f"{base_url}/verify"
                headers = {"Authorization": f"Bearer {api_key}"}
                payload = {
                    "full_name": full_name,
                    "state": kwargs.get("state", ""),
                    "date_of_birth": kwargs.get("date_of_birth", ""),
                    "ssn": kwargs.get("ssn", ""),
                }

                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(url, headers=headers, json=payload)

                    if response.status_code == 200:
                        result = response.json()
                        result["mode"] = "REALTIME"

                        elapsed_ms = int((time.time() - start_time) * 1000)
                        if EMIT_TOOL_TRACES:
                            print(
                                f"  [REALTIME] death_registry: {elapsed_ms}ms verified={result.get('verified')}"
                            )

                        return result

            except Exception as e:
                if os.getenv("LOG_REALTIME_ERRORS", "true").lower() == "true":
                    print(f"[ERROR] Death registry API failed: {e}")
                    print("[FALLBACK] Switching to mock")

                mode = "MOCK_FALLBACK"

        # MOCK PATH
        result = await mock_death_registry(
            full_name=full_name,
            date_of_birth=kwargs.get("date_of_birth"),
        )
        result["mode"] = mode

        elapsed_ms = int((time.time() - start_time) * 1000)
        if EMIT_TOOL_TRACES:
            print(f"  [{mode}] death_registry: {elapsed_ms}ms")

        return result


# ----------------------------------------------------------------------------
# CRYPTO PRICE FEED API
# ----------------------------------------------------------------------------

class CryptoPriceFeedAPI:
    """OpenAPI Tool: Real-time cryptocurrency price feed"""

    openapi_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Crypto Price Feed API",
            "version": "1.0.0",
            "description": "Real-time cryptocurrency prices and gas fees",
        },
        "servers": [{"url": "https://api.cryptoprices.io/v1"}],
        "paths": {
            "/prices": {
                "get": {
                    "operationId": "get_crypto_prices",
                    "summary": "Get current crypto prices",
                    "parameters": [
                        {
                            "name": "symbols",
                            "in": "query",
                            "schema": {"type": "string"},
                            "description": "Comma-separated symbols (BTC,ETH,MATIC)",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Price data",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "prices": {"type": "array"},
                                            "timestamp": {"type": "string"},
                                        },
                                    }
                                }
                            },
                        }
                    },
                }
            },
            "/gas": {
                "get": {
                    "operationId": "get_gas_prices",
                    "summary": "Get current gas prices",
                    "parameters": [
                        {
                            "name": "chain",
                            "in": "query",
                            "schema": {"type": "string"},
                            "description": "Blockchain (ethereum, polygon)",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Gas price data",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "safe": {"type": "number"},
                                            "standard": {"type": "number"},
                                            "fast": {"type": "number"},
                                            "block_number": {"type": "integer"},
                                        },
                                    }
                                }
                            },
                        }
                    },
                }
            },
        },
    }

    # ---------------------------------------------------------------------
    # get_crypto_prices
    # ---------------------------------------------------------------------

    async def get_crypto_prices(self, symbols: str) -> Dict:
        """Get cryptocurrency prices with REALTIME/MOCK mode support"""
        from config import should_use_realtime, EMIT_TOOL_TRACES
        from mock_generators import mock_crypto_prices
        import time

        start_time = time.time()
        mode = "REALTIME" if should_use_realtime() else "MOCK"

        # Try REALTIME CoinGecko API
        if should_use_realtime():
            try:
                symbol_map = {
                    "BTC": "bitcoin",
                    "ETH": "ethereum",
                    "MATIC": "matic-network",
                }

                symbol_list = [s.strip() for s in symbols.split(",")]
                ids = ",".join(symbol_map.get(s, s.lower()) for s in symbol_list)

                url = "https://api.coingecko.com/api/v3/simple/price"
                params = {
                    "ids": ids,
                    "vs_currencies": "usd",
                    "include_24hr_change": "true",
                }

                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.get(url, params=params)

                    if response.status_code == 200:
                        data = response.json()
                        prices = []

                        for symbol in symbol_list:
                            coin_id = symbol_map.get(symbol, symbol.lower())
                            if coin_id in data:
                                prices.append(
                                    {
                                        "symbol": symbol,
                                        "price_usd": data[coin_id]["usd"],
                                        "change_24h": data[coin_id].get(
                                            "usd_24h_change", 0
                                        ),
                                    }
                                )

                        if prices:
                            elapsed_ms = int((time.time() - start_time) * 1000)
                            if EMIT_TOOL_TRACES:
                                print(
                                    f"  [REALTIME] crypto_prices: {elapsed_ms}ms symbols={len(prices)}"
                                )

                            return {
                                "prices": prices,
                                "mode": "REALTIME",
                                "timestamp": datetime.now().isoformat(),
                            }

            except Exception as e:
                if os.getenv("LOG_REALTIME_ERRORS", "true").lower() == "true":
                    print(f"[ERROR] CoinGecko failed: {e}")
                    print("[FALLBACK] Switching to mock")

                mode = "MOCK_FALLBACK"

        # MOCK PATH
        result = await mock_crypto_prices(symbols)
        result["mode"] = mode

        elapsed_ms = int((time.time() - start_time) * 1000)
        if EMIT_TOOL_TRACES:
            print(f"  [{mode}] crypto_prices: {elapsed_ms}ms")

        return result

    # ---------------------------------------------------------------------
    # get_gas_prices
    # ---------------------------------------------------------------------

    async def get_gas_prices(self, chain: str) -> Dict:
        """Get gas prices with REALTIME/MOCK mode support"""
        from config import should_use_realtime, EMIT_TOOL_TRACES
        from load_env import is_key_available, get_api_key
        from mock_generators import mock_gas_price
        import time

        start_time = time.time()
        mode = "REALTIME" if should_use_realtime() else "MOCK"

        # REALTIME PATH (ETHERSCAN)
        if (
            should_use_realtime()
            and chain == "ethereum"
            and is_key_available("ETHERSCAN_API_KEY")
        ):
            try:
                key = get_api_key("ETHERSCAN_API_KEY")

                url = "https://api.etherscan.io/api"
                params = {
                    "module": "gastracker",
                    "action": "gasoracle",
                    "apikey": key,
                }

                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.get(url, params=params)

                    if response.status_code == 200:
                        data = response.json()

                        if data.get("status") == "1":
                            res = data["result"]

                            elapsed_ms = int((time.time() - start_time) * 1000)
                            if EMIT_TOOL_TRACES:
                                print(
                                    f"  [REALTIME] gas_prices: {elapsed_ms}ms chain={chain}"
                                )

                            return {
                                "chain": chain,
                                "safe": int(res["SafeGasPrice"]),
                                "standard": int(res["ProposeGasPrice"]),
                                "fast": int(res["FastGasPrice"]),
                                "block_number": int(res.get("LastBlock", 0)),
                                "mode": "REALTIME",
                                "timestamp": datetime.now().isoformat(),
                            }

            except Exception as e:
                if os.getenv("LOG_REALTIME_ERRORS", "true").lower() == "true":
                    print(f"[ERROR] Gas API failed: {e}")
                    print("[FALLBACK] Switching to mock")

                mode = "MOCK_FALLBACK"

        # MOCK PATH
        result = await mock_gas_price(chain)
        result["mode"] = mode

        elapsed_ms = int((time.time() - start_time) * 1000)
        if EMIT_TOOL_TRACES:
            print(f"  [{mode}] gas_prices: {elapsed_ms}ms")

        return result

# ======================================================================
# TOOL REGISTRY
# ======================================================================

class RealtimeToolRegistry:
    """Central registry for all MCP + OpenAPI tools.
    
    Agents (RealtimeDeathDetectionAgent, RealtimeDigitalAssetAgent, 
    RealtimeSmartContractAgent) depend on this registry.
    """

    def __init__(self):
        self.tools = {}
        self._register_all_tools()

    # ------------------------------------------------------------------
    # Register all tools
    # ------------------------------------------------------------------

    def _register_all_tools(self):
        """Register all MCP and OpenAPI tools in a single registry."""

        # MCP Tools ------------------------------------------------------
        self.tools["get_recent_obituaries"] = {
            "type": "mcp",
            "instance": ObituaryLookupTool(),
            "schema": ObituaryLookupTool.schema,
        }

        self.tools["fetch_blockchain_balance"] = {
            "type": "mcp",
            "instance": BlockchainBalanceTool(),
            "schema": BlockchainBalanceTool.schema,
        }

        self.tools["get_recent_emails"] = {
            "type": "mcp",
            "instance": EmailActivityTool(),
            "schema": EmailActivityTool.schema,
        }

        self.tools["get_cloud_activity"] = {
            "type": "mcp",
            "instance": CloudActivityTool(),
            "schema": CloudActivityTool.schema,
        }

        # OpenAPI Tools --------------------------------------------------
        self.tools["verify_death_certificate"] = {
            "type": "openapi",
            "instance": DeathRegistryAPI(),
            "spec": DeathRegistryAPI.openapi_spec,
        }

        self.tools["get_crypto_prices"] = {
            "type": "openapi",
            "instance": CryptoPriceFeedAPI(),
            "spec": CryptoPriceFeedAPI.openapi_spec,
        }

        self.tools["get_gas_prices"] = {
            "type": "openapi",
            "instance": CryptoPriceFeedAPI(),
            "spec": CryptoPriceFeedAPI.openapi_spec,
        }

        # Built-in Tools -------------------------------------------------
        # (Provided by the ADK runtime)
        self.tools["google_search"] = {
            "type": "builtin",
            "name": "GOOGLE_SEARCH",
            "description": "Search Google for real-time information.",
        }

        # NOTE:
        # code_execution tool is intentionally NOT included.
        # All agents execute Python directly; no remote sandbox is used.

    # ------------------------------------------------------------------
    # Tool lookup
    # ------------------------------------------------------------------

    def get_tool(self, name: str) -> Optional[Dict]:
        """Fetch tool definition by name."""
        return self.tools.get(name)

    def list_tools(self) -> List[str]:
        """List all tool names."""
        return list(self.tools.keys())

    # ------------------------------------------------------------------
    # Tool execution
    # ------------------------------------------------------------------

    async def execute_tool(self, name: str, params: Dict) -> Dict:
        """Execute a tool by name. Supports MCP, OpenAPI, and built-in tools."""

        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found in registry.")

        ttype = tool["type"]

        # MCP and OpenAPI tools use .execute()
        if ttype in ["mcp", "openapi"]:
            instance = tool["instance"]

            # Execute with proper signature
            if hasattr(instance, "execute"):
                return await instance.execute(params)
            elif hasattr(instance, name):
                method = getattr(instance, name)
                return await method(**params)
            else:
                raise ValueError(f"Tool '{name}' has no callable execute() method.")

        # Built-in tools (Google Search, etc.)
        elif ttype == "builtin":
            return {
                "error": "Built-in tools must be invoked through ADK runtime.",
                "tool": name,
            }

        raise ValueError(f"Unsupported tool type '{ttype}'.")

    # ------------------------------------------------------------------
    # Helpers for debugging and introspection
    # ------------------------------------------------------------------

    def describe(self) -> Dict[str, Any]:
        """Return a detailed description of all registered tools."""
        out = {}
        for name, tool in self.tools.items():
            entry = {"type": tool["type"]}
            if tool["type"] == "mcp":
                entry["schema"] = tool["schema"].__dict__
            elif tool["type"] == "openapi":
                entry["openapi_spec"] = tool["spec"]
            out[name] = entry
        return out


# ======================================================================
# DEBUG USAGE (manual test)
# ======================================================================

async def example_usage():
    """Manual debugging helper (not used in production)."""

    registry = RealtimeToolRegistry()

    # Test: Obituary Lookup (MCP)
    obits = await registry.execute_tool(
        "get_recent_obituaries",
        {
            "full_name": "John Doe",
            "location": "California",
            "date_range_days": 30,
        },
    )
    print(f"[DEBUG] Obituaries found: {obits.get('total_found')}")

    # Test: Blockchain Balance (MCP)
    bal = await registry.execute_tool(
        "fetch_blockchain_balance",
        {
            "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            "chains": ["ETH", "MATIC"],
        },
    )
    print(f"[DEBUG] Total USD balance: {bal.get('total_usd')}")

    # Test: Death Registry (OpenAPI)
    verify = await registry.execute_tool(
        "verify_death_certificate",
        {
            "full_name": "John Doe",
            "state": "CA",
        },
    )
    print(f"[DEBUG] Verified: {verify.get('verified')}")


# ======================================================================
# MAIN BLOCK
# ======================================================================

if __name__ == "__main__":
    import asyncio

    print("Running realtime_tools example usage...")
    asyncio.run(example_usage())

# ======================================================================
# CLOUD ACTIVITY TOOL (continued)
# ======================================================================

class CloudActivityTool:
    """MCP Tool: Monitor cloud storage activity (Drive, Dropbox, OneDrive)."""

    schema = MCPToolSchema(
        name="get_cloud_activity",
        description="Get recent cloud storage activity.",
        parameters={
            "user_id": {"type": "string", "required": True},
            "services": {
                "type": "array",
                "items": "string",
                "default": ["gdrive", "dropbox", "onedrive"],
            },
            "days_back": {"type": "integer", "default": 30},
        },
        returns={
            "activity": {"type": "array"},
            "total_files": {"type": "integer"},
            "storage_used_gb": {"type": "float"},
        },
    )

    async def execute(self, params: Dict) -> Dict:
        """Execute cloud activity with REALTIME/MOCK support."""
        from config import should_use_realtime, EMIT_TOOL_TRACES
        from load_env import is_key_available, get_api_key
        from mock_generators import mock_cloud_activity
        import time

        start_time = time.time()
        mode = "REALTIME" if should_use_realtime() else "MOCK"

        user_id = params.get("user_id")
        services = params.get("services", ["gdrive", "dropbox"])
        days_back = params.get("days_back", 30)

        # REALTIME: Dropbox API
        if should_use_realtime() and "dropbox" in services and is_key_available("DROPBOX_ACCESS_TOKEN"):
            try:
                token = get_api_key("DROPBOX_ACCESS_TOKEN")

                url = "https://api.dropboxapi.com/2/files/list_folder"
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }
                body = {"path": "", "recursive": False}

                async with httpx.AsyncClient(timeout=10) as client:
                    resp = await client.post(url, json=body, headers=headers)

                if resp.status_code == 200:
                    data = resp.json()
                    entries = data.get("entries", [])

                    files = [e for e in entries if e.get(".tag") == "file"]
                    total_size = sum(f.get("size", 0) for f in files)
                    used_gb = total_size / (1024**3)

                    result = {
                        "activity": [
                            {
                                "service": "dropbox",
                                "total_files": len(files),
                                "storage_used_gb": round(used_gb, 2),
                                "recent_files": [
                                    {
                                        "name": f.get("name"),
                                        "size_mb": round(f.get("size", 0) / (1024**2), 2),
                                        "modified": f.get("client_modified", ""),
                                    }
                                    for f in files[:5]
                                ],
                            }
                        ],
                        "total_files": len(files),
                        "storage_used_gb": round(used_gb, 2),
                        "mode": "REALTIME",
                        "timestamp": datetime.now().isoformat(),
                    }

                    if EMIT_TOOL_TRACES:
                        print(f"[REALTIME] cloud_activity: {len(files)} files, {used_gb:.3f} GB")

                    return result

            except Exception as e:
                if os.getenv("LOG_REALTIME_ERRORS", "true") == "true":
                    print(f"[ERROR] Dropbox cloud activity failed: {e}")
                    print("[FALLBACK] Using mock data")
                mode = "MOCK_FALLBACK"

        # FALLBACK: Mock
        result = await mock_cloud_activity(services=services)
        result["mode"] = mode

        if EMIT_TOOL_TRACES:
            print(f"[{mode}] cloud_activity executed")

        return result


# ======================================================================
# OPENAPI TOOL: Death Registry Verification (continued)
# ======================================================================

class DeathRegistryAPI:
    """OpenAPI Tool: Government death certificate verification."""

    openapi_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Death Registry Verification API",
            "version": "1.0.0",
        },
        "paths": {
            "/verify": {
                "post": {
                    "operationId": "verify_death_certificate",
                    "summary": "Government death record lookup",
                }
            }
        },
    }

    async def execute(self, params: Dict) -> Dict:
        """Execute via wrapper -> verify_death_certificate"""
        return await self.verify_death_certificate(**params)

    async def verify_death_certificate(self, **kwargs) -> Dict:
        """REALTIME/MOCK death registry verification."""
        from config import should_use_realtime, EMIT_TOOL_TRACES
        from load_env import get_api_key, is_key_available
        from mock_generators import mock_death_registry
        import time

        start_time = time.time()

        full_name = kwargs.get("full_name", "")
        state = kwargs.get("state", "")
        dob = kwargs.get("date_of_birth", "")
        ssn = kwargs.get("ssn", "")

        mode = "REALTIME" if should_use_realtime() else "MOCK"

        if should_use_realtime() and is_key_available("DEATH_REGISTRY_API_KEY"):
            try:
                base_url = os.getenv("DEATH_REGISTRY_BASE_URL", "https://api.deathregistry.gov/v1")
                api_key = get_api_key("DEATH_REGISTRY_API_KEY")

                url = f"{base_url}/verify"
                headers = {"Authorization": f"Bearer {api_key}"}

                payload = {"full_name": full_name, "state": state, "date_of_birth": dob, "ssn": ssn}

                async with httpx.AsyncClient(timeout=10) as client:
                    resp = await client.post(url, json=payload, headers=headers)

                if resp.status_code == 200:
                    data = resp.json()
                    data["mode"] = "REALTIME"

                    if EMIT_TOOL_TRACES:
                        elapsed = int((time.time() - start_time) * 1000)
                        print(f"[REALTIME] death_registry verified={data.get('verified')} in {elapsed}ms")

                    return data

            except Exception as e:
                if os.getenv("LOG_REALTIME_ERRORS", "true") == "true":
                    print(f"[ERROR] Death registry API error: {e}")
                    print("[FALLBACK] Using mock data")

                mode = "MOCK_FALLBACK"

        # Fallback
        result = await mock_death_registry(full_name=full_name, date_of_birth=dob)
        result["mode"] = mode

        if EMIT_TOOL_TRACES:
            print(f"[{mode}] death_registry executed")

        return result


# ======================================================================
# OPENAPI TOOL: Crypto Price Feed (continued)
# ======================================================================

class CryptoPriceFeedAPI:
    """OpenAPI Tool: Real-time cryptocurrency prices and gas fees."""

    openapi_spec = {
        "openapi": "3.0.0",
        "info": {"title": "Crypto Price Feed API", "version": "1.0.0"},
    }

    # --------------------------------------------------------------
    # get_crypto_prices (continued)
    # --------------------------------------------------------------

    async def get_crypto_prices(self, symbols: str) -> Dict:
        """Continuation of CoinGecko-based real price fetch."""
        from config import should_use_realtime, EMIT_TOOL_TRACES
        from mock_generators import mock_crypto_prices
        import time

        start_time = time.time()
        mode = "REALTIME" if should_use_realtime() else "MOCK"

        if should_use_realtime():
            try:
                mapping = {
                    "BTC": "bitcoin",
                    "ETH": "ethereum",
                    "MATIC": "matic-network",
                }

                symbol_list = [s.strip() for s in symbols.split(",")]
                ids = ",".join(mapping.get(s, s.lower()) for s in symbol_list)

                url = "https://api.coingecko.com/api/v3/simple/price"
                params = {
                    "ids": ids,
                    "vs_currencies": "usd",
                    "include_24hr_change": "true",
                }

                async with httpx.AsyncClient(timeout=10) as client:
                    resp = await client.get(url, params=params)

                if resp.status_code == 200:
                    json_data = resp.json()
                    prices = []

                    for s in symbol_list:
                        cid = mapping.get(s, s.lower())
                        if cid in json_data:
                            prices.append(
                                {
                                    "symbol": s,
                                    "price_usd": json_data[cid]["usd"],
                                    "change_24h": json_data[cid].get("usd_24h_change", 0),
                                }
                            )

                    if prices:
                        if EMIT_TOOL_TRACES:
                            elapsed = int((time.time() - start_time) * 1000)
                            print(f"[REALTIME] crypto_prices {elapsed}ms {symbol_list}")

                        return {"prices": prices, "mode": "REALTIME", "timestamp": datetime.now().isoformat()}

            except Exception as e:
                if os.getenv("LOG_REALTIME_ERRORS", "true") == "true":
                    print(f"[ERROR] crypto_prices failed: {e}")
                mode = "MOCK_FALLBACK"

        # fallback
        data = await mock_crypto_prices(symbols)
        data["mode"] = mode

        return data

# ================================================================
# CryptoPriceFeedAPI (continued) — Gas Prices Section
# ================================================================

    async def get_gas_prices(self, chain: str) -> Dict:
        """Get gas prices (REALTIME/MOCK)."""
        from config import should_use_realtime, EMIT_TOOL_TRACES
        from load_env import get_api_key, is_key_available
        from mock_generators import mock_gas_price
        import time

        start_time = time.time()
        mode = "REALTIME" if should_use_realtime() else "MOCK"

        # Ethereum (Etherscan) real gas feed
        if should_use_realtime() and chain.lower() == "ethereum" and is_key_available("ETHERSCAN_API_KEY"):
            try:
                api_key = get_api_key("ETHERSCAN_API_KEY")

                url = "https://api.etherscan.io/api"
                params = {
                    "module": "gastracker",
                    "action": "gasoracle",
                    "apikey": api_key,
                }

                async with httpx.AsyncClient(timeout=10) as client:
                    resp = await client.get(url, params=params)

                if resp.status_code == 200:
                    data = resp.json()

                    if data.get("status") == "1":
                        gas = data["result"]

                        result = {
                            "chain": chain,
                            "safe": int(gas["SafeGasPrice"]),
                            "standard": int(gas["ProposeGasPrice"]),
                            "fast": int(gas["FastGasPrice"]),
                            "block_number": int(gas.get("LastBlock", 0)),
                            "mode": "REALTIME",
                            "timestamp": datetime.now().isoformat(),
                        }

                        if EMIT_TOOL_TRACES:
                            elapsed = int((time.time() - start_time) * 1000)
                            print(f"[REALTIME] gas_prices eth: {elapsed}ms")

                        return result

            except Exception as e:
                if os.getenv("LOG_REALTIME_ERRORS", "true") == "true":
                    print(f"[ERROR] Gas price fetch failed: {e}")
                    print("[FALLBACK] Using mock data")
                mode = "MOCK_FALLBACK"

        # fallback for all other chains
        result = await mock_gas_price(chain)
        result["mode"] = mode

        if EMIT_TOOL_TRACES:
            print(f"[{mode}] gas_prices executed")

        return result


# ======================================================================
# TOOL REGISTRY
# ======================================================================

class RealtimeToolRegistry:
    """Central registry for all tools used in realtime agents."""

    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        self._register_all_tools()

    # --------------------------------------------------------------
    # Register tools
    # --------------------------------------------------------------

    def _register_all_tools(self):
        """Registers MCP + OpenAPI tools."""

        # MCP Tools
        self.tools["get_recent_obituaries"] = {
            "type": "mcp",
            "instance": ObituaryLookupTool(),
            "schema": ObituaryLookupTool.schema,
        }

        self.tools["fetch_blockchain_balance"] = {
            "type": "mcp",
            "instance": BlockchainBalanceTool(),
            "schema": BlockchainBalanceTool.schema,
        }

        self.tools["get_recent_emails"] = {
            "type": "mcp",
            "instance": EmailActivityTool(),
            "schema": EmailActivityTool.schema,
        }

        self.tools["get_cloud_activity"] = {
            "type": "mcp",
            "instance": CloudActivityTool(),
            "schema": CloudActivityTool.schema,
        }

        # OpenAPI Tools
        self.tools["verify_death_certificate"] = {
            "type": "openapi",
            "instance": DeathRegistryAPI(),
            "spec": DeathRegistryAPI.openapi_spec,
        }

        self.tools["get_crypto_prices"] = {
            "type": "openapi",
            "instance": CryptoPriceFeedAPI(),
            "spec": CryptoPriceFeedAPI.openapi_spec,
        }

        # NOTE: Gas tool is separate but uses same instance pattern
        self.tools["get_gas_prices"] = {
            "type": "openapi",
            "instance": CryptoPriceFeedAPI(),
            "spec": CryptoPriceFeedAPI.openapi_spec,
        }

        # Built-in Tools (ADK)
        self.tools["google_search"] = {
            "type": "builtin",
            "name": "GOOGLE_SEARCH",
            "description": "Search Google for recent information",
        }

    # --------------------------------------------------------------
    # Accessors
    # --------------------------------------------------------------

    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        """Return tool definition."""
        return self.tools.get(name)

    def list_tools(self) -> List[str]:
        """List all registered tools."""
        return list(self.tools.keys())

    # --------------------------------------------------------------
    # Execution
    # --------------------------------------------------------------

    async def execute_tool(self, name: str, params: Dict) -> Dict:
        """Execute a tool by name (MCP or OpenAPI)."""

        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found in registry.")

        ttype = tool["type"]

        if ttype in ("mcp", "openapi"):
            instance = tool["instance"]
            return await instance.execute(params)

        if ttype == "builtin":
            return {"error": "Built-in tools must be invoked via ADK runtime."}

        raise ValueError(f"Unknown tool type: {ttype}")


# ======================================================================
# Example usage section (continued)
# ======================================================================

async def example_usage():
    """Demonstration of tool registry usage."""

    registry = RealtimeToolRegistry()

    # obituary lookup
    obit = await registry.execute_tool(
        "get_recent_obituaries",
        {"full_name": "John Doe", "location": "NY", "date_range_days": 30},
    )
    print("Obituary:", obit.get("total_found"))

    # blockchain
    bal = await registry.execute_tool(
        "fetch_blockchain_balance",
        {"address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"},
    )
    print("ETH balance:", bal.get("total_usd"))

    # registry
    reg = await registry.execute_tool(
        "verify_death_certificate", {"full_name": "John Doe", "state": "CA"}
    )
    print("Verified:", reg.get("verified"))

    print("Death registry verified:", reg.get("verified"))

    # crypto prices
    prices = await registry.execute_tool(
        "get_crypto_prices",
        {"symbols": "BTC,ETH,MATIC"},
    )
    print("Crypto prices returned:", len(prices.get("prices", [])))

    # gas prices
    gas = await registry.execute_tool(
        "get_gas_prices",
        {"chain": "ethereum"},
    )
    print("Gas prices (safe):", gas.get("safe"))

    print("Example usage completed.")


# ======================================================================
# MAIN (for standalone testing)
# ======================================================================

if __name__ == "__main__":
    import asyncio

    print("Running realtime_tools example usage...")
    asyncio.run(example_usage())


# ======================================================================
# Notes
# ======================================================================
# This file defines three tool classes:
#   - MCP Tools     (Obituary, Balance, Email, Cloud)
#   - OpenAPI Tools (DeathRegistryAPI, CryptoPriceFeedAPI)
#   - Built-in Tools handled externally
#
# And exposes a central registry:
#   RealtimeToolRegistry
#
# Agents call: registry.execute_tool(name, params)
#
# REALTIME vs MOCK mode is controlled by:
#   should_use_realtime() from config.py
#
# Mock fallbacks come from mock_generators.py
#
# No logic here should reference agents or backend API.
#
# ======================================================================
