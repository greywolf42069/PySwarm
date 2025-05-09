from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import os

PYWAVES_TEST_SECRET = os.getenv('PYWAVES_TEST_SECRET')
PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')

pw.setThrowOnError(True)
pw.setNode(PYWAVES_TEST_NODE, 'T')

helpers = Helpers()
faucet = address.Address(privateKey=PYWAVES_TEST_SECRET)

# use test asset
assets = faucet.assets()
myToken = asset.Asset(assets[0])

def test_succesfullReissueAsset():
    txId = faucet.reissueAsset(myToken, 10, reissuable=True)
    blockchaintx = helpers.waitFor(txId)

    assert blockchaintx['id'] == txId

def test_reissueAssetPywavesOffline():   
    pw.setOffline()
    tx = faucet.reissueAsset(myToken, 10, reissuable=True)
    pw.setOnline()
    assert tx['api-type'] == 'POST'

