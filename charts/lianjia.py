# coding: utf-8
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
###要去掉单价小于
df.drop(df.loc[(df['房屋用途'] == '车库') | (df['房屋用途'] == '别墅') | (df['房屋用途'] == '地下室')].index, inplace=True)
df['成交单价'] = df['成交单价'].astype(float)
df['成交时间'] = pd.to_datetime(df['成交时间'])
df['成交年份'] = df['成交时间'].dt.year
df['成交月份'] = df['成交时间'].dt.month
df['成交季度'] = df['成交时间'].dt.quarter
df['年份季度'] = pd.to_datetime(df['成交时间'])
df['年份季度'] = df['年份季度'].dt.to_period('Q')

price_table = df.groupby(['小区名', '年份季度'], as_index=False)['成交单价'].mean()

#####价格大表结束

###筛选出成交量前50%的小区为26
count = pd.DataFrame(df['小区名'].value_counts())
medium = count.quantile(0.5)
counts = count.loc[count['小区名']>int(medium.values)].reset_index()
counts.columns = ['小区名', '成交量']



danjia = df.loc[(df['成交年份'] >= 2013) & (df['成交年份'] <= 2015)]
danjia = danjia.groupby(['小区名', '成交年份', '成交季度', '年份季度'], as_index=False)['成交单价'].mean()

####danjia2 = danjia.groupby(['小区名'], as_index=False)['成交年份'].count()
####names = danjia2.loc[danjia2['成交年份'] == 8, ['小区名']]

danjia = pd.merge(counts, danjia, how='left', on=['小区名'])

new = danjia.groupby(['年份季度'], as_index=False)['成交单价'].mean()
danjia['涨跌幅度'] = 0

#g = sns.factorplot(x="年份季度", y="成交单价",data=new,
#                    size=5, aspect=1.5, scale=0.8,
#                   markers=["o", "o", "o", "o", "o", "o", "o", "o", "o", "o", "x"],)
#g.despine(left=True)
#sns.plt.show()

######填充缺少的数据#########
danjia2 = danjia.groupby(['小区名'], as_index=False)['成交年份'].count()
names = danjia2.loc[danjia2['成交年份'] >= 8, ['小区名']]
danjia = pd.merge(names, danjia, how='left', on=['小区名'])

tt = pd.pivot_table(danjia, index=['年份季度'], columns = ['小区名'], values = ['成交单价'])




#g = sns.factorplot(x="年份季度", y="成交单价",hue = 'Index' ,data=danjia,
#                    size=5, aspect=1.5, scale=0.8,
#                   markers=["o", "o", "o", "o", "o", "o", "o", "o", "o", "o", "x"],)
#g.despine(left=True)
#sns.plt.show()



tt = tt.fillna(method = 'bfill')



a = tt.ix['2014Q3']
b = tt.ix['2015Q1']
c = b/a
c = c.reset_index()


c.columns = ['单价','小区名','幅度']
c.set_index('小区名', inplace=True)
c = c.sort_values(['幅度'], ascending=0)
c_new = c['幅度'].head(10) # 年度平均涨幅前十
c_new.index


tt = tt.T
tt = tt.reset_index()

tt_max = tt.loc[tt['小区名'].isin(list(c_new.index))]
del tt_max['level_0']

tmp = pd.DataFrame(columns=['小区名','成交年份', '成交价格'])  
i = 0
while i<tt_max.shape[0]:
    print(i)
    b1= tt_max.iloc[i]
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






g = sns.FacetGrid(x='成交年份',y='成交价格', hue = '小区名',data=tmp,
                    size=5, aspect=1.5, scale=0.8,
                   markers=["o", "o", "o", "o", "o", "o", "o", "o", "o", "o", "x"],)
g.despine(left=True)
sns.plt.show()

# 计算涨幅
change = pd.DataFrame()


#hanzepeng######################################################

q12014 = danjia.loc[danjia['成交季度'] == 1]
q12014 = q12014.loc[q12014['成交年份'] == 2014,['成交单价']]
q12014.reset_index(drop=True, inplace=True)

q42013 = danjia.loc[danjia['成交季度'] == 4]
q42013 = q42013.loc[q42013['成交年份'] == 2013,['成交单价']]
q42013.reset_index(drop=True, inplace=True)



index0 = danjia.loc[danjia['年份季度'] == pd.Period('2014Q1'), ['涨跌幅度']].index


      
          
          
          
          
###############################################################





q1 = danjia.loc[danjia['成交季度'] == 1, ['成交单价']]
q1 = q1.astype(float)
q1.reset_index(drop=True, inplace=True)
q1.rename(columns={'成交单价': 'qrt1'}, inplace=True)


