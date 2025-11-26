# Smart Contract Layer - Ghost Protocol

## Overview

Decentralized smart contract for automated digital will execution with time-lock, multi-sig approval, and dead-man switch.

## Files

### 1. `smart_will.sol`
Full Solidity contract implementing:
- **Time-lock**: 30-day delay after death confirmation
- **Multi-sig approval**: 2+ validators required to confirm death
- **Dead-man switch**: Auto-trigger after 90 days inactivity
- **Asset distribution**: Percentage-based beneficiary shares
- **Events**: Full audit trail on-chain

### 2. `deploy.py`
Python deployment script:
- Compiles Solidity contract using `solcx`
- Deploys to Mumbai testnet (Polygon)
- Saves ABI and deployment info
- Estimates gas costs

### 3. `mumbai_simulation.py`
Mock blockchain for testing:
- Simulates complete workflow without spending gas
- Dead-man switch scenario
- Multi-sig validation flow
- Asset distribution verification

### 4. `contract_interactions.py`
Python wrapper for contract interactions:
- Full ABI definition
- `SmartWillContract` class with all methods
- Write functions: `add_beneficiary`, `report_death`, `execute_will`
- Read functions: `get_beneficiary`, `is_death_confirmed`, `get_time_lock_remaining`
- Event parsing and transaction handling

## Smart Contract Features

### Time-Lock (30 days)
```solidity
uint256 public constant TIME_LOCK_PERIOD = 30 days;
```
After death confirmation, beneficiaries must wait 30 days before will execution.

### Multi-Sig Approval
```solidity
function reportDeath() external onlyValidator
```
Requires 2+ validators to confirm death. Prevents false triggers.

### Dead-Man Switch
```solidity
uint256 public constant INACTIVITY_THRESHOLD = 90 days;
function triggerDeadManSwitch() external
```
Auto-confirms death if owner inactive for 90+ days.

### Events
- `WillCreated` - Contract deployed
- `DeathValidated` - Validator confirms death
- `DeathConfirmed` - Multi-sig threshold reached
- `TimeLockActivated` - 30-day countdown starts
- `WillExecuted` - Assets distributed
- `AssetDistributed` - Per-beneficiary transfers
- `ActivityRecorded` - Owner check-in
- `DeadManSwitchTriggered` - Inactivity trigger

## Usage

### Deploy Contract
```bash
cd contracts
python deploy.py
```

### Run Simulation
```bash
python mumbai_simulation.py
```

### Interact with Contract
```python
from contract_interactions import SmartWillContract
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://rpc-mumbai.maticvigil.com"))
contract = SmartWillContract(w3, contract_address, private_key)

# Add beneficiary
contract.add_beneficiary("0xBeneficiary...", 6000)  # 60%

# Record activity
contract.record_activity()

# Check status
contract.is_death_confirmed()
contract.get_time_lock_remaining()
```

## Contract State Flow

```
1. DEPLOYED
   ↓
2. MONITORING (owner records activity)
   ↓
3. DEATH_REPORTED (validators submit confirmations)
   ↓
4. DEATH_CONFIRMED (multi-sig threshold reached)
   ↓
5. TIME_LOCK (30-day waiting period)
   ↓
6. WILL_EXECUTED (assets distributed)
```

## Gas Estimates (Mumbai Testnet)

- Deploy: ~2.5M gas (~$0.50)
- Add beneficiary: ~50k gas (~$0.01)
- Report death: ~60k gas (~$0.01)
- Execute will: ~150k gas (~$0.03)

## Security Features

1. **Owner-only functions**: `addBeneficiary`, `recordActivity`
2. **Validator-only**: `reportDeath`
3. **Time-lock protection**: Cannot execute will immediately
4. **Multi-sig**: Prevents single point of failure
5. **Immutable audit trail**: All events on-chain
6. **Reentrancy protection**: Uses transfer() for ETH

## Testing

### Unit Tests (Simulation)
```bash
python mumbai_simulation.py
```

### Testnet Deployment
1. Get Mumbai MATIC from faucet: https://faucet.polygon.technology/
2. Configure `deploy.py` with your private key
3. Run deployment script
4. Verify on PolygonScan: https://mumbai.polygonscan.com/

## Integration with Agents

**SmartContractAgent** uses this layer to:
1. Deploy contract on user setup
2. Add beneficiaries from user preferences
3. Execute will after death confirmation + time-lock
4. Monitor transaction status
5. Generate immutable audit trail

## Network Support

Currently configured for:
- **Mumbai Testnet** (Polygon)
- Chain ID: 80001
- RPC: https://rpc-mumbai.maticvigil.com

Can be adapted for:
- Polygon Mainnet
- Ethereum
- BSC
- Avalanche

## Next Steps

1. Deploy to Mumbai testnet
2. Test multi-sig flow with 3 validators
3. Verify time-lock mechanism
4. Test dead-man switch
5. Audit contract (optional: Certik/OpenZeppelin)
6. Integrate with SmartContractAgent

## License

MIT
