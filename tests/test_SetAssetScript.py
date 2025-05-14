import os
from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import pytest
import base58
import random
import string

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')

pw.setThrowOnError(True)
helpers = Helpers()
testwallet = helpers.prepareTestcase(310000000)

seed = str(base58.b58encode(os.urandom(32)))
address1 = address.Address(seed=seed)


try: 

    def test_setScriptWithoutPrivateKey():
        myAddress = address.Address(address1.address)
        script = 'match tx { \n' + \
                '  case _ => true\n' + \
                '}'

        with pytest.raises(Exception) as error:
            myAddress.setAssetScript('loremipsum', script)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Private key required\') tblen=3>'

    def test_assetScriptOnAnAssetWithoutScript():
        assetWithoutScriptName = ''.join(random.choices(string.ascii_lowercase, k=8))
        tx = testwallet.issueAsset(assetWithoutScriptName, 'This is just a Test asset', 10000000)
        assetWithoutScript = asset.Asset(tx['id'])
        helpers.waitFor(tx['id'])

        script = 'match tx { \n' + \
                '  case _ => true\n' + \
                '}'

        tx = testwallet.setAssetScript(assetWithoutScript, script)
        assert tx['message'] == 'State check failed. Reason: Cannot set script on an asset issued without a script'


    def test_acceptedAssetScript():
        
        script = 'match tx { \n' + \
                '  case _ => true\n' + \
                '}'
        assetWithScriptName = ''.join(random.choices(string.ascii_lowercase, k=8))
        assetWithScript = testwallet.issueSmartAsset(assetWithScriptName, 'This is just a test smart asset', 10000000, scriptSource = script)
        while not assetWithScript.status():
            pass

        tx = testwallet.setAssetScript(assetWithScript, script)
        print(tx)
        blockchainTx = helpers.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

            
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)
