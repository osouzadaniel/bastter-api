# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 10:35:33 2021

@author: Daniel Souza - PC
"""

from bs4 import BeautifulSoup
import requests
import json
import keyring


class BastterWeb():
    """
    A class used to encapsulate and access data from Bastter.com web site
    
    ...
    
    Attributes
    ----------
    TODO: fill atributes
    

    Methods
    -------
    login(username = None, password = None)
        Login to Bastter.com
        
    is_authenticated()
        Checks if authentication was successfull
        
    update_stocks_list()
        Get the list of US Stocks from Bastter.com
        
    get_stock_data(stock)
        Get data retrieved from a specific stock
    """
    
    __USERNAME = keyring.get_password("bastter", "username") # Your username here
    __PASSWORD = keyring.get_password("bastter", "password") # Your password here
    URL_LOGIN = 'https://bastter.com/Mercado/WebServices/WsUsuario.asmx/Login'
    URL_VERIFY_AUTH = 'https://bastter.com/mercado/webservices/WsUsuario.asmx/IsAuthenticated'
    URL_STOCKS_SEARCH = 'https://bastter.com/mercado/webservices/WS_Company.asmx/Search'
    URL_REITS_SEARCH = 'https://bastter.com/mercado/webservices/WS_Company.asmx/SearchREIT'
    URL_ACOES_SEARCH = 'https://bastter.com/mercado/webservices/WS_Empresa.asmx/Pesquisar'
    URL_FIIS_SEARCH = 'https://bastter.com/mercado/webservices/WS_FII.asmx/Pesquisar'
    URL_STATUS_OK = 200
    
    STOCKS_INDEX = 0
    REITS_INDEX = 1
    ACOES_INDEX = 2
    FIIS_INDEX = 3
    
    AMOUNT_ASSETS = 4
    
    def __init__(self):
        self.__headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'content-type': 'application/json; charset=UTF-8',
            }
        self.__session = requests.Session()
        self.__response = None
        self.__stocks_list = [[] * self.AMOUNT_ASSETS] # TODO: Import data locally
        self.__company_indexes = {self.STOCKS_INDEX : {},
                                  self.REITS_INDEX : {},
                                  self.ACOES_INDEX : {},
                                  self.FIIS_INDEX : {}}  # TODO: Import data locally
    
    
    def login(self, username = None, password = None):        
        data = {}
        
        # Set username if provided
        if username == None:
            data["login"] = self.__USERNAME
        else:
            data['login'] = username
        
        # Set password if provided
        if password == None:
            data["password"] = self.__PASSWORD
        else:
            data["password"] = password
        
        # Login to website
        self.__response = self.__session.post(self.URL_LOGIN, headers=self.__headers, data=str(data))
        
        return self.is_authenticated()

        
    
    def is_authenticated(self):
        # Check authentication
        data = '{}'
        self.__response = self.__session.post(self.URL_VERIFY_AUTH, headers=self.__headers, data=data)
        
        if self.__response.status_code == self.URL_STATUS_OK:
            status = json.loads(self.__response.json()['d'])["IsAuthenticated"]
            
            return status
        # Return auth error
        return False
    
    
    def update_stocks_list(self):

        # Send post request
        stocks_list = self.search_stocks()
        
        if self.__response.status_code == self.URL_STATUS_OK:
            # Create stocks index dictionary
            company_indexes = {}
        
            # Populate dictionary
            for num, item in enumerate(stocks_list):
                company_indexes[item['Symbol']] = num
            
            # TODO: Eventually append to existing data
            self.__stocks_list[self.STOCKS_INDEX] = stocks_list
            self.__company_indexes[self.STOCKS_INDEX] = company_indexes
            
            if len(stocks_list) > 0:
                return True
            else:
                return False
            
        return False
            
    
    def get_stock_data(self, stock):
        try:
            stock_index = self.__company_indexes[self.STOCKS_INDEX][stock]
            stock_data = self.__stocks_list[self.STOCKS_INDEX][stock_index]
        except KeyError:
            raise KeyError("Unknown Company: '" + stock + "'")
            
        return stock_data
    
    def search_stocks(self, search = '[ALL]'):
        return self.__search_us(self.URL_STOCKS_SEARCH, search)
    
    def search_reits(self, search = '[ALL]'):
        return self.__search_us(self.URL_REITS_SEARCH, search)
    
    def __search_us(self, url, search):
        data = '{"text":"' + search + '","page":1,"pageSize":30000,"countryID":0}'


        self.__response = self.__session.post(url, headers=self.__headers, data=data)
        if self.__response.status_code == self.URL_STATUS_OK:
            return json.loads(self.__response.json()['d'])
        else:
            return []
        
    # TODO: Standardize return dict keys
    
    def search_acoes(self, search = ''):
        return self.__search_br(self.URL_ACOES_SEARCH, search)
    
    def search_fiis(self, search = ''):
        return self.__search_br(self.URL_FIIS_SEARCH, search, locator="Fundos")
    
    def __search_br(self, url, search, locator = "Items"):
        data = '{"ativo":"' + search + '","pagina":0}'
        
        self.__response = self.__session.post(url, headers=self.__headers, data=data)
        if self.__response.status_code == self.URL_STATUS_OK:
            return json.loads(self.__response.json()['d'])[locator]
        else:
            return []
'''
TODO:
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