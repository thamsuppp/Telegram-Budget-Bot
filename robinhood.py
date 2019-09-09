import pandas as pd 
import numpy as np 
from datetime import datetime, timedelta
import robin_stocks

#Login to Robinhood

robin_stocks.login('','')


def get_stock_data(symbol):
    
    previous_close = float(robin_stocks.stocks.get_quotes(symbol)[0]['adjusted_previous_close'])
    current_price = float(robin_stocks.stocks.get_latest_price(symbol)[0])
    
    today_change = current_price - previous_close
    today_pct_change = today_change / previous_close * 100
    
    return '{}: {}, {} ({}%)'.format(symbol, current_price, 
                                        round(today_change, 2), round(today_pct_change, 2))

class Robinhood():

    #Constructor method
    def __init__(self):
        pass

    #Returns information about current positions
    def get_my_positions(self):
        
        my_stocks = robin_stocks.build_holdings()

        my_stocks_out = ''''''
        
        for symbol, info in my_stocks.items():
            
            previous_close = float(robin_stocks.stocks.get_quotes(symbol)[0]['adjusted_previous_close'])
            current_price = float(robin_stocks.stocks.get_latest_price(symbol)[0])
            today_change = current_price - previous_close
                
            my_stocks_out = my_stocks_out + '''{}
Equity: Today {}, Overall {} ({}%) \n'''.format(get_stock_data(symbol),
                                                            round(float(info['quantity']) * today_change, 2),
                                                            round(float(info['equity_change']), 2),
                                                            info['percent_change'])

        print(my_stocks_out)

        return my_stocks_out

    #Returns price information about any symbol
    def get_symbol(self, symbol):

        return get_stock_data(symbol)

