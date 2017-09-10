# -*- coding: utf-8 -*-

import urllib2
import urllib
import hashlib
import json
import time
import pandas as pd
import numpy as np
import demjson

# def convert():
#     data_xls = pd.read_excel('changping.xlsx', 'Sheet1', index_col=None)
#     data_xls.to_csv('changping.csv', encoding='utf-8', index=False)



def commute(origin, destination):
    # key = '9c833dc6c982f91b71a3165320ee9cff'
    # strategy = '0'
    # date = '2017-9-4'
    # time = '07:45'
    dt = "2017-09-04 07:45:00"

    # 转换成时间数组
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = time.mktime(timeArray)

    # 以 GET 请求为例
    uri = '/direction/v1?'
    queryStr = '&origin='+origin+'&destination='+destination+'&origin_region=' \
                   '北京&destination_region=北京&output=json&timestamp='+str(timestamp)+'&ak=qHEZ9Wz9N0kv59q6CzruYD4AvuViBjoo'
    # 对queryStr进行转码，safe内的保留字符不转换
    paramsStr = urllib.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")

    # 在最后直接追加上yoursk
    wholeStr = uri + paramsStr + 'ALtPGfIqLNr556dQQlksND1KMdQnSz7E'
    tempStr = urllib.quote_plus(wholeStr);
    # md5计算出的sn值7de5a22212ffaa9e326444c75a58f9a0
    snStr = hashlib.md5(tempStr).hexdigest()
    # 最终合法请求url是http://api.map.baidu.com/geocoder/v2/?address=%E7%99%BE%E5%BA%A6%E5%A4%A7%E5%8E%A6&output=json&ak=yourAK&sn=7de5a22212ffaa9e326444c75a58f9a0
    html_transit = 'http://api.map.baidu.com' + uri + paramsStr + '&sn=' + snStr


    # html_transit = 'http://api.map.baidu.com/direction/v1?mode=driving' \
    #                '&origin='+origin+'&destination='+destination+'&origin_region=' \
    #                '北京&destination_region=北京&output=json&ak=Ai4dq15AVmqGmYvWiONavTE4rPsRQo3n'
    response = urllib2.urlopen(html_transit)
    hjson = json.loads(response.read())

    # aaa =json.dumps(hjson, sort_keys=True, indent=2)  # 排序并且缩进两个字符输出
    # print aaa.decode('"unicode-escape')
    # f = open("test_log.txt", 'a')
    # f.write(aaa)
    # f.close()
    #
    # # print aaa
    #
    #
    # try:
    #     commute_time = float(hjson['route']['transits'][0]['duration'])/60
    # except Exception, e:
    #     print e
    #     commute_time = -1
    #     return commute_time

    return hjson



def gotowork(origin):
    # start_time = time.time()
    start_time = 1504518657.77
    df = pd.read_csv('/Users/lixiao24/PycharmProjects/untitled/maps/TEST/xierqi.csv')
    length = len(df[0:])
    i = 0
    f_result = open('/Users/lixiao24/PycharmProjects/untitled/maps/TEST/00.txt', 'w')

    f_result.write('小区名,节点经度,节点纬度,时间戳\n')


    while (i < length):
        try:
            destination = str(df.iloc[i, 2]) + ',' + str(df.iloc[i, 1])
            neigbor = df.iloc[i, 0]
            commute_time = commute(origin, destination)
            data1 = get_data1(commute_time)
            path_num = data1['num']
            point_time = start_time
            for m in range(path_num):
                points = get_data2(commute_time, m)
                point_num = len(points)
                # 计算出以i为起点，j为终点的路径中，每个节点之间的平均时间
                for point in points:
                    time_per = point['duration'] / point_num
                    point_time = point_time + time_per
                    # 算出每个节点的时间点
                    point_time2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(point_time))
                    # 写入数据
                    f_result.writelines([
                        neigbor, ',',
                        str(point['lng']), ',',
                        str(point['lat']), ',',
                        point_time2, '\n'
                    ])
            i += 1
        except Exception,e:
            print str(df.iloc[i, 0])
            i +=1

    f_result.close()



def get_data1(js):
    """
    创建路径距离/时间获取函数
    输出一个字典，结果包括该条路径的总距离、总时间以及路段数量
    """
    result_ = js['result']
    routes_ = result_['routes'][0]
    distance_ = routes_['distance']
    duration_ = routes_['duration']
    num = len(routes_['steps'])
    data_dic = dict([['dis', distance_], ['time', duration_], ['num', num]])
    # print(data_dic)
    return data_dic


def get_data2(js, n):
    """
    创建路径节点获取函数
    输出为一个字典列表，包括每一个节点的经度纬度
    """
    result_ = js['result']
    routes_ = result_['routes'][0]
    steps_ = routes_['steps']
    step = steps_[n]
    duration = step['duration']
    path_points = step['path'].split(';')
    point_lst = []
    for point in path_points[::5]:
        lng = point.split(',')[0]
        lat = point.split(',')[1]
        point_geo = dict([['lng', lng], ['lat', lat],['duration',duration]])
        point_lst.append(point_geo)
    # print(point_lst)
    return (point_lst)




if __name__ =="__main__":
    # 西二旗坐标
    origin = '116.30603,40.05296'
    destination = '40.05296,116.30603'
    gotowork(destination)
