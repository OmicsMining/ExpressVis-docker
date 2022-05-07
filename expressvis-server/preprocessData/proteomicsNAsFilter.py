'''
These functions are written by KAIKUN xu
'''

"""
## 函数功能:实现对于输入DataFrame的缺失值过滤.
## 备注:
## 1.函数输入输出均为pandas.DataFrame格式;
## 2.naFilter()支持四种缺失值筛选方法
##    + method="all",基于全样本计算缺失值,而后根据缺失比例阈值过滤
##    + method="each",分别基于各组别样本计算缺失值,在每个组别中缺失值比例均满足阈值标准
##    + method="alo"(At least once),分别基于各组别样本计算缺失值,在至少一个组别中缺失值比例均满足阈值标准
##    + method="some",分别基于各组别样本计算缺失值,在大于等于给定的组别数目中满足阈值标准，两组设计中等同于alo(n=1)或者each(n=2)
"""

import numpy as np
import pandas as pd

def naConvert(dataframe:pd.core.frame.DataFrame):
    """
    函数功能：将非常规缺失值外的缺失值表示形式，替换为空值，并将剩余数据转化为float类型
    """
    naDict = {"Filtered":np.nan}; zeroDict = {0:np.nan}
    # 如下写法比dataframe.replace(dict)运行速度快
    dataframe = dataframe.apply(lambda row: row.map(lambda x:naDict.get(x,x)),axis=0).astype(float)
    if dataframe.min().min()>=0: dataframe = dataframe.apply(lambda row: row.map(lambda x:zeroDict.get(x,x)),axis=0)
    return dataframe


def naFilter(dataframe:pd.core.frame.DataFrame,
             naThreshold:float=0.3,
             method:str="all",
             suitableGroup:int=1 # method=="some" valid
            ):
    """
    ## 函数功能: 根据缺失比例阈值过滤蛋白,返回满足要求的蛋白质列表
    ##    + naThreshold: 缺失值比例小于naThreshold的蛋白质被保留,naThreshold=0.3表示仅保留缺失值比例小于30%的蛋白质;
    ##    + method: 用于缺失值过滤的方法,本函数支持常用的四种:
    ##        - "all",基于全样本计算缺失值,而后根据缺失比例阈值过滤蛋白质
    ##        - "each",分别基于各组别样本计算缺失值,保留的蛋白质在每个组别中缺失值比例均满足阈值标准
    ##        - "alo"(At least once),分别基于各组别样本计算缺失值,保留的蛋白质在至少一个组别中缺失值比例均满足阈值标准
    ##        - "some",分别基于各组别样本计算缺失值,保留的蛋白质在大于等于给定的组别数目中满足阈值标准,两组设计中等同于alo(n=1)或者each(n=2)
    ##   + suitableGroup: method="some"时有效,保留至少在suitableGroup组别数目中满足阈值标准的蛋白质
    """
    assert (method in ("all","each","alo","some")), "ValueError: Method parameter must be in [all, each, alo, some]."

    if method=="all":
        naPercentSeries = dataframe.isnull().sum(axis=1)/dataframe.shape[1]; qualifiedList = naPercentSeries[naPercentSeries<=naThreshold].index
    else:
        groupList = dataframe.columns.levels[0]; naPercentDF = pd.DataFrame(index=dataframe.index)
        for group in groupList:
            naPercentSub = dataframe[group].isnull().sum(axis=1)/dataframe[group].shape[1]; naPercentDF = pd.concat([naPercentDF,naPercentSub],axis=1)
        naPercentDF = naPercentDF.set_axis(groupList, axis=1)
        # naPercentDF = dataframe.apply(lambda row:row.isnull().unstack().sum(axis=1)/row.isnull().unstack().notnull().sum(axis=1),axis=1)
        if method == "each": naPercentSeries = naPercentDF.max(axis=1); qualifiedList = naPercentSeries[naPercentSeries<=naThreshold].index
        elif method == "alo": naPercentSeries = naPercentDF.min(axis=1); qualifiedList = naPercentSeries[naPercentSeries<=naThreshold].index
        elif method == "some": suitableCountSeries = naPercentDF[naPercentDF<=naThreshold].notnull().sum(axis=1); qualifiedList = suitableCountSeries[suitableCountSeries>=suitableGroup].index
    dataframeFilter = dataframe.loc[qualifiedList]
    return dataframeFilter
