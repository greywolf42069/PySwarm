import pywaves as pw
from pywaves import address
import pytest
from tests.helpers import Helpers
import os
import base58   

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')

pw.setThrowOnError(True)
pw.setNode(PYWAVES_TEST_NODE, 'T')
helpers = Helpers()
testwallet = helpers.prepareTestcase(100000000, sendTokens=True)

seed = str(base58.b58encode(os.urandom(32)))
dappaddress1 = address.Address(seed=seed)

# fund dappaddress1
tx = testwallet.sendWaves(dappaddress1, 500000)
helpers.waitFor(tx['id'])

try:

    def test_addressWithoutScript():
        result = dappaddress1.script()

        assert (result['script'] is None and result['extraFee'] == 0)

    def test_adddressWithScript():
        script = '''{-# STDLIB_VERSION 6 #-}
        {-# CONTENT_TYPE DAPP #-}
        {-# SCRIPT_TYPE ACCOUNT #-}

        @Callable(inv)
        func default() = {
            let message = "Hello from RIDE contract!"
            [
                StringEntry("lastMessage", message),
                StringEntry("caller", inv.caller.toString())
            ]
        }'''

        tx = dappaddress1.setScript(script, txFee=500000)
        helpers.waitFor(tx['id'])

        result = dappaddress1.script()

        assert (result['script'].startswith('base64:') and result['extraFee'] == 0)

    # Dummy test case to return funds to faucet
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)
