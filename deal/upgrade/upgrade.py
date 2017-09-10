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
#####################
# 思路是指定日期，取所有最新
####################


def getData(url):
    data = []
    driver.get(url)
    name = driver.find_element_by_class_name('house-title').find_element_by_class_name('wrapper')\
        .find_element_by_class_name('index_h1').text.split(' ')[0]
    data.append(name)
    date = driver.find_element_by_class_name('house-title'). \
        find_element_by_class_name('wrapper').find_element_by_tag_name('span')

    date = (date.text).replace('链家成交', '').replace('其他公司成交', '')
    data.append(date)
    price_total = driver.find_elements_by_class_name('dealTotalPrice')
    if len(price_total) == 0:
        data.append(' ')
    else:
        data.append(price_total[0].text)

    price = driver.find_element_by_class_name('price').find_elements_by_tag_name('b')
    if len(price) == 0:
        data.append(' ')
    else:
        data.append(price[0].text)

    process = driver.find_element_by_class_name('msg').find_elements_by_tag_name('label')
    if len(process) == 0:
        append_index = 0
        while append_index < 6:
            data.append(' ')
            append_index += 1
    else:
        for p in process:
            data.append(p.text)

    contents = driver.find_elements_by_class_name('content')
    for content in contents:
        basics = content.find_elements_by_tag_name('li')
        for i in basics:
            x = str(i.text)
            i_new = x[12:100]
            data.append(unicode(i_new, encoding='utf-8'))
    record = driver.find_element_by_class_name('record_list')
    record_price = record.find_elements_by_class_name('record_price')
    record_detail = record.find_elements_by_class_name('record_detail')
    index = 0
    while index < len(record_price):
        data.append(record_price[index].text)
        data.append(record_detail[index].text)
        index += 1
        # 把第8个数据拿出来，量化并拆成两个
    data_10_list = data[11].split(' ')
    new_data_10 = data_10_list[0]
    new_data_11 = data_10_list[1].split('共')[1].split('层')[0]
    # 插入到第九列（共多少层）
    data[11] = new_data_10
    data.insert(12, new_data_11)
    return data


def writeFile(date):
    f = open('log.txt', 'w')
    pageIndex = 1
    w = xlwt.Workbook()
    ws = w.add_sheet('test', cell_overwrite_ok=True)
    num = 1
    error_urls = []
    row0 = [u'小区名',u'成交时间', u'成交价格', u'成交单价', u'挂牌价格（万）', u'成交周期（天）', u'调价（次）', u'带看（次）', u'关注（人）', u'浏览（次）',
            u'房屋户型', u'所在楼层', u'总共层数', u'建筑面积', u'户型结构', u'套内面积', u'建筑类型', u'房屋朝向',
            u'建成年代', u'装修情况', u'建筑结构', u'供暖方式', u'梯户比例', u'产权年限', u'配备电梯', u'链家编号',
            u'交易权属', u'挂牌时间', u'房屋用途', u'房屋年限', u'房权所属', u'历史成交记录']
    for index in range(0, len(row0)):
        ws.write(0, index, row0[index])

    end = False

    while end == False:

        print('pageIndex:   ' + str(pageIndex))
        try:
            driver.get('https://bj.lianjia.com/chengjiao/xicheng/pg' + str(pageIndex))
        except Exception, e:
            print 'driver error'+str(e)
            continue
        info = driver.find_elements_by_class_name('info')
        titles = []
        for i in info:
            try:
                date_now = i.find_element_by_class_name('dealDate').text
                if date_now != '近30天内成交':
                    date_now = pd.to_datetime(date_now)
                    if date_now <= date:
                        end = True
                        break
                title = i.find_element_by_partial_link_text('平米').get_attribute("href")
                titles.append(title)
            except Exception, e:
                f.write('get titles error'+str(e))
        for url in titles:
            try:
                data = getData(url)
            except:
                error_urls.append(url)
                print('urls with warning:', error_urls)
                time.sleep(4)
                continue
            for data_index in range(0, len(data)):
                ws.write(num, data_index, json.dumps(data[data_index], ensure_ascii=False))
            num += 1
        pageIndex+=1


    for error_url in error_urls:
        try:
            data = getData(error_url)
        except:
            f.write('error occured!!!!!!!!!!!!!\n')
            f.close()
            break
        for data_index in range(0, len(data)):
            ws.write(num, data_index, json.dumps(data[data_index], ensure_ascii=False))
        num += 1
    w.save('test' + '.xls')


if __name__ =="__main__":
    ################修改这个########
    date =  pd.to_datetime('2017-06-01 00:00:00')
    try:
        writeFile(date)
    except:
        driver.quit()














