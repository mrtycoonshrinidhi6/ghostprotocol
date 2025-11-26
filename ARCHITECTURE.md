# Ghost Protocol AI Digital Executor - System Architecture

## Project Folder Structure

```
ghostprotocol/
├── agents/
│   ├── death_detection/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── tools/
│   ├── digital_asset/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── tools/
│   ├── legacy/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── ai_twin.py
│   │   └── tools/
│   ├── smart_contract/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── tools/
│   └── orchestrator/
│       ├── __init__.py
│       ├── pipeline.py
│       └── scheduler.py
├── shared/
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── memory_bank.py
│   │   └── session_manager.py
│   ├── tools/
│   │   ├── mcp/
│   │   ├── custom/
│   │   ├── builtin/
│   │   └── openapi/
│   ├── observability/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   └── metrics.py
│   └── a2a/
│       ├── __init__.py
│       └── protocol.py
├── config/
│   ├── agents.yaml
│   ├── orchestration.yaml
│   └── memory.yaml
├── contracts/
│   └── solidity/
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
├── requirements.txt
└── main.py
```

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        GHOST PROTOCOL SYSTEM                        │
└─────────────────────────────────────────────────────────────────────┘

                    ┌──────────────────────────┐
                    │   User/Family Setup      │
                    │  - Profile Creation      │
                    │  - Digital Asset Mapping │
                    │  - Legacy Preferences    │
                    └────────────┬─────────────┘
                                 │
                                 ▼
        ┌────────────────────────────────────────────────┐
        │          ORCHESTRATOR (Main Pipeline)          │
        │  - Sequential Agent Coordination               │
        │  - Parallel Sub-Agent Management               │
        │  - 30-Day Loop Scheduler                       │
        └───┬────────────────────────────────────────┬───┘
            │                                        │
            │ Every 30 Days                         │ On Death Detection
            │                                        │
    ┌───────▼──────────┐                    ┌───────▼──────────────────┐
    │ LOOP AGENT       │                    │  TRIGGER SEQUENCE        │
    │ - Health Check   │                    └──────────┬───────────────┘
    │ - Status Update  │                               │
    └──────────────────┘                               │
                                                        │
                           ┌────────────────────────────┼────────────────┐
                           │                            │                │
                           ▼                            ▼                ▼
            ┌──────────────────────────┐  ┌─────────────────────────────────┐
            │ 1. DeathDetectionAgent   │  │  Parallel Sub-Agents            │
            │ ─────────────────────────│  │  ┌────────────────────────────┐ │
            │ Tools:                   │  │  │ - Social Media Scanner     │ │
            │ - Obituary API           │  │  │ - News API                 │ │
            │ - Death Registry         │  │  │ - Email Inbox Monitor      │ │
            │ - Social Proof           │  │  │ - Inactivity Detector      │ │
            │ - Family Notification    │  │  └────────────────────────────┘ │
            │                          │  └─────────────────────────────────┘
            │ Output: Death Confirmed  │
            └────────────┬─────────────┘
                         │
                         │ IF DEATH = TRUE
                         │
                         ▼
            ┌──────────────────────────┐
            │ 2. DigitalAssetAgent     │
            │ ─────────────────────────│
            │ Tools:                   │
            │ - Email Access (IMAP)    │
            │ - Cloud Scanner          │
            │ - Crypto Wallet Locator  │
            │ - Social Media API       │
            │ - Document Parser        │
            │                          │
            │ Output: Asset Inventory  │
            └────────────┬─────────────┘
                         │
                         ▼
            ┌──────────────────────────┐
            │ 3. LegacyAgent           │
            │    (AI Twin)             │
            │ ─────────────────────────│
            │ Components:              │
            │ - Memory Replay          │
            │ - Voice Clone            │
            │ - Message Generator      │
            │ - Family Notifier        │
            │                          │
            │ Tools:                   │
            │ - Email Composer         │
            │ - Video Message Creator  │
            │ - Social Post Scheduler  │
            │                          │
            │ Output: Messages Sent    │
            └────────────┬─────────────┘
                         │
                         ▼
            ┌──────────────────────────┐
            │ 4. SmartContractAgent    │
            │ ─────────────────────────│
            │ Tools:                   │
            │ - Blockchain RPC         │
            │ - Wallet Integration     │
            │ - Contract Executor      │
            │ - Multi-Sig Handler      │
            │                          │
            │ Output: Assets Transferred│
            └──────────────────────────┘

                         │
                         ▼
            ┌──────────────────────────┐
            │   COMPLETION REPORT      │
            │ - Logs                   │
            │ - Audit Trail            │
            │ - Family Dashboard       │
            └──────────────────────────┘
