
## Library Imports ---------------------------------------------
from binance.client import Client
from decouple import config
import bitmex
import urllib3


## -------------------------------------------------------------

class Connections:
    
    def getBitmexConnection():
        """Return Bitmex Connection Client

        Returns:
            [type]: Bitmex Client
        """
        
        ### Initialize Bitmex Client
        ### A Good Resource to start using bitmex API https://medium.com/coinmonks/a-bitmex-python-tutorial-5f3cdf2491a7
        ### Bitmex Costs https://hackernoon.com/a-quick-starter-guide-to-using-leveraged-trading-at-bitmex-5383de4cb320
        
        
        bitmex_api_key = config('BITMEX_API_KEY')  # Enter your own API-key here
        bitmex_api_secret = config('BITMEX_SECRET_KEY')  # Enter your own API-secret here
        client = bitmex.bitmex(test = False, api_key=bitmex_api_key, api_secret=bitmex_api_secret)
        
        return client
    
    def getBinanceConnection():
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        BINANCE_API_KEY = config('BINANCE_API_KEY')
        BINANCE_API_SECRET_KEY = config('BINANCE_API_SECRET_KEY')
        
        client = Client(BINANCE_API_KEY, BINANCE_API_SECRET_KEY, {"verify": False, "timeout": 20})
        
        return client