import os
from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import time
from random import randint

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
PYWAVES_FAUCET_PRIVATEKEY = os.getenv('PYWAVES_TEST_SECRET')
PYWAVES_TEST_ASSET = os.getenv('PYWAVES_TEST_ASSET')

pw.setThrowOnError(True)

pw.setNode(PYWAVES_TEST_NODE, 'T')
faucet = address.Address(privateKey=PYWAVES_FAUCET_PRIVATEKEY)
print(f"Operating on address: {faucet.address}")
balance = faucet.balance()
if (balance < 100000000):
    raise Exception('Faucet balance is too low. Please refill it.')

def test_succesfullBurnAsset():
    helpers = Helpers()
    tokenQuantity = randint(1000000, 99999999)
    tokenDecimals = randint(0, 8)
    tokenName = "PW_" + str(tokenQuantity) + str(tokenDecimals)
    print(f"Creating asset {tokenName} with quantity {tokenQuantity} and decimal {tokenDecimals}")
    token = faucet.issueAsset(tokenName, f"Test Token {tokenName}", tokenQuantity, tokenDecimals, reissuable=False)
    while not token.status():
	    pass
    txId = faucet.burnAsset(token, 1)
    blockchaintx = helpers.waitFor(txId)
    
    assert blockchaintx['id'] == txId


'''
def test_pywavesOfflineBurnAsset():
    pw.setNode(PYWAVES_TEST_NODE, 'T')
    myAddress = address.Address(privateKey=PYWAVES_TEST_PRIVATEKEY)
    print(f"Operating on address: {myAddress.address}")
    myToken = asset.Asset(PYWAVES_TEST_ASSET)
    pw.setOffline()
    tx = myAddress.burnAsset(myToken, 1)
    pw.setOnline()

    assert tx['api-type'] == 'POST'
'''