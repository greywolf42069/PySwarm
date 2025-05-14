import pywaves as pw
from pywaves import address
from pywaves import asset
import time
from random import randint
from tests.helpers import Helpers
import os

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
pw.setThrowOnError(True)
pw.setNode(PYWAVES_TEST_NODE, 'T')

helpers = Helpers()
testwallet = helpers.prepareTestcase(sendTokens=True)

try:
    
    def test_succesfullBurnAsset():
        tokens = testwallet.assets()
        myToken = asset.Asset(tokens[0])
        tx = testwallet.burnAsset(myToken, 1)
        blockchaintx = helpers.waitFor(tx['id'])
        
        assert blockchaintx['id'] == tx['id']
        
    def test_pywavesOfflineBurnAsset():
        tokens = testwallet.assets()
        myToken = asset.Asset(tokens[0])
        pw.setOffline()       
        tx = testwallet.burnAsset(myToken, 1)
        pw.setOnline()

        assert tx['api-type'] == 'POST'

    # Dummy test case to return funds to faucet
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)

