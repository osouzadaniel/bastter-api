# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 09:59:16 2021

@author: Daniel Souza - PC
"""

import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))

from bastter_web import BastterWeb

# 
bs = BastterWeb()

# You can pass login data in this function, like:
# bs.login("your_username", "your_password")
if bs.login():
    print("Logged in to Bastter.com!")
else:
    print("Error while logging in :(")

# Get list of all stocks
if bs.update_stocks_list():
    print("Stocks updated!")
else:
    print("Error while obtaining stocks data :(")
    
stock_data = bs.get_stock_data("MSFT")
print(stock_data['Symbol'] + " is the ticker of " + stock_data['Company'])

stock_data = bs.get_stock_data("DIS")
print(stock_data['Symbol'] + " is the ticker of " + stock_data['Company'])
print(stock_data['Description'])
