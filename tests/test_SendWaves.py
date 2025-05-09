from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import base58
import pywaves.crypto as crypto
import os
from tests.helpers import Helpers
import pytest

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')

pw.setThrowOnError(True)
pw.setNode(PYWAVES_TEST_NODE, 'T')

helpers = Helpers()
testwallet = helpers.prepareTestcase()

try:

    def test_sendWaveswithoutPrivateKey():
        myAddress = address.Address('3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm')
        with pytest.raises(Exception) as error:
            myAddress.sendWaves(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), 100*10**8)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Private key required\') tblen=3>'

    def test_sendWavesButSelfBalanceIsInsufficient():
        with pytest.raises(Exception) as error:
            testwallet.sendWaves(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), 100*10**8)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Insufficient Waves balance\') tblen=3>'

    def test_sendWavesButWithoutAmount():
        with pytest.raises(Exception) as error:
            testwallet.sendWaves(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), 0)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Amount must be > 0\') tblen=3>'

    def test_successfulTransfer():
        tx = testwallet.sendWaves(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), 1*10*4, txFee=500000)
        blockchainTx = helpers.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

    def test_successfulTransferWithAttachment():
        attachment = 'this is just a test'
        tx = testwallet.sendWaves(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), 1*10*4, attachment=attachment)
        blockchainTx = helpers.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

    # Dummy test case to return funds to faucet
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)
