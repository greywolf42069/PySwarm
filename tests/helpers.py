import os
import pywaves as pw
import requests
import time
import base58
from pywaves import address
from pywaves import asset

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
PYWAVES_TEST_SECRET = os.getenv('PYWAVES_TEST_SECRET')

class Helpers:

    def waitFor(self, id, timeout=30):
        pw.setNode(PYWAVES_TEST_NODE, 'T')
        response = requests.get(pw.NODE + '/transactions/info/' + id).json()
        if 'error' in response:
            if timeout <= 0:
                raise TimeoutError(f"Transaction {id} not confirmed after timeout")
            print(f"Tx: {id}")
            print(response)

            if  (response['error'] == 311) :
                print('Waiting 5 sec...')
                time.sleep(5)
                return self.waitFor(id, timeout - 1)
            else:
                raise Exception(f"Transaction {id} failed")
        else:
            return response

    def prepareTestcase(self):
        pw.setNode(PYWAVES_TEST_NODE, 'T')
        faucet = address.Address(privateKey=PYWAVES_TEST_SECRET)
        
        # generate a random address using 32 random bytes converted to base58
        seed = str(base58.b58encode(os.urandom(32)))
        print(f"Using seed: {seed}")
        testwallet = address.Address(seed=seed)
        print(f"Operating on address: {testwallet.address}")
        
        testwalletBalance = testwallet.balance()
        # refill test wallet
       
        if (testwalletBalance < 50000000):
            print(f"----- Sending waves to testwallet -----")
            tx = faucet.sendWaves(testwallet, 100000000-testwalletBalance)
            self.waitFor(tx['id'])
        
        # check it faucet has test asset
        assets = faucet.assets()
        if (len(assets) == 0):
            testtoken = faucet.issueAsset('pw_testasset-3', f"Test Token", 10000000*(10**8), 8, reissuable=True)
            while not testtoken.status():
                pass
            # sponsor asset           
            assets = faucet.assets()        
            tx = faucet.sponsorAsset(assetId=assets[0], minimalFeeInAssets = 1000000)
            self.waitFor(tx['id'])
        else:
            testtoken = asset.Asset(assets[0])
            

        # send some assets to testwallet
        print(f"----- Sending assets to testwallet -----")
        tx = faucet.sendAsset(testwallet, testtoken, 100000000)
        self.waitFor(tx['id'])
        
        return testwallet

    def closeTestcase(self, testwallet):
        pw.setNode(PYWAVES_TEST_NODE, 'T')
        faucet = address.Address(privateKey=PYWAVES_TEST_SECRET)
        testwalletBalance = testwallet.balance()
        print(f"Testwallet balance: {testwalletBalance}")   
        if (testwalletBalance > 100000):
            testwallet.sendWaves(faucet, testwalletBalance-100000)


    