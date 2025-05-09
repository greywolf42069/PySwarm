from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import random
import string
import pytest

pw.setThrowOnError(True)

helpers = Helpers()
testwallet = helpers.prepareTestcase()
alias = ''.join(random.choices(string.ascii_lowercase, k=8))

try:

    def test_aliasWithoutPrivateKey():
        myAddress = address.Address('3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm')
        with pytest.raises(Exception) as error:
            myAddress.createAlias(alias)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Private key required\') tblen=3>'

    def test_succesfullAlias():
        tx = testwallet.createAlias(alias)
        blockchainTx = helpers.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']
    
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)
