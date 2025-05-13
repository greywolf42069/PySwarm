from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
from pywaves import oracle
from pywaves.oracle import Oracle
import os  
import base58


PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')

pw.setThrowOnError(True)
pw.setNode(PYWAVES_TEST_NODE, 'T')

helpers = Helpers()
testwallet = helpers.prepareTestcase(1500000)

try:

    def test_setOracleScript():
        
        script = '''{-# STDLIB_VERSION 5 #-}
        {-# SCRIPT_TYPE ACCOUNT #-}
        {-# CONTENT_TYPE DAPP #-}

        @Callable(i)
        func storeValue (name: String, value: Int) = [IntegerEntry(name, value)]

        @Callable(i)
        func storeBinaryValue (name: String, value: ByteVector) = [BinaryEntry(name, value)]

        @Callable(i)
        func storeBooleanValue (name: String, value: Boolean) = [BooleanEntry(name, value)]

        @Verifier(tx)
        func verify () = sigVerify(tx.bodyBytes, tx.proofs[0], tx.senderPublicKey)

        @Callable(i)
        func storeListValue (name: String, value1: List[String], value2: List[Int], value3: List[Boolean]) = [
        StringEntry((name + "_0"), value1[0]),
        IntegerEntry((name + "_1"), value2[0]),
        BooleanEntry((name + "_2"), value3[0])
        ]'''

        tx = testwallet.setScript(script, txFee=500000)
        blockchainTx = helpers.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

    def test_storeData():
        oracle = Oracle(seed=testwallet.seed)
        tx = oracle.storeData(type='string', key= 'testOracle', dataEntry='Hello')
        blockchainTx = helpers.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']
    
    def test_getDataWithKey():
       oracle = Oracle(oracleAddress=testwallet.address)
       data = oracle.getData(key = 'testOracle')

       assert data != None

    def test_getDataWithoutKey():
        oracle = Oracle(oracleAddress=testwallet.address)
        data = oracle.getData(key = None)

        assert len(data) != 0

    def test_getDataWithRegex():
        oracle = Oracle(oracleAddress=testwallet.address)
        data = oracle.getData(regex='^test.*$')

        assert data != None
    # Dummy test case to return funds to faucet
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)

