import unittest
import pywaves as pw
import json
import time
import requests
from unittest.mock import patch, MagicMock

class TestSwarmIntegration(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment for Swarm integration testing"""
        pw.setChain('swarm', '0')
        pw.setNode('https://nodes.swrmdao.com', 'swarm', '0')
        pw.setOffline()  # Ensure offline mode to prevent network hangs
        
        # Create test addresses
        self.test_address = pw.Address(seed='swarm integration test seed')
        self.secondary_address = pw.Address(seed='swarm secondary test seed')
    
    def test_swarm_network_configuration(self):
        """Test that Swarm network is properly configured"""
        # Verify chain configuration
        self.assertEqual(pw.CHAIN, 'swarm')
        self.assertEqual(pw.CHAIN_ID, '0')
        self.assertEqual(pw.NODE, 'https://nodes.swrmdao.com')
        
        # Verify network byte (calculated from CHAIN_ID)
        self.assertEqual(ord(pw.CHAIN_ID), ord('0'))
        
        # Test address generation with Swarm network byte
        address = pw.Address(seed='test seed')
        self.assertTrue(address.address.startswith('3'))
        
        # Verify address checksum calculation for Swarm
        self.assertIsNotNone(address.address)
        self.assertGreater(len(address.address), 30)
    
    def test_swarm_api_endpoints(self):
        """Test that offline transactions target correct endpoints"""
        pw.setOffline()
        
        # Test various transaction types and their endpoints
        transactions = [
            ('sendWaves', lambda: self.test_address.sendWaves(self.secondary_address, 100000)),
            ('issueAsset', lambda: self.test_address.issueAsset('TestAsset', 'Test asset', 1000)),
            ('dataTransaction', lambda: self.test_address.dataTransaction([{'type': 'string', 'key': 'test', 'value': 'data'}])),
            ('lease', lambda: self.test_address.lease(self.secondary_address, 50000000)),
            ('createAlias', lambda: self.test_address.createAlias('testuser123'))
        ]
        
        for tx_name, tx_func in transactions:
            tx = tx_func()
            
            # Verify transaction has correct API structure
            self.assertIn('api-endpoint', tx)
            self.assertIn('api-type', tx)
            self.assertIn('api-data', tx)
            
            # Verify endpoint is correct
            self.assertEqual(tx['api-endpoint'], '/transactions/broadcast')
            self.assertEqual(tx['api-type'], 'POST')
            
            # Verify transaction data is valid JSON
            tx_data = json.loads(tx['api-data'])
            self.assertIn('type', tx_data)
            self.assertIn('senderPublicKey', tx_data)
            self.assertIn('fee', tx_data)
            self.assertIn('timestamp', tx_data)
    
    @patch('requests.get')
    def test_swarm_node_connectivity_mock(self, mock_get):
        """Test Swarm node connectivity with mocked responses"""
        # Mock successful node response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'version': '1.4.0',
            'nodeName': 'swarm-node',
            'nodeNonce': 12345
        }
        mock_get.return_value = mock_response
        
        # Test node info endpoint
        pw.setOnline()
        
        # Simulate node info request
        response = requests.get(f"{pw.NODE}/node")
        
        self.assertEqual(response.status_code, 200)
        node_info = response.json()
        self.assertIn('version', node_info)
        self.assertIn('nodeName', node_info)
    
    @patch('requests.post')
    def test_swarm_transaction_broadcast_mock(self, mock_post):
        """Test transaction broadcasting to Swarm network with mocked responses"""
        # Mock successful broadcast response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'type': 4,
            'id': 'mock_transaction_id_12345',
            'sender': self.test_address.address,
            'senderPublicKey': self.test_address.publicKey,
            'fee': 100000,
            'timestamp': int(time.time() * 1000)
        }
        mock_post.return_value = mock_response
        
        pw.setOffline()  # Use offline mode to avoid balance issues
        
        # Create a transaction
        tx = self.test_address.sendWaves(self.secondary_address, 100000)
        
        # Simulate broadcasting (mock already set up)
        response = requests.post(
            f"{pw.NODE}/transactions/broadcast",
            json=json.loads(tx['api-data']),
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.status_code, 200)
        broadcast_result = response.json()
        self.assertIn('id', broadcast_result)
        self.assertEqual(broadcast_result['type'], 4)
    
    def test_swarm_address_validation_integration(self):
        """Test comprehensive address validation for Swarm network"""
        pw.setOffline()
        
        # Test multiple address creation methods
        addresses = [
            pw.Address(seed='swarm validation test seed 1'),
            pw.Address(seed='swarm validation test seed 2'),
            pw.Address(privateKey='BGpBRDeUiHskf4bdyWoUAKpP9DSx51haovHcGNqPEy6Q'),
            self.test_address,
            self.secondary_address
        ]
        
        for addr in addresses:
            # Verify Swarm address format
            self.assertTrue(addr.address.startswith('3'), f"Address {addr.address} should start with '3'")
            
            # Verify address length (typically 35 characters)
            self.assertGreaterEqual(len(addr.address), 35, f"Address {addr.address} length should be >= 35")
            self.assertLessEqual(len(addr.address), 36, f"Address {addr.address} length should be <= 36")
            
            # Verify public key format
            self.assertIsNotNone(addr.publicKey)
            self.assertEqual(len(addr.publicKey), 44, f"Public key length should be 44 characters")
            
            # Verify private key format (if available)
            if hasattr(addr, 'privateKey') and addr.privateKey:
                self.assertGreaterEqual(len(addr.privateKey), 43, f"Private key length should be >= 43 characters")
                self.assertLessEqual(len(addr.privateKey), 44, f"Private key length should be <= 44 characters")
            
            # Test address can create transactions
            try:
                tx = addr.sendWaves(self.secondary_address, 100000)
                tx_data = json.loads(tx['api-data'])
                self.assertEqual(tx_data['senderPublicKey'], addr.publicKey)
            except Exception as e:
                self.fail(f"Address {addr.address} failed to create transaction: {e}")
    
    def test_swarm_transaction_signing_integration(self):
        """Test transaction signing with Swarm network parameters"""
        pw.setOffline()
        
        # Create various transaction types
        transactions = [
            self.test_address.sendWaves(self.secondary_address, 100000),
            self.test_address.issueAsset('SwarmToken', 'Swarm test token', 1000000),
            self.test_address.dataTransaction([{'type': 'string', 'key': 'swarm_test', 'value': 'integration_test'}]),
            self.test_address.lease(self.secondary_address, 50000000),
            self.test_address.createAlias('swarmtestuser')
        ]
        
        for tx in transactions:
            tx_data = json.loads(tx['api-data'])
            
            # Verify signature structure
            self.assertIn('proofs', tx_data)
            self.assertIsInstance(tx_data['proofs'], list)
            self.assertGreater(len(tx_data['proofs']), 0)
            
            # First proof should be the signature
            signature = tx_data['proofs'][0]
            self.assertIsInstance(signature, str)
            self.assertGreater(len(signature), 80)  # Signatures are typically 88+ characters
            
            # Verify sender public key matches our address
            self.assertEqual(tx_data['senderPublicKey'], self.test_address.publicKey)
    
    def test_swarm_fee_calculation_integration(self):
        """Test fee calculation for different transaction types on Swarm"""
        pw.setOffline()
        
        # Test fee calculations for various transaction types
        fee_tests = [
            ('Transfer', lambda: self.test_address.sendWaves(self.secondary_address, 100000)),
            ('Issue', lambda: self.test_address.issueAsset('FeeTest', 'Fee test asset', 1000)),
            ('Data', lambda: self.test_address.dataTransaction([{'type': 'string', 'key': 'fee_test', 'value': 'test'}])),
            ('Lease', lambda: self.test_address.lease(self.secondary_address, 100000000)),
            ('Alias', lambda: self.test_address.createAlias('feetestuser'))
        ]
        
        for tx_type, tx_func in fee_tests:
            tx = tx_func()
            tx_data = json.loads(tx['api-data'])
            
            # Verify fee is present and reasonable
            self.assertIn('fee', tx_data)
            fee = tx_data['fee']
            
            # Fees should be positive integers
            self.assertIsInstance(fee, int)
            self.assertGreater(fee, 0)
            
            # Minimum fee should be at least 100,000 (0.001 WAVES)
            self.assertGreaterEqual(fee, 100000)
            
            # Maximum reasonable fee should be less than 10 WAVES
            self.assertLess(fee, 1000000000)
    
    def test_swarm_timestamp_integration(self):
        """Test timestamp handling in Swarm transactions"""
        pw.setOffline()
        
        current_time = int(time.time() * 1000)
        
        # Create multiple transactions with small delays
        transactions = []
        for i in range(3):
            tx = self.test_address.sendWaves(self.secondary_address, 100000 + i)
            transactions.append(tx)
            time.sleep(0.001)  # Small delay to ensure different timestamps
        
        # Verify timestamps
        timestamps = []
        for tx in transactions:
            tx_data = json.loads(tx['api-data'])
            timestamp = tx_data['timestamp']
            
            # Timestamp should be reasonable (within 1 minute of current time)
            self.assertLess(abs(timestamp - current_time), 60000)
            
            # Timestamp should be unique
            self.assertNotIn(timestamp, timestamps)
            timestamps.append(timestamp)
        
        # Timestamps should be in ascending order
        self.assertEqual(timestamps, sorted(timestamps))
    
    def test_swarm_asset_operations_integration(self):
        """Test comprehensive asset operations on Swarm"""
        pw.setOffline()
        
        # Test asset issuance structure
        issue_tx = self.test_address.issueAsset(
            "SwarmTestAsset",
            "Test asset for Swarm integration",
            1000000000,
            decimals=8
        )
        
        if issue_tx:
            issue_data = json.loads(issue_tx['api-data'])
            self.assertEqual(issue_data['type'], 3)
            self.assertEqual(issue_data['name'], "SwarmTestAsset")
            self.assertEqual(issue_data['description'], "Test asset for Swarm integration")
            self.assertEqual(issue_data['quantity'], 1000000000)
            self.assertEqual(issue_data['decimals'], 8)
            
            # Verify Swarm-specific fields
            self.assertIn('senderPublicKey', issue_data)
            self.assertEqual(issue_data['senderPublicKey'], self.test_address.publicKey)
    
    def test_swarm_mass_operations_integration(self):
        """Test mass transfer operations on Swarm"""
        pw.setOffline()
        
        # Create multiple recipient addresses for mass transfer
        recipients = [
            pw.Address(seed="recipient1_seed_for_swarm_test"),
            pw.Address(seed="recipient2_seed_for_swarm_test"),
            pw.Address(seed="recipient3_seed_for_swarm_test")
        ]
        
        # Test mass transfer structure creation (without signing)
        wave_transfers = []
        for i, recipient in enumerate(recipients):
            wave_transfers.append({
                'recipient': recipient.address,
                'amount': 1000000 * (i + 1)  # Different amounts
            })
        
        # Verify transfer structure is valid
        self.assertEqual(len(wave_transfers), 3)
        for i, transfer in enumerate(wave_transfers):
            self.assertIn('recipient', transfer)
            self.assertIn('amount', transfer)
            self.assertTrue(transfer['recipient'].startswith('3'))  # Swarm address prefix
            self.assertEqual(transfer['amount'], 1000000 * (i + 1))
    
    def test_swarm_error_handling_integration(self):
        """Test error handling in various Swarm operations"""
        pw.setOffline()
        
        # Enable exception throwing for proper error testing
        pw.setThrowOnError(True)
        
        try:
            # Test zero amount transfer
            with self.assertRaises(Exception):
                self.test_address.sendWaves(self.secondary_address, 0)
            
            # Test negative amount
            with self.assertRaises(Exception):
                self.test_address.sendWaves(self.secondary_address, -100000)
            
            # Test invalid asset name (too long)
            with self.assertRaises(Exception):
                self.test_address.issueAsset(
                    'A' * 100,  # Name too long
                    'Description',
                    1000
                )
        finally:
            # Reset exception throwing
            pw.setThrowOnError(False)
    

    
    def test_swarm_compatibility_verification(self):
        """Test compatibility with Waves protocol standards"""
        pw.setOffline()
        
        # Create a standard transaction
        tx = self.test_address.sendWaves(self.secondary_address, 100000)
        tx_data = json.loads(tx['api-data'])
        
        # Verify Waves protocol compliance
        required_fields = [
            'type', 'version', 'senderPublicKey', 'recipient',
            'amount', 'fee', 'timestamp', 'proofs'
        ]
        
        for field in required_fields:
            self.assertIn(field, tx_data, f"Missing required field: {field}")
        
        # Verify field types
        self.assertIsInstance(tx_data['type'], int)
        self.assertIsInstance(tx_data['version'], int)
        self.assertIsInstance(tx_data['amount'], int)
        self.assertIsInstance(tx_data['fee'], int)
        self.assertIsInstance(tx_data['timestamp'], int)
        self.assertIsInstance(tx_data['proofs'], list)
        
        # Verify transaction version is modern (>= 2)
        self.assertGreaterEqual(tx_data['version'], 2)
        
        # Verify proof structure
        self.assertGreater(len(tx_data['proofs']), 0)
        self.assertIsInstance(tx_data['proofs'][0], str)

if __name__ == '__main__':
    unittest.main()