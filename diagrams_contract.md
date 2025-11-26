# Smart Contract Lifecycle Diagram

## Blockchain Will Execution Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      SMART CONTRACT LIFECYCLE                               │
└─────────────────────────────────────────────────────────────────────────────┘

PHASE 1: DEPLOYMENT
═══════════════════════════════════════════════════════════════════════════

Owner (0xOwner)
    │
    │ Deploy SmartWill.sol
    │ Constructor args: [validators[], requiredValidations]
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ SmartWill Contract                                      │
│ Address: 0x1234...abcd                                  │
├─────────────────────────────────────────────────────────┤
│ State:                                                  │
│   owner = 0xOwner                                       │
│   validators = [0xVal1, 0xVal2, 0xVal3]                 │
│   requiredValidations = 2                               │
│   isDeathConfirmed = false                              │
│   willExecuted = false                                  │
│   lastActivityTimestamp = NOW                           │
│   beneficiaries = []                                    │
└─────────────────────────────────────────────────────────┘
    │
    │ Event: WillCreated(0xOwner, timestamp)
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ Blockchain Confirmation                                 │
│ Block: #12345678                                        │
│ Gas Used: 2,500,000                                     │
│ Status: Success ✓                                       │
└─────────────────────────────────────────────────────────┘


PHASE 2: SETUP (Owner Actions)
═══════════════════════════════════════════════════════════════════════════

Owner calls addBeneficiary()
    │
    ├─► addBeneficiary(0xSon, 6000)      // 60% share
    │   └─ Event: BeneficiaryAdded(0xSon, 6000)
    │
    ├─► addBeneficiary(0xDaughter, 4000) // 40% share
    │   └─ Event: BeneficiaryAdded(0xDaughter, 4000)
    │
    └─► Fund contract with 5 MATIC
        └─ Transfer 5 MATIC to contract address

Contract State Updated:
┌─────────────────────────────────────────────────────────┐
│ beneficiaries = [                                       │
│   {wallet: 0xSon, sharePercentage: 6000, claimed: false}│
│   {wallet: 0xDaughter, sharePercentage: 4000, ...}      │
│ ]                                                       │
│ balance = 5 MATIC                                       │
└─────────────────────────────────────────────────────────┘


PHASE 3: MONITORING (Owner Activity)
═══════════════════════════════════════════════════════════════════════════

Every 30 days, owner calls recordActivity()

Day 0          Day 30         Day 60         Day 90
  │              │              │              │
  │ Activity     │ Activity     │ (No activity)│ (No activity)
  │ Recorded     │ Recorded     │              │
  ▼              ▼              ▼              ▼
┌────────┐    ┌────────┐    ┌────────┐    ┌─────────────┐
│ Active │    │ Active │    │ ALERT! │    │ TRIGGER     │
│        │    │        │    │ 60 days│    │ Dead-Man    │
│        │    │        │    │inactive│    │ Switch      │
└────────┘    └────────┘    └────────┘    └─────────────┘

lastActivityTimestamp continuously updated
↓
If (NOW - lastActivityTimestamp) > 90 days → Dead-Man Switch


PHASE 4A: DEATH DETECTION (Multi-Sig Validation)
═══════════════════════════════════════════════════════════════════════════

Validator 1 calls reportDeath()
    │
    ├─► hasValidated[0xVal1] = true
    ├─► currentValidations = 1
    └─► Event: DeathValidated(0xVal1, 1)

Validator 2 calls reportDeath()
    │
    ├─► hasValidated[0xVal2] = true
    ├─► currentValidations = 2
    ├─► Event: DeathValidated(0xVal2, 2)
    │
    └─► currentValidations >= requiredValidations? YES!
        │
        ├─► isDeathConfirmed = true
        ├─► deathTimestamp = NOW
        ├─► Event: DeathConfirmed(timestamp, unlockTime)
        └─► Event: TimeLockActivated(unlockTime)

Contract State:
┌─────────────────────────────────────────────────────────┐
│ isDeathConfirmed = true                                 │
│ deathTimestamp = 1732579200  (Nov 25, 2025)             │
│ unlockTimestamp = 1735257600 (Dec 25, 2025) [+30 days] │
│ currentValidations = 2                                  │
└─────────────────────────────────────────────────────────┘


