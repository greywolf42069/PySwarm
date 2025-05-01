# PyWaves-CE Test Results

## Failed Tests (❌)

### type15Test.py
- test_setScriptWithoutPrivateKey (Failed: JSONDecodeError)
- test_assetScriptOnAnAssetWithoutScript (Failed: JSONDecodeError)
- test_acceptedAssetScript (Failed: JSONDecodeError)

### wxFeeCalculatorTestTN.py
- 1 test failing
- Error: SSLCertVerificationError - Self-signed certificate issue

### buyOrderTest.py
- test_buyPywavesOffline (PASSED)
- test_succesfullBuyOrder (FAILED)

## Partially Successful Tests (⚠️)

### type16Test.py
- test_invokeScriptWithoutPrivateKey (PASSED)
- test_callToDefaultCallable (Failed: KeyError: 'id')
- test_acceptInvokeScriptWithStrAndInt (PASSED)
- test_invokeScriptWithBooleanTrue (PASSED)
- test_invokeScriptWithBooleanFalse (PASSED)
- test_invokeScriptWithListBooleanTrue (PASSED)
- test_invokeScriptWithAssetPayment (PASSED)
- test_invokeScriptWithListBooleanFalse (PASSED)
- test_invokeScriptWithWavesPayment (PASSED)
- test_invokeScriptWithFeeAsset (PASSED)
- test_invokeButPywavesOffline (PASSED)

### wxFeeCalculatorTest.py
- test_getCalculatePercentDiscountedBuyingFee (Failed: Assertion Error)
- test_getCalculatePercentDiscountedSellingFee (PASSED)
- test_getCalculatePercentBuyingFee_01 (PASSED)
- test_getCalculatePercentBuyingFee_02 (PASSED)
- test_getCalculatePercentBuyingFee_03 (PASSED)
- test_getCalculatePercentSellingFee (PASSED)
- test_discountedFee (PASSED)
- test_dynamicFee (PASSED)

## Successful Tests (✅)

### type06Test.py
- test_succesfullBurnAsset
- test_pywavesOfflineBurnAsset

### type02Test.py
- test_sendWaveswithoutPrivateKey
- test_sendWavesButSelfBalanceIsEmpty
- test_sendWavesButWithoutAmount
- test_successfulTransfer
- test_successfulTransferWithAttachment

### type03Test.py
- test_issueAssetWithoutPrivateKey
- test_issueAssetWithTooShortName
- test_pywavesOffline
- test_issueAssetWithTooLongName
- test_succesfullIssueAsset

### type04Test.py
- test_assetTransactionWithoutPrivateKey
- test_assetTransactionWithAmountSmallerEqualsZero
- test_nonExistantAssetTransaction
- test_assetTransactionButAmountBiggerThanBalance
- test_succesfullAssetTransaction
- test_succesfullAssetTransactionWithAttachment
- test_transactionWithNotAsset
- test_transactionFeeIsBiggerThanSelfBalance
- test_successfulTransactionWithSponsoredFee

### type05Test.py
- test_succesfullReissueAsset
- test_reissueAssetPywavesOffline

### type08Test.py
- test_leasingWithoutPrivateKey
- test_leasingWithAmountSmallerEqualsZero
- test_balanceSmallerThanAmount
- test_succesfullLeasing

### type09Test.py
- test_cancelWithoutPrivateKey
- test_cancelWithFeeIsBiggerThanBalance
- test_succesfullCancelLeasing
- test_pywavesOffline

### type10Test.py
- test_aliasWithoutPrivateKey
- test_succesfullAlias

### type11Test.py
- test_massTransferWithoutPrivateKey
- test_massTransferWithoutEnoughWaves
- test_succesfullMassTransfer
- test_MassTransferWithTooMuchRecipients
- test_massTransferWavesFromAccountThatExceedComplexityThreshold

### type12Test.py
- test_stringDataTransaction
- test_integerDataTransaction
- test_booleanDataTransaction
- test_binaryDataTransaction

### type13Test.py
- test_setScriptWithoutPrivateKey
- test_succesfullSetScript

### type14Test.py
- test_sponsoringAssetWithoutPrivateKey
- test_succesfullSponsoringAsset

### type17Test.py
- test_updateAssetInfo

### type11AssetTest.py
- test_assetMassTransferWithoutPrivateKey
- test_assetMassTransferWithTooMuchRecipients
- test_feeIsBiggerThanAmountMassTransfer
- test_amountIsBiggerThanBalanceMassTransfer
- test_succesfullAssetMassTransfer
- test_succesfullSmartAssetMassTransfer
- test_massTransferAssetsFromAccountThatExceedComplexityThreshold

### tradesTest.py
- test_tradesLimit
- test_tradesTimestamp

### type03SmartAssetTest.py
- test_issueSmartAssetWithoutPrivateKey
- test_nameTooShort
- test_nameTooLong
- test_pywavesOffline
- test_succesfullIssueSmartAsset

### oracleTest.py
- test_getDataWithKey
- test_getDataWithoutKey
- test_getDataWithRegex
- test_storeData

### orderClassTest.py
- test_cancelOrder

### parallelPywavesTest.py
- test_successfulTransfer

### sellOrderTest.py
- test_sellPywavesOffline
- test_succesfullSellOrder

### simpleMultisigTest.py
- All tests passed (2/2)
- Fixed capitalization issues in imports

### type12deleteTest.py
- All tests passed (4/4)
- No issues found

### cancelOpenOrdersTest.py
- test_succesfullCancelOpenOrders (PASSED)

### cancelOrderByIdTest.py
- test_pywavesOffline (PASSED)
- test_succesfullCancelOrderById (PASSED)

### cancelOrderTest.py
- test_pywavesOfflineCancelOrder (PASSED)
- test_orderFilled (PASSED)
- test_orderWithoutStatus (PASSED)
- test_succesfullCancelOrder (PASSED)

### getOrderHistoryTest.py
- test_getOrderHistory (PASSED)

### addressCreationTest.py
- All tests passed (13/13)

### addressScriptTest.py
- All tests passed (3/3)

### assetsTest.py
- test_assets (PASSED)

### tradableBalanceTest.py
- test_tradableBalance (PASSED)
- test_tradableBalanceButPywavesOffline (PASSED)

---
Total tests passed: 95
Total tests failed: 8 