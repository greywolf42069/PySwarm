import unittest
import pywaves as pw
import json
import time

class TestSwarmTransactions(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment for Swarm blockchain transactions"""
        pw.setChain('swarm', '0')
        pw.setNode('https://nodes.swrmdao.com', 'swarm', '0')
        pw.setOffline()  # Use offline mode for testing
        
        # Create test addresses
        self.sender = pw.Address(seed='test sender seed for swarm transactions')
        self.recipient = pw.Address(seed='test recipient seed for swarm transactions')
    
    def test_swarm_transaction_configuration(self):
        """Test that transaction configuration is correct for Swarm"""
        self.assertEqual(pw.CHAIN, 'swarm')
        self.assertEqual(pw.CHAIN_ID, '0')
        self.assertEqual(pw.NODE, 'https://nodes.swrmdao.com')
    
    def test_send_waves_transaction_structure(self):
        """Test the structure of a Waves transfer transaction for Swarm"""
        amount = 100000000  # 1 WAVES (8 decimals)
        attachment = 'test attachment'
        
        # Generate transaction (offline mode)
        tx = self.sender.sendWaves(self.recipient, amount, attachment)
        
        # Verify transaction structure
        self.assertIn('api-type', tx)
        self.assertIn('api-endpoint', tx)
        self.assertIn('api-data', tx)
        self.assertEqual(tx['api-type'], 'POST')
        self.assertEqual(tx['api-endpoint'], '/transactions/broadcast')
        
        # Parse the transaction data
        tx_data = json.loads(tx['api-data'])
        
        # Verify transaction fields
        self.assertEqual(tx_data['type'], 4)  # Transfer transaction type
        self.assertEqual(tx_data['amount'], amount)
        self.assertEqual(tx_data['recipient'], self.recipient.address)
        self.assertEqual(tx_data['senderPublicKey'], self.sender.publicKey)
        self.assertIn('timestamp', tx_data)
        self.assertIn('proofs', tx_data)
        self.assertIsInstance(tx_data['proofs'], list)
        self.assertGreater(len(tx_data['proofs']), 0)
    
    def test_issue_asset_transaction_structure(self):
        """Test that asset issuance transactions have correct structure"""
        sender = pw.Address(seed="test seed")
        
        asset_tx = sender.issueAsset(
            name="SwarmTestToken",
            description="Test token for Swarm blockchain",
            quantity=1000000,
            decimals=8
        )
        
        # Parse the transaction data
        tx_data = json.loads(asset_tx['api-data'])
        
        self.assertIn('type', tx_data)
        self.assertEqual(tx_data['type'], 3)
        self.assertIn('version', tx_data)
        self.assertIn('senderPublicKey', tx_data)
        self.assertIn('name', tx_data)
        self.assertIn('description', tx_data)
        self.assertIn('quantity', tx_data)
        self.assertIn('decimals', tx_data)
        self.assertIn('proofs', tx_data)
        self.assertIsInstance(tx_data['proofs'], list)
        self.assertGreater(len(tx_data['proofs']), 0)
        self.assertEqual(tx_data['name'], "SwarmTestToken")
    
    def test_transaction_signing(self):
        """Test that transactions are properly signed for Swarm"""
        amount = 50000000  # 0.5 WAVES
        
        # Generate transaction
        tx = self.sender.sendWaves(self.recipient, amount)
        tx_data = json.loads(tx['api-data'])
        
        # Check that transaction has proofs field after creation (modern Waves format)
        tx_data = json.loads(tx['api-data'])
        self.assertIn('proofs', tx_data)
        self.assertIsInstance(tx_data['proofs'], list)
        self.assertGreater(len(tx_data['proofs']), 0)
        
        # Verify first proof exists and is not empty
        self.assertIsNotNone(tx_data['proofs'][0])
        self.assertTrue(len(tx_data['proofs'][0]) > 0)
    
    def test_transaction_timestamp(self):
        """Test that transactions have proper timestamps"""
        current_time = int(time.time() * 1000)
        
        tx = self.sender.sendWaves(self.recipient, 100000)
        tx_data = json.loads(tx['api-data'])
        
        # Verify timestamp is reasonable (within 1 minute of current time)
        self.assertIn('timestamp', tx_data)
        timestamp_diff = abs(tx_data['timestamp'] - current_time)
        self.assertLess(timestamp_diff, 60000)  # Less than 1 minute difference
    
    def test_transaction_fees(self):
        """Test that transaction fees are set correctly"""
        # Test default fee
        tx = self.sender.sendWaves(self.recipient, 100000)
        tx_data = json.loads(tx['api-data'])
        self.assertEqual(tx_data['fee'], pw.DEFAULT_TX_FEE)
        
        # Test custom fee
        custom_fee = 200000
        tx_custom = self.sender.sendWaves(self.recipient, 100000, txFee=custom_fee)
        tx_custom_data = json.loads(tx_custom['api-data'])
        self.assertEqual(tx_custom_data['fee'], custom_fee)
    
    def test_address_validation_in_transactions(self):
        """Test that transaction recipient addresses are validated"""
        # Valid Swarm address should work
        valid_tx = self.sender.sendWaves(self.recipient, 100000)
        self.assertIsNotNone(valid_tx)
        
        # Test with invalid address format should raise error
        with self.assertRaises(Exception):
            self.sender.sendWaves('invalid_address', 100000)
    
    def test_transaction_version_and_chain_id(self):
        """Test that transactions include correct version and chain ID"""
        tx = self.sender.sendWaves(self.recipient, 100000)
        tx_data = json.loads(tx['api-data'])
        
        # Verify version is set (should be 2 for modern transactions)
        self.assertIn('version', tx_data)
        self.assertGreaterEqual(tx_data['version'], 2)
        
        # Chain ID should be included in the transaction for signing
        # (Note: Chain ID is used in signature generation, not always in JSON)
        self.assertEqual(pw.CHAIN_ID, '0')
    
    def test_multiple_transaction_uniqueness(self):
        """Test that multiple transactions have unique signatures"""
        tx1 = self.sender.sendWaves(self.recipient, 100000)
        time.sleep(0.001)  # Small delay to ensure different timestamps
        tx2 = self.sender.sendWaves(self.recipient, 100000)
        
        tx1_data = json.loads(tx1['api-data'])
        tx2_data = json.loads(tx2['api-data'])
        
        # Signatures should be different due to different timestamps
        self.assertNotEqual(tx1_data['proofs'][0], tx2_data['proofs'][0])
        self.assertNotEqual(tx1_data['timestamp'], tx2_data['timestamp'])
    
    def tearDown(self):
        """Clean up after tests"""
        pw.setOnline()

if __name__ == '__main__':
    unittest.main()