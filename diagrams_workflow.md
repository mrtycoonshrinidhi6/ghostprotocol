# Multi-Agent Workflow Diagram

## Complete Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        GHOST PROTOCOL - MULTI-AGENT WORKFLOW                │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────┐
                              │  USER SETUP      │
                              │  - Profile       │
                              │  - Validators    │
                              │  - Beneficiaries │
                              └────────┬─────────┘
                                       │
                                       ▼
                         ┌─────────────────────────┐
                         │   ORCHESTRATOR START    │
                         │   Session Created       │
                         │   State: MONITORING     │
                         └────────┬────────────────┘
                                  │
                      ┌───────────┴───────────┐
                      │                       │
                      ▼                       ▼
           ┌──────────────────┐    ┌──────────────────┐
           │  LOOP AGENT      │    │ MAIN PIPELINE    │
           │  (Background)    │    │ (Conditional)    │
           └──────────────────┘    └──────────────────┘
                  │                          │
                  │ Every 30 days            │ On Death
                  │                          │
                  ▼                          ▼
         ┌─────────────────┐      ┌──────────────────────┐
         │ Health Check    │      │ 1. DEATH DETECTION   │
         │ - API Status    │      │    AGENT             │
         │ - Token Refresh │      └──────────┬───────────┘
         │ - Activity Log  │                 │
         └─────────────────┘                 │
                  │                          │
                  └──────────┬───────────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Death Confirmed?    │
                  └──────┬──────────────┘
                         │
                    YES  │  NO → Continue Monitoring
                         │
                         ▼
              ┌─────────────────────────┐
              │ 2. DIGITAL ASSET AGENT  │
              │    (Parallel Execution) │
              └──────────┬──────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    ┌─────────┐    ┌──────────┐   ┌──────────┐
    │ Email   │    │ Wallet   │   │ Cloud    │
    │ Scanner │    │ Scanner  │   │ Scanner  │
    └────┬────┘    └────┬─────┘   └────┬─────┘
         │              │              │
         └──────────────┼──────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │ Asset Inventory  │
              │ Aggregated       │
              └─────────┬────────┘
                        │
                        │
         ┌──────────────┴──────────────┐
         │                             │
         ▼                             ▼
┌─────────────────────┐      ┌─────────────────────┐
│ 3. LEGACY AGENT     │      │ 4. SMART CONTRACT   │
│    (AI Twin)        │      │    AGENT            │
│                     │      │                     │
│ - Memory Compact    │      │ - Deploy Contract   │
│ - Message Gen       │      │ - Multi-Sig Wait    │
│ - Email/Video       │      │ - Time-Lock (30d)   │
│ - Schedule Send     │      │ - Execute Transfers │
└──────────┬──────────┘      └──────────┬──────────┘
           │                            │
           │ Parallel Execution         │
           │                            │
           └──────────┬─────────────────┘
                      │
                      ▼
            ┌──────────────────────┐
            │  COMPLETION          │
            │  - Audit Log         │
            │  - Family Notified   │
            │  - State: COMPLETED  │
            └──────────────────────┘


═══════════════════════════════════════════════════════════════════════════

AGENT-TO-AGENT MESSAGE FLOW
═══════════════════════════════════════════════════════════════════════════

DeathDetectionAgent
         │
         │ A2AMessage(DEATH_CONFIRMED, confidence=0.98)
         ▼
DigitalAssetAgent
         │
         │ A2AMessage(ASSETS_DISCOVERED, total=12)
         ├───────────────────┬──────────────────┐
         ▼                   ▼                  ▼
LegacyAgent         SmartContractAgent    Orchestrator
         │                   │                  │
         │                   │                  │
         └───────────────────┴──────────────────┘
                             │
                             ▼
                    Final Acknowledgment


═══════════════════════════════════════════════════════════════════════════

PARALLEL SUB-AGENT EXECUTION (Digital Asset Agent)
═══════════════════════════════════════════════════════════════════════════

