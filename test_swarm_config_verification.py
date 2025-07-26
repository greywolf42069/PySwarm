#!/usr/bin/env python3
"""
Swarm Configuration Verification Test

This script verifies that our PySwarm configuration:
1. Creates addresses with network byte '0'
2. Uses the correct RPC endpoint 'https://nodes.swrmdao.com'
3. Generates addresses starting with '3' (Swarm format)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pywaves'))

import pywaves as pw
import base58

def verify_swarm_config():
    """Verify Swarm configuration is correct."""
    print("=== Swarm Configuration Verification ===")
    
    # Configure for Swarm
    pw.setNode('https://nodes.swrmdao.com', 'swarm')
    pw.setOffline()
    
    print(f"Current node: {pw.NODE}")
    print(f"Current chain: {pw.CHAIN}")
    print(f"Current chain ID: {pw.CHAIN_ID}")
    
    # Verify RPC endpoint
    expected_node = 'https://nodes.swrmdao.com'
    if pw.NODE == expected_node:
        print(f"✅ RPC endpoint correct: {pw.NODE}")
    else:
        print(f"❌ RPC endpoint incorrect. Expected: {expected_node}, Got: {pw.NODE}")
        return False
    
    # Verify chain ID is '0' for Swarm
    if pw.CHAIN_ID == '0':
        print(f"✅ Chain ID correct: '{pw.CHAIN_ID}'")
    else:
        print(f"❌ Chain ID incorrect. Expected: '0', Got: '{pw.CHAIN_ID}'")
        return False
    
    # Create test address
    test_seed = "test_seed_for_swarm_verification"
    test_address = pw.Address(seed=test_seed)
    
    print(f"Generated address: {test_address.address}")
    
    # Verify address starts with '3' (Swarm format)
    if test_address.address.startswith('3'):
        print(f"✅ Address format correct: starts with '3'")
    else:
        print(f"❌ Address format incorrect. Expected to start with '3', Got: {test_address.address[0]}")
        return False
    
    # Verify network byte by decoding address
    try:
        decoded = base58.b58decode(test_address.address)
        network_byte = decoded[1]  # Second byte is the network byte
        
        if network_byte == 0:  # Network byte '0' for Swarm
            print(f"✅ Network byte correct: {network_byte} (0x{network_byte:02x})")
        else:
            print(f"❌ Network byte incorrect. Expected: 0, Got: {network_byte} (0x{network_byte:02x})")
            return False
            
    except Exception as e:
        print(f"❌ Error decoding address: {e}")
        return False
    
    # Test transaction creation in offline mode
    try:
        recipient = "3P8JdJGYc7vaLu4UXUZc1iRLdzrkGtdCyJM"  # Another Swarm address
        tx = test_address.sendWaves(recipient=recipient, amount=1000000, fee=100000)
        
        if tx and 'type' in tx:
            print(f"✅ Transaction creation successful in offline mode")
            print(f"   Transaction type: {tx.get('type')}")
            print(f"   Amount: {tx.get('amount')}")
            print(f"   Fee: {tx.get('fee')}")
        else:
            print(f"❌ Transaction creation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error creating transaction: {e}")
        return False
    
    print("\n✅ All Swarm configuration checks passed!")
    return True

if __name__ == "__main__":
    success = verify_swarm_config()
    if success:
        print("\n🎉 Swarm configuration is correctly set up!")
        sys.exit(0)
    else:
        print("\n❌ Swarm configuration has issues that need to be fixed.")
        sys.exit(1)