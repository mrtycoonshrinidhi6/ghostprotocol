"""
Smart Contract Interactions
ABI definitions and interaction functions for SmartWill contract
"""

from web3 import Web3
from typing import Dict, List, Any
import json


# ============================================================================
# ABI DEFINITION
# ============================================================================

SMART_WILL_ABI = [
    {
        "inputs": [
            {"internalType": "address[]", "name": "_validators", "type": "address[]"},
            {"internalType": "uint256", "name": "_requiredValidations", "type": "uint256"}
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}
        ],
        "name": "ActivityRecorded",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "beneficiary", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
            {"indexed": False, "internalType": "string", "name": "assetType", "type": "string"}
        ],
        "name": "AssetDistributed",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "beneficiary", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "sharePercentage", "type": "uint256"}
        ],
        "name": "BeneficiaryAdded",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "deathTimestamp", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "executionTimestamp", "type": "uint256"}
        ],
        "name": "DeathConfirmed",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "reporter", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}
        ],
        "name": "DeathReported",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "validator", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "validationCount", "type": "uint256"}
        ],
        "name": "DeathValidated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "inactiveDays", "type": "uint256"}
        ],
        "name": "DeadManSwitchTriggered",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "unlockTimestamp", "type": "uint256"}
        ],
        "name": "TimeLockActivated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "validator", "type": "address"}
        ],
        "name": "ValidatorAdded",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "validator", "type": "address"}
        ],
        "name": "ValidatorRemoved",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}
        ],
        "name": "WillExecuted",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "owner", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}
        ],
        "name": "WillCreated",
        "type": "event"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "_assetType", "type": "string"},
            {"internalType": "address", "name": "_tokenAddress", "type": "address"},
            {"internalType": "uint256", "name": "_tokenId", "type": "uint256"},
            {"internalType": "string", "name": "_metadataURI", "type": "string"}
        ],
        "name": "addAsset",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address payable", "name": "_wallet", "type": "address"},
            {"internalType": "uint256", "name": "_sharePercentage", "type": "uint256"}
        ],
        "name": "addBeneficiary",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_validator", "type": "address"}
        ],
        "name": "addValidator",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "assetIndex", "type": "uint256"}
        ],
        "name": "claimAsset",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "executeWill",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "index", "type": "uint256"}
        ],
        "name": "getBeneficiary",
        "outputs": [
            {"internalType": "address", "name": "wallet", "type": "address"},
            {"internalType": "uint256", "name": "sharePercentage", "type": "uint256"},
            {"internalType": "bool", "name": "claimed", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getBeneficiaryCount",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getContractBalance",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getInactiveDays",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getTimeLockRemaining",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "recordActivity",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_validator", "type": "address"}
        ],
        "name": "removeValidator",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "reportDeath",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "triggerDeadManSwitch",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {"internalType": "address", "name": "", "type": "address"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "isDeathConfirmed",
        "outputs": [
            {"internalType": "bool", "name": "", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "willExecuted",
        "outputs": [
            {"internalType": "bool", "name": "", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "stateMutability": "payable",
        "type": "receive"
    }
]


# ============================================================================
# CONTRACT INTERACTION CLASS
# ============================================================================

class SmartWillContract:
    """Interact with deployed SmartWill contract"""
    
    def __init__(self, w3: Web3, contract_address: str, private_key: str):
        self.w3 = w3
        self.contract_address = Web3.to_checksum_address(contract_address)
        self.contract = w3.eth.contract(address=self.contract_address, abi=SMART_WILL_ABI)
        self.private_key = private_key
        self.account = w3.eth.account.from_key(private_key)
    
    # ---- Write Functions (State-Changing) ----
    
    def add_beneficiary(self, wallet_address: str, share_percentage: int) -> Dict:
        """Add beneficiary to will"""
        
        function = self.contract.functions.addBeneficiary(
            Web3.to_checksum_address(wallet_address),
            share_percentage
        )
        
        return self._send_transaction(function)
    
    def add_asset(self, asset_type: str, token_address: str, 
                  token_id: int, metadata_uri: str) -> Dict:
        """Add digital asset to inventory"""
        
        function = self.contract.functions.addAsset(
            asset_type,
            Web3.to_checksum_address(token_address) if token_address else "0x" + "0"*40,
            token_id,
            metadata_uri
        )
        
        return self._send_transaction(function)
    
    def record_activity(self) -> Dict:
        """Record owner activity (prevents dead-man switch)"""
        
        function = self.contract.functions.recordActivity()
        return self._send_transaction(function)
    
    def report_death(self) -> Dict:
        """Validator reports death (multi-sig)"""
        
        function = self.contract.functions.reportDeath()
        return self._send_transaction(function)
    
    def trigger_dead_man_switch(self) -> Dict:
        """Trigger dead-man switch after inactivity"""
        
        function = self.contract.functions.triggerDeadManSwitch()
        return self._send_transaction(function)
    
    def execute_will(self) -> Dict:
        """Execute will and distribute assets"""
        
        function = self.contract.functions.executeWill()
        return self._send_transaction(function)
    
    def add_validator(self, validator_address: str) -> Dict:
        """Add new validator"""
        
        function = self.contract.functions.addValidator(
            Web3.to_checksum_address(validator_address)
        )
        return self._send_transaction(function)
    
    def remove_validator(self, validator_address: str) -> Dict:
        """Remove validator"""
        
        function = self.contract.functions.removeValidator(
            Web3.to_checksum_address(validator_address)
        )
        return self._send_transaction(function)
    
    # ---- Read Functions (View) ----
    
    def get_owner(self) -> str:
        """Get contract owner address"""
        return self.contract.functions.owner().call()
    
    def is_death_confirmed(self) -> bool:
        """Check if death is confirmed"""
        return self.contract.functions.isDeathConfirmed().call()
    
    def is_will_executed(self) -> bool:
        """Check if will has been executed"""
        return self.contract.functions.willExecuted().call()
    
    def get_time_lock_remaining(self) -> int:
        """Get remaining time-lock seconds"""
        return self.contract.functions.getTimeLockRemaining().call()
    
    def get_inactive_days(self) -> int:
        """Get days since last activity"""
        return self.contract.functions.getInactiveDays().call()
    
    def get_contract_balance(self) -> int:
        """Get contract balance in wei"""
        return self.contract.functions.getContractBalance().call()
    
    def get_beneficiary_count(self) -> int:
        """Get number of beneficiaries"""
        return self.contract.functions.getBeneficiaryCount().call()
    
    def get_beneficiary(self, index: int) -> Dict:
        """Get beneficiary details"""
        wallet, share, claimed = self.contract.functions.getBeneficiary(index).call()
        return {
            "wallet": wallet,
            "share_percentage": share,
            "claimed": claimed
        }
    
    def get_all_beneficiaries(self) -> List[Dict]:
        """Get all beneficiaries"""
        count = self.get_beneficiary_count()
        return [self.get_beneficiary(i) for i in range(count)]
    
    # ---- Transaction Helpers ----
    
    def _send_transaction(self, function) -> Dict:
        """Send transaction to blockchain"""
        
        # Build transaction
        transaction = function.build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 500000,
            'gasPrice': self.w3.eth.gas_price,
        })
        
        # Sign transaction
        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
        
        # Send transaction
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for receipt
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            "tx_hash": tx_hash.hex(),
            "block_number": tx_receipt.blockNumber,
            "gas_used": tx_receipt.gasUsed,
            "status": tx_receipt.status,
            "logs": self._parse_logs(tx_receipt.logs)
        }
    
    def _parse_logs(self, logs: List) -> List[Dict]:
        """Parse transaction logs (events)"""
        
        parsed = []
        
        for log in logs:
            try:
                event = self.contract.events
                # Try to decode each event type
                for event_name in ["BeneficiaryAdded", "ActivityRecorded", "DeathValidated", 
                                  "DeathConfirmed", "WillExecuted", "AssetDistributed"]:
                    try:
                        decoded = getattr(event, event_name)().process_log(log)
                        parsed.append({
                            "event": event_name,
                            "args": dict(decoded.args)
                        })
                        break
                    except:
                        continue
            except:
                pass
        
        return parsed
    
    # ---- Utility Functions ----
    
    def fund_contract(self, amount_matic: float) -> Dict:
        """Send MATIC to contract"""
        
        amount_wei = self.w3.to_wei(amount_matic, 'ether')
        
        transaction = {
            'from': self.account.address,
            'to': self.contract_address,
            'value': amount_wei,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 21000,
            'gasPrice': self.w3.eth.gas_price,
        }
        
        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            "tx_hash": tx_hash.hex(),
            "amount_matic": amount_matic,
            "status": tx_receipt.status
        }


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def example_contract_interactions():
    """Example usage of contract interaction functions"""
    
    # Setup
    w3 = Web3(Web3.HTTPProvider("https://rpc-mumbai.maticvigil.com"))
    contract_address = "0x1234567890123456789012345678901234567890"
    private_key = "YOUR_PRIVATE_KEY"
    
    # Initialize contract
    contract = SmartWillContract(w3, contract_address, private_key)
    
    # Example 1: Add beneficiary
    result = contract.add_beneficiary(
        wallet_address="0xBeneficiary1...",
        share_percentage=6000  # 60%
    )
    print(f"Beneficiary added: {result['tx_hash']}")
    
    # Example 2: Record activity
    result = contract.record_activity()
    print(f"Activity recorded: {result['tx_hash']}")
    
    # Example 3: Check status
    owner = contract.get_owner()
    is_confirmed = contract.is_death_confirmed()
    inactive_days = contract.get_inactive_days()
    
    print(f"Owner: {owner}")
    print(f"Death confirmed: {is_confirmed}")
    print(f"Inactive days: {inactive_days}")
    
    # Example 4: Get all beneficiaries
    beneficiaries = contract.get_all_beneficiaries()
    for i, b in enumerate(beneficiaries):
        print(f"Beneficiary {i}: {b['wallet']} ({b['share_percentage']/100}%)")
    
    # Example 5: Fund contract
    result = contract.fund_contract(amount_matic=5.0)
    print(f"Contract funded: {result['tx_hash']}")
    
    # Example 6: Execute will (after time-lock)
    remaining = contract.get_time_lock_remaining()
    if remaining == 0:
        result = contract.execute_will()
        print(f"Will executed: {result['tx_hash']}")
        print(f"Events: {result['logs']}")


# ============================================================================
# EXPORT ABI TO FILE
# ============================================================================

def save_abi_to_file(filename: str = "SmartWill_ABI.json"):
    """Save ABI to JSON file"""
    with open(f"contracts/{filename}", 'w') as f:
        json.dump(SMART_WILL_ABI, f, indent=2)
    print(f"ABI saved to contracts/{filename}")


if __name__ == "__main__":
    # Save ABI
    save_abi_to_file()
    
    # Print sample interaction code
    print("\nSample Contract Interaction:")
    print("="*60)
    example_contract_interactions()
