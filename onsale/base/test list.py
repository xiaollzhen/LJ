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

firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.stylesheet', 2)
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
firefox_profile.set_preference('browser.migration.version', 9001)
driver = webdriver.Firefox(firefox_profile)
driver.set_page_load_timeout(10)

# 全局变量
fileName = '/Users/lixiao24/PycharmProjects/untitled/now/onsale.xlsx'
flag = True


def getUrl(data, link):
    global flag
    driver.get(link)
    if flag:
        driver.refresh()
        flag = False
    focus = driver.find_element_by_class_name('btnContainer ').find_element_by_id('favCount').text
    show = driver.find_element_by_class_name('btnContainer ').find_element_by_id('cartCount').text
    data.append(focus)
    data.append(show)

    overview = driver.find_element_by_class_name('overview')
    total = overview.find_element_by_class_name('total').text
    unit = overview.find_element_by_class_name('unitPriceValue').text
    community = overview.find_element_by_class_name('aroundInfo').find_element_by_class_name('info ').text
    data.append(total)
    data.append(unit)
    data.append(community)

    mcontent = driver.find_element_by_class_name('m-content')
    baseinfo = mcontent.find_element_by_id('introduction').find_element_by_class_name('base').\
        find_element_by_class_name('content').find_elements_by_tag_name('li')
    for i in baseinfo:
        i= i.text
        data.append(i[4:])
    for i in range(len(baseinfo), 16):
        data.append('null')

    transinfo = mcontent.find_element_by_id('introduction').find_element_by_class_name('transaction').\
        find_element_by_class_name('content').find_elements_by_tag_name('li')
    for i in transinfo:
        i=i.text
        data.append(i[4:])

    show_seven = mcontent.find_element_by_id('record').find_element_by_class_name('panel').\
        find_element_by_class_name('count').text
    data.append(show_seven)
    return data



def getRegionInfo(district, region, regionUrl):
    f = open('log.txt', 'w')
    pageIndex = 1
    error_urls = {}
    data_all = []
    flag = False
    while flag==False:
        driver.get(regionUrl + 'pg' + str(pageIndex))
        total_number = int(driver.find_element_by_class_name('total').find_element_by_tag_name('span').text)
        if total_number%30 == 0:
            total_pages = total_number / 30
        else:
            total_pages = (total_number / 30) + 1
        print str(total_number / 30)
        print str(total_number%30)
        print('current page:'+str(pageIndex)+'total pages:'+str(total_pages))
        if total_number == 0:
            f.write(district+region+'num is 0, double check')
        if total_pages > 100:
            f.write(district+region+'num exceed 100 pages, double check')

        info = driver.find_element_by_class_name('sellListContent').find_elements_by_class_name('info')
        linklist=[]
        for i in info:
            link = i.find_element_by_class_name('title').find_element_by_tag_name('a').get_attribute('href')
            linklist.append(link)

        for link in linklist:
            data = [district, region]
            try:
                subway = i.find_element_by_class_name('subway').text
            except Exception, e:
                subway = 'null'
                pass
            try:
                data = getUrl(data, link)
            except Exception, e:
                error_urls[link] = subway
            data.append(subway)
            data_all.append(data)
        pageIndex+=1
        if pageIndex > total_pages:
            flag = True

    for error_url in error_urls:
        try:
            data = getUrl(error_url)
            data.append(subway)
            data = [district, region].append(data)
            data_all.append(data)
        except:
            f.write(district+region+'error occured!!!!!!!!!!!!!\n')
            break
    f.close()
    return data_all

    #     for list in list:
    #         data = get(district, region, list)
    #         df.append(data)
    # df.to_csv


def getRegions(district):
    # excel = pd.read_excel('onsale.xlsx', '工作表1', index_col=0)
    # excel.to_csv('onsale.csv', encoding='UTF-8')
    df = pd.read_csv('onsale.csv', encoding='UTF-8')
    df.drop(df.loc[df['district'] != district].index, inplace=True)
    df = df['url'].groupby(df['region']).max()
    return df




if __name__ =="__main__":
    districts = ['平谷']

    for district in districts:
        regions = getRegions(district)
        regionList = regions.index.tolist()
        for region in regionList:
            regionUrl = regions[region]
            print district, region
            data_all = getRegionInfo(district, region, regionUrl)

            df = pd.DataFrame(data_all, columns=['城区', '区域', '关注', '带看', '挂牌价', '单价', '小区','房屋户型',
                                                 '所在楼层', '建筑面积', '户型结构', '套内面积', '建筑类型',
                                                 '房屋朝向', '建筑结构', '装修情况', '梯户比例','供暖方式','配备电梯',
                                                 '产权年限','用水类型', '用电类型', '燃气价格','挂牌时间', '交易属性',
                                                 '上次交易','房屋用途','房屋年限',
                                                 '产权所属','抵押信心','房本备件','近七天带看','地铁'])
            df.to_csv(district+region+'.csv', encoding='UTF-8', index=False)



    # data=[]
    # getUrl(data, 'https://bj.lianjia.com/ershoufang/101102025949.html')




















