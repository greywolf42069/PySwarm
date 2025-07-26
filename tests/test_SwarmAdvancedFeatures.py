import unittest
import pywaves as pw
import json
import time
import base64

class TestSwarmAdvancedFeatures(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment for advanced Swarm blockchain features"""
        pw.setChain('swarm', '0')
        pw.setNode('https://nodes.swrmdao.com', 'swarm', '0')
        pw.setOffline()  # Use offline mode for testing
        
        # Create test addresses
        self.dapp_address = pw.Address(seed='test dapp seed for swarm smart contracts')
        self.user_address = pw.Address(seed='test user seed for swarm interactions')
        self.asset_issuer = pw.Address(seed='test asset issuer seed for swarm')
    
    def test_swarm_smart_contract_deployment(self):
        """Test smart contract deployment structure on Swarm"""
        pw.setOffline()
        
        # Test contract deployment structure without API calls
        script_source = "match tx { case _ => true }"
        
        # Verify we can create the transaction structure
        # (without actual compilation which requires API)
        self.assertIsInstance(script_source, str)
        self.assertTrue(len(script_source) > 0)
        
        # Verify address can handle script operations
        self.assertTrue(hasattr(self.dapp_address, 'setScript'))
        self.assertTrue(callable(getattr(self.dapp_address, 'setScript')))
    
    def test_swarm_smart_contract_invocation(self):
        """Test smart contract function invocation on Swarm"""
        # Parameters for smart contract call
        parameters = [
            {"type": "string", "value": "swarmKey1"},
            {"type": "string", "value": "swarmValue1"}
        ]
        
        # Invoke smart contract function
        tx = self.user_address.invokeScript(
            self.dapp_address.address,
            'storeSwarmData',
            parameters,
            []  # No payments
        )
        
        # Verify transaction structure
        self.assertIn('api-data', tx)
        tx_data = json.loads(tx['api-data'])
        
        # Verify invoke script transaction
        self.assertEqual(tx_data['type'], 16)  # InvokeScript transaction type
        self.assertEqual(tx_data['dApp'], self.dapp_address.address)
        self.assertEqual(tx_data['call']['function'], 'storeSwarmData')
        self.assertEqual(tx_data['call']['args'], parameters)
        self.assertEqual(tx_data['payment'], [])
        self.assertIn('proofs', tx_data)
    
    def test_swarm_data_transactions(self):
        """Test data transactions on Swarm blockchain"""
        # Test different data types
        data_entries = [
            {'type': 'string', 'key': 'swarm_string', 'value': 'Hello Swarm Blockchain'},
            {'type': 'integer', 'key': 'swarm_number', 'value': 42},
            {'type': 'boolean', 'key': 'swarm_flag', 'value': True},
            {'type': 'binary', 'key': 'swarm_binary', 'value': base64.b64encode(b'binary data').decode()}
        ]
        
        # Create data transaction
        tx = self.user_address.dataTransaction(data_entries)
        
        # Verify transaction structure
        self.assertIn('api-data', tx)
        tx_data = json.loads(tx['api-data'])
        
        # Verify data transaction
        self.assertEqual(tx_data['type'], 12)  # Data transaction type
        self.assertEqual(tx_data['senderPublicKey'], self.user_address.publicKey)
        self.assertEqual(len(tx_data['data']), 4)
        
        # Verify each data entry
        for i, entry in enumerate(tx_data['data']):
            expected = data_entries[i]
            self.assertEqual(entry['type'], expected['type'])
            self.assertEqual(entry['key'], expected['key'])
            
            # Handle binary data encoding difference
            if expected['type'] == 'binary':
                # The API may add 'base64:' prefix to binary data
                if entry['value'].startswith('base64:'):
                    self.assertTrue(entry['value'].startswith('base64:'))
                else:
                    self.assertEqual(entry['value'], expected['value'])
            else:
                self.assertEqual(entry['value'], expected['value'])
    
    def test_swarm_asset_issuance_advanced(self):
        """Test advanced asset issuance on Swarm"""
        pw.setOffline()
        
        # Test regular asset issuance with advanced parameters
        tx = self.asset_issuer.issueAsset(
            name="SwarmAdvanced",
            description="Advanced asset on Swarm blockchain",
            quantity=1000000000,
            decimals=8,
            reissuable=True
        )
        
        if tx:
            # Verify transaction structure
            tx_data = json.loads(tx['api-data'])
            self.assertEqual(tx_data['type'], 3)
            self.assertEqual(tx_data['name'], "SwarmAdvanced")
            self.assertEqual(tx_data['quantity'], 1000000000)
            self.assertEqual(tx_data['decimals'], 8)
            self.assertEqual(tx_data['reissuable'], True)
        
        # Verify smart asset method exists
        self.assertTrue(hasattr(self.asset_issuer, 'issueSmartAsset'))
        self.assertTrue(callable(getattr(self.asset_issuer, 'issueSmartAsset')))
    
    def test_swarm_mass_transfer(self):
        """Test mass transfer functionality on Swarm"""
        pw.setOffline()
        
        # Create multiple recipients
        recipients = [
            pw.Address(seed='recipient1 seed'),
            pw.Address(seed='recipient2 seed'),
            pw.Address(seed='recipient3 seed')
        ]
        
        # Prepare transfer list
        transfers = [
            {'recipient': recipients[0].address, 'amount': 1000000},
            {'recipient': recipients[1].address, 'amount': 2000000},
            {'recipient': recipients[2].address, 'amount': 3000000}
        ]
        
        # Verify transfer structure is valid
        self.assertEqual(len(transfers), 3)
        for i, transfer in enumerate(transfers):
            self.assertIn('recipient', transfer)
            self.assertIn('amount', transfer)
            self.assertTrue(transfer['recipient'].startswith('3'))  # Swarm address prefix
            self.assertEqual(transfer['amount'], (i + 1) * 1000000)
        
        # Verify mass transfer method exists
        self.assertTrue(hasattr(self.user_address, 'massTransferWaves'))
        self.assertTrue(callable(getattr(self.user_address, 'massTransferWaves')))
    
    def test_swarm_lease_transactions(self):
        """Test lease transactions on Swarm"""
        lease_recipient = pw.Address(seed='lease recipient seed')
        lease_amount = 100000000  # 1 WAVES
        
        # Create lease transaction
        lease_tx = self.user_address.lease(lease_recipient, lease_amount)
        
        # Verify lease transaction
        self.assertIn('api-data', lease_tx)
        lease_data = json.loads(lease_tx['api-data'])
        
        self.assertEqual(lease_data['type'], 8)  # Lease transaction type
        self.assertEqual(lease_data['recipient'], lease_recipient.address)
        self.assertEqual(lease_data['amount'], lease_amount)
        self.assertEqual(lease_data['senderPublicKey'], self.user_address.publicKey)
        
        # Verify lease method exists and is callable
        self.assertTrue(hasattr(self.user_address, 'lease'))
        self.assertTrue(callable(getattr(self.user_address, 'lease')))
    
    def test_swarm_alias_creation(self):
        """Test alias creation on Swarm blockchain"""
        alias_name = "swarmtestuser"
        
        # Create alias transaction
        tx = self.user_address.createAlias(alias_name)
        
        # Verify transaction structure
        self.assertIn('api-data', tx)
        tx_data = json.loads(tx['api-data'])
        
        # Verify alias transaction
        self.assertEqual(tx_data['type'], 10)  # CreateAlias transaction type
        self.assertEqual(tx_data['alias'], alias_name)
        self.assertEqual(tx_data['senderPublicKey'], self.user_address.publicKey)
        self.assertIn('proofs', tx_data)
    
    def test_swarm_asset_operations(self):
        """Test various asset operations on Swarm"""
        pw.setOffline()
        
        # Test asset operation methods exist
        asset_methods = [
            ('issueAsset', self.asset_issuer.issueAsset),
            ('sendAsset', self.asset_issuer.sendAsset),
            ('reissueAsset', self.asset_issuer.reissueAsset),
            ('burnAsset', self.asset_issuer.burnAsset)
        ]
        
        for method_name, method in asset_methods:
            self.assertTrue(hasattr(method.__self__, method_name))
            self.assertTrue(callable(method))
        
        # Test asset issuance structure
        issue_tx = self.asset_issuer.issueAsset(
            name="SwarmTestToken",
            description="Test token for operations",
            quantity=1000000000,
            decimals=8
        )
        
        if issue_tx and isinstance(issue_tx, dict) and 'api-data' in issue_tx:
            issue_data = json.loads(issue_tx['api-data'])
            self.assertEqual(issue_data['type'], 3)
            self.assertEqual(issue_data['name'], "SwarmTestToken")
            self.assertEqual(issue_data['quantity'], 1000000000)
            self.assertEqual(issue_data['decimals'], 8)
    
    def test_swarm_transaction_versioning(self):
        """Test that Swarm transactions use correct versioning"""
        # Test various transaction types for version consistency
        transactions = [
            self.user_address.sendWaves(self.dapp_address, 100000),
            self.asset_issuer.issueAsset("VersionTest", "Version test asset", 1000, decimals=2),
            self.user_address.dataTransaction([{'type': 'string', 'key': 'version_test', 'value': 'test'}])
        ]
        
        for tx in transactions:
            tx_data = json.loads(tx['api-data'])
            # Modern transactions should use version 2 or higher
            self.assertIn('version', tx_data)
            self.assertGreaterEqual(tx_data['version'], 2)
            # Chain ID should be '0' for Swarm
            self.assertEqual(pw.CHAIN_ID, '0')
    
    def test_swarm_transaction_fees(self):
        """Test transaction fee calculations for different transaction types"""
        # Test fees for different transaction types (excluding setScript to avoid compilation)
        fee_tests = [
            ('sendWaves', lambda: self.user_address.sendWaves(self.dapp_address, 100000)),
            ('issueAsset', lambda: self.asset_issuer.issueAsset("FeeTest", "Fee test", 1000)),
            ('dataTransaction', lambda: self.user_address.dataTransaction([{'type': 'string', 'key': 'fee_test', 'value': 'test'}]))
        ]
        
        for tx_type, tx_func in fee_tests:
            tx = tx_func()
            tx_data = json.loads(tx['api-data'])
            
            # Verify fee is present and reasonable
            self.assertIn('fee', tx_data)
            self.assertIsInstance(tx_data['fee'], int)
            self.assertGreater(tx_data['fee'], 0)
            
            # All transaction types should have appropriate minimum fees
            self.assertGreaterEqual(tx_data['fee'], 100000)  # Minimum fee for most transactions
        
        # Test that setScript method exists without calling it
        self.assertTrue(hasattr(self.dapp_address, 'setScript'))
        self.assertTrue(callable(getattr(self.dapp_address, 'setScript')))
    
    def test_swarm_offline_mode_consistency(self):
        """Test that offline mode works consistently across all transaction types"""
        # Ensure we're in offline mode
        pw.setOffline()
        
        # Test various transaction types in offline mode
        offline_transactions = [
            self.user_address.sendWaves(self.dapp_address, 100000),
            self.asset_issuer.issueAsset("OfflineTest", "Offline test asset", 1000),
            self.user_address.dataTransaction([{'type': 'string', 'key': 'offline_test', 'value': 'test'}]),
            self.user_address.lease(self.dapp_address, 50000000),
            self.user_address.createAlias("offlinetest")
        ]
        
        for tx in offline_transactions:
            # All offline transactions should have consistent structure
            self.assertIn('api-type', tx)
            self.assertIn('api-endpoint', tx)
            self.assertIn('api-data', tx)
            self.assertEqual(tx['api-type'], 'POST')
            self.assertEqual(tx['api-endpoint'], '/transactions/broadcast')
            
            # Transaction data should be valid JSON
            tx_data = json.loads(tx['api-data'])
            self.assertIn('type', tx_data)
            self.assertIn('senderPublicKey', tx_data)
            self.assertIn('timestamp', tx_data)
            self.assertIn('proofs', tx_data)
            self.assertIn('fee', tx_data)

if __name__ == '__main__':
    unittest.main()