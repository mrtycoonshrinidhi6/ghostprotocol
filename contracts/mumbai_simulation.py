"""
Mumbai Testnet Simulation
Mock blockchain interactions for testing
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import time


# ============================================================================
# MOCK BLOCKCHAIN STATE
# ============================================================================

@dataclass
class MockTransaction:
    tx_hash: str
    from_address: str
    to_address: str
    value: int
    gas_used: int
    status: bool
    block_number: int
    timestamp: datetime


class MockBlockchain:
    """Simulated blockchain for testing"""
    
    def __init__(self):
        self.blocks = []
        self.transactions = []
        self.accounts = {}
        self.contracts = {}
        self.current_block = 0
        self.current_timestamp = int(datetime.now().timestamp())
        
        # Initialize test accounts
        self._init_accounts()
    
    def _init_accounts(self):
        """Create test accounts with balances"""
        self.accounts = {
            "0xOwner": {"balance": 10 * 10**18, "nonce": 0},  # 10 MATIC
            "0xValidator1": {"balance": 1 * 10**18, "nonce": 0},
            "0xValidator2": {"balance": 1 * 10**18, "nonce": 0},
            "0xValidator3": {"balance": 1 * 10**18, "nonce": 0},
            "0xBeneficiary1": {"balance": 0, "nonce": 0},
            "0xBeneficiary2": {"balance": 0, "nonce": 0},
        }
    
    def deploy_contract(self, from_address: str, bytecode: str, 
                       constructor_args: List) -> str:
        """Deploy contract to mock blockchain"""
        
        contract_address = f"0xContract{len(self.contracts)}"
        
        # Initialize contract state
        self.contracts[contract_address] = {
            "bytecode": bytecode,
            "storage": {
                "owner": from_address,
                "deathTimestamp": 0,
                "isDeathConfirmed": False,
                "willExecuted": False,
                "lastActivityTimestamp": self.current_timestamp,
                "validators": constructor_args[0],
                "requiredValidations": constructor_args[1],
                "currentValidations": 0,
                "beneficiaries": [],
                "assets": [],
                "balance": 0
            }
        }
        
        # Create transaction
        tx_hash = self._create_transaction(
            from_address=from_address,
            to_address=contract_address,
            value=0,
            gas_used=2500000
        )
        
        print(f"Contract deployed: {contract_address}")
        print(f"Transaction: {tx_hash}")
        
        return contract_address
    
    def call_function(self, contract_address: str, from_address: str,
                     function_name: str, args: List = None) -> Dict:
        """Call contract function"""
        
        if contract_address not in self.contracts:
            raise ValueError("Contract not found")
        
        contract = self.contracts[contract_address]
        args = args or []
        
        # Simulate function execution
        if function_name == "addBeneficiary":
            return self._add_beneficiary(contract, from_address, args)
        
        elif function_name == "recordActivity":
            return self._record_activity(contract, from_address)
        
        elif function_name == "reportDeath":
            return self._report_death(contract, from_address)
        
        elif function_name == "triggerDeadManSwitch":
            return self._trigger_dead_man_switch(contract)
        
        elif function_name == "executeWill":
            return self._execute_will(contract, contract_address)
        
        elif function_name == "getTimeLockRemaining":
            return self._get_time_lock_remaining(contract)
        
        elif function_name == "getInactiveDays":
            return self._get_inactive_days(contract)
        
        else:
            return {"error": f"Function {function_name} not implemented"}
    
    def _add_beneficiary(self, contract: Dict, from_address: str, args: List) -> Dict:
        """Add beneficiary to will"""
        
        if from_address != contract["storage"]["owner"]:
            return {"error": "Only owner can add beneficiaries"}
        
        wallet, share = args[0], args[1]
        
        contract["storage"]["beneficiaries"].append({
            "wallet": wallet,
            "sharePercentage": share,
            "claimed": False
        })
        
        tx_hash = self._create_transaction(from_address, "contract", 0, 50000)
        
        return {
            "success": True,
            "tx_hash": tx_hash,
            "event": f"BeneficiaryAdded({wallet}, {share})"
        }
    
    def _record_activity(self, contract: Dict, from_address: str) -> Dict:
        """Record owner activity"""
        
        if from_address != contract["storage"]["owner"]:
            return {"error": "Only owner can record activity"}
        
        contract["storage"]["lastActivityTimestamp"] = self.current_timestamp
        
        tx_hash = self._create_transaction(from_address, "contract", 0, 30000)
        
        return {
            "success": True,
            "tx_hash": tx_hash,
            "event": f"ActivityRecorded({self.current_timestamp})"
        }
    
    def _report_death(self, contract: Dict, from_address: str) -> Dict:
        """Validator reports death"""
        
        if from_address not in contract["storage"]["validators"]:
            return {"error": "Only validators can report death"}
        
        if contract["storage"]["isDeathConfirmed"]:
            return {"error": "Death already confirmed"}
        
        contract["storage"]["currentValidations"] += 1
        
        tx_hash = self._create_transaction(from_address, "contract", 0, 60000)
        
        # Check if threshold reached
        if contract["storage"]["currentValidations"] >= contract["storage"]["requiredValidations"]:
            contract["storage"]["isDeathConfirmed"] = True
            contract["storage"]["deathTimestamp"] = self.current_timestamp
            
            return {
                "success": True,
                "tx_hash": tx_hash,
                "event": "DeathConfirmed",
                "unlock_timestamp": self.current_timestamp + (30 * 24 * 3600)
            }
        
        return {
            "success": True,
            "tx_hash": tx_hash,
            "event": f"DeathValidated({contract['storage']['currentValidations']})"
        }
    
    def _trigger_dead_man_switch(self, contract: Dict) -> Dict:
        """Trigger dead-man switch after inactivity"""
        
        inactive_seconds = self.current_timestamp - contract["storage"]["lastActivityTimestamp"]
        threshold = 90 * 24 * 3600  # 90 days
        
        if inactive_seconds < threshold:
            return {"error": f"Only {inactive_seconds // 86400} days inactive, need 90"}
        
        contract["storage"]["isDeathConfirmed"] = True
        contract["storage"]["deathTimestamp"] = self.current_timestamp
        
        tx_hash = self._create_transaction("system", "contract", 0, 80000)
        
        return {
            "success": True,
            "tx_hash": tx_hash,
            "event": "DeadManSwitchTriggered",
            "inactive_days": inactive_seconds // 86400
        }
    
    def _execute_will(self, contract: Dict, contract_address: str) -> Dict:
        """Execute will and distribute assets"""
        
        if not contract["storage"]["isDeathConfirmed"]:
            return {"error": "Death not confirmed"}
        
        time_lock_end = contract["storage"]["deathTimestamp"] + (30 * 24 * 3600)
        if self.current_timestamp < time_lock_end:
            return {"error": f"Time-lock not expired. {(time_lock_end - self.current_timestamp) // 86400} days remaining"}
        
        if contract["storage"]["willExecuted"]:
            return {"error": "Will already executed"}
        
        # Distribute assets
        total_balance = contract["storage"]["balance"]
        distributions = []
        
        for beneficiary in contract["storage"]["beneficiaries"]:
            share_amount = (total_balance * beneficiary["sharePercentage"]) // 10000
            
            if share_amount > 0:
                # Transfer to beneficiary
                self.accounts[beneficiary["wallet"]]["balance"] += share_amount
                beneficiary["claimed"] = True
                
                distributions.append({
                    "wallet": beneficiary["wallet"],
                    "amount": share_amount,
                    "asset_type": "MATIC"
                })
        
        contract["storage"]["willExecuted"] = True
        contract["storage"]["balance"] = 0
        
        tx_hash = self._create_transaction("system", contract_address, 0, 150000)
        
        return {
            "success": True,
            "tx_hash": tx_hash,
            "event": "WillExecuted",
            "distributions": distributions
        }
    
    def _get_time_lock_remaining(self, contract: Dict) -> Dict:
        """Get remaining time-lock duration"""
        
        if not contract["storage"]["isDeathConfirmed"]:
            return {"remaining_seconds": 0}
        
        unlock_time = contract["storage"]["deathTimestamp"] + (30 * 24 * 3600)
        
        if self.current_timestamp >= unlock_time:
            return {"remaining_seconds": 0}
        
        return {"remaining_seconds": unlock_time - self.current_timestamp}
    
    def _get_inactive_days(self, contract: Dict) -> Dict:
        """Get days since last activity"""
        
        inactive_seconds = self.current_timestamp - contract["storage"]["lastActivityTimestamp"]
        return {"inactive_days": inactive_seconds // 86400}
    
    def _create_transaction(self, from_address: str, to_address: str,
                          value: int, gas_used: int) -> str:
        """Create mock transaction"""
        
        self.current_block += 1
        
        tx_hash = f"0x{''.join([str(i) for i in range(64)])}"[:10]
        
        tx = MockTransaction(
            tx_hash=tx_hash,
            from_address=from_address,
            to_address=to_address,
            value=value,
            gas_used=gas_used,
            status=True,
            block_number=self.current_block,
            timestamp=datetime.now()
        )
        
        self.transactions.append(tx)
        return tx_hash
    
    def advance_time(self, days: int):
        """Fast-forward blockchain time"""
        self.current_timestamp += days * 24 * 3600
        print(f"Time advanced by {days} days")
    
    def fund_contract(self, contract_address: str, amount: int):
        """Add funds to contract"""
        if contract_address in self.contracts:
            self.contracts[contract_address]["storage"]["balance"] += amount
            print(f"Funded contract with {amount / 10**18} MATIC")


# ============================================================================
# SIMULATION SCENARIOS
# ============================================================================

def simulate_complete_workflow():
    """Simulate complete Ghost Protocol workflow"""
    
    print("="*60)
    print("GHOST PROTOCOL - MUMBAI SIMULATION")
    print("="*60 + "\n")
    
    # Initialize blockchain
    blockchain = MockBlockchain()
    
    # Step 1: Deploy contract
    print("Step 1: Deploy SmartWill contract")
    contract_address = blockchain.deploy_contract(
        from_address="0xOwner",
        bytecode="0x608060405234801561001057600080fd5b50...",
        constructor_args=[
            ["0xValidator1", "0xValidator2", "0xValidator3"],
            2  # Required validations
        ]
    )
    print()
    
    # Step 2: Add beneficiaries
    print("Step 2: Add beneficiaries")
    blockchain.call_function(contract_address, "0xOwner", "addBeneficiary", 
                           ["0xBeneficiary1", 6000])  # 60%
    blockchain.call_function(contract_address, "0xOwner", "addBeneficiary",
                           ["0xBeneficiary2", 4000])  # 40%
    print()
    
    # Step 3: Fund contract
    print("Step 3: Fund contract")
    blockchain.fund_contract(contract_address, 5 * 10**18)  # 5 MATIC
    print()
    
    # Step 4: Owner records activity
    print("Step 4: Owner records activity")
    result = blockchain.call_function(contract_address, "0xOwner", "recordActivity")
    print(f"Activity recorded: {result['event']}")
    print()
    
    # Step 5: Death detection (multi-sig)
    print("Step 5: Death detection via multi-sig")
    result1 = blockchain.call_function(contract_address, "0xValidator1", "reportDeath")
    print(f"Validator 1: {result1['event']}")
    
    result2 = blockchain.call_function(contract_address, "0xValidator2", "reportDeath")
    print(f"Validator 2: {result2['event']}")
    
    if "unlock_timestamp" in result2:
        unlock_date = datetime.fromtimestamp(result2["unlock_timestamp"])
        print(f"Time-lock will expire at: {unlock_date}")
    print()
    
    # Step 6: Wait for time-lock (simulate)
    print("Step 6: Time-lock period (30 days)")
    remaining = blockchain.call_function(contract_address, "0xOwner", "getTimeLockRemaining")
    print(f"Remaining: {remaining['remaining_seconds'] // 86400} days")
    
    blockchain.advance_time(31)  # Advance 31 days
    
    remaining = blockchain.call_function(contract_address, "0xOwner", "getTimeLockRemaining")
    print(f"After time advance - Remaining: {remaining['remaining_seconds']} seconds")
    print()
    
    # Step 7: Execute will
    print("Step 7: Execute will and distribute assets")
    result = blockchain.call_function(contract_address, "0xOwner", "executeWill")
    
    if result.get("success"):
        print("Will executed successfully!")
        print("\nDistributions:")
        for dist in result["distributions"]:
            print(f"  - {dist['wallet']}: {dist['amount'] / 10**18} MATIC ({dist['asset_type']})")
    print()
    
    # Step 8: Verify balances
    print("Step 8: Final balances")
    print(f"Beneficiary 1: {blockchain.accounts['0xBeneficiary1']['balance'] / 10**18} MATIC")
    print(f"Beneficiary 2: {blockchain.accounts['0xBeneficiary2']['balance'] / 10**18} MATIC")
    print()
    
    print("="*60)
    print("SIMULATION COMPLETE")
    print("="*60)


def simulate_dead_man_switch():
    """Simulate dead-man switch scenario"""
    
    print("\n" + "="*60)
    print("DEAD-MAN SWITCH SIMULATION")
    print("="*60 + "\n")
    
    blockchain = MockBlockchain()
    
    # Deploy
    contract_address = blockchain.deploy_contract(
        "0xOwner", "bytecode", [["0xValidator1", "0xValidator2"], 2]
    )
    
    # Check inactivity
    result = blockchain.call_function(contract_address, "0xOwner", "getInactiveDays")
    print(f"Current inactivity: {result['inactive_days']} days\n")
    
    # Advance time 95 days
    blockchain.advance_time(95)
    
    result = blockchain.call_function(contract_address, "0xOwner", "getInactiveDays")
    print(f"After 95 days: {result['inactive_days']} days inactive\n")
    
    # Trigger dead-man switch
    result = blockchain.call_function(contract_address, "system", "triggerDeadManSwitch")
    
    if result.get("success"):
        print(f"Dead-man switch triggered!")
        print(f"Event: {result['event']}")
        print(f"Inactive days: {result['inactive_days']}")
    
    print()


if __name__ == "__main__":
    # Run complete simulation
    simulate_complete_workflow()
    
    # Run dead-man switch scenario
    simulate_dead_man_switch()
