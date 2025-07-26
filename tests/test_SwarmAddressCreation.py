import unittest
import pywaves as pw
import pywaves.crypto as crypto

class TestSwarmAddressCreation(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment for Swarm blockchain"""
        pw.setChain('swarm', '0')
        pw.setNode('https://nodes.swrmdao.com', 'swarm', '0')
        pw.setOffline()  # Use offline mode for testing
    
    def test_swarm_chain_configuration(self):
        """Test that Swarm chain is configured correctly"""
        self.assertEqual(pw.CHAIN, 'swarm')
        self.assertEqual(pw.CHAIN_ID, '0')
        self.assertEqual(pw.NODE, 'https://nodes.swrmdao.com')
    
    def test_address_generation_with_seed(self):
        """Test address generation with a known seed for Swarm network"""
        test_seed = 'test seed for swarm blockchain address generation'
        address = pw.Address(seed=test_seed)
        
        # Verify address is generated
        self.assertIsNotNone(address.address)
        self.assertIsNotNone(address.publicKey)
        self.assertIsNotNone(address.privateKey)
        self.assertEqual(address.seed, test_seed)
        
        # Verify address format (should be base58 encoded)
        self.assertIsInstance(address.address, str)
        self.assertTrue(len(address.address) > 0)
        
        # Verify the address contains the correct chain ID
        decoded_address = pw.b58decode(address.address)
        address_str = crypto.bytes2str(decoded_address)
        # Second byte should be the chain ID ('0' for Swarm)
        self.assertEqual(address_str[1], '0')
    
    def test_address_validation_swarm(self):
        """Test address validation for Swarm addresses"""
        test_seed = 'swarm validation test seed'
        address = pw.Address(seed=test_seed)
        
        # Test that the generated address is valid
        self.assertTrue(pw.validateAddress(address.address))
    
    def test_multiple_addresses_different_seeds(self):
        """Test that different seeds generate different addresses"""
        seed1 = 'first test seed for swarm'
        seed2 = 'second test seed for swarm'
        
        address1 = pw.Address(seed=seed1)
        address2 = pw.Address(seed=seed2)
        
        # Addresses should be different
        self.assertNotEqual(address1.address, address2.address)
        self.assertNotEqual(address1.publicKey, address2.publicKey)
        self.assertNotEqual(address1.privateKey, address2.privateKey)
    
    def test_address_generation_with_nonce(self):
        """Test address generation with nonce for Swarm network"""
        test_seed = 'test seed with nonce'
        nonce = 1
        
        address = pw.Address(seed=test_seed, nonce=nonce)
        
        self.assertIsNotNone(address.address)
        self.assertEqual(address.nonce, nonce)
        
        # Verify chain ID in generated address
        decoded_address = pw.b58decode(address.address)
        address_str = crypto.bytes2str(decoded_address)
        self.assertEqual(address_str[1], '0')
    
    def test_address_from_private_key(self):
        """Test address generation from private key"""
        # First generate an address to get a valid private key
        original_address = pw.Address(seed='test seed for private key')
        private_key = original_address.privateKey
        
        # Create new address from the private key
        new_address = pw.Address(privateKey=private_key)
        
        # Should generate the same address
        self.assertEqual(original_address.address, new_address.address)
        self.assertEqual(original_address.publicKey, new_address.publicKey)
    
    def test_address_from_public_key(self):
        """Test address generation from public key"""
        # First generate an address to get a valid public key
        original_address = pw.Address(seed='test seed for public key')
        public_key = original_address.publicKey
        
        # Create new address from the public key
        new_address = pw.Address(publicKey=public_key)
        
        # Should generate the same address
        self.assertEqual(original_address.address, new_address.address)
        self.assertEqual(original_address.publicKey, new_address.publicKey)
    
    def test_chain_id_consistency(self):
        """Test that all generated addresses use the correct chain ID"""
        seeds = [
            'first consistency test seed',
            'second consistency test seed', 
            'third consistency test seed'
        ]
        
        for seed in seeds:
            address = pw.Address(seed=seed)
            decoded_address = pw.b58decode(address.address)
            address_str = crypto.bytes2str(decoded_address)
            
            # Verify chain ID is '0' for all addresses
            self.assertEqual(address_str[1], '0', 
                           f"Address {address.address} does not have correct chain ID")
    
    def tearDown(self):
        """Clean up after tests"""
        pw.setOnline()

if __name__ == '__main__':
    unittest.main()