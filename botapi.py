from bittrex import Bittrex
from poloniex import poloniex
import requests
from urllib2 import urlopen
import json
import urllib
import urllib2
import time
import random
import string
import datetime
import unirest as unirest
import hmac, hashlib

bittrexConn = Bittrex('apikey','secretkey')
poloniexConn = poloniex('apikey', 'secretkey')

liquiCurrencies = []
liquiNormCurrencies = []
bittrexCurrencies = []
bittrexNormCurrencies = []
poloniexCurrencies = []
poloniexNormCurrencies = []
hitbtcCurrencies = []
hitbtcNormCurrencies = []
bitfinexCurrencies = []
bitfinexNormCurrencies = []

### HIT BTC ###
hitbtcApiKey = 'apikey'
hitbtcSecretKey = 'secretkey'
### HIT BTC ###

### POLONIEX ADDRESSES ###
req={}

APIKey = "apikey"
Secret = "secretkey"

command="returnDepositAddresses"

req['command'] = command

req['nonce'] = int(time.time()*1000)
post_data = urllib.urlencode(req)

sign = hmac.new(Secret, post_data, hashlib.sha512).hexdigest()
#print sign
headers = {
    'Sign': sign,
    'Key': APIKey
}

ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', post_data, headers))
poloniexAddresses = json.loads(ret.read())

### POLONIEX ADDRESSES ###

