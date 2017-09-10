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
################
# 思路是每个小区取最新的时间，挨个循环
############################


def getXiaoquNames(districtName):
    df = pd.read_csv(districtName)
    df['成交时间'] = pd.to_datetime(df['成交时间'])
    df = df['成交时间'].groupby(df['小区名']).max()
    print df
    return df



def getData(url):
    data = []
    driver.get(url)
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
    data_10_list = data[10].split(' ')
    new_data_10 = data_10_list[0]
    new_data_11 = data_10_list[1].split('共')[1].split('层')[0]
    # 插入到第九列（共多少层）
    data[10] = new_data_10
    data.insert(11, new_data_11)
    return data


def writeFile(xiaoquname, date):

    f_error = open("error日志.txt", 'a')
    f_new = open("小区日志.txt", 'a')
    pageIndex = 1
    w = xlwt.Workbook()
    ws = w.add_sheet('test', cell_overwrite_ok=True)
    num = 1
    error_urls = []
    row0 = [u'成交时间', u'成交价格', u'成交单价', u'挂牌价格（万）', u'成交周期（天）', u'调价（次）', u'带看（次）', u'关注（人）', u'浏览（次）',
            u'房屋户型', u'所在楼层', u'总共层数', u'建筑面积', u'户型结构', u'套内面积', u'建筑类型', u'房屋朝向',
            u'建成年代', u'装修情况', u'建筑结构', u'供暖方式', u'梯户比例', u'产权年限', u'配备电梯', u'链家编号',
            u'交易权属', u'挂牌时间', u'房屋用途', u'房屋年限', u'房权所属', u'历史成交记录']
    for index in range(0, len(row0)):
        ws.write(0, index, row0[index])
    while 1 == 1:
        print('pageIndex:   ' + str(pageIndex))
        try:
            driver.get("http://bj.lianjia.com/chengjiao/pg" + str(pageIndex) + "rs" + xiaoquname)
            total_number_1 = driver.find_element_by_class_name('total').find_element_by_tag_name('span')
            total_pages_1 = int(total_number_1.text) / 30 + 1
            if total_pages_1 > 100:
                f_new.write("error：：：：：：：：：：：：：：：：：：：：：：：小区成交数量异常：  " + xiaoquname + '\n')
                f_new.close()
                f_error.write("error：：：：：：：：：：：：：：：：：：：：：：：小区成交数量异常：  " + xiaoquname + '\n')
                f_error.close()
                break
            if int(total_number_1.text) == 0:
                f_new.write("error：：：：：：：：：：：：：：：：：：：：：：：total_number::0 " + xiaoquname + '\n')
                f_new.close()
                f_error.write("error：：：：：：：：：：：：：：：：：：：：：：：total_number::0 " + xiaoquname + '\n')
                f_error.close()
                break
            aaa = driver.find_element_by_xpath("//span[text()="+"\"" + xiaoquname + "\""+ "]/ancestor::a").get_attribute("href")
            tmp = aaa[10:1000]
            partial = tmp.split('chengjiao/')[1]
            driver.get("http://bj.lianjia.com/chengjiao/pg" + str(pageIndex) + partial)
            total_number = driver.find_element_by_class_name('total').find_element_by_tag_name('span')
            total_pages = int(total_number.text) / 30 + 1
            if int(total_number.text) == 0:
                break
            print('total pages  : ', total_pages)

        except Exception, e:
            if repr(e) == 'NoSuchElementException()':
                f_new.write("error：：：：：：：：：：：：：：：：：：：：：：：小区名称没有发现：  " + xiaoquname + '\n')
                f_error.write("小区名称没有发现: " + xiaoquname + '\n')
            else:
                f_new.write("error：：：：：：：：：：：：：：：：：：：：：：：小区存在其它异常：  " + xiaoquname + '\n')
                f_error.write("小区存在其它异常: " + xiaoquname + '\n')
            f_new.close()
            f_error.close()
            break

        info = driver.find_elements_by_class_name('info')
        titles = []
        for i in info:
            try:
                date_now = i.find_element_by_class_name('dealDate').text
                if date_now != '近30天内成交':
                    date_now = pd.to_datetime(date_now)
                    if date_now <= date:
                        pageIndex = 100
                        break
                title = i.find_element_by_partial_link_text('平米').get_attribute("href")
                titles.append(title)
            except:
                pass
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
        pageIndex += 1
        if pageIndex > total_pages:
            f_new.write("小区页数：  " + str(pageIndex - 1)+ '\n')
            f_new.flush()
            f_new.close()
            break

    for error_url in error_urls:
        try:
            data = getData(error_url)
        except:
            print('url with error:', error_url)
            f = open(xiaoquname + '.txt', 'w')
            f.write(error_url + '\n')
            f.close()
            continue
        for data_index in range(0, len(data)):
            ws.write(num, data_index, json.dumps(data[data_index], ensure_ascii=False))
        num += 1

    if num > 1:
        w.save(xiaoquname + '.xls')


if __name__ =="__main__":
    ######修改这里#####
    districtName = '/Users/lixiao24/PycharmProjects/untitled/merge/西城2017-08-11 16:02.csv'
    df = getXiaoquNames(districtName)
    names = df.index.tolist()
    # names=['佳慧雅园', '德胜里西街5号院', '砖塔胡同86号院']

    for xiaoquname in names:
        date = df[xiaoquname]
        try:
            f = open("小区日志.txt", 'a')
            f.write("开始爬小区："+xiaoquname+time.strftime('%H%M', time.localtime(time.time()))+'\n')
            f.flush()
            # print(xiaoquname.encode('gb2312') + 'start  :', time.strftime('%H%M', time.localtime(time.time())))
            writeFile(xiaoquname, date)
            # print(xiaoquname.encode('gb2312') + 'end  :', time.strftime('%H%M', time.localtime(time.time())))
            f.write("结束爬小区：" + xiaoquname + time.strftime('%H%M', time.localtime(time.time())) + '\n')
        except:
            f.write("爬小区报错：" + xiaoquname + '\n')
            driver.quit()
        f.close()