q2 = danjia.loc[danjia['成交季度'] == 2, ['成交单价']]
q2 = q2.astype(float)
q2.reset_index(drop=True, inplace=True)
q2.rename(columns={'成交单价': 'qrt2'}, inplace=True)

q3 = danjia.loc[danjia['成交季度'] == 3, ['成交单价']]
q3 = q3.astype(float)
q3.reset_index(drop=True, inplace=True)
q3.rename(columns={'成交单价': 'qrt3'}, inplace=True)

q4 = danjia.loc[danjia['成交季度'] == 4, ['成交单价']]
q4 = q4.astype(float)
q4.reset_index(drop=True, inplace=True)
q4.rename(columns={'成交单价': 'qrt4'}, inplace=True)

change = pd.concat([change, q1], axis=1, ignore_index=True)
change = pd.concat([change, q2], axis=1, ignore_index=True)
change = pd.concat([change, q3], axis=1, ignore_index=False)
change = pd.concat([change, q4], axis=1, ignore_index=False)
change['q2/q1'] = change[1] / change[0] - 1
change['q3/q2'] = change['qrt3'] / change[1] - 1
change['q4/q3'] = change['qrt4'] / change['qrt3'] - 1

####hanzp##########################################################################

change['q1/q4'] = q12014 / q42013 - 1

c0 = pd.Series(list(change['q1/q4'][:158]), index=index0)

danjia.loc[danjia['年份季度'] == pd.Period('2014Q1'), ['涨跌幅度']] = c0    


###################################################################################


index1 = danjia.loc[danjia['成交季度'] == 2, ['涨跌幅度']].index
c1 = pd.Series(list(change['q2/q1']), index=index1)

index2 = danjia.loc[danjia['成交季度'] == 3, ['涨跌幅度']].index
c2 = pd.Series(list(change['q3/q2']), index=index2)

index3 = danjia.loc[danjia['成交季度'] == 4, ['涨跌幅度']].index
c3 = pd.Series(list(change['q4/q3']), index=index3)

danjia.loc[danjia['成交季度'] == 2, ['涨跌幅度']] = c1
danjia.loc[danjia['成交季度'] == 3, ['涨跌幅度']] = c2
danjia.loc[danjia['成交季度'] == 4, ['涨跌幅度']] = c3
danjia['涨跌幅度'] = danjia['涨跌幅度'] * 100
names = danjia.loc[(danjia['涨跌幅度'] >= 100) | (danjia['涨跌幅度'] <= -100), '小区名']
index = danjia.loc[danjia['小区名'].isin(names), ['小区名']].index
danjia.drop(list(index), axis=0, inplace=True)

danjia2 = danjia.groupby(['小区名'], as_index=False)['涨跌幅度'].sum()
danjia_positive = danjia2.loc[danjia2['涨跌幅度'] >= 0]
danjia_positive = danjia_positive.sort_values(['涨跌幅度'], ascending=0)
names_positive = danjia_positive['小区名'].head(10) # 年度平均涨幅前十
danjia_positive = danjia.loc[danjia['小区名'].isin(list(names_positive))]


# 年度平均涨幅前十
# sns.set(style="whitegrid")
g = sns.factorplot(x="年份季度", y="成交单价", hue='小区名', data=danjia_positive,
                   join=True, palette="Set2", size=5, aspect=1.3, scale=0.2)
g.despine(left=True)
sns.plt.show()

# 加入大盘后的趋势图
dapan = danjia.groupby(['年份季度'], as_index=False)['成交单价'].mean()
dapan['小区名'] = '大盘'
dapan['成交年份'] = 0
dapan['成交季度'] = 0
dapan['涨跌幅度'] = 0
cols = danjia_positive.columns
dapan = dapan.loc[:, cols]
chart3 = pd.concat([danjia_positive, dapan], axis=0, ignore_index=True)

# sns.set(style="darkgrid")
g = sns.factorplot(x="年份季度", y="成交单价", hue='小区名', data=chart3,
                   join=True, palette="Set2", size=5, aspect=1.5, scale=0.2,
                   markers=["o", "o", "o", "o", "o", "o", "o", "o", "o", "o", "x"],
                   linestyles=['--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '-'])
g.despine(left=True)
sns.plt.show()

# 分布图
sns.set(style="darkgrid")
chart3 = danjia
#rows = chart3.loc[chart3['成交年份'] == 1].index
#chart3.drop(list(rows), axis=0, inplace=True)
chart3
g = sns.FacetGrid(chart3, row='成交年份', col='成交季度', margin_titles=True)
g.map(sns.distplot, u'涨跌幅度', color='black')
sns.plt.show()
