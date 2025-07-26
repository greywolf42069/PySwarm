import pywaves as pw
import requests
import math

class WXFeeCalculator(object):

    priceConstantExp = 8
    discountAssetDecimals = 8
    #baseFee = 1000000

    def __init__(self):
        self.matcher = pw.MATCHER
        self.node = pw.NODE
        
        # Check if offline mode is enabled
        if hasattr(pw, 'OFFLINE') and pw.OFFLINE:
            # Use mock settings for offline mode
            self.settings = {
                'orderFee': {
                    'composite': {
                        'default': {'dynamic': {'baseFee': 300000}},
                        'discount': {'value': 50, 'assetId': 'Atqv59EYzjFGuitKVnMRk6H8FukjoV3ktPorbEys25on'},
                        'custom': {}
                    }
                },
                'rates': {
                    'WAVES': 1.0,
                    'DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p': 1.0,
                    'Atqv59EYzjFGuitKVnMRk6H8FukjoV3ktPorbEys25on': 1.0,
                    '34N9YcEETLWn93qYQ64EsP1x89tSruJU44RrEMSXXEPJ': 1.0,
                    'bPWkA3MNyEr1TuDchWgdpqJZhGhfPXj7dJdr3qiW2kD': 1.0
                }
            }
            self.baseFee = 300000
        else:
            self.settings = requests.get(pw.MATCHER + '/matcher/settings').json()
            self.baseFee = self.settings['orderFee']['composite']['default']['dynamic']['baseFee']

    def _correctRate(self, rate, assetDecimals):
        return rate * math.pow(10, (assetDecimals - self.priceConstantExp))

    def _getAssetDecimals(self, assetId):
        if assetId == pw.DEFAULT_CURRENCY: #'WAVES':
            return 8
        else:
            # Check if offline mode is enabled
            if hasattr(pw, 'OFFLINE') and pw.OFFLINE:
                # Return default decimals for offline mode
                return 8
            else:
                assetInfo = requests.get(self.node + '/assets/details/' + assetId).json()
                return assetInfo['decimals']

    def _getMinFee(self, assetId):
        if assetId == pw.DEFAULT_CURRENCY: #'WAVES':
            return self.baseFee
        else:
            # Check if offline mode is enabled
            if hasattr(pw, 'OFFLINE') and pw.OFFLINE:
                # Return default minimum fee for offline mode
                return self.baseFee
            else:
                assetInfo = requests.get(self.node + '/assets/details/' + assetId).json()
                assetDecimals = assetInfo['decimals']
                rates = self.settings['rates']
                assetRate = self._correctRate(rates[assetId], assetDecimals)
                wavesRate = self._correctRate(rates[pw.DEFAULT_CURRENCY], 8)

                return int(self.baseFee * assetRate / wavesRate)

    def _getMinFeeInDiscountAsset(self, assetId):
        discount = self.settings['orderFee']['composite']['discount']['value']
        
        # Check if offline mode is enabled
        if hasattr(pw, 'OFFLINE') and pw.OFFLINE:
            # Return default minimum fee for offline mode
            return int(self.baseFee * (100 - discount) / 100) + 1
        else:
            discountAssetInfo = requests.get(self.node + '/assets/details/' + assetId).json()
            discountAssetDecimals = discountAssetInfo['decimals']
            rates = self.settings['rates']
            discountAssetRate = self._correctRate(rates[assetId], discountAssetDecimals)
            wavesRate = self._correctRate(rates[pw.DEFAULT_CURRENCY], 8)
            
            return int(self.baseFee * discountAssetRate / wavesRate * (100 - discount) / 100) + 1

    def calculateDynamicFee(self):
        # Check if offline mode is enabled
        if hasattr(pw, 'OFFLINE') and pw.OFFLINE:
            # Return default dynamic fee for offline mode
            return self.baseFee + 1
        else:
            return int(self.baseFee * self.settings['rates'][self.amountAssetId]) + 1

    def calculateDynamicDiscountFee(self):
        discount = self.settings['orderFee']['composite']['discount']['value']
        discountAssetId = self.settings['orderFee']['composite']['discount']['assetId']
        
        # Check if offline mode is enabled
        if hasattr(pw, 'OFFLINE') and pw.OFFLINE:
            # Return default dynamic discount fee for offline mode
            return int(self.baseFee * (100 - discount) / 100) + 1
        else:
            discountAssetRate = self.settings['rates'][discountAssetId]
            correctedRate = self._correctRate(discountAssetRate, self.discountAssetDecimals)
            calculatedFee = int(self.baseFee * correctedRate * (100 - discount) / 100) + 1
            minFee = self._getMinFeeInDiscountAsset(discountAssetId)

            return max(calculatedFee, minFee)

    def calculatePercentSellingFee(self, priceAsset, amountAsset, amountToSell):
        # Handle offline mode with default values
        if hasattr(pw, 'OFFLINE') and pw.OFFLINE:
            minFee = 0.1  # Default 0.1% fee
        else:
            custom_key = amountAsset + '-' + priceAsset
            if custom_key in self.settings['orderFee']['composite']['custom']:
                minFee = self.settings['orderFee']['composite']['custom'][custom_key]['percent']['minFee']
            else:
                minFee = 0.1  # Default fallback
        
        calculatedFee = int(amountToSell * minFee / 100) + 1
        minFeeValue = self._getMinFee(amountAsset)

        return max(calculatedFee, minFeeValue)

    def calculatePercentDiscountedSellingFee(self, priceAssetId, amountAssetId, amountToSell):
        discount = self.settings['orderFee']['composite']['discount']['value']
        
        # Handle offline mode with default values
        if hasattr(pw, 'OFFLINE') and pw.OFFLINE:
            minFee = 0.1  # Default 0.1% fee
        else:
            custom_key = self.amountAssetId + '-' + priceAssetId
            if custom_key in self.settings['orderFee']['composite']['custom']:
                minFee = self.settings['orderFee']['composite']['custom'][custom_key]['percent']['minFee']
            else:
                minFee = 0.1  # Default fallback
        
        discountAssetId = self.settings['orderFee']['composite']['discount']['assetId']
        rates = self.settings['rates']
        discountAssetRate = self._correctRate(rates[discountAssetId], self.discountAssetDecimals)
        amountAssetDecimals = self._getAssetDecimals(amountAssetId)
        amountAssetRate = self._correctRate(rates[amountAssetId], amountAssetDecimals)
        calculatedFee = int(amountToSell * (minFee / 100) * (discountAssetRate / amountAssetRate) * (100 - discount) / 100) + 1
        minFeeValue = self._getMinFeeInDiscountAsset(discountAssetId)

        return max(calculatedFee, minFeeValue)

    def calculatePercentBuyingFee(self, amountAssetId, priceAssetId, price, amountToBuy):
        # Handle offline mode with default values
        if hasattr(pw, 'OFFLINE') and pw.OFFLINE:
            minFee = 0.1  # Default 0.1% fee
        else:
            custom_key = amountAssetId + '-' + priceAssetId
            if custom_key in self.settings['orderFee']['composite']['custom']:
                minFee = self.settings['orderFee']['composite']['custom'][custom_key]['percent']['minFee']
            else:
                minFee = 0.1  # Default fallback
        
        priceAssetDecimals = self._getAssetDecimals(priceAssetId)
        amountAssetDecimals = self._getAssetDecimals(amountAssetId)
        price = price / math.pow(10, priceAssetDecimals)
        amount = amountToBuy / math.pow(10, amountAssetDecimals)
        calculatedFee = amount * price * minFee / 100
        calculatedFee = int(calculatedFee * math.pow(10, priceAssetDecimals))
        minFeeValue = self._getMinFee(priceAssetId)

        return int(max(calculatedFee, minFeeValue))

    def calculatePercentDiscountedBuyingFee(self, amountAssetId, priceAssetId, price, amountToBuy):
        discount = self.settings['orderFee']['composite']['discount']['value']
        
        # Handle offline mode with default values
        if hasattr(pw, 'OFFLINE') and pw.OFFLINE:
            minFee = 0.1  # Default 0.1% fee
        else:
            custom_key = amountAssetId + '-' + priceAssetId
            if custom_key in self.settings['orderFee']['composite']['custom']:
                minFee = self.settings['orderFee']['composite']['custom'][custom_key]['percent']['minFee']
            else:
                minFee = 0.1  # Default fallback
        
        discountAssetId = self.settings['orderFee']['composite']['discount']['assetId']
        rates = self.settings['rates']
        discountAssetRate = self._correctRate(rates[discountAssetId], self.discountAssetDecimals)
        priceAssetDecimals = self._getAssetDecimals(priceAssetId)
        priceAssetRate = self._correctRate(rates[priceAssetId], priceAssetDecimals)
        amountAssetDecimals = self._getAssetDecimals(amountAssetId)
        price = price / math.pow(10, priceAssetDecimals)
        amount = amountToBuy / math.pow(10, amountAssetDecimals)
        calculatedFee = amount * price * (minFee / 100) * (discountAssetRate / priceAssetRate) * (100 - discount) / 100
        calculatedFee = int(calculatedFee * math.pow(10, self.discountAssetDecimals))
        minFeeValue = self._getMinFeeInDiscountAsset(discountAssetId)

        return int(max(calculatedFee, minFeeValue))
