# -*- coding: utf-8 -*-
import xlwt
import xlrd
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import csv
#全量需要修改以下两个文件，增量需修改下方第三个地方
filePath = '/Users/lixiao24/PycharmProjects/untitled/accumulated/xicheng/'
fileName = '西城'
def getXiaoquNames(districtName):
    data = xlrd.open_workbook(districtName)
    table = data.sheet_by_name(u'test')
    names = table.col_values(0)
    del names[0]
    return names


def convert(xiaoquname, writer):
    try:
        data = xlrd.open_workbook(filePath + xiaoquname + '.xls')
        table = data.sheet_by_index(0)
        nrows = table.nrows  # 行数
        ncols = table.ncols  # 列数
        for rownum in range(1, nrows):
            temp = []
            row = table.row_values(rownum)
            for colnum in range(0, ncols):

                row[colnum] = row[colnum].replace('"', '')
                if colnum == 0:
                    row[colnum] = row[colnum].replace('自行成交', '')
                if colnum == 12 or 14:
                    row[colnum] = row[colnum].replace('㎡', '')
                if colnum == 27:
                    row[colnum] = row[colnum].replace('万', '')

                if colnum in range(30, ncols):
                    if row[colnum].find("自行") == 0 or row[colnum].find("其他") == 0:
                        ccc = row[colnum].split(',')
                        temp.append(ccc[0])
                        temp.append(ccc[1])

                    elif row[colnum].strip() != '':
                        if colnum % 2 == 1:
                            a = row[colnum].split(',链家成交,')[0]
                            aa = a.split('单价')[1].split('元/平')[0]
                            b = row[colnum].split(',链家成交,')[1]
                            temp.append(aa)
                            temp.append(b)
                        if colnum % 2 == 0:
                            c = row[colnum].replace('万', '')
                            temp.append(c)
            for num in range(30, ncols):
                row.pop()
            row.extend(temp)
            row.insert(0, xiaoquname.replace('"', ''))
            writer.writerow(row)

    except:
        f.write("无小区：" + xiaoquname + time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())) + '\n')
        f.flush()



if __name__ =="__main__":
    f = open("11111111.txt", 'w')
    districtName = filePath + fileName + '.xls'
    names = getXiaoquNames(districtName)
    csvfile = open(fileName+ str(time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())))+'.csv', 'wb')
    writer = csv.writer(csvfile)
    row0 = [u'小区名', u'成交时间', u'成交价格', u'成交单价', u'挂牌价格（万）', u'成交周期（天）', u'调价（次）', u'带看（次）',
            u'关注（人）', u'浏览（次）', u'房屋户型', u'所在楼层', u'总共层数', u'建筑面积', u'户型结构', u'套内面积', u'建筑类型',
            u'房屋朝向',u'建成年代', u'装修情况', u'建筑结构', u'供暖方式', u'梯户比例', u'产权年限', u'配备电梯', u'链家编号',
            u'交易权属', u'挂牌时间', u'房屋用途', u'房屋年限', u'房权所属',u'成交价格（历史1）', u'成交单价（历史1）',
            u'成交时间（历史1）', u'成交价格（历史2）', u'成交单价（历史2）', u'成交时间（历史2）', u'成交价格（历史3）',
            u'成交单价（历史3）', u'成交时间（历史3）', u'成交价格（历史4）', u'成交单价（历史4）', u'成交时间（历史4）',
            u'成交价格（历史5）', u'成交单价（历史5）', u'成交时间（历史5）', u'成交价格（历史6）', u'成交单价（历史6）',
            u'成交时间（历史6）']
    writer.writerow(row0)
    for xiaoquname in names:
        # 增量条件使用
        xiaoquname = xiaoquname.replace('"', '')
        convert(xiaoquname, writer)
    csvfile.close()
    f.close()



