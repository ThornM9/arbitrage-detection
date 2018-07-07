from botapi import apiCalls
from transactions import Transactions
from pricecomparisons import PriceComparisons
import json

apiCalls().getMarkets('bittrex')
apiCalls().getMarkets('poloniex')
apiCalls().getMarkets('hitbtc')

bittrexNormCurrencies = apiCalls().returnCurrencies('bittrex')
poloniexNormCurrencies = apiCalls().returnCurrencies('poloniex')
hitbtcNormCurrencies = apiCalls().returnCurrencies('hitbtc')

PriceComparisons().findCommonCurrencies(bittrexNormCurrencies, poloniexNormCurrencies, hitbtcNormCurrencies)
PriceComparisons().getData()
PriceComparisons().comparePrices()

PriceComparisons().findTriangleArb(bittrexNormCurrencies, poloniexNormCurrencies, hitbtcNormCurrencies)
