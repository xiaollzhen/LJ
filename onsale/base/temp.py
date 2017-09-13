# -*- coding: utf-8 -*-

from selenium import webdriver

import xlwt
import xlrd
import json
import sys
import time
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')




if __name__ =="__main__":

    excel = pd.read_excel('onsale.xlsx', '工作表1', index_col=0)
    excel.to_csv('onsale.csv', encoding='UTF-8')
    df = pd.read_csv('onsale.csv')
    data_all = []
    i = 0
    while i < len(df.index):
        fileName = str(df['district'][i])+str(df['region'][i])+'.csv'
        data = pd.read_csv(fileName)
        data_all.append(data)
        i+=1
    print i
    # result = pd.concat(data_all)
    # result.to_csv('test.csv')



















