"""
BlockDAG Investment Smart Contract Interface
"""
from typing import Dict, List, Optional
from blockdag_network_sdk import SmartContract
from .blockdag_wallet import BlockDAGWallet

class InvestmentContract:
    """Smart contract for managing investments on BlockDAG network"""
    
    CONTRACT_ABI = [
        {
            "inputs": [],
            "stateMutability": "payable",
            "type": "constructor"
        },
        {
            "inputs": [{"internalType": "address", "name": "investor", "type": "address"}],
            "name": "getInvestments",
            "outputs": [{"components": [
                {"internalType": "uint256", "name": "amount", "type": "uint256"},
                {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
                {"internalType": "bool", "name": "active", "type": "bool"}
            ], "internalType": "struct InvestmentManager.Investment[]", "name": "", "type": "tuple[]"}],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "invest",
            "outputs": [],
            "stateMutability": "payable",
            "type": "function"
        }
    ]
    
    def __init__(self, wallet: BlockDAGWallet, contract_address: str = None):
        """Initialize with wallet and optional existing contract"""
        self.wallet = wallet
        self.contract = SmartContract(
            client=wallet.client,
            abi=self.CONTRACT_ABI,
            address=contract_address
        )
        
    def deploy(self) -> str:
        """Deploy a new investment contract"""
        contract_code = """
        // SPDX-License-Identifier: MIT
        pragma solidity ^0.8.0;
        
        contract InvestmentManager {
            struct Investment {
                uint256 amount;
                uint256 timestamp;
                bool active;
            }
            
            mapping(address => Investment[]) public investments;
            
            event InvestmentMade(address indexed investor, uint256 amount);
            
            function invest() public payable {
                require(msg.value > 0, "Investment amount must be greater than 0");
                investments[msg.sender].push(Investment({
                    amount: msg.value,
                    timestamp: block.timestamp,
                    active: true
                }));
                emit InvestmentMade(msg.sender, msg.value);
            }
            
            function getInvestments(address investor) public view returns (Investment[] memory) {
                return investments[investor];
            }
        }
        """
        
        self.contract = self.wallet.client.deploy_contract(
            contract_code,
            private_key=self.wallet.private_key
        )
        return self.contract.address
        
    def make_investment(self, amount: int) -> Dict:
        """Make a new investment"""
        return self.contract.functions.invest().transact({
            'value': amount,
            'from': self.wallet.address
        })
        
    def get_investments(self, address: str = None) -> List[Dict]:
        """Get investments for an address"""
        if not address:
            address = self.wallet.address
        return self.contract.functions.getInvestments(address).call()
