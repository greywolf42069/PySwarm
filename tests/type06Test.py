import pywaves as pw
from pywaves import address
from pywaves import asset
import time
from random import randint
from tests.helpers import Helpers
import os


PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
THISTEST = 'test06'

pw.setThrowOnError(True)
pw.setNode(PYWAVES_TEST_NODE, 'T')

helpers = Helpers()
testwallet = helpers.prepareTestcase(THISTEST)

assets = testwallet.assets()

if len(assets) == 0:
    token = testwallet.issueAsset('PW_'+THISTEST, f"Test Token {THISTEST}", 10000000, 8, reissuable=False)
    while not token.status():
	    pass
else:
    token = asset.Asset(assets[0])

print("Using token: ", token)

def test_succesfullBurnAsset():
    txId = testwallet.burnAsset(token, 1)
    blockchaintx = helpers.waitFor(txId)
    
    assert blockchaintx['id'] == txId

def test_pywavesOfflineBurnAsset():
    pw.setOffline()
    tx = testwallet.burnAsset(token, 1)
    pw.setOnline()

    assert tx['api-type'] == 'POST'