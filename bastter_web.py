# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 10:35:33 2021

@author: Daniel Souza - PC
"""

from bs4 import BeautifulSoup
import requests
import json
import keyring

company = 'MSFT'

class BastterWeb():
    
    USERNAME_ = keyring.get_password("bastter", "username") # Your username here
    PASSWORD_ = keyring.get_password("bastter", "password") # Your password here
    URL_LOGIN = 'https://bastter.com/Mercado/WebServices/WsUsuario.asmx/Login'
    URL_STOCKS_LIST = 'https://bastter.com/mercado/webservices/WS_Company.asmx/ListRating'
    
    def __init__(self):
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'content-type': 'application/json; charset=UTF-8',
            }
        self.session = requests.Session()
        self.response = None
        self.stocks_list = [] # TODO: Import data locally
        self.company_indexes = {} # TODO: Import data locally
    
    
    def login(self, username = None, password = None):        
        data = {}
        
        # Set username if provided
        if username == None:
            data["login"] = self.USERNAME_
        else:
            data['login'] = username
        
        # Set password if provided
        if password == None:
            data["password"] = self.PASSWORD_
        else:
            data["password"] = password
        
        # Login to website
        self.response = self.session.post(self.URL_LOGIN, headers=self.header, data=str(data))
        
        # Return response code
        return self.response.status_code
    
    
    def update_stocks_list(self):
        # Data to post request
        data = '{"tamanho":10000,"data":null}'

        # Send post request
        self.response = self.session.post(self.URL_STOCKS_LIST, headers=self.header, data=data)
        
        if self.response.status_code == 200:
            # Read response JSON
            stocks_list = json.loads(self.response.json()['d'])["Items"]
            # Create stocks index dictionary
            company_indexes ={}
        
            # Populate dictionary
            for num, item in enumerate(stocks_list):
                company_indexes[item['Symbol']] = num
            
            # TODO: Eventually append to existing data
            self.stocks_list = stocks_list
            self.company_indexes = company_indexes
            
        return self.response.status_code
            
    
    
    def get_stock_data(self, stock):
        try:
            stock_index = self.company_indexes[stock]
            stock_data = self.stocks_list[stock_index]
        except KeyError:
            raise KeyError("Unknown Company: '" + stock + "'")
            
        print(stock_data)
        

bs = BastterAccess()
print(bs.login())
print(bs.update_stocks_list())
bs.get_stock_data("MSFT")

'''
###################################################################################
response = session.get('https://bastter.com/mercado/stock/'+company, headers=headers)

print("Second: {}".format(response.status_code))

sector_id = response.text.split('"Sector":{"SectorID":')[1].split(',')[0]

###################################################################################
data = '{"companyID":' + str(comp_id) + \
    ',"symbol":"CMD","sectorID":' + sector_id + \
    ',"lastBalance":"3Q21","ordemDesc":true,"datasetGraficoResultado":true,"isAnualResumo":true,"isReit":false}'


response = session.post('https://bastter.com/mercado/webservices/WS_Company.asmx/GetQuadro', headers=headers, data=data)

print("Third: {}".format(response.status_code))
if response.status_code == 200:
    d2 = json.loads(response.json()['d'])
    
######################
'''