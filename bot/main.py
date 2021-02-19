import logging
from decouple import config
import backtrader as bt

import time
import datetime as dt
from core.backtest.backtest import Backtest
from core.modes.modes import Modes


def main():
    print("--BOT UP--")
    mode = config('MODE')
    
    if Modes.DEVELOPMENT.value == "DEVELOPMENT":
        print("Dev Mode")
        Backtest()
        
    elif Modes.TRADE.value == "TRADE":
        print("Trading Mode")
    
    else:
        print("Mode Invalid")
    

if __name__ == "__main__":
    try:
        main()
        
    except KeyboardInterrupt:
        print("finished.")
        time = dt.datetime.now().strftime("%d-%m-%y %H:%M")
        
    except Exception as err:
        print("Finished with error: ", err)
        time = dt.datetime.now().strftime("%d-%m-%y %H:%M")
        raise
