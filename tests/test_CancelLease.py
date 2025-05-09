from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import pytest
import os

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
TEST_NODE_ADDRESS = os.getenv('TEST_NODE_ADDRESS')

pw.setThrowOnError(True)
pw.setNode(PYWAVES_TEST_NODE, 'T')
PYWAVES_TEST_SECRET = os.getenv('PYWAVES_TEST_SECRET')

helpers = Helpers()
testwallet = helpers.prepareTestcase()

faucet = address.Address(privateKey=PYWAVES_TEST_SECRET)
leasingAddress = address.Address(TEST_NODE_ADDRESS)

try:

    def test_cancelWithoutPrivateKey():
        myAddress = address.Address('3MpvqThrQUCC1DbkY9sMmo4fp77e2h11NaM')
        leasingID = 'testLeaseID'

        with pytest.raises(Exception) as error:
            myAddress.leaseCancel(leasingID)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Private key required\') tblen=3>'
    '''
    # commented test. This can't be worked on as now balance() returns regular balance.
    def test_cancelWithFeeIsBiggerThanBalance():
    pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
    myAddress = address.Address(privateKey='G6aEiT1ih4jwLfgJ89EvULbsziixDuqnEUTpEkvZ76hv')
    leasingID = address.Address('3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm')

    with pytest.raises(Exception) as error:
        myAddress.leaseCancel(leasingID)

    assert str(error) == '<ExceptionInfo PyWavesException(\'Insufficient Waves balance\') tblen=3>'
    '''
    
    def test_succesfullCancelLeasing():
        leaseTransaction = testwallet.lease(leasingAddress, 9700000)
        helpers.waitFor(leaseTransaction['id'])
        print(leaseTransaction['id'])
        leaseCancelTransactionId = testwallet.leaseCancel(leaseTransaction['id'])
        print(leaseCancelTransactionId)
        blockchainTx = helpers.waitFor(leaseCancelTransactionId)

        assert blockchainTx['id'] == leaseCancelTransactionId
    
    def test_pywavesOffline():
        pw.setOffline()
        leaseCancelTransactionId = testwallet.leaseCancel('3sEGi6tL8Ptg4L9wJv8FZRYu1hJxFJrWZGC4tWVrcycS')
        pw.setOnline()

        assert leaseCancelTransactionId['api-type'] == 'POST'
    
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)