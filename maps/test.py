# -*- coding: utf-8 -*-

import urllib2
import json
import time
import pandas as pd
import demjson

def convert():
    data_xls = pd.read_excel('changping.xlsx', 'Sheet1', index_col=None)
    data_xls.to_csv('changping.csv', encoding='utf-8', index=False)



def commute(origin, destination):
    key = '9c833dc6c982f91b71a3165320ee9cff'
    strategy = '0'
    date = '2017-9-4'
    time = '07:45'

    html_transit = 'http://restapi.amap.com/v3/direction/transit/integrated?' \
                   'origin=' + origin + '&destination=' + destination + '&strategy=' + strategy + \
                   '&date=' + date + '&time=' + time + '&city=010' + '&key=' + key

    response = urllib2.urlopen(html_transit)
    hjson = json.loads(response.read())

    aaa =json.dumps(hjson, sort_keys=True, indent=2)  # 排序并且缩进两个字符输出
    print aaa.decode('"unicode-escape')
    f = open("test_log.txt", 'a')
    f.write(aaa)
    f.close()

    # print aaa


    try:
        commute_time = float(hjson['route']['transits'][0]['duration'])/60
    except Exception, e:
        print e
        commute_time = -1
        return commute_time

    return commute_time



def gotowork(destination):
    df = pd.read_csv('changping.csv')
    length = 1
    i = 0
    while(i < length):

        print 'loop：'+str(i)
        origin = str(df.iloc[i, 1]) + ',' + str(df.iloc[i, 2])
        commute_time = commute(origin, destination)
        df.set_value(i, '上班时间', commute_time)
        i += 1
        time.sleep(0.005)

    # df.to_csv('changping.csv', encoding='UTF-8')








if __name__ =="__main__":
    # 西二旗坐标
    origin = '116.30603,40.05296'
    destination = '116.30603,40.05296'
    gotowork(destination)