DigitalAssetAgent.execute()
         │
         └─► ParallelCoordinator.run_all()
                      │
         ┌────────────┼────────────┬────────────┐
         │            │            │            │
         ▼            ▼            ▼            ▼
   EmailScan    WalletScan    CloudScan   SocialScan
   Agent        Agent         Agent       Agent
         │            │            │            │
         │ IMAP       │ Vault      │ Drive API  │ FB/Twitter
         │ Scan       │ Decrypt    │ OneDrive   │ API
         │            │            │            │
         ▼            ▼            ▼            ▼
   [2 accounts] [3 wallets]  [2 clouds]  [4 accounts]
         │            │            │            │
         └────────────┴────────────┴────────────┘
                      │
                      ▼
            ParallelCoordinator.aggregate()
                      │
                      ▼
              Asset Inventory (12 total)


═══════════════════════════════════════════════════════════════════════════

LOOP AGENT - 30-DAY HEALTH CHECK CYCLE
═══════════════════════════════════════════════════════════════════════════

Day 0              Day 30            Day 60            Day 90
  │                  │                 │                 │
  │ Start           │ Check #1        │ Check #2        │ Check #3
  │                  │                 │                 │
  ▼                  ▼                 ▼                 ▼
┌──────┐          ┌──────┐          ┌──────┐          ┌──────┐
│Health│          │Health│          │Health│          │Health│
│Check │          │Check │          │Check │          │Check │
└──┬───┘          └──┬───┘          └──┬───┘          └──┬───┘
   │                 │                 │                 │
   │ Status: OK      │ Status: OK      │ Inactive!       │ Trigger
   │                 │                 │ Warning sent    │ Dead-Man
   │                 │                 │                 │ Switch
   ▼                 ▼                 ▼                 ▼
Sleep 30d         Sleep 30d         Sleep 30d         Death
                                                        Confirmed


═══════════════════════════════════════════════════════════════════════════

STATE TRANSITIONS
═══════════════════════════════════════════════════════════════════════════

CREATED ──init──► MONITORING ──death──► DEATH_DETECTED ──trigger──► ASSET_SCANNING
                      │                                                    │
                      │                                                    │
                   pause                                                   │
                      │                                                    │
                      ▼                                                    │
                   PAUSED ◄────────resume────────────────────────────────┘
                      │                                                    │
                      │                                                    │
                      └──resume──► LEGACY_EXECUTING ──parallel──► CONTRACT_EXECUTING
                                          │                              │
                                          └──────────┬─────────────────┘
                                                     │
                                                     ▼
                                                COMPLETED
                                                     │
                                                     │
                                              Any stage │ error
                                                     │
                                                     ▼
                                                  FAILED


═══════════════════════════════════════════════════════════════════════════

TIMING DIAGRAM
═══════════════════════════════════════════════════════════════════════════

Time ──────────────────────────────────────────────────────────────────────►

0s                    Setup Complete
│
├─ Monitoring Phase (Continuous)
│  ├─ Loop Agent: Day 0 Check
│  ├─ Loop Agent: Day 30 Check
│  ├─ Loop Agent: Day 60 Check
│  └─ Loop Agent: Day 90 Check (Inactive!)
│
90d                   Dead-Man Switch Triggered
│
├─ Death Detection (5 min)
│  ├─ Obituary scan: 30s
│  ├─ Registry check: 45s
│  ├─ Social scan: 2m
│  └─ Confidence aggregate: 10s
│
90d + 5m              Death Confirmed (0.98 confidence)
│
├─ Asset Scanning (15 min)
│  ├─ Email scan: 3m (parallel)
│  ├─ Wallet scan: 5m (parallel)
│  ├─ Cloud scan: 4m (parallel)
│  └─ Social scan: 3m (parallel)
│
90d + 20m             Assets Discovered (12 total)
│
├─ Legacy Messages (10 min, parallel)
│  └─ AI Twin generates 5 messages
│
├─ Contract Execution (30 days + 5 min)
│  ├─ Contract deployed: 2m
│  ├─ Time-lock wait: 30 days
│  └─ Asset distribution: 3m
│
120d + 25m            COMPLETED

Total: ~120 days (90d monitoring + 30d time-lock + 25m execution)
```
