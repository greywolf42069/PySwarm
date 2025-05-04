import os
from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
PYWAVES_TEST_PRIVATEKEY = os.getenv('PYWAVES_TEST_PRIVATEKEY')
PYWAVES_TEST_ASSET = os.getenv('PYWAVES_TEST_ASSET')

pw.setThrowOnError(True)

def test_succesfullBurnAsset():
    helpers = Helpers()
    pw.setNode(PYWAVES_TEST_NODE, 'T')
    myAddress = address.Address(privateKey=PYWAVES_TEST_PRIVATEKEY)
    print(f"Operating on address: {myAddress.address}")
    myToken = asset.Asset(PYWAVES_TEST_ASSET)

    txId = myAddress.burnAsset(myToken, 1)
    blockchaintx = helpers.waitFor(txId)

    assert blockchaintx['id'] == txId

def test_pywavesOfflineBurnAsset():
    pw.setNode(PYWAVES_TEST_NODE, 'T')
    myAddress = address.Address(privateKey=PYWAVES_TEST_PRIVATEKEY)
    print(f"Operating on address: {myAddress.address}")
    myToken = asset.Asset(PYWAVES_TEST_ASSET)
    pw.setOffline()
    tx = myAddress.burnAsset(myToken, 1)
    pw.setOnline()

    assert tx['api-type'] == 'POST'
