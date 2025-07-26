from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
import json

pw.setThrowOnError(True)

def test_successfulTransfer():
    """Test parallel PyWaves transfer functionality offline"""
    # Set offline mode first to avoid any network calls
    pw.setOffline()
    
    helpers = Helpers()
    parallelPW = pw.ParallelPyWaves()
    
    # Configure for Swarm network, set offline mode and throw on error
    parallelPW.setNode('http://localhost:6869', 'S')
    parallelPW.setOffline()
    parallelPW.setThrowOnError(True)

    myAddress = address.Address(privateKey='BGpBRDeUiHskf4bdyWoUAKpP9DSx51haovHcGNqPEy6Q', pywaves=parallelPW)
    # Generate a proper Swarm address instead of using hardcoded address
    recipientAddress = address.Address(seed='test recipient seed for swarm parallel test', pywaves=parallelPW)

    # Test transaction creation (offline)
    tx = myAddress.sendWaves(recipientAddress, 1*10**4, txFee=500000)
    
    # Verify transaction structure (offline mode returns wrapped API structure)
    assert 'api-data' in tx
    assert 'api-type' in tx
    assert 'api-endpoint' in tx
    
    # Parse the actual transaction data
    tx_data = json.loads(tx['api-data'])
    
    assert 'type' in tx_data
    assert 'amount' in tx_data
    assert 'fee' in tx_data
    assert 'recipient' in tx_data
    assert 'proofs' in tx_data
    
    assert tx_data['type'] == 4  # Transfer transaction type
    assert tx_data['amount'] == 1*10**4
    assert tx_data['fee'] == 500000
    assert tx_data['recipient'] == recipientAddress.address
    
    # Verify ParallelPyWaves functionality
    assert hasattr(parallelPW, 'setNode')
    assert callable(getattr(parallelPW, 'setNode'))
    assert parallelPW.NODE == 'http://localhost:6869'
    assert parallelPW.CHAIN_ID == 'S'
