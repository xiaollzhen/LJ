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
t_str = '2015-04-07 19:11:21'




def getData(url):
    driver.get(url)
    df = pd.DataFrame()
    list = []
    name = driver.find_element_by_class_name('current-school-name')
    list.append(name.text)
    details = driver.find_element_by_class_name('current-school-detail').find_elements_by_class_name('data')
    for i in details:
        list.append(i.text)
    try:
        highschools = driver.find_element_by_class_name('dui-kou').find_elements_by_tag_name('p')
        tmp = ''
        for i in highschools:
            tmp = tmp + i.text + '/'
        list.append(tmp)
    except Exception, e:
        if repr(e) == 'NoSuchElementException()':
            list.append('Null')
        else:
            print('error::::' + url)

    try:
        xiaoqus = driver.find_element_by_class_name('hua-pian').find_elements_by_tag_name('p')
    except Exception, e:
        if repr(e) == 'NoSuchElementException()':
            newlist = []
            for j in list:
                newlist.append(j)
            newlist.append('Null')
            newlist.append('Null')
            df_tmp = pd.DataFrame(newlist)
            df = df.append(df_tmp.T)
            return df
        else:
            print('error::::' + url)
    for i in xiaoqus:
        data = i.text.split('---')
        newlist = []
        for j in list:
            newlist.append(j)
        newlist.append(data[0])
        newlist.append(data[1])
        df_tmp = pd.DataFrame(newlist)
        df = df.append(df_tmp.T)
    return df


def writeFile(districtName):
    f = open(districtName + '.txt', 'w')
    pageIndex = 1
    df = pd.DataFrame()
    error_urls = []
    while pageIndex < 15:
        print('pageIndex:   ' + str(pageIndex))
        try:

            driver.get('http://www.genshuixue.com/i-youshengxiao/school/?&province=北京&city=北京&district=' +
                                districtName + '&school_property=全部&level=全部&attend_way=全部&p=' + str(pageIndex))
        except Exception, e:
            print e

        info = driver.find_elements_by_class_name('xxk-content-title')
        titles = []
        for i in info:
            try:
                title = i.find_element_by_tag_name('a').get_attribute("href")
                titles.append(title)
            except Exception, e:
                print e
        for url in titles:
            try:
                df = df.append(getData(url))
            except:
                error_urls.append(url)
                print('urls with warning:', error_urls)
                time.sleep(4)
                continue
        pageIndex += 1

    df.columns = ['学校名称', '学校简称', '学校性质', '学校等级', '升学方式', '咨询电话', '学校地址',
                  '学校网址', '对口中学', '划片小区', '小区详细']
    df.to_csv(districtName+'.csv')
    f.close()


if __name__ =="__main__":
    districtNames = ['朝阳区']

    for districtName in districtNames:
        try:
            # f = open("小区日志.txt", 'a')
            # f.write("开始爬小区："+districtName+time.strftime('%H%M', time.localtime(time.time()))+'\n')
            # f.flush()
            # print(xiaoquname.encode('gb2312') + 'start  :', time.strftime('%H%M', time.localtime(time.time())))
            writeFile(districtName)
            # print(xiaoquname.encode('gb2312') + 'end  :', time.strftime('%H%M', time.localtime(time.time())))
            # f.write("结束爬小区：" + districtName + time.strftime('%H%M', time.localtime(time.time())) + '\n')
        except Exception, e:
            print e
            driver.quit()
        # f.close()











