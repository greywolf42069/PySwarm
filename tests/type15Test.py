import os
from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import pytest

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
PYWAVES_TEST_PRIVATEKEY = 'BGpBRDeUiHskf4bdyWoUAKpP9DSx51haovHcGNqPEy6Q'
PYWAVES_TEST_ASSET1 = '5Cs2APZPHeXqhB2At2qWT2wUuCe9SjxitFYdXhj6Q8FL'
PYWAVES_TEST_ASSET2 = '2X2xWhF9hzdQa2so459dbnQTBbyikdXqX3cfXiaATufv'

pw.setThrowOnError(True)

def test_setScriptWithoutPrivateKey():
    pw.setNode(PYWAVES_TEST_NODE, 'T')
    myAddress = address.Address('3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm')
    myToken = asset.Asset(PYWAVES_TEST_ASSET1)
    script = 'match tx { \n' + \
            '  case _ => true\n' + \
            '}'

    with pytest.raises(Exception) as error:
        myAddress.setAssetScript(myToken, script)

    assert str(error) == '<ExceptionInfo PyWavesException(\'Private key required\') tblen=3>'

def test_assetScriptOnAnAssetWithoutScript():
    pw.setNode(PYWAVES_TEST_NODE, 'T')
    myAddress = address.Address(privateKey=PYWAVES_TEST_PRIVATEKEY)
    myToken = asset.Asset(PYWAVES_TEST_ASSET1)

    script = 'match tx { \n' + \
             '  case _ => true\n' + \
             '}'

    tx = myAddress.setAssetScript(myToken, script)
    assert tx['message'] == 'State check failed. Reason: Cannot set script on an asset issued without a script'


def test_acceptedAssetScript():
    helpers = Helpers()
    pw.setNode(PYWAVES_TEST_NODE, 'T')
    myAddress = address.Address(privateKey=PYWAVES_TEST_PRIVATEKEY)
    myToken = asset.Asset(PYWAVES_TEST_ASSET2)

    script = 'match tx { \n' + \
             '  case _ => true\n' + \
             '}'

    tx = myAddress.setAssetScript(myToken, script)
    blockchainTx = helpers.waitFor(tx['id'])

    assert blockchainTx['id'] == tx['id']