# 👻 Ghost Protocol - AI Digital Executor

An autonomous AI system that executes your digital will after death, managing asset distribution, sending legacy messages, and maintaining your digital presence through an AI twin.

## 🎯 What is Ghost Protocol?

Ghost Protocol is a multi-agent AI system that:
1. **Detects death** using multiple verification sources (obituaries, registries, social media)
2. **Discovers digital assets** (email, cloud storage, cryptocurrency, social accounts)
3. **Sends personalized messages** via an AI twin trained on your memories
4. **Executes smart contracts** to distribute assets to beneficiaries

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GHOST PROTOCOL SYSTEM                    │
└─────────────────────────────────────────────────────────────┘

         ┌──────────────┐
         │  Streamlit   │  ← Frontend UI
         │  Frontend    │
         └──────┬───────┘
                │
         ┌──────▼───────┐
         │   FastAPI    │  ← Backend API
         │   Backend    │
         └──────┬───────┘
                │
         ┌──────▼───────────┐
         │  Orchestrator    │  ← Agent Coordination
         └──────┬───────────┘
                │
    ┌───────────┼───────────┬──────────────┐
    ▼           ▼           ▼              ▼
┌────────┐ ┌─────────┐ ┌────────┐ ┌──────────────┐
│ Death  │ │ Digital │ │ Legacy │ │ Smart        │
│ Agent  │ │ Asset   │ │ Agent  │ │ Contract     │
│        │ │ Agent   │ │(AI Twin)│ │ Agent        │
└────────┘ └─────────┘ └────────┘ └──────────────┘
    │           │           │              │
    └───────────┴───────────┴──────────────┘
                │
         ┌──────▼───────┐
         │ Memory Bank  │  ← Long-term Memory
         │ + Sessions   │
         └──────────────┘
                │
         ┌──────▼───────┐
         │ Smart Will   │  ← Blockchain Layer
         │ (Solidity)   │
         └──────────────┘
