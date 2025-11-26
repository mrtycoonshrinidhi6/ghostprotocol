# Tool Orchestration Diagram

## Tool Layer Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          TOOL ORCHESTRATION LAYER                           │
└─────────────────────────────────────────────────────────────────────────────┘

                         ┌────────────────────────┐
                         │   TOOL REGISTRY        │
                         │   (Central Manager)    │
                         └───────────┬────────────┘
                                     │
                ┌────────────────────┼────────────────────┐
                │                    │                    │
                ▼                    ▼                    ▼
        ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
        │  MCP TOOLS   │    │CUSTOM TOOLS  │    │BUILTIN TOOLS │
        └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
               │                   │                    │
               │                   │                    │
               ▼                   ▼                    ▼
        ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
        │OPENAPI TOOLS │    │              │    │              │
        └──────────────┘    │              │    │              │
                            │              │    │              │
        ┌───────────────────┴──────────────┴────┴──────────────┐
        │                                                       │
        │            AGENTS ACCESS TOOLS VIA REGISTRY           │
        │                                                       │
        └───────────────────┬───────────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
        ▼                                       ▼
┌──────────────────┐                  ┌──────────────────┐
│DeathDetection    │                  │DigitalAsset      │
│Agent             │                  │Agent             │
│- obituary_lookup │                  │- email_scanner   │
│- death_registry  │                  │- crypto_extract  │
└──────────────────┘                  └──────────────────┘


═══════════════════════════════════════════════════════════════════════════

TOOL TYPE BREAKDOWN
═══════════════════════════════════════════════════════════════════════════

1. MCP TOOL (Model Context Protocol)
┌──────────────────────────────────────────────────────────────┐
│ Tool: obituary_lookup                                        │
├──────────────────────────────────────────────────────────────┤
│ Protocol:  MCP v1.0                                          │
│ Interface: Standardized schema                               │
│                                                              │
│ Schema:                                                      │
│   {                                                          │
│     "name": "obituary_lookup",                               │
│     "parameters": {                                          │
│       "full_name": "string",                                 │
│       "date_of_birth": "date",                               │
│       "location": "string"                                   │
│     },                                                       │
│     "returns": {                                             │
│       "found": "boolean",                                    │
│       "obituaries": "array",                                 │
│       "confidence": "float"                                  │
│     }                                                        │
│   }                                                          │
│                                                              │
│ Agent Call:                                                  │
│   result = registry.get_tool("obituary_lookup")             │
│   output = await result.execute({                            │
│       "full_name": "John Doe",                               │
│       "location": "San Francisco"                            │
│   })                                                         │
│                                                              │
│ Output:                                                      │
│   {                                                          │
│     "found": true,                                           │
│     "obituaries": [                                          │
│       {"source": "Legacy.com", "confidence": 0.98}           │
│     ]                                                        │
│   }                                                          │
└──────────────────────────────────────────────────────────────┘


2. CUSTOM TOOL
┌──────────────────────────────────────────────────────────────┐
│ Tool: crypto_wallet_extractor                               │
├──────────────────────────────────────────────────────────────┤
│ Type:      Custom-built                                      │
│ Purpose:   Extract crypto wallets from encrypted vault      │
│                                                              │
│ Schema:                                                      │
│   {                                                          │
│     "name": "crypto_wallet_extractor",                       │
│     "parameters": {                                          │
│       "vault_path": "string",                                │
│       "master_password": "string",                           │
│       "wallet_types": ["BTC", "ETH"],                        │
│       "include_private_keys": "boolean"                      │
│     },                                                       │
│     "returns": {                                             │
│       "wallets": "array",                                    │
│       "total_value_usd": "float"                             │
│     }                                                        │
│   }                                                          │
│                                                              │
│ Implementation:                                              │
│   class CryptoWalletExtractor:                               │
│       def __init__(self, encryption_service):                │
│           self.encryption = encryption_service               │
│                                                              │
│       async def execute(self, params):                       │
│           # Decrypt vault                                    │
│           # Parse wallet addresses                           │
│           # Fetch balances from blockchain                   │
│           # Return inventory                                 │
│                                                              │
│ Agent Call:                                                  │
│   tool = registry.get_tool("crypto_wallet_extractor")       │
│   wallets = await tool.execute({                             │
│       "vault_path": "/secure/vault.kdbx",                    │
│       "master_password": "***",                              │
│       "wallet_types": ["BTC", "ETH", "SOL"]                  │
│   })                                                         │
└──────────────────────────────────────────────────────────────┘


3. BUILT-IN TOOL
┌──────────────────────────────────────────────────────────────┐
│ Tool: code_execution                                         │
├──────────────────────────────────────────────────────────────┤
│ Type:      ADK Built-in                                      │
│ Purpose:   Execute Python code in sandbox                    │
│                                                              │
│ Schema:                                                      │
│   {                                                          │
│     "name": "code_execution",                                │
│     "parameters": {                                          │
│       "code": "string",                                      │
│       "timeout": "integer",                                  │
│       "allowed_imports": ["json", "math"]                    │
│     },                                                       │
│     "returns": {                                             │
│       "stdout": "string",                                    │
│       "return_value": "any",                                 │
│       "execution_time": "float"                              │
│     }                                                        │
│   }                                                          │
│                                                              │
│ Use Case: Calculate total portfolio value                   │
│   code = """                                                 │
│   total = sum([w['balance'] * w['price'] for w in wallets]) │
│   print(f'Total: ${total:.2f}')                              │
│   total                                                      │
│   """                                                        │
│                                                              │
│ Agent Call:                                                  │
│   result = await adk.execute_code(code, timeout=10)         │
│                                                              │
│ Output:                                                      │
│   {                                                          │
│     "stdout": "Total: $7843.25\n",                           │
│     "return_value": 7843.25,                                 │
│     "execution_time": 0.002                                  │
│   }                                                          │
└──────────────────────────────────────────────────────────────┘