```

## Agent Descriptions

### 1. DeathDetectionAgent
**Purpose:** Continuously monitors for signs of user death through multiple data sources.

**Key Responsibilities:**
- Query obituary databases and death registries
- Monitor social media for condolence patterns
- Analyze email inbox for death-related keywords
- Track user inactivity across platforms
- Coordinate parallel sub-agents for distributed detection
- Implement confidence scoring system (threshold: 95%+)
- Send verification requests to designated family contacts

**Inputs:** User profile, monitoring configuration
**Outputs:** Death confirmation (Boolean + confidence score + evidence)

---

### 2. DigitalAssetAgent
**Purpose:** Discovers, catalogs, and prepares digital assets for transfer.

**Key Responsibilities:**
- Scan email for account confirmations and receipts
- Identify cloud storage locations (Google Drive, Dropbox, etc.)
- Detect cryptocurrency wallets and keys
- Map social media accounts
- Extract login credentials from secure vaults
- Generate comprehensive asset inventory with access metadata
- Classify assets by type and priority

**Inputs:** User credentials (encrypted), asset hints
**Outputs:** Structured asset inventory (JSON), access credentials, priority rankings

---

### 3. LegacyAgent (AI Twin)
**Purpose:** Creates personalized farewell messages and maintains digital presence post-mortem.

**Key Components:**

**AI Twin Engine:**
- Trained on user's communication history (emails, messages, journals)
- Mimics writing style, tone, and personality
- Stores episodic memories and important life events
- Generates contextually appropriate messages

**Execution Functions:**
- Compose personalized emails to family/friends
- Create video messages (text-to-speech with cloned voice)
- Schedule social media farewell posts
- Deliver time-released messages (birthdays, anniversaries)
- Provide closure through simulated conversations

**Inputs:** User memory bank, recipient list, message templates
**Outputs:** Generated messages, delivery confirmations, interaction logs

---

### 4. SmartContractAgent
**Purpose:** Executes blockchain-based asset transfers via smart contracts.

**Key Responsibilities:**
- Deploy or interact with pre-configured smart contracts
- Verify beneficiary wallet addresses
- Execute multi-signature transactions
- Transfer cryptocurrency holdings
- Distribute NFTs and digital collectibles
- Handle gas fee optimization
- Generate immutable audit trail on-chain
- Support multiple blockchain networks (Ethereum, Polygon, etc.)

**Inputs:** Asset inventory, beneficiary mappings, smart contract addresses
**Outputs:** Transaction hashes, transfer confirmations, gas reports

---

## Multi-Agent Orchestration

### Sequential Pipeline
```
DeathDetectionAgent → DigitalAssetAgent → LegacyAgent → SmartContractAgent
```

**Flow Logic:**
1. **Gate 1:** DeathDetectionAgent runs continuously until death confirmed
2. **Gate 2:** Only trigger DigitalAssetAgent if death = TRUE
3. **Gate 3:** LegacyAgent executes in parallel with SmartContractAgent
4. **Gate 4:** Final verification and reporting

**State Management:**
- Each agent outputs state to shared memory
- Next agent reads previous state before execution
- Rollback capability for failed steps
- Human-in-the-loop checkpoints (family approval)

---

### Parallel Sub-Agents

**Within DeathDetectionAgent:**
```
┌─────────────────────┐
│ ObituaryScanner     │──┐
│ SocialMediaMonitor  │──┤
│ EmailAnalyzer       │──┼──→ Confidence Aggregator → Final Decision
│ InactivityTracker   │──┤
│ NewsAPIChecker      │──┘
└─────────────────────┘
```

**Within DigitalAssetAgent:**
```
┌─────────────────────┐
│ EmailVaultScanner   │──┐
│ CloudDiscovery      │──┤
│ CryptoWalletFinder  │──┼──→ Asset Aggregator → Inventory
│ SocialAccountMapper │──┤
└─────────────────────┘
```

**Benefits:**
- Faster data collection
- Redundancy and cross-validation
- Independent failure handling

---

### Loop Agent (30-Day Delay)

**Purpose:** Periodic health checks and status updates during monitoring phase.

**Schedule:**
```
Day 0 → Day 30 → Day 60 → Day 90 → ... → Death Event
  ↓       ↓        ↓        ↓