PHASE 4B: DEAD-MAN SWITCH (Alternative Path)
═══════════════════════════════════════════════════════════════════════════

Anyone calls triggerDeadManSwitch()
    │
    ├─► Check: (NOW - lastActivityTimestamp) >= 90 days?
    │   └─► YES: Owner inactive for 95 days
    │
    ├─► isDeathConfirmed = true
    ├─► deathTimestamp = NOW
    ├─► Event: DeadManSwitchTriggered(95)
    ├─► Event: DeathConfirmed(timestamp, unlockTime)
    └─► Event: TimeLockActivated(unlockTime)


PHASE 5: TIME-LOCK PERIOD (30 Days)
═══════════════════════════════════════════════════════════════════════════

Timeline:

Death Confirmed                                    Time-Lock Expires
      │                                                    │
      │◄───────────── 30 Days ──────────────────────────►│
      │                                                    │
      ▼                                                    ▼
Nov 25, 2025                                        Dec 25, 2025
1732579200                                          1735257600

During this period:
┌─────────────────────────────────────────────────────────┐
│ - Will CANNOT be executed                               │
│ - Family can contest if false trigger                   │
│ - Owner can emergency pause (if alive)                  │
│ - Blockchain time checked: block.timestamp              │
└─────────────────────────────────────────────────────────┘

Check time remaining:
    getTimeLockRemaining() → returns seconds until unlock


PHASE 6: WILL EXECUTION
═══════════════════════════════════════════════════════════════════════════

Dec 25, 2025 (Time-Lock Expired)

Anyone calls executeWill()
    │
    ├─► Verify: isDeathConfirmed? ✓
    ├─► Verify: block.timestamp >= (deathTimestamp + 30 days)? ✓
    ├─► Verify: !willExecuted? ✓
    │
    ├─► willExecuted = true
    │
    ├─► DISTRIBUTE ASSETS
    │   │
    │   ├─► Calculate shares from total balance (5 MATIC)
    │   │   ├─ Son: 5 * 6000/10000 = 3 MATIC
    │   │   └─ Daughter: 5 * 4000/10000 = 2 MATIC
    │   │
    │   ├─► Transfer 3 MATIC to 0xSon
    │   │   └─ Event: AssetDistributed(0xSon, 3 MATIC, "ETH")
    │   │
    │   └─► Transfer 2 MATIC to 0xDaughter
    │       └─ Event: AssetDistributed(0xDaughter, 2 MATIC, "ETH")
    │
    └─► Event: WillExecuted(timestamp)

Final Contract State:
┌─────────────────────────────────────────────────────────┐
│ willExecuted = true                                     │
│ balance = 0 MATIC (all distributed)                     │
│ beneficiaries[0].claimed = true                         │
│ beneficiaries[1].claimed = true                         │
└─────────────────────────────────────────────────────────┘


TRANSACTION FLOW
═══════════════════════════════════════════════════════════════════════════

executeWill() Transaction
         │
         ├─► Transaction Hash: 0xabc123def456...
         ├─► Block Number: #12456789
         ├─► Gas Used: 150,000
         ├─► Gas Price: 30 Gwei
         ├─► Total Cost: 0.0045 MATIC
         │
         └─► Status: Success ✓

Blockchain State:
┌────────────────────────────────────────────────────────┐
│ Block #12456789                                        │
│ Timestamp: 1735257605                                  │
│                                                        │
│ Transactions:                                          │
│   0xabc123... → SmartWill.executeWill()                │
│     ├─ Transfer: Contract → 0xSon (3 MATIC)            │
│     └─ Transfer: Contract → 0xDaughter (2 MATIC)       │
│                                                        │
│ Events:                                                │
│   - AssetDistributed(0xSon, 3000000000000000000, "ETH")│
│   - AssetDistributed(0xDaughter, 2000000000000000000)  │
│   - WillExecuted(1735257605)                           │
└────────────────────────────────────────────────────────┘


VERIFICATION (PolygonScan)
═══════════════════════════════════════════════════════════════════════════

https://mumbai.polygonscan.com/address/0x1234...abcd

