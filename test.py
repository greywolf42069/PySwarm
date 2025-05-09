import pywaves as pw
from pywaves import address

pw.setThrowOnError(True)
pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
myaddress = address.Address(privateKey='98o2CutFqbqCbVTHjpbHGx7RKk5V1mnGz2sx9fsJLN8j')
scriptAcc = '3Mwoa267qo1oQcTFdMKRMVq1Av4zTHdFsqX'
parameters = []
# tx = myaddress.txGenerator.generateInvokeScript(scriptAcc, None, myaddress.publicKey, [], [], None, txFee=5000000)
tx = myaddress.invokeScript(scriptAcc, 'default', parameters, [])
print(tx)
