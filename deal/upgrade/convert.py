# -*- coding: utf-8 -*-
import xlwt
import xlrd
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import csv

file = '/Users/lixiao/PycharmProjects/lianjia/acc/石景山up99.xls'


def convert(file, writer):
    try:
        data = xlrd.open_workbook(file)
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
                if colnum == 13 or 15:
                    row[colnum] = row[colnum].replace('㎡', '')
                if colnum == 28:
                    row[colnum] = row[colnum].replace('万', '')

                if colnum in range(31, ncols):
                    if row[colnum].find("自行") == 0 or row[colnum].find("其他") == 0:
                        ccc = row[colnum].split(',')
                        temp.append(ccc[0])
                        temp.append(ccc[1])

                    elif row[colnum].strip() != '':
                        if colnum % 2 == 0:
                            a = row[colnum].split(',链家成交,')[0]
                            aa = a.split('单价')[1].split('元/平')[0]
                            b = row[colnum].split(',链家成交,')[1]
                            temp.append(aa)
                            temp.append(b)
                        if colnum % 2 == 1:
                            c = row[colnum].replace('万', '')
                            temp.append(c)
            for num in range(31, ncols):
                row.pop()
            row.extend(temp)
            writer.writerow(row)

    except Exception, e:
        print e
        f.write("erorrrrr")
        f.flush()



if __name__ =="__main__":
    f = open("11111111.txt", 'w')
    csvfile = open('石景山up'+str(time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())))+'.csv', 'wb')
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

    convert(file, writer)
    csvfile.close()
    f.close()