┌────────────────────────────────────────────────────────┐
│ Contract Overview                                      │
├────────────────────────────────────────────────────────┤
│ Address:   0x1234...abcd                               │
│ Balance:   0 MATIC                                     │
│ Txn Count: 7                                           │
│ Verified:  ✓                                           │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ Transaction History                                    │
├────────────────────────────────────────────────────────┤
│ 1. Contract Creation        (Nov 20, 2025)             │
│ 2. addBeneficiary(0xSon)    (Nov 20, 2025)             │
│ 3. addBeneficiary(0xDaught) (Nov 20, 2025)             │
│ 4. Transfer In (5 MATIC)    (Nov 20, 2025)             │
│ 5. reportDeath (Val1)       (Nov 25, 2025)             │
│ 6. reportDeath (Val2)       (Nov 25, 2025)             │
│ 7. executeWill()            (Dec 25, 2025) ✓           │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ Events                                                 │
├────────────────────────────────────────────────────────┤
│ WillCreated(0xOwner, 1732060800)                       │
│ BeneficiaryAdded(0xSon, 6000)                          │
│ BeneficiaryAdded(0xDaughter, 4000)                     │
│ DeathValidated(0xVal1, 1)                              │
│ DeathValidated(0xVal2, 2)                              │
│ DeathConfirmed(1732579200, 1735257600)                 │
│ TimeLockActivated(1735257600)                          │
│ AssetDistributed(0xSon, 3 MATIC, "ETH")                │
│ AssetDistributed(0xDaughter, 2 MATIC, "ETH")           │
│ WillExecuted(1735257605)                               │
└────────────────────────────────────────────────────────┘


SECURITY FEATURES
═══════════════════════════════════════════════════════════════════════════

1. MULTI-SIG VALIDATION
   ┌────────────────────────────────────────┐
   │ Requires 2 out of 3 validators         │
   │ Prevents single validator false trigger│
   │ Validators: Family lawyer, trusted     │
   │             friend, estate executor    │
   └────────────────────────────────────────┘

2. TIME-LOCK (30 Days)
   ┌────────────────────────────────────────┐
   │ Cannot execute immediately after death │
   │ Gives time for:                        │
   │   - Family verification                │
   │   - Legal review                       │
   │   - Contest if needed                  │
   └────────────────────────────────────────┘

3. DEAD-MAN SWITCH
   ┌────────────────────────────────────────┐
   │ Auto-triggers if owner inactive 90+ days│
   │ Prevents will from never executing     │
   │ Owner must check-in periodically       │
   └────────────────────────────────────────┘

4. IMMUTABLE AUDIT TRAIL
   ┌────────────────────────────────────────┐
   │ All actions recorded on blockchain     │
   │ Cannot be deleted or modified          │
   │ Transparent and verifiable             │
   └────────────────────────────────────────┘

5. OWNER CONTROLS
   ┌────────────────────────────────────────┐
   │ Only owner can:                        │
   │   - Add/remove beneficiaries           │
   │   - Add/remove validators              │
   │   - Record activity                    │
   │   - Pause execution (emergency)        │
   └────────────────────────────────────────┘


FAILURE SCENARIOS
═══════════════════════════════════════════════════════════════════════════

Scenario 1: FALSE DEATH REPORT
    │
    ├─► Validator 1 reports death (malicious)
    │   └─ currentValidations = 1
    │
    ├─► Owner is ALIVE and sees notification
    │   └─ Owner calls recordActivity()
    │       └─ Resets suspicion, continues monitoring
    │
    └─► Multi-sig prevents single validator from triggering

Scenario 2: TIME-LOCK CONTEST
    │
    ├─► Death confirmed, time-lock active
    │   └─ Family discovers owner is alive
    │
    ├─► Owner calls emergencyPause() (if implemented)
    │   OR
    │   Family contacts validators to reverse
    │
    └─► 30-day period allows time for resolution

Scenario 3: LOST VALIDATOR KEYS
    │
    ├─► Only 1 validator can sign (2 lost keys)
    │   └─ Cannot reach required 2 signatures
    │
    ├─► Owner (while alive) can:
    │   └─ addValidator(newValidator)
    │   └─ removeValidator(lostValidator)
    │
    └─► Dead-man switch as fallback (90 days)

Scenario 4: NETWORK CONGESTION
    │
    ├─► Gas prices spike to 500 Gwei
    │   └─ executeWill() costs $50+
    │
    ├─► Wait for gas prices to drop
    │   OR
    │   Use flashbots/MEV for guaranteed execution
    │
    └─► No deadline after time-lock expires
```
