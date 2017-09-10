#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 13:33:35 2017

@author: lixiao24
"""

import pandas as pd
import seaborn as sns

import matplotlib as plt


plt.rcParams['font.sans-serif'] = ['Microsoft YaHei'] #指定默认字体  
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题




#字体文件
#myfont=FontProperties(fname='/System/Library/Fonts/SimHei.ttf',size=14)
#sns.set(font=myfont.get_name())
#sns.set_context("notebook")
pd.set_option('max_columns', 500)
pd.set_option('max_row', 1000)

# 数据清洗
df = pd.read_csv('haidian.csv',sep=',')
df.drop(df.loc[(df['成交单价'] == '其他公司成交') | (df['成交单价'] == '自行成交')].index, inplace=True)
df.drop(df.loc[(df['房屋用途'] == '车库') | (df['房屋用途'] == '别墅') | (df['房屋用途'] == '地下室')].index, inplace=True)
df['成交单价'] = df['成交单价'].astype(float)
df['成交时间'] = pd.to_datetime(df['成交时间'])
df['成交年份'] = df['成交时间'].dt.year
df['成交月份'] = df['成交时间'].dt.month
df['成交季度'] = df['成交时间'].dt.quarter
df['年份季度'] = pd.to_datetime(df['成交时间'])
df['年份季度'] = df['年份季度'].dt.to_period('Q')


###筛选出成交量前50%、在2013到2015年之间的小区
count = pd.DataFrame(df['小区名'].value_counts())
medium = count.quantile(0.5)
counts = count.loc[count['小区名']>int(medium.values)].reset_index()
counts.columns = ['小区名', '成交量']

danjia = df.loc[(df['成交年份'] >= 2013) & (df['成交年份'] <= 2015)]
danjia = danjia.groupby(['小区名', '成交年份', '成交季度', '年份季度'], as_index=False)['成交单价'].mean()
danjia = pd.merge(counts, danjia, how='left', on=['小区名'])

danjia['成交量'] = danjia['成交量'].astype(float)
danjia['成交单价'] = danjia['成交单价'].astype(float)
g = sns.JointGrid(x="成交量", y="成交单价", data=danjia)
g.plot_joint(sns.regplot, order=2)
g.plot_marginals(sns.distplot)


#取均值并作图
price_table = danjia.groupby(['年份季度'], as_index=False)['成交单价'].mean()
g = sns.factorplot(x="年份季度", y="成交单价",data=price_table,
                    size=5, aspect=1.5, scale=0.8,
                   markers=["o", "o", "o", "o", "o", "o", "o", "o", "o", "o", "x"],)
g.despine(left=True)
sns.plt.show()

######填充缺少的数据（成交季度个数大于等于8）#########
danjia2 = danjia.groupby(['小区名'], as_index=False)['成交年份'].count()
names = danjia2.loc[danjia2['成交年份'] >= 8, ['小区名']]
danjia = pd.merge(names, danjia, how='left', on=['小区名'])

#######做透视图用于填充####
pivot_table = pd.pivot_table(danjia, index=['年份季度'], columns = ['小区名'], values = ['成交单价'])
pivot_table = pivot_table.fillna(method = 'bfill')


#####计算增长率
start = pivot_table.ix['2014Q3']
end = pivot_table.ix['2015Q1']
ratio = end/start
ratio = ratio.reset_index()


ratio.columns = ['单价','小区名','幅度']
ratio.set_index('小区名', inplace=True)
ratio = ratio.sort_values(['幅度'], ascending=0)

ratio = ratio['幅度'].head(10) # 年度平均涨幅前十



pivot_table = pivot_table.T
pivot_table = pivot_table.reset_index()

top = pivot_table.loc[pivot_table['小区名'].isin(list(ratio.index))]
del top['level_0']

tmp = pd.DataFrame(columns=['小区名','成交年份', '成交价格'])  
i = 0
while i<top.shape[0]:
    b1= top.iloc[i]
    b1 = b1.reset_index()
    b1.columns=['成交年份', '成交价格']
    name = b1.ix[0, '成交价格']
    b1['小区名']=name

    # get a list of columns
    cols = list(b1)
    # move the column to head of list using index, pop and insert
    cols.insert(0, cols.pop(cols.index('小区名')))
    b1 = b1.ix[:, cols]
    b1 = b1.drop(0)
    tmp = tmp.append(b1)
    i = i+1


g = sns.factorplot(x='成交年份',y='成交价格', hue = '小区名',data=tmp,
                    size=5, aspect=1.5, scale=0.8,
                   markers=["o", "o", "o", "o", "o", "o", "o", "o", "o", "o", "x"],)
g.despine(left=True)
sns.plt.show()



      
          
          
          

