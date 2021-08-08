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
print(stock_data['Symbol'] + " is the ticker of " + stock_data['Name'])

stock_data = bs.get_stock_data("DIS")
print(stock_data['Symbol'] + " is the ticker of " + stock_data['Name'])


print("------------")
search_string = 'HG'
search_result = bs.search_fiis(search_string)
print("Search FIIs with '" + search_string +"' returned {} itens: ".format(len(search_result)))
for item in search_result:
    print(item['Codigo'] + " -> " + item["Nome"])
    
print("------------")
search_string = 'PET'
search_result = bs.search_acoes(search_string)
print("Search Ações with '" + search_string +"' returned {} itens: ".format(len(search_result)))
for item in search_result:
    print(item['CodBolsa'] + " -> " + item["Nome"])
    
print("------------")
search_string = 'Alp'
search_result = bs.search_stocks(search_string)
print("Search Stocks with '" + search_string +"' returned {} itens: ".format(len(search_result)))
for item in search_result:
    print(item['Symbol'] + " -> " + item["Name"])
    
print("------------")
search_string = 'FR'
search_result = bs.search_reits(search_string)
print("Search REITs with '" + search_string +"' returned {} itens: ".format(len(search_result)))
for item in search_result:
    print(item['Symbol'] + " -> " + item["Name"])