Check   Check    Check    Check
```

**Loop Agent Tasks:**
1. Run lightweight death detection checks
2. Update user activity logs
3. Verify system health (APIs, credentials)
4. Send "still alive" confirmation to user
5. Refresh authentication tokens
6. Log system status to memory bank

**Implementation:**
- Cron-based scheduler in orchestrator
- Async task queue (Celery/APScheduler)
- Exponential backoff on failures
- Email alerts on missed check-ins

---

## ADK Concepts (To Be Implemented)

### 1. Tools
**MCP (Model Context Protocol):**
- Standardized tool interface for agents
- Shared tool registry across agents
- Context-aware tool selection

**Custom Tools:**
- DeathRegistryAPI
- EmailVaultScanner
- CryptoWalletDetector
- SocialMediaPoster

**Built-in Tools:**
- File I/O
- HTTP requests
- Database queries
- Encryption/decryption

**OpenAPI Tools:**
- Dynamic API client generation
- Automatic schema validation
- Rate limiting and retries

---

### 2. Memory Bank + Sessions

**Memory Bank Structure:**
```
- User Profile Memory
  ├── Personal Info
  ├── Communication History
  ├── Life Events Timeline
  └── Preferences

- Agent Memory
  ├── Detection History
  ├── Asset Discovery Logs
  ├── Message Drafts
  └── Transaction Records

- Session Memory
  ├── Current Pipeline State
  ├── Agent Outputs
  └── Error Logs
```

**Session Management:**
- Persistent sessions across agent handoffs
- State snapshots for rollback
- Memory retrieval via semantic search
- Privacy-preserving encryption

---

### 3. Long-Running Operations

**Challenges:**
- Death detection may take months/years
- Blockchain confirmations require waiting
- Email delivery scheduling spans time

**Solutions:**
- Async task queues
- Webhook-based callbacks
- Persistent job tracking
- Resume-from-checkpoint logic

---

### 4. Observability

**Monitoring:**
- Agent execution traces
- Tool call logs
- Performance metrics (latency, success rate)
- Cost tracking (API calls, LLM tokens)

**Dashboards:**
- Real-time pipeline status
- Detection confidence visualization
- Asset discovery progress
- Family-facing transparency portal

**Alerting:**
- Critical failures
- Death detection triggers
- Security anomalies

---

### 5. A2A Protocol (Agent-to-Agent)

**Communication Patterns:**
- Synchronous handoffs (pipeline steps)
- Asynchronous notifications (sub-agents → parent)
- Broadcast updates (orchestrator → all agents)

**Message Format:**
```
{
  "sender": "DeathDetectionAgent",
  "receiver": "DigitalAssetAgent",
  "type": "DEATH_CONFIRMED",
  "payload": {
    "confidence": 0.98,
    "evidence": [...],
    "timestamp": "2025-11-25T18:00:00Z"
  },
  "session_id": "uuid-1234"
}
```

**Protocol Features:**
- Typed message schemas
- Acknowledgment system
- Retry logic
- Message queuing (RabbitMQ/Kafka)

---

## Next Steps
1. Implement individual agents (start with DeathDetectionAgent)
2. Build shared tool infrastructure
3. Design memory bank schema
4. Create orchestrator pipeline logic
5. Deploy smart contracts (testnet)
6. Integrate observability stack
7. End-to-end testing

---

**Version:** 1.0  
**Last Updated:** 2025-11-25  
**Status:** Architecture Design Phase