class apiCalls(object):
    def ExchangeCurrencytoNormCurrency(self, exchange, exchangeCurrency):
        if exchange == "liqui":
            x = exchangeCurrency.split("_")
            base = x[1]
            coin = x[0]
            normCurrency = base + "-" + coin
            append = [normCurrency, exchange]
            liquiNormCurrencies.append(append)

        if exchange == "bittrex":
            normCurrency = exchangeCurrency
            append = [normCurrency, exchange]
            bittrexNormCurrencies.append(append)

        if exchange == "poloniex":
            x = exchangeCurrency.split("_")
            base = x[0]
            coin = x[1]
            normCurrency = base + "-" + coin
            append = [normCurrency, exchange]
            poloniexNormCurrencies.append(append)

        if exchange == "hitbtc":
            normCurrency = exchangeCurrency
            append = [normCurrency, exchange]
            hitbtcNormCurrencies.append(append)

    def NormCurrencytoExchangeCurrency(self, exchange, normCurrency):
        if exchange == "liqui":
            x = normCurrency.split("-")
            base = x[0]
            coin = x[1]
            exchangeCurrency = coin + "_" + base
            return exchangeCurrency
        if exchange == "bittrex":
            exchangeCurrency = normCurrency
            return exchangeCurrency
        if exchange == "poloniex":
            x = normCurrency.split("-")
            base = x[0]
            coin = x[1]
            exchangeCurrency = base + "_" + coin
            return exchangeCurrency
        if exchange == "hitbtc":
            x = normCurrency.split("-")
            base = x[0]
            coin = x[1]
            if base == 'USDT':
                base = 'USD'
            if coin == 'USDT':
                coin = 'USD'
            exchangeCurrency = coin + base
            return exchangeCurrency

    def getMarkets(self, exchange):
        global liquiCurrencies
        global liquiNormCurrencies
        global bittrexCurrencies
        global bittrexNormCurrencies
        global poloniexCurrencies
        global poloniexNormCurrencies

        if exchange == "liqui":
            response = requests.get('https://api.liqui.io/api/3/info')
            response = json.loads(response.text)
            response = response['pairs']
            response = response.items()

            i = len(response)
            j = 0
            for j in range(0,i):
                liquiCurrencies.append(response[j][0])
                j = j + 1


            for currency in liquiCurrencies:
                self.ExchangeCurrencytoNormCurrency("liqui", currency)

        if exchange == "bittrex":
            response = requests.get('https://bittrex.com/api/v1.1/public/getmarkets')
            response = json.loads(response.text)
            response = response['result']

            i = len(response)
            j = 0
            for j in range(0,i):
                base = response[j]['BaseCurrency']
                coin = response[j]['MarketCurrency']
                bittrexCurrencies.append(base + "-" + coin)
                j = j + 1

            for currency in bittrexCurrencies:
                self.ExchangeCurrencytoNormCurrency("bittrex", currency)

        if exchange == "poloniex":
            response = requests.get('https://poloniex.com/public?command=returnTicker')
            response = json.loads(response.text)
            response = response.items()

            i = len(response)
            j = 0
            for j in range(0,i):
                poloniexCurrencies.append(response[j][0])
                j = j + 1

            for currency in poloniexCurrencies:
                self.ExchangeCurrencytoNormCurrency("poloniex", currency)

        if exchange == "hitbtc":
            response = requests.get('http://api.hitbtc.com/api/1/public/symbols')
            response = json.loads(response.text)
            response = response['symbols']

            i = len(response)
            j = 0
            for j in range(0,i):
                base = response[j]['currency']
                coin = response[j]['commodity']
                if base == 'USD':
                    base = 'USDT'
                hitbtcCurrencies.append(base + "-" + coin)
                j = j + 1

            for currency in hitbtcCurrencies:
                self.ExchangeCurrencytoNormCurrency("hitbtc", currency)

    def getLastPrice(self, exchange):
        if exchange == "bittrex":
            response = requests.get('https://bittrex.com/api/v1.1/public/getmarketsummaries')
            response = json.loads(response.text)
            return response['result']
        if exchange == "poloniex":
            response = requests.get('https://poloniex.com/public?command=returnTicker')
            response = json.loads(response.text)
            return response
        if exchange == 'hitbtc':
            response = requests.get('http://api.hitbtc.com/api/1/public/ticker')
            response = json.loads(response.text)
            return response

    def getAddress(self, exchange, currency):
        global bittrexConn
        global poloniexConn
        if exchange == 'bittrex':
            while True:
                address = bittrexConn.get_deposit_address(currency)
                if address['message'] == 'ADDRESS_GENERATING':
                    print 'ADDRESS GENERATING'
                    continue
                else:
                    address = address['result']['Address']
                    return address
        if exchange == 'poloniex':
            print poloniexAddresses
            if currency in poloniexAddresses:
                address = poloniexAddresses[currency]
            else:
                print 'ADDRESS GENERATING'
                address = self.generatePoloniexAddress(currency)
            return address

        if exchange == 'hitbtc':
            nonce = str(int(time.mktime(datetime.datetime.now().timetuple()) * 1000 + datetime.datetime.now().microsecond / 1000))
            path = "/api/1/payment/address/" + currency + "?apikey=" + hitbtcApiKey + "&nonce=" + nonce
            signature = hmac.new(hitbtcSecretKey, path, hashlib.sha512).hexdigest()
            result = unirest.get("http://api.hitbtc.com" + path, headers={"Api-Signature": signature})

            address = result.body['address']
            return address
    def generatePoloniexAddress(self, currency):
        req={}

        command="generateNewAddress"

        req['command'] = command
        req['nonce'] = int(time.time()*1000)
        req['currency'] = currency
        post_data = urllib.urlencode(req)

        sign = hmac.new(Secret, post_data, hashlib.sha512).hexdigest()
        headers = {
            'Sign': sign,
            'Key': APIKey
        }

        ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', post_data, headers))
        jsonRet = json.loads(ret.read())
        address = jsonRet['response']
        return address
    def withdraw(self, originalExchange, destinationExchange, currency, amount):
        address = self.getAddress(destinationExchange, currency)
        if originalExchange == 'bittrex':
            withdraw = bittrexConn.withdraw(currency, amount, address)
            if withdraw['success'] == 'true':
                print 'success!'
            else:
                print 'failure!'
        if originalExchange == 'poloniex':
            poloniexConn.withdraw(currency, amount, address)
        if originalExchange == 'hitbtc':
            nonce = str(int(time.mktime(datetime.datetime.now().timetuple()) * 1000 + datetime.datetime.now().microsecond / 1000))
            path = "/api/1/payment/payout?apikey=" + key + "&nonce=" + nonce
            command = "amount=" + amount + "&currency_code=" + currency + "&address=" + address
            signature = hmac.new(secret, path + command, hashlib.sha512).hexdigest()
            result = unirest.post("http://api.hitbtc.com" + path, headers={"Api-Signature": signature}, params=command)

    def getBalance(self, exchange, currency):
        if exchange == 'bittrex':
            bittrexBalances = bittrexConn.get_balances()
            for result in bittrexBalances['result']:
                if result['Currency'] == currency:
                    balance = result['Available']
        if exchange == 'poloniex':
            poloniexBalances = poloniexConn.returnBalances()
            for key in poloniexBalances.keys():
                if key == currency:
                    balance = poloniexBalances[key]
        if exchange == 'hitbtc':
            var = 0
        return balance
    def buy(self, exchange, currency, amount, rate):
        if exchange == 'bittrex':
            var = 0
        if exchange == 'poloniex':
            var = 0
        if exchange == 'hitbtc':
            var = 0
    def sell(self, exchange, currency, amount, rate):
        if exchange == 'bittrex':
            var = 0
        if exchange == 'poloniex':
            var = 0
        if exchange == 'hitbtc':
            var = 0
    def returnCurrencies(self, exchange):
        if exchange == "liqui":
            return liquiNormCurrencies
        if exchange == "bittrex":
            return bittrexNormCurrencies
        if exchange == "poloniex":
            return poloniexNormCurrencies
        if exchange == "hitbtc":
            return hitbtcNormCurrencies
