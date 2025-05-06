import pywaves as pw
from pywaves import address
from pywaves import asset
import time
from tests.helpers import Helpers
import os

PYWAVES_FAUCET_SECRET = os.getenv('PYWAVES_TEST_SECRET')
PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
THISTEST = 'testIssue'

NAME = THISTEST + time.strftime('%y%m%d')

pw.setThrowOnError(True)
pw.setNode(PYWAVES_TEST_NODE, 'T')

helpers = Helpers()
faucet = address.Address(privateKey=PYWAVES_FAUCET_SECRET)
testwallet = helpers.prepareTestcase()

# add an extra 1 wves funding to the testwallet
tx = faucet.sendWaves(testwallet, 100000000)
helpers.waitFor(tx['id'])

try:

    def test_successfulIssueAsset():
        token = testwallet.issueAsset(NAME, f"Test Token {NAME}", 100, 8, reissuable=True)
        while not token.status():
            pass
        
        assert token.status() == 'Issued'
        assert token.name == NAME.encode('ascii', 'ignore')
        assert token.description == f"Test Token {NAME}".encode('ascii', 'ignore')
        assert token.quantity == 100
        assert token.decimals == 8
        assert token.reissuable == True

    # Dummy test case to return funds to faucet
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)
