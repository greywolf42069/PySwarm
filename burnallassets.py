import os
import pywaves as pw
from pywaves import address
from pywaves import asset
from tests.helpers import Helpers

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
PYWAVES_FAUCET_SECRET = os.getenv('PYWAVES_TEST_SECRET')

def burn_all_assets():
    pw.setNode(PYWAVES_TEST_NODE, 'T')
    faucet = address.Address(privateKey=PYWAVES_FAUCET_SECRET)
    helpers = Helpers()
    
    # Get all assets owned by faucet
    assets = faucet.assets()
   
    for assetId in assets:
        assetBalance = faucet.balance(assetId)
        _asset = asset.Asset(assetId)
        tx = faucet.burnAsset(_asset, assetBalance)
        print(tx)
        if tx:
            helpers.waitFor(tx['id'])
            print(f"Successfully burned asset {assetId}")
        else:
            print(f"Failed to burn asset {assetId}")
    
if __name__ == "__main__":
    burn_all_assets()
