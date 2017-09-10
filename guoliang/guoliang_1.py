# -*- coding: utf-8 -*-

from selenium import webdriver
import xlrd
import sys
import pandas as pd
from pandas.core.frame import DataFrame

reload(sys)
sys.setdefaultencoding('utf-8')

firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.stylesheet', 2)
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
firefox_profile.set_preference('browser.migration.version', 9001)

driver = webdriver.Firefox(firefox_profile)
driver.set_page_load_timeout(30)
t_str = '2015-04-07 19:11:21'


def getParams(fileName):
    data = xlrd.open_workbook(fileName)
    table = data.sheet_by_name(u'test')
    names = table.col_values(0)
    titles = table.col_values(1)
    del names[0]
    del titles[0]
    dic = {}
    i = 0
    while i < len(names):
        dic[names[i]] = titles[i]
        i = i + 1
    return dic


def writeFile(name, title, year):
    name_new = name.replace(' ', '+')
    title_new = title.replace(' ', '+')
    df = pd.DataFrame()
    driver.get("http://visadoor.com/h1b/index?company=" + name_new + "&job=" +
               title_new + "&state=&year=" + str(year) + "&submit=Search")
    info = driver.find_element_by_class_name('table').find_elements_by_css_selector("[valign='top']")

    for i in range(0, len(info), 6):
        b = info[i:i + 6]
        link = b[0].find_element_by_tag_name('a').get_attribute("href")
        tmp = []
        for j in b:
            tmp.append(str(j.text))
        tmp.append(link)
        tmp[4] = tmp[4].lower()
        df_tmp = DataFrame(tmp)
        df = df.append(df_tmp.T)
    df.columns = ['Id', 'Decision Date', 'Employer', 'Status', 'Job Title', 'Wage Offer', 'link']
    df = df.loc[df['Job Title'] == title.lower()]
    if df.size != 0:
        df = getLinks(df)
        df.to_csv(name + str(year) + title + '.csv', sep=',', index=False)
    else:
        f.write("error(maybe 0 data)：" +
                "company name：" + name + "    title：" + title + "    year：" + str(year) + '\n')
        return 1


def getLinks(df):
    links = df['link']
    df_new = pd.DataFrame()
    for link in links:
        driver.get(link)
        info = driver.find_element_by_class_name('table').find_elements_by_css_selector("[valign='top']")
        tmp = []
        for i in info:
            if str(i.text) == 'Official iCert Registry':
                iCert = i.find_element_by_tag_name('a').get_attribute("href")
                tmp.append(iCert)
            else:
                tmp.append(str(i.text))
        if len(tmp) == 23:
            tmp.append('nan')
        df_tmp = DataFrame(tmp)
        # print df_tmp

        df_new = df_new.append(df_tmp.T)
        # print df_new
    df_new.columns = ['Id',
                      'Submit Date',
                      'Decision Date',
                      'Case Status',
                      'Employer',
                      'Employer Address',
                      'City, State',
                      'Employer Postal Code',
                      'Work Start Date',
                      'Work End Date',
                      'Prevailing Wage SOC Code',
                      'Prevailing Wage SOC Name',
                      'Prevailing Wage Job Title',
                      'NAICS Code',
                      'Prevailing Wage Source',
                      'Wage Offer From',
                      'Wage Offer To',
                      'Prevailing Wage',
                      'Full Time Position',
                      'Total Workers',
                      'Job City',
                      'Job State',
                      'Visa Class',
                      'Link to iCert Registry']


    iCerts = df_new['Link to iCert Registry']

    tmp = []
    for iCert in iCerts:

        if str(iCert) == 'nan':
            tmp.append('Null')
        else:
            driver.get(iCert)
            workers = driver.find_element_by_id('detail').find_element_by_class_name('numericCell')
            tmp.append(str(workers.text))
    df_iCert = DataFrame(tmp)
    df_new['workers numbers'] = df_iCert
    return df_new


if __name__ == "__main__":
    fileName = 'hire.xls'
    dic = getParams(fileName)
    for name in dic.keys():
        title = dic.get(name)
        for year in range(2017, 2018):
            while 1 == 1:
                try:
                    f = open("日志.txt", 'a')
                    f.flush()
                    if writeFile(name, title, year) == 1:
                        break
                    f.write("success：" +
                            "company name：" + name + "    title：" + title + "    year：" + str(year) + '\n')
                    break
                except Exception, e:
                    if repr(e) == 'NoSuchElementException()':
                        f.write("error(maybe 0 data)：" +
                                "company name：" + name + "    title：" + title + "    year：" + str(year) + '\n')
                        print e
                        break
                    else:
                        f.write("error(other error)：" +
                                "company name：" + name + "    title：" + title + "    year：" + str(year) + '\n')
                        print e
                        continue

            f.close()