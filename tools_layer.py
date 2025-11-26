"""
Ghost Protocol - Tool Layer Definitions
MCP, Custom, Built-in, and OpenAPI tools
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# TOOL SCHEMAS
# ============================================================================

@dataclass
class ToolSchema:
    name: str
    description: str
    parameters: Dict[str, Any]
    returns: Dict[str, Any]
    tool_type: str


@dataclass
class ToolResult:
    success: bool
    data: Any
    error: Optional[str] = None
    metadata: Optional[Dict] = None


# ============================================================================
# 1. MCP TOOL - OBITUARY LOOKUP (DEPRECATED - Use realtime_tools.py)
# ============================================================================
# NOTE: This tool is superseded by get_recent_obituaries in realtime_tools.py
# Kept for reference only. DO NOT USE.

# [DEPRECATED CODE REMOVED - See realtime_tools.py for active implementation]


# ============================================================================
# 2. CUSTOM TOOLS - REMOVED (Not integrated into RealtimeToolRegistry)
# ============================================================================
# NOTE: Custom tools were defined here but not used by agents.
# They have been removed to comply with ADK requirement:
# "no tool is declared but not used"
# 
# If you need custom tools in the future, add them to:
# realtime_tools.py -> RealtimeToolRegistry
#
# Example custom tool implementation can be found in git history.


# ============================================================================
# 3. BUILT-IN TOOL - CODE EXECUTION (DEPRECATED - Use realtime_tools.py)
# ============================================================================
# NOTE: This tool is superseded by code_execution in realtime_tools.py
# Kept for reference only. DO NOT USE.

# [DEPRECATED CODE REMOVED - See realtime_tools.py for active implementation]


# ============================================================================
# 4. OPENAPI TOOL - DEATH REGISTRY VERIFICATION
# ============================================================================

DEATH_REGISTRY_OPENAPI_SCHEMA = {
    "openapi": "3.0.0",
    "info": {
        "title": "Death Registry Verification API",
        "version": "1.0.0",
        "description": "Verify death records against government registries"
    },
    "servers": [
        {"url": "https://api.deathregistry.gov/v1"}
    ],
    "paths": {
        "/verify": {
            "post": {
                "operationId": "verify_death_record",
                "summary": "Verify death record",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "ssn": {
                                        "type": "string",
                                        "description": "Social Security Number"
                                    },
                                    "full_name": {
                                        "type": "string"
                                    },
                                    "date_of_birth": {
                                        "type": "string",
                                        "format": "date"
                                    },
                                    "state": {
                                        "type": "string",
                                        "description": "State code (e.g., CA, NY)"
                                    }
                                },
                                "required": ["ssn", "full_name"]
                            }
                        }
                    }
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
                                        "date_of_death": {"type": "string"},
                                        "certificate_number": {"type": "string"},
                                        "issuing_authority": {"type": "string"},
                                        "verification_timestamp": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                },
                "security": [
                    {"ApiKeyAuth": []}
                ]
            }
        }
    },
    "components": {
        "securitySchemes": {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "X-API-Key"
            }
        }
    }
}


class DeathRegistryOpenAPI:
    """OpenAPI-based death registry verification"""
    
    schema = DEATH_REGISTRY_OPENAPI_SCHEMA
    
    def __init__(self, api_key: str, base_url: str = "https://api.deathregistry.gov/v1"):
        self.api_key = api_key
        self.base_url = base_url
    
    async def verify_death_record(self, ssn: str, full_name: str, 
                                  date_of_birth: Optional[str] = None,
                                  state: Optional[str] = None) -> ToolResult:
        # Mock API call
        return ToolResult(
            success=True,
            data={
                "verified": True,
                "date_of_death": "2025-11-20",
                "certificate_number": "2025-CA-12345",
                "issuing_authority": "California Department of Public Health",
                "verification_timestamp": "2025-11-25T18:00:00Z"
            }
        )


# ============================================================================
# TOOL REGISTRY (LEGACY - Not actively used)
# ============================================================================
# WARNING: This registry is NOT used by agents_realtime.py
# The active tool registry is RealtimeToolRegistry in realtime_tools.py
# 
# This class is kept for reference and backward compatibility only.
# DO NOT register new tools here.
# Use realtime_tools.py instead.

class ToolRegistry:
    """Central registry for all tools"""
    
    def __init__(self):
        self.tools = {}
    
    def register_mcp_tool(self, tool_class):
        self.tools[tool_class.schema["name"]] = {
            "type": "mcp",
            "schema": tool_class.schema,
            "instance": tool_class()
        }
    
    def register_custom_tool(self, tool_class, **init_kwargs):
        schema = tool_class.schema
        self.tools[schema["name"]] = {
            "type": "custom",
            "schema": schema,
            "instance": tool_class(**init_kwargs)
        }
    
    def register_builtin_tool(self, name: str, schema: Dict):
        self.tools[name] = {
            "type": "builtin",
            "schema": schema,
            "instance": None  # Handled by ADK runtime
        }
    
    def register_openapi_tool(self, tool_class, **init_kwargs):
        instance = tool_class(**init_kwargs)
        self.tools["death_registry_verification"] = {
            "type": "openapi",
            "schema": tool_class.schema,
            "instance": instance
        }
    
    def get_tool(self, name: str):
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        return list(self.tools.keys())


# ============================================================================
# ADK TOOL REGISTRATION
# ============================================================================

def register_all_tools() -> ToolRegistry:
    """Register all tools with ADK (LEGACY - Not used by agents)
    
    WARNING: This registry is DEPRECATED and NOT used by the application.
    Active tools are registered in: realtime_tools.py -> RealtimeToolRegistry
    
    This function is kept only for backward compatibility reference.
    """
    
    registry = ToolRegistry()
    
    # All tools have been migrated to realtime_tools.py
    # This legacy registry returns an empty registry
    # 
    # Active tool registry location:
    # - File: realtime_tools.py
    # - Class: RealtimeToolRegistry
    # - Tools: 7 active tools (4 MCP, 3 OpenAPI, 1 Built-in)
    
    return registry


# ============================================================================
# EXAMPLE TOOL CALL SIGNATURES (REMOVED - Outdated)
# ============================================================================
# NOTE: Example functions removed as they referenced deprecated tools.
# For current tool usage examples, see:
# - realtime_tools.py (lines 508-537) for active tool examples
# - agents_realtime.py for real agent-tool integration patterns


# ============================================================================
# ADDITIONAL TOOL SCHEMAS (REMOVED - Incomplete)
# ============================================================================
# NOTE: The following tools were incomplete and have been removed.
# If needed, implement them properly in realtime_tools.py with full schemas.
#
# Previously defined but incomplete:
# - email_scanner: Scan email inbox for account confirmations
# - social_media_api: Access social media accounts via API  
# - blockchain_rpc: Interact with blockchain networks via RPC

# [INCOMPLETE SCHEMAS REMOVED]
