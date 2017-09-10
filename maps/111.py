# -*- coding: utf-8 -*-

import urllib2
import json
import time
import pandas as pd

def convert():
    data_xls = pd.read_excel('changping.xlsx', 'Sheet1', index_col=None)
    data_xls.to_csv('changping.csv', encoding='utf-8', index=False)



def commute(origin, destination):
    key = '9c833dc6c982f91b71a3165320ee9cff'
    strategy = '0'
    date = '2017-8-19'
    time = '18:00'

    html_transit = 'http://restapi.amap.com/v3/direction/transit/integrated?' \
                   'origin=' + origin + '&destination=' + destination + '&strategy=' + strategy + \
                   '&date=' + date + '&time=' + time + '&city=010' + '&key=' + key

    response = urllib2.urlopen(html_transit)
    hjson = json.loads(response.read())
    try:
        commute_time = float(hjson['route']['transits'][0]['duration'])/60
    except Exception, e:
        print e
        commute_time = -1
        return commute_time

    return commute_time


# def commute_driving(origin, destination):
#     key = '9c833dc6c982f91b71a3165320ee9cff'
#     strategy = '1'
#     html_transit = 'http://restapi.amap.com/v3/direction/driving?' \
#                    'origin=' + origin + '&destination=' + destination + '&strategy=' + strategy + '&key=' + key
#
#     response = urllib2.urlopen(html_transit)
#     hjson = json.loads(response.read())
#     try:
#         commute_time = float(hjson['route']['paths'][0]['duration']) / 60
#     except Exception, e:
#         print e
#         commute_time = -1
#         return commute_time
#
#     return commute_time


def gotowork(destination):
    df = pd.read_csv('changping.csv')
    length = len(df[0:])
    i = 0
    while(i < length):

        print 'loop：'+str(i)
        origin = str(df.iloc[i, 1]) + ',' + str(df.iloc[i, 2])
        commute_time = commute(origin, destination)
        df.set_value(i, '上班时间', commute_time)
        i += 1
        time.sleep(0.005)

    df.to_csv('changping.csv', encoding='UTF-8')

def backfromwork(origin):
    df = pd.read_csv('changping.csv')
    df.drop([df.columns[0]], axis=1, inplace=True)
    length = len(df[0:])
    i = 0
    while(i < length):

        print 'loop：'+str(i)
        destination = str(df.iloc[i, 1]) + ',' + str(df.iloc[i, 2])
        commute_time = commute(origin, destination)
        df.set_value(i, '下班时间', commute_time)
        i += 1
        # time.sleep(0.005)

    df.to_csv('changping.csv', encoding='UTF-8', index=False)

# def drivingfromwork(origin):
#     df = pd.read_csv('jingwei8.csv', encoding='GBK')
#     length = len(df[0:])
#     i = 0
#     while (i < length):
#         print 'loop：' + str(i)
#         destination = str(df.iloc[i, 1]) + ',' + str(df.iloc[i, 2])
#         commute_time = commute_driving(origin, destination)
#         df.set_value(i, '下班时间', commute_time)
#         i += 1
#         # time.sleep(0.005)
#
#     df.to_csv('driving8.csv', encoding='UTF-8', index=False)







if __name__ =="__main__":
    # 西二旗坐标
    origin = '116.30603,40.05296'
    destination = '116.30603,40.05296'
    # gotowork(destination)
    backfromwork(origin)
    # drivingfromwork(origin)
    # convert()