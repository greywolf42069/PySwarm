from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import pywaves.crypto as crypto
from pywaves.txSigner import TxSigner
from pywaves.txGenerator import TxGenerator
import base58
import pytest

pw.setThrowOnError(True)

def test_sendWaves():
    helpers = Helpers()
    pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
    firstAddress = address.Address(seed = 'this is just a simple test seed one')
    secondAddress = address.Address(seed = 'this is just a simple test seed two')

    generator = TxGenerator()
    signer = TxSigner()
    tx = generator.generateSendWaves(secondAddress, 1, firstAddress.publicKey, txFee=500000)
    signer.signTx(tx, firstAddress.privateKey)
    signer.signTx(tx, secondAddress.privateKey)

    res = firstAddress.broadcastTx(tx)
    blockchainTx = helpers.waitFor(res['id'])

    assert blockchainTx['id'] == res['id']

def test_sendWavesWithAttachment():
    helpers = Helpers()
    pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
    firstAddress = address.Address(seed = 'this is just a simple test seed one')
    secondAddress = address.Address(seed = 'this is just a simple test seed two')
    attachment = 'just a test transfer'

    generator = TxGenerator()
    signer = TxSigner()
    tx = generator.generateSendWaves(secondAddress, 1, firstAddress.publicKey, attachment = attachment, txFee=500000)
    signer.signTx(tx, firstAddress.privateKey)
    signer.signTx(tx, secondAddress.privateKey)

    res = firstAddress.broadcastTx(tx)
    blockchainTx = helpers.waitFor(res['id'])

    assert blockchainTx['id'] == res['id']