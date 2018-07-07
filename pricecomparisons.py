from botapi import apiCalls
import operator

commonCurrencies = []
commonCurrenciesAndExchanges = []
finalDatum = []
finalPrices = {}
arbOpportunities = []
triangleArbOpportunities = {}
finalArbOpportunities = []

class PriceComparisons(object):
    def findCommonCurrencies(self, bittrexNormCurrencies, poloniexNormCurrencies, hitbtcNormCurrencies):
        global commonCurrencies
        global commonCurrenciesAndExchanges
        currency = 0
        for bittrexCurrency in bittrexNormCurrencies:
            exchangesAvailableForCurrency = []
            exchanges = {}
            currency = bittrexCurrency[0]
            if currency in commonCurrencies:
                continue
            else:
                commonCurrencies.append(currency)
            for poloniexCurrency in poloniexNormCurrencies:
                if currency == poloniexCurrency[0]:
                    exchangesAvailableForCurrency.append('poloniex')
            for hitbtcCurrency in hitbtcNormCurrencies:
                if currency == hitbtcCurrency[0]:
                    exchangesAvailableForCurrency.append('hitbtc')
            exchangesAvailableForCurrency.append('bittrex')
            exchanges['exchanges'] = exchangesAvailableForCurrency
            exchanges['currency'] = currency
            commonCurrenciesAndExchanges.append(exchanges)

        for poloniexCurrency in poloniexNormCurrencies:
            exchangesAvailableForCurrency = []
            exchanges = {}
            currency = poloniexCurrency[0]
            if currency in commonCurrencies:
                continue
            else:
                commonCurrencies.append(currency)
            for bittrexCurrency in bittrexNormCurrencies:
                if currency == bittrexCurrency[0]:
                    exchangesAvailableForCurrency.append('bittrex')
            for hitbtcCurrency in hitbtcNormCurrencies:
                if currency == hitbtcCurrency[0]:
                    exchangesAvailableForCurrency.append('hitbtc')
            exchangesAvailableForCurrency.append('poloniex')
            exchanges['exchanges'] = exchangesAvailableForCurrency
            exchanges['currency'] = currency
            commonCurrenciesAndExchanges.append(exchanges)

        for hitbtcCurrency in hitbtcNormCurrencies:
            exchangesAvailableForCurrency = []
            exchanges = {}
            currency = hitbtcCurrency[0]
            if currency in commonCurrencies:
                continue
            else:
                commonCurrencies.append(currency)
            for bittrexCurrency in bittrexNormCurrencies:
                if currency == bittrexCurrency[0]:
                    exchangesAvailableForCurrency.append('bittrex')
            for poloniexCurrency in poloniexNormCurrencies:
                if currency == poloniexCurrency[0]:
                    exchangesAvailableForCurrency.append('poloniex')
            exchangesAvailableForCurrency.append('hitbtc')
            exchanges['exchanges'] = exchangesAvailableForCurrency
            exchanges['currency'] = currency
            commonCurrenciesAndExchanges.append(exchanges)

    def findTriangleArb(self, bittrexNormCurrencies, poloniexNormCurrencies, hitbtcNormCurrencies):
        allNormCurrencies = []
        for currency in bittrexNormCurrencies:
            allNormCurrencies.append(currency)
        for currency in poloniexNormCurrencies:
            allNormCurrencies.append(currency)
        for currency in hitbtcNormCurrencies:
            allNormCurrencies.append(currency)

        for currency in allNormCurrencies:
            append = []
            coin1 = currency[0]
            coin1 = coin1.split('-')
            coin1 = coin1[1]
            if coin1 in triangleArbOpportunities.keys():
                continue
            for result in allNormCurrencies:
                coin2 = result[0]
                coin2 = coin2.split('-')
                coin2 = coin2[1]
                if coin1 == coin2:
                    append.append(result)
            if len(append) > 1:
                triangleArbOpportunities[coin1] = append

    def getData(self):
        global commonCurrenciesAndExchanges
        global finalDatum
        bittrexRawData = apiCalls().getLastPrice('bittrex')
        poloniexRawData = apiCalls().getLastPrice('poloniex')
        hitbtcRawData = apiCalls().getLastPrice('hitbtc')
        for currency in commonCurrenciesAndExchanges:
            bittrexExchangeCurrency = apiCalls().NormCurrencytoExchangeCurrency('bittrex', currency['currency'])
            poloniexExchangeCurrency = apiCalls().NormCurrencytoExchangeCurrency('poloniex', currency['currency'])
            hitbtcExchangeCurrency = apiCalls().NormCurrencytoExchangeCurrency('hitbtc', currency['currency'])
            bittrexData = {}
            poloniexData = {}
            hitbtcData = {}
            Datum = {}
            if len(currency['exchanges']) > 1:
                if 'bittrex' in currency['exchanges']:
                    for result in bittrexRawData:
                        if result['MarketName'] == bittrexExchangeCurrency:
                            bittrexNormCurrency = currency['currency']
                            x = bittrexNormCurrency.split("-")
                            base = x[0]
                            coin = x[1]

                            last = result['Last']
                            ask = result['Ask']
                            bid = result['Bid']
                            if base == 'BTC':
                                volume = result['BaseVolume']
                            elif base == 'ETH':
                                for item in bittrexRawData:
                                    if item['MarketName'] == 'BTC-ETH':
                                        lastEthPrice = item['Last']
                                    if item['MarketName'] == 'USDT-BTC':
                                        lastBtcPrice = item['Last']
                                volume = result['BaseVolume']*lastEthPrice
                            elif base == 'USDT':
                                for item in bittrexRawData:
                                    if item['MarketName'] == 'USDT-BTC':
                                        lastBtcPrice = item['Last']
                                volume = result['BaseVolume']/lastBtcPrice

                            bittrexData['last'] = last
                            bittrexData['ask'] = ask
                            bittrexData['bid'] = bid
                            bittrexData['volume'] = volume
                            Datum['bittrexData'] = bittrexData
                if 'poloniex' in currency['exchanges']:
                    poloniexNormCurrency = currency['currency']
                    x = poloniexNormCurrency.split("-")
                    base = x[0]
                    coin = x[1]

                    last = poloniexRawData[poloniexExchangeCurrency]['last']
                    ask = poloniexRawData[poloniexExchangeCurrency]['lowestAsk']
                    bid = poloniexRawData[poloniexExchangeCurrency]['highestBid']
                    if base == 'USDT':
                        volume = float(poloniexRawData[poloniexExchangeCurrency]['baseVolume'])/lastBtcPrice
                    elif base == 'BTC':
                        volume = float(poloniexRawData[poloniexExchangeCurrency]['baseVolume'])
                    else:
                        volume = float(poloniexRawData[poloniexExchangeCurrency]['baseVolume'])*float(poloniexRawData['BTC_'+base]['last'])

                    poloniexData['last'] = last
                    poloniexData['ask'] = ask
                    poloniexData['bid'] = bid
                    poloniexData['volume'] = volume
                    Datum['poloniexData'] = poloniexData

                if 'hitbtc' in currency['exchanges']:
                    hitbtcNormCurrency = currency['currency']
                    x = hitbtcNormCurrency.split("-")
                    base = x[0]
                    coin = x[1]
                    try:
                        last = hitbtcRawData[hitbtcExchangeCurrency]['last']
                        ask = hitbtcRawData[hitbtcExchangeCurrency]['ask']
                        bid = hitbtcRawData[hitbtcExchangeCurrency]['bid']
                    except:
                        hitbtcExchangeCurrency = coin + base
                        last = hitbtcRawData[hitbtcExchangeCurrency]['last']
                        ask = hitbtcRawData[hitbtcExchangeCurrency]['ask']
                        bid = hitbtcRawData[hitbtcExchangeCurrency]['bid']

                    if base == 'BTC':
                        volume = hitbtcRawData[hitbtcExchangeCurrency]['volume_quote']
                    elif base == 'USDT':
                        volume = float(hitbtcRawData[hitbtcExchangeCurrency]['volume_quote'])/lastBtcPrice
                    elif base == 'ETH':
                        volume = float(hitbtcRawData[hitbtcExchangeCurrency]['volume_quote'])*lastEthPrice
                    hitbtcData['last'] = last
                    hitbtcData['ask'] = ask
                    hitbtcData['bid'] = bid
                    hitbtcData['volume'] = volume
                    Datum['hitbtcData'] = hitbtcData
                Datum['currency'] = currency['currency']
                finalDatum.append(Datum)

    def comparePrices(self):
        global finalDatum
        global finalPrices
        global arbOpportunities
        global finalArbOpportunities
        for currency in commonCurrenciesAndExchanges:
            pricesForCurrency = {}
            if len(currency['exchanges']) > 1:
                for data in finalDatum:
                    if data['currency'] == currency['currency']:
                        if 'bittrex' in currency['exchanges']:
                            bittrexLastPrice = data['bittrexData']['last']
                            pricesForCurrency['bittrex'] = bittrexLastPrice
                        if 'poloniex' in currency['exchanges']:
                            poloniexLastPrice = data['poloniexData']['last']
                            pricesForCurrency['poloniex'] = poloniexLastPrice
                        if 'hitbtc' in currency['exchanges']:
                            hitbtcLastPrice = data['hitbtcData']['last']
                            pricesForCurrency['hitbtc'] = hitbtcLastPrice

                maxKey = max(pricesForCurrency, key=lambda k: pricesForCurrency[k])
                maxValue = float(max(pricesForCurrency.values()))

                minKey = min(pricesForCurrency, key=lambda k: pricesForCurrency[k])
                minValue = float(min(pricesForCurrency.values()))
                finalPrices[currency['currency']] = pricesForCurrency

                if ((maxValue-minValue)/minValue) > 0.01 and ((maxValue-minValue)/minValue) < 0.1:
                    append = {}
                    append[currency['currency']] = pricesForCurrency
                    arbOpportunities.append(append)

        for opportunity in arbOpportunities:
            currency = opportunity.keys()[0]
            maxKey = max(opportunity[currency], key=lambda k: opportunity[currency][k])
            maxValue = float(max(opportunity[currency].values()))
            x = currency.split('-')
            coin = x[1]

            minKey = min(opportunity[currency], key=lambda k: opportunity[currency][k])
            minValue = float(min(opportunity[currency].values()))
            for data in finalDatum:
                if data['currency'] == opportunity.keys()[0]:
                    if 'bittrexData' in data:
                        bittrexVolume = data['bittrexData']['volume']
                        bittrexBid = data['bittrexData']['bid']
                        bittrexAsk = data['bittrexData']['ask']
                    if 'poloniexData' in data:
                        poloniexVolume = data['poloniexData']['volume']
                        poloniexBid = data['poloniexData']['bid']
                        poloniexAsk = data['poloniexData']['ask']
                    if 'hitbtcData' in data:
                        hitbtcVolume = data['hitbtcData']['volume']
                        hitbtcBid = data['hitbtcData']['bid']
                        hitbtcAsk = data['hitbtcData']['ask']
            if minKey == 'bittrex':
                minVolume = bittrexVolume
            if minKey == 'poloniex':
                minVolume = poloniexVolume
            if minKey == 'hitbtc':
                minVolume = hitbtcVolume

            if maxKey == 'bittrex':
                maxVolume = bittrexVolume
            if maxKey == 'poloniex':
                maxVolume = poloniexVolume
            if maxKey == 'hitbtc':
                maxVolume = hitbtcVolume

            #Here are the conditions for making an arb trade
            if float(minVolume) > 1 and float(maxVolume) > 1 and coin != 'XRP':
                print currency
                print minKey+"("+str(minVolume)+"VOL)"+" => "+maxKey+"("+str(maxVolume)+"VOL)"
                print "Profit Potential: " + str(((maxValue-minValue)/minValue)*100) + "\n"
                finalArbOpportunities.append(opportunity)
