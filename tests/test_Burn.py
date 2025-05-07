import pywaves as pw
from pywaves import address
from pywaves import asset
import time
from random import randint
from tests.helpers import Helpers
import os

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
THISTEST = 'Burn'
pw.setThrowOnError(True)
pw.setNode(PYWAVES_TEST_NODE, 'T')

helpers = Helpers()
testwallet = helpers.prepareTestcase()

try:
    
    def test_succesfullBurnAsset():
        print("----- test_succesfullBurnAsset -----")
        token = testwallet.assets()
        if len(token) == 0:
            raise Exception("No assets found")
        token = asset.Asset(token[0])

        txId = testwallet.burnAsset(token, 1)
        blockchaintx = helpers.waitFor(txId)
        
        assert blockchaintx['id'] == txId
        
    def test_pywavesOfflineBurnAsset():
        print("----- test_pywavesOfflineBurnAsset -----")
        token = testwallet.assets()
        if len(token) == 0:
            raise Exception("No assets found")
        token = token[0]
        token = asset.Asset(token[0])
        pw.setOffline()       
        tx = testwallet.burnAsset(token, 1)
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

