#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 15:17:57 2017

@author: lixiao
"""
# coding=utf-8
from numpy import *
import pandas as pd
import random
import seaborn as sns
import matplotlib.pyplot as plt


def distEclud(vecA1, vecB1, vecA2, vecB2):
    return sqrt(power(vecA1 - vecA2, 2) + power(vecB1 - vecB2, 2))


k = 50
dataSet = pd.read_csv('location.csv', sep=',')
names = dataSet['小区名']
seed = random.sample(names.tolist(), k)
centroids = dataSet.loc[dataSet['小区名'].isin(seed)]
centroids.columns = ['中心index', '中心经度', '中心纬度']

dataSet['中心index'] = 0
dataSet['距离'] = inf
centroids = centroids.reset_index()
del centroids['index']
del centroids['中心index']

m = shape(dataSet)[0]
clusterChanged = True
while clusterChanged:
    clusterChanged = False
    for i in range(m):
        for j in range(k):
            vecA1 = (dataSet['经度'][i]).astype(float)
            vecB1 = (dataSet['纬度'][i]).astype(float)
            vecA2 = (centroids['中心经度'][j]).astype(float)
            vecB2 = (centroids['中心纬度'][j]).astype(float)
            dist = distEclud(vecA1, vecB1, vecA2, vecB2)
            if dist < dataSet['距离'][i]:
                clusterChanged = True
                dataSet.set_value(i, '距离', dist)
                dataSet.set_value(i, '中心index', j)

    for j in range(k):
        tmp = dataSet.loc[(dataSet['中心index'] == j)]
        jingdu = tmp['经度'].mean()
        weidu = tmp['纬度'].mean()
        centroids.set_value(j, '中心经度', jingdu)
        centroids.set_value(j, '中心纬度', weidu)

g = sns.FacetGrid(dataSet, hue="中心index", size=10).map(plt.scatter, "经度", "纬度").add_legend()