```

## 📁 Project Structure

```
ghostprotocol/
├── ARCHITECTURE.md              # System architecture
├── agents_pseudocode.py         # Agent definitions (ADK-style)
├── tools_layer.py               # MCP, custom, built-in tools
├── memory_session.py            # Memory bank + session management
├── observability.py             # Logging, tracing, metrics
├── backend/
│   ├── api.py                   # FastAPI REST endpoints
│   └── requirements.txt
├── frontend/
│   ├── app.py                   # Streamlit UI
│   └── requirements.txt
├── contracts/
│   ├── smart_will.sol           # Solidity smart contract
│   ├── deploy.py                # Deployment script
│   ├── mumbai_simulation.py    # Testnet simulation
│   ├── contract_interactions.py # ABI + interactions
│   └── README.md
└── run.py                       # Quick start script
```

## 🚀 Quick Start

### Option 1: Automated (Recommended)
```bash
python run.py
```

### Option 2: Manual

**Start Backend:**
```bash
cd backend
pip install -r requirements.txt
python api.py
```

**Start Frontend (New Terminal):**
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### Access
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🤖 Four Core Agents

### 1. DeathDetectionAgent 🔍
**Purpose:** Continuously monitor for death signals

**Sources:**
- Obituary databases (Legacy.com, Tributes.com)
- Government death registries
- Social media condolence patterns
- Email inbox analysis
- News API

**Output:** Death confirmation with 95%+ confidence

### 2. DigitalAssetAgent 💰
**Purpose:** Discover and catalog all digital assets

**Scans:**
- Email accounts (Gmail, Outlook)
- Cloud storage (Google Drive, Dropbox, OneDrive)
- Cryptocurrency wallets (BTC, ETH, SOL)
- Social media (Facebook, Twitter, Instagram)

**Output:** Comprehensive asset inventory with access credentials

### 3. LegacyAgent (AI Twin) 💬
**Purpose:** Send personalized farewell messages

**Features:**
- Trained on your communication history
- Mimics your writing style and personality
- Generates contextual messages for loved ones
- Delivers time-released messages (birthdays, anniversaries)

**Output:** Personalized emails, video messages, social posts

### 4. SmartContractAgent ⚖️
**Purpose:** Execute blockchain-based asset distribution

**Features:**
- 30-day time-lock after death confirmation
- Multi-sig validation (2+ validators)
- Dead-man switch (90-day inactivity trigger)
- Immutable audit trail on-chain

**Output:** Transaction hashes, beneficiary transfers

## 🛠️ Technology Stack

**Agents & Orchestration:**
- Python 3.11+
- ADK (Agent Development Kit) concepts
- Async/await for parallel execution

**Backend:**
- FastAPI
- Pydantic for validation
- Uvicorn ASGI server

**Frontend:**
- Streamlit
- Pandas for data display
- Requests for API calls

**Blockchain:**
- Solidity 0.8.20
- Web3.py
- Mumbai Testnet (Polygon)

**Observability:**
- Structured logging (JSON)
- Distributed tracing (spans)
- Metrics collection (Prometheus-style)

## 📊 Features

### Multi-Agent Orchestration
- **Sequential pipeline:** Death → Assets → Legacy → Contract
- **Parallel execution:** Email scan + wallet scan run simultaneously
- **Loop agent:** 30-day health checks

### Memory & Context
- **Memory Bank:** Episodic, semantic, and procedural memories
- **Context compaction:** Fit 8000 tokens for AI twin generation
- **Session management:** Checkpoints, rollback, pause/resume

### Smart Contract
- **Time-lock:** 30-day waiting period
- **Multi-sig:** 2+ validators required
- **Dead-man switch:** Auto-trigger after 90 days inactivity
- **Asset distribution:** Percentage-based beneficiary shares

### Observability
- **Structured logs:** JSON-formatted for CloudWatch/Datadog
- **Tracing:** Distributed traces with trace_id/span_id
- **Metrics:** Accuracy, latency, satisfaction, time saved
- **Evaluation:** Mock dataset with test cases

## 📖 Documentation

- [**ARCHITECTURE.md**](ARCHITECTURE.md) - High-level system design
- [**agents_pseudocode.py**](agents_pseudocode.py) - Agent class definitions
- [**tools_layer.py**](tools_layer.py) - Tool schemas and usage
- [**memory_session.py**](memory_session.py) - Memory and session architecture
- [**observability.py**](observability.py) - Logging, tracing, metrics
- [**contracts/README.md**](contracts/README.md) - Smart contract documentation
- [**BACKEND_FRONTEND_README.md**](BACKEND_FRONTEND_README.md) - API and UI guide

## 🧪 Testing

### Unit Tests
```bash
pytest tests/
```

### Integration Tests
```bash
python contracts/mumbai_simulation.py
```

### Agent Evaluation
```python
from observability import AgentEvaluator

evaluator = AgentEvaluator(logger, metrics)
evaluator.load_mock_dataset()
report = evaluator.generate_report()
```

## 🔐 Security

1. **Encryption:** All credentials stored in encrypted vault
2. **Multi-sig:** Prevents single validator from triggering execution
3. **Time-lock:** 30-day delay prevents premature execution
4. **Audit trail:** All actions logged on blockchain
5. **Dead-man switch:** Requires 90+ days inactivity

## 🚢 Deployment

### Backend (Docker)
```bash
docker build -t ghost-protocol-backend -f backend/Dockerfile .
docker run -p 8000:8000 ghost-protocol-backend
```

### Frontend (Streamlit Cloud)
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Configure secrets
4. Deploy

### Smart Contract (Mumbai)
```bash
cd contracts
python deploy.py
```

## 📈 Roadmap

- [x] Architecture design
- [x] Agent pseudocode
- [x] Tool layer
- [x] Memory & session management
- [x] Observability layer
- [x] Smart contract (Solidity)
- [x] Backend API
- [x] Frontend UI
- [ ] Full agent implementation
- [ ] Database persistence
- [ ] Production deployment
- [ ] Security audit
- [ ] Mainnet launch

## 🤝 Contributing

This is a conceptual/educational project demonstrating multi-agent AI systems with blockchain integration.

## ⚠️ Disclaimer

Ghost Protocol is a proof-of-concept system. Do not use for actual estate planning without:
1. Legal consultation
2. Security audit
3. Testnet validation
4. Family approval

## 📄 License

MIT License - See LICENSE file

## 🙏 Acknowledgments

- ADK (Agent Development Kit) for agent architecture concepts
- OpenAI for LLM capabilities
- Polygon for blockchain infrastructure
- Streamlit for rapid UI development

---

**Built with ❤️ by GHOST-PROTOCOL-BUILDER**

For questions or issues, please open a GitHub issue.
