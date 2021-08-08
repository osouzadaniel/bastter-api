# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 10:12:45 2021

@author: Daniel Souza - PC
"""
import sys
from pathlib import Path
import pytest

sys.path.append(str(Path('.').absolute().parent))
from bastter_web import BastterWeb

URL_SUCCESS = 200


def test_wrong_login_url():
    bs = BastterWeb()
    bs.URL_LOGIN += "a"
    resp = bs.login()
    
    assert resp == False
    
def test_wrong_update_stocks_list_url():
    bs = BastterWeb()
    bs.URL_STOCKS_LIST += "a"
    resp = bs.update_stocks_list()
    
    assert resp == False
    
def test_update_stocks_list_ok():
    bs = BastterWeb()
    resp = bs.update_stocks_list()
    
    assert resp == True

def test_proper_login():
    bs = BastterWeb()
    resp = bs.login()
    
    assert resp
    
def test_stock_data_exception():
    company = "MSFT2"
    bs = BastterWeb()
    with pytest.raises(KeyError) as e_info:
        bs.get_stock_data(company)
        
    assert e_info.value.args[0] == "Unknown Company: '" + company + "'"

if __name__ == '__main__':
    ret_code = pytest.main()