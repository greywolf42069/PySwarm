import os
import pywaves as pw
import requests
import time

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')

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
