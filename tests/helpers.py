import os
import pywaves as pw
import requests
import time
from pywaves import address

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
PYWAVES_FAUCET_SECRET = os.getenv('PYWAVES_TEST_SECRET')

class Helpers:

    def waitFor(self, id):
        pw.setNode(PYWAVES_TEST_NODE, 'T')
        response = requests.get(pw.NODE + '/transactions/info/' + id).json()

        if 'error' in response:
            print(response)
            print('Waiting 1 sec...')
            time.sleep(1)
            return self.waitFor(id)
        else:
            return response

    def prepareTestcase(self, testcase):
        pw.setNode(PYWAVES_TEST_NODE, 'T')
        faucet = address.Address(privateKey=PYWAVES_FAUCET_SECRET)
        balance = faucet.balance()
        if (balance < 100000000):
            raise Exception('Faucet balance is too low. Please refill it.')

        testwallet = address.Address(seed=PYWAVES_FAUCET_SECRET+testcase)
        testwalletBalance = testwallet.balance()
        if (testwalletBalance < 100000000):
            faucet.sendWaves(testwallet, 100000000-testwalletbalance)
        print(f"Operating on address: {testwallet.address}")
        return testwallet


