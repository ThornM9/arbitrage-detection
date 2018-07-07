# arbitrage-detection
Python cryptocurrency arbitrage detection written by Thornton Mills

Accesses open crypto exchange APIs, finds common markets and grabs prices then finds arbitrage opportunities. Modular implementation so more exchanges can be added later.

Written in python 2.7. Detects arbitrage opportunities between hitbtc, bittrex and poloniex. Transactions.py is a redundant file, just in case I decide to work on automatically. Most necessary API functions for executing arbitrage automatically are already implemented in botapi.py, you'd just need to input your API keys as strings.

I probably won't be working on this any further, but if anyone comes up with a good update I'm happy to merge it to the Github repo.
