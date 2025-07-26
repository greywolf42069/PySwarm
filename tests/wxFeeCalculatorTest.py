from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
from pywaves.WXFeeCalculator import WXFeeCalculator
import requests

# Set offline mode for all tests
pw.setOffline()
pw.setMatcher('http://localhost:6869')

def test_getCalculatePercentDiscountedBuyingFee():
    """Test WX fee calculator discounted buying fee calculation offline"""
    pw.setMatcher('http://localhost:6869')
    pw.setNode('http://localhost:6869')
    priceAssetId = 'DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p'
    amountAssetId = 'WAVES'
    price = 10 * 10 ** 6
    amount = 10 * 10 ** 8
    wxFeeCalculator = WXFeeCalculator()

    # Test fee calculation method exists and is callable
    assert hasattr(wxFeeCalculator, 'calculatePercentDiscountedBuyingFee')
    assert callable(getattr(wxFeeCalculator, 'calculatePercentDiscountedBuyingFee'))
    
    # Test calculation returns a reasonable fee
    calculatedFee = wxFeeCalculator.calculatePercentDiscountedBuyingFee(amountAssetId, priceAssetId, price, amount)
    assert isinstance(calculatedFee, int)
    assert calculatedFee > 0
    assert calculatedFee < amount  # Fee should be less than the amount

def test_getCalculatePercentDiscountedSellingFee():
    """Test WX fee calculator discounted selling fee calculation offline"""
    priceAssetId = 'DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p'
    amountAssetId = 'WAVES'
    price = 10 * 10 ** 6
    amount = 10 * 10 ** 8
    wxFeeCalculator = WXFeeCalculator()

    # Test fee calculation method exists and is callable
    assert hasattr(wxFeeCalculator, 'calculatePercentDiscountedSellingFee')
    assert callable(getattr(wxFeeCalculator, 'calculatePercentDiscountedSellingFee'))
    
    # Test calculation returns a reasonable fee
    calculatedFee = wxFeeCalculator.calculatePercentDiscountedSellingFee(priceAssetId, amountAssetId, amount)
    assert isinstance(calculatedFee, int)
    assert calculatedFee > 0
    assert calculatedFee < amount  # Fee should be less than the amount

def test_getCalculatePercentBuyingFee_01():
    """Test WX fee calculator percent buying fee calculation offline"""
    priceAssetId = '34N9YcEETLWn93qYQ64EsP1x89tSruJU44RrEMSXXEPJ'
    amountAssetId = 'Atqv59EYzjFGuitKVnMRk6H8FukjoV3ktPorbEys25on'
    price = 109185
    amount = 999000000
    wxFeeCalculator = WXFeeCalculator()

    # Test fee calculation method exists and is callable
    assert hasattr(wxFeeCalculator, 'calculatePercentBuyingFee')
    assert callable(getattr(wxFeeCalculator, 'calculatePercentBuyingFee'))
    
    # Test calculation returns a reasonable fee
    calculatedFee = wxFeeCalculator.calculatePercentBuyingFee(amountAssetId, priceAssetId, price, amount)
    assert isinstance(calculatedFee, int)
    assert calculatedFee > 0
    assert calculatedFee < amount  # Fee should be less than the amount

def test_getCalculatePercentBuyingFee_02():
    """Test WX fee calculator percent buying fee calculation offline (case 2)"""
    priceAssetId = 'DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p'
    amountAssetId = 'WAVES'
    price = 1 * 10 ** 6
    amount = 1 * 10 ** 8
    wxFeeCalculator = WXFeeCalculator()

    # Test calculation returns a reasonable fee
    calculatedFee = wxFeeCalculator.calculatePercentBuyingFee(amountAssetId, priceAssetId, price, amount)
    assert isinstance(calculatedFee, int)
    assert calculatedFee > 0
    assert calculatedFee < amount  # Fee should be less than the amount

def test_getCalculatePercentBuyingFee_03():
    """Test WX fee calculator percent buying fee calculation offline (case 3)"""
    priceAssetId = 'DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p'
    amountAssetId = 'WAVES'
    price = 100 * 10 ** 6
    amount = 100 * 10 ** 8
    wxFeeCalculator = WXFeeCalculator()

    # Test calculation returns a reasonable fee
    calculatedFee = wxFeeCalculator.calculatePercentBuyingFee(amountAssetId, priceAssetId, price, amount)
    assert isinstance(calculatedFee, int)
    assert calculatedFee > 0
    assert calculatedFee < amount  # Fee should be less than the amount

def test_getCalculatePercentSellingFee():
    """Test WX fee calculator percent selling fee calculation offline"""
    priceAssetId = 'DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p'
    amountAssetId = 'WAVES'
    price = 10 * 10 ** 6
    amount = 10 * 10 ** 8
    wxFeeCalculator = WXFeeCalculator()

    # Test fee calculation method exists and is callable
    assert hasattr(wxFeeCalculator, 'calculatePercentSellingFee')
    assert callable(getattr(wxFeeCalculator, 'calculatePercentSellingFee'))
    
    # Test calculation returns a reasonable fee
    calculatedFee = wxFeeCalculator.calculatePercentSellingFee(priceAssetId, amountAssetId, amount)
    assert isinstance(calculatedFee, int)
    assert calculatedFee > 0
    assert calculatedFee < amount  # Fee should be less than the amount

def test_discountedFee():
    """Test WX fee calculator dynamic discount fee calculation offline"""
    wxFeeCalculator = WXFeeCalculator()

    # Test fee calculation method exists and is callable
    assert hasattr(wxFeeCalculator, 'calculateDynamicDiscountFee')
    assert callable(getattr(wxFeeCalculator, 'calculateDynamicDiscountFee'))
    
    # Test calculation returns a reasonable fee
    calculatedFee = wxFeeCalculator.calculateDynamicDiscountFee()
    assert isinstance(calculatedFee, int)
    assert calculatedFee > 0

def test_dynamicFee():
    """Test WX fee calculator dynamic fee calculation offline"""
    wxFeeCalculator = WXFeeCalculator()

    # Test fee calculation method exists and is callable
    assert hasattr(wxFeeCalculator, 'calculateDynamicFee')
    assert callable(getattr(wxFeeCalculator, 'calculateDynamicFee'))
    
    # Test calculation returns a reasonable fee
    calculatedFee = wxFeeCalculator.calculateDynamicFee()
    assert isinstance(calculatedFee, int)
    assert calculatedFee > 0
