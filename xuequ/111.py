# -*- coding: utf-8 -*-



import xlwt
import xlrd
import json
import sys
import time
import pandas as pd
reload(sys)
sys.setdefaultencoding('utf-8')

target = pd.read_csv('海淀.csv', sep=',')
origin = pd.read_csv('海淀区.csv', sep=',')

originlist = origin['划片小区']
targetlist = target['小区名']

print originlist
print targetlist