4. OPENAPI TOOL
┌──────────────────────────────────────────────────────────────┐
│ Tool: death_registry_verification                           │
├──────────────────────────────────────────────────────────────┤
│ Type:      OpenAPI 3.0 Integration                           │
│ API:       Government Death Registry                         │
│                                                              │
│ OpenAPI Spec:                                                │
│   {                                                          │
│     "openapi": "3.0.0",                                      │
│     "info": {"title": "Death Registry API"},                 │
│     "servers": [                                             │
│       {"url": "https://api.deathregistry.gov/v1"}            │
│     ],                                                       │
│     "paths": {                                               │
│       "/verify": {                                           │
│         "post": {                                            │
│           "operationId": "verify_death_record",              │
│           "requestBody": {                                   │
│             "ssn": "string",                                 │
│             "full_name": "string",                           │
│             "state": "string"                                │
│           },                                                 │
│           "responses": {                                     │
│             "200": {                                         │
│               "verified": "boolean",                         │
│               "certificate_number": "string"                 │
│             }                                                │
│           }                                                  │
│         }                                                    │
│       }                                                      │
│     }                                                        │
│   }                                                          │
│                                                              │
│ Agent Call:                                                  │
│   tool = registry.get_tool("death_registry_verification")   │
│   result = await tool.verify_death_record(                  │
│       ssn="123-45-6789",                                     │
│       full_name="John Doe",                                  │
│       state="CA"                                             │
│   )                                                          │
│                                                              │
│ Output:                                                      │
│   {                                                          │
│     "verified": true,                                        │
│     "certificate_number": "2025-CA-12345",                   │
│     "issuing_authority": "CA Dept of Public Health"          │
│   }                                                          │
└──────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════

TOOL EXECUTION FLOW
═══════════════════════════════════════════════════════════════════════════

Agent Needs Tool
      │
      ▼
┌─────────────────────┐
│ 1. Tool Discovery   │
│    registry.list()  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 2. Tool Selection   │
│    get_tool(name)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 3. Schema Validation│
│    validate(params) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 4. Tool Execution   │
│    tool.execute()   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 5. Result Parsing   │
│    parse_output()   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 6. Error Handling   │
│    retry/fallback   │
└──────────┬──────────┘
           │
           ▼
    Return to Agent


═══════════════════════════════════════════════════════════════════════════

TOOL REGISTRY OPERATIONS
═══════════════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────┐
│ class ToolRegistry:                                        │
│                                                            │
│   def register_mcp_tool(tool_class):                       │
│       """Register MCP-compliant tool"""                    │
│       self.tools[tool.name] = {                            │
│           "type": "mcp",                                   │
│           "schema": tool.schema,                           │
│           "instance": tool()                               │
│       }                                                    │
│                                                            │
│   def register_custom_tool(tool_class, **kwargs):          │
│       """Register custom tool with init args"""           │
│       self.tools[tool.name] = {                            │
│           "type": "custom",                                │
│           "schema": tool.schema,                           │
│           "instance": tool(**kwargs)                       │
│       }                                                    │
│                                                            │
│   def register_builtin_tool(name, schema):                 │
│       """Register ADK built-in tool"""                     │
│       self.tools[name] = {                                 │
│           "type": "builtin",                               │
│           "schema": schema,                                │
│           "instance": None  # Handled by ADK runtime       │
│       }                                                    │
│                                                            │
│   def register_openapi_tool(tool_class, **kwargs):         │
│       """Register OpenAPI tool"""                          │
│       self.tools[name] = {                                 │
│           "type": "openapi",                               │
│           "schema": tool.openapi_spec,                     │
│           "instance": tool(**kwargs)                       │
│       }                                                    │
│                                                            │
│   def get_tool(name):                                      │
│       """Retrieve tool by name"""                          │
│       return self.tools.get(name)                          │
│                                                            │
│   def list_tools():                                        │
│       """List all registered tools"""                      │
│       return list(self.tools.keys())                       │
└────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════

TOOL COMPOSITION (Multiple Tools in Sequence)
═══════════════════════════════════════════════════════════════════════════

Example: Asset Discovery → Wallet Balance → USD Conversion

Step 1: crypto_wallet_extractor
        ↓
        Output: [{"type": "ETH", "address": "0xABC", "balance": 2.5}]
        
Step 2: code_execution (calculate USD value)
        ↓
        Code: "balance = 2.5; price = 3200; balance * price"
        Output: 8000.0
        
Step 3: Store in session
        ↓
        session.set_data("wallet_value_usd", 8000.0)


═══════════════════════════════════════════════════════════════════════════

ERROR HANDLING & RETRIES
═══════════════════════════════════════════════════════════════════════════

Tool Call → Execute → Error?
                        │
                  ┌─────┴─────┐
                  │           │
                 YES         NO
                  │           │
                  ▼           ▼
         ┌─────────────┐   Return
         │ Retry Logic │   Success
         └──────┬──────┘
                │
         ┌──────┴──────┐
         │             │
    Rate Limit    Network Error
         │             │
         ▼             ▼
    Wait 60s      Retry 3x
    Retry         Exponential
                  Backoff
         │             │
         └──────┬──────┘
                │
         Still failing?
                │
                ▼
         ┌─────────────┐
         │  Fallback   │
         │  Strategy   │
         └──────┬──────┘
                │
                ▼
         Log error
         Return partial results
```
