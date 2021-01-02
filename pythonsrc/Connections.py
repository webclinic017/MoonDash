
## Library Imports ---------------------------------------------
from decouple import config
import bitmex
## -------------------------------------------------------------

class Connections:
    
    def getBitmexConnection():
        """Return Bitmex Connection Client

        Returns:
            [type]: Bitmex Client
        """
        bitmex_api_key = config('BITMEX_API_KEY')  # Enter your own API-key here
        bitmex_api_secret = config('BITMEX_SECRET_KEY')  # Enter your own API-secret here
        client = bitmex.bitmex(test = False, api_key=bitmex_api_key, api_secret=bitmex_api_secret)
        
        return client