"""
Smart Will - Deployment Script
Deploys SmartWill contract to Mumbai testnet
"""

from web3 import Web3
from solcx import compile_standard, install_solc
import json
from pathlib import Path
from typing import Dict, Any


# ============================================================================
# CONFIGURATION
# ============================================================================

MUMBAI_RPC_URL = "https://rpc-mumbai.maticvigil.com"
PRIVATE_KEY = "YOUR_PRIVATE_KEY_HERE"  # Load from env in production
CHAIN_ID = 80001  # Mumbai testnet

# Validator addresses (mock for testing)
VALIDATORS = [
    "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
    "0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed",
    "0x5B38Da6a701c568545dCfcB03FcB875f56beddC4"
]

REQUIRED_VALIDATIONS = 2


# ============================================================================
# DEPLOYMENT CLASS
# ============================================================================

class SmartWillDeployer:
    """Deploy and manage SmartWill contract"""
    
    def __init__(self, rpc_url: str, private_key: str, chain_id: int):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.private_key = private_key
        self.chain_id = chain_id
        self.account = self.w3.eth.account.from_key(private_key)
        
        print(f"Connected to network: {self.w3.is_connected()}")
        print(f"Account: {self.account.address}")
        print(f"Balance: {self.w3.from_wei(self.w3.eth.get_balance(self.account.address), 'ether')} MATIC")
    
    def compile_contract(self, contract_path: str) -> Dict[str, Any]:
        """Compile Solidity contract"""
        
        # Install solc compiler
        install_solc("0.8.20")
        
        # Read contract source
        with open(contract_path, 'r') as file:
            contract_source = file.read()
        
        # Compile
        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {"SmartWill.sol": {"content": contract_source}},
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                        }
                    }
                },
            },
            solc_version="0.8.20",
        )
        
        # Extract ABI and bytecode
        contract_id = "SmartWill.sol:SmartWill"
        abi = compiled_sol["contracts"]["SmartWill.sol"]["SmartWill"]["abi"]
        bytecode = compiled_sol["contracts"]["SmartWill.sol"]["SmartWill"]["evm"]["bytecode"]["object"]
        
        # Save ABI to file
        abi_path = Path(contract_path).parent / "SmartWill_ABI.json"
        with open(abi_path, 'w') as f:
            json.dump(abi, f, indent=2)
        
        print(f"Contract compiled successfully")
        print(f"ABI saved to: {abi_path}")
        
        return {
            "abi": abi,
            "bytecode": bytecode
        }
    
    def deploy_contract(self, abi: list, bytecode: str, 
                       validators: list, required_validations: int) -> str:
        """Deploy contract to blockchain"""
        
        # Create contract instance
        Contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        
        # Build constructor transaction
        construct_txn = Contract.constructor(validators, required_validations).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 3000000,
            'gasPrice': self.w3.eth.gas_price,
            'chainId': self.chain_id
        })
        
        # Sign transaction
        signed_txn = self.w3.eth.account.sign_transaction(construct_txn, self.private_key)
        
        # Send transaction
        print("Deploying contract...")
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for receipt
        print(f"Transaction hash: {tx_hash.hex()}")
        print("Waiting for confirmation...")
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        contract_address = tx_receipt.contractAddress
        print(f"Contract deployed at: {contract_address}")
        print(f"Gas used: {tx_receipt.gasUsed}")
        
        return contract_address
    
    def save_deployment_info(self, contract_address: str, abi: list):
        """Save deployment information"""
        
        deployment_info = {
            "contract_address": contract_address,
            "network": "mumbai",
            "chain_id": self.chain_id,
            "deployer": self.account.address,
            "deployed_at": "timestamp",
            "abi": abi
        }
        
        with open("contracts/deployment.json", 'w') as f:
            json.dump(deployment_info, f, indent=2)
        
        print("Deployment info saved to contracts/deployment.json")


# ============================================================================
# DEPLOYMENT SCRIPT
# ============================================================================

def deploy_smart_will():
    """Main deployment function"""
    
    # Initialize deployer
    deployer = SmartWillDeployer(
        rpc_url=MUMBAI_RPC_URL,
        private_key=PRIVATE_KEY,
        chain_id=CHAIN_ID
    )
    
    # Compile contract
    contract_path = "contracts/smart_will.sol"
    compiled = deployer.compile_contract(contract_path)
    
    # Deploy contract
    contract_address = deployer.deploy_contract(
        abi=compiled["abi"],
        bytecode=compiled["bytecode"],
        validators=VALIDATORS,
        required_validations=REQUIRED_VALIDATIONS
    )
    
    # Save deployment info
    deployer.save_deployment_info(contract_address, compiled["abi"])
    
    return {
        "contract_address": contract_address,
        "abi": compiled["abi"]
    }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_contract_instance(w3: Web3, contract_address: str, abi: list):
    """Get contract instance for interaction"""
    return w3.eth.contract(address=contract_address, abi=abi)


def estimate_deployment_cost(w3: Web3, bytecode: str, gas_price: int) -> Dict:
    """Estimate deployment cost"""
    
    # Rough estimate: bytecode size + execution
    gas_estimate = 3000000
    cost_wei = gas_estimate * gas_price
    cost_matic = w3.from_wei(cost_wei, 'ether')
    
    return {
        "gas_estimate": gas_estimate,
        "gas_price_gwei": w3.from_wei(gas_price, 'gwei'),
        "cost_matic": float(cost_matic),
        "cost_usd": float(cost_matic) * 0.5  # Approximate MATIC price
    }


if __name__ == "__main__":
    # Run deployment
    result = deploy_smart_will()
    print("\n" + "="*60)
    print("DEPLOYMENT COMPLETE")
    print("="*60)
    print(f"Contract Address: {result['contract_address']}")
    print(f"Network: Mumbai Testnet")
    print(f"Explorer: https://mumbai.polygonscan.com/address/{result['contract_address']}")
