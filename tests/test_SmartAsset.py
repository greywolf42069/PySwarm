from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import pytest
import os
import time

PYWAVES_FAUCET_SECRET = os.getenv('PYWAVES_TEST_SECRET')
PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
THISTEST = 'SmartAsset'
NAME = THISTEST + time.strftime('%y%m%d')

pw.setThrowOnError(True)
pw.setNode(PYWAVES_TEST_NODE, 'T')

helpers = Helpers()
faucet = address.Address(privateKey=PYWAVES_FAUCET_SECRET)

testwallet = helpers.prepareTestcase()
# add an extra 1 wves funding to the testwallet
tx = faucet.sendWaves(testwallet, 100000000)


try: 
    def test_issueSmartAssetWithoutPrivateKey():
        myAddress = address.Address('3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm')
        script = 'match tx { \n' + \
                '  case _ => true\n' + \
                '}'
        with pytest.raises(Exception) as error:
            myAddress.issueSmartAsset('SmartAsset2', 'This is just a test smart asset', 10000000, scriptSource = script)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Private key required\') tblen=3>'

    def test_nameTooShort():
        script = 'match tx { \n' + \
                '  case _ => true\n' + \
                '}'
        with pytest.raises(Exception) as error:
            testwallet.issueSmartAsset('Sma', 'This is just a test smart asset', 10000000, scriptSource=script)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Asset name must be between 4 and 16 characters long\') tblen=3>'

    def test_nameTooLong():
        script = 'match tx { \n' + \
                '  case _ => true\n' + \
                '}'
        with pytest.raises(Exception) as error:
            testwallet.issueSmartAsset('SmartTestAssetTeststst', 'This is just a test smart asset', 10000000, scriptSource=script)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Asset name must be between 4 and 16 characters long\') tblen=3>'


    def test_pywavesOffline():
        script = 'match tx { \n' + \
                'case _ => true\n' + \
                '}'

        pw.setOffline()
        with pytest.raises(Exception) as error:
            testwallet.issueSmartAsset('SMartAsset', 'This is just a test smart asset', 10000000, scriptSource = script)

        assert str(error) == '<ExceptionInfo PyWavesException(\'PyWaves currently offline\') tblen=3>'
        pw.setOnline()

    def test_succesfullIssueSmartAsset():    
        script = 'match tx { \n' + \
                'case _ => true\n' + \
                '}'

        token = testwallet.issueAsset(NAME, f"Test Token {NAME}", 100, 8, reissuable=True)
        while not token.status():
            pass

        assert token.status() == 'Issued'
        assert token.name == NAME.encode('ascii', 'ignore')
        assert token.description == f"Test Token {NAME}".encode('ascii', 'ignore')
        assert token.quantity == 100
        assert token.decimals == 8
        assert token.reissuable == True

    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)
