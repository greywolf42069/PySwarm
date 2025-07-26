#!/usr/bin/env python3
"""
Swarm Blockchain Example

This example demonstrates how to use the forked PySwarm library
to interact with the Swarm blockchain using network byte "0".
"""

import sys
import os

# Add the parent directory to the path to import pywaves
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pywaves as pw
import time

def main():
    print("=== Swarm Blockchain Example ===")
    print()
    
    # Configure for Swarm blockchain
    print("1. Configuring PyWaves for Swarm blockchain...")
    pw.setChain('swarm')
    pw.setOffline()  # Use offline mode for this example
    
    print(f"   Chain: {pw.getChain()}")
    print(f"   Chain ID: {pw.CHAIN_ID}")
    print(f"   Node: {pw.NODE}")
    print()
    
    # Create addresses
    print("2. Creating Swarm addresses...")
    
    # Create address from seed
    sender = pw.Address(seed="example sender seed phrase")
    recipient = pw.Address(seed="example recipient seed phrase")
    
    print(f"   Sender address: {sender.address}")
    print(f"   Sender public key: {sender.publicKey}")
    print(f"   Recipient address: {recipient.address}")
    print()
    
    # Verify addresses use Swarm network byte
    print("3. Verifying Swarm network byte...")
    print(f"   Sender address starts with '3': {sender.address.startswith('3')}")
    print(f"   Recipient address starts with '3': {recipient.address.startswith('3')}")
    print()
    
    # Create a transaction
    print("4. Creating a Swarm transaction...")
    amount = 100000000  # 1 WAVES (8 decimals)
    
    # Generate transaction (offline mode)
    tx = sender.sendWaves(recipient, amount)
    
    # Parse transaction data
    import json
    tx_data = json.loads(tx['api-data'])
    
    print(f"   Transaction type: {tx_data['type']}")
    print(f"   Amount: {amount / 100000000} WAVES")
    print(f"   Fee: {tx_data['fee'] / 100000000} WAVES")
    print(f"   Timestamp: {tx_data['timestamp']}")
    print()
    
    # Show transaction data
    print("5. Transaction details:")
    print(f"   Sender: {tx_data['senderPublicKey']}")
    print(f"   Recipient: {tx_data['recipient']}")
    print(f"   Amount: {tx_data['amount']}")
    print(f"   Fee: {tx_data['fee']}")
    print(f"   Version: {tx_data['version']}")
    print(f"   Proofs: {len(tx_data['proofs'])} proof(s)")
    print()
    
    # Asset issuance example
    print("6. Creating asset issuance transaction...")
    
    asset_tx = sender.issueAsset(
        name="SwarmToken",
        description="Example token on Swarm blockchain",
        quantity=1000000000,  # 10 tokens with 8 decimals
        decimals=8
    )
    
    asset_data = json.loads(asset_tx['api-data'])
    print(f"   Asset name: {asset_data['name']}")
    print(f"   Asset description: {asset_data['description']}")
    print(f"   Asset quantity: {asset_data['quantity'] / 100000000} tokens")
    print(f"   Asset decimals: {asset_data['decimals']}")
    print()
    
    print("=== Example completed successfully! ===")
    print()
    print("Note: This example runs in offline mode. To broadcast transactions")
    print("to the live Swarm network, remove pw.setOffline() and ensure")
    print("you have sufficient balance in your addresses.")

if __name__ == "__main__":
    main()