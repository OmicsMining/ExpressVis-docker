'''
The code is written by Kaikun Xu. Just copy his code
'''

'''
## 函数功能:实现对于输入DataFrame的缺失值插补.
## 备注:
## 1.函数输入输出均为pandas.DataFrame格式
## 2.method表示缺失值的插补方式：
##   + 若method为minimum_value_impute，表示使用列最小值/全局最小值进行插补，这是最广泛使用的插补方法；
##   + 若method为group_minimum_value_impute，表示使用同组(行)最小值进行插补（用户可指定分组列索引的名称，默认为首行）——**优化计算速度**；
##   + 若method为random_number_impute，则使用各列中小于指定百分位数（默认1%，即0.01）的非零值构建随机数完成插补——**优化计算速度**;
##   + 若method为KNN_impute，则基于K近邻算法进行缺失值的估算及插补——**新增**。
'''
import sys,os,re
import numpy as np
import pandas as pd

def minimum_value_impute(x:pd.core.frame.DataFrame,minStrategy="global"):
    '''
    ## 函数功能:使用最小值插补缺失值.
    ## 备注:
    ## 函数输入输出均为pandas.DataFrame格式.
    '''
    if minStrategy == "global": x_imputation = x.fillna(x.min().min())
    elif minStrategy in ("column","sample"): x_imputation = x.fillna(x.min(axis=0))
    return x_imputation

def group_minimum_value_impute(x:pd.core.frame.DataFrame, groupRow="Status"):
    '''
    ## 函数功能:使用同组的行（蛋白、肽段）最小值插补缺失值
    ## 备注:
    ## 1.groupRow为列索引的名称，即将依据指定列索引行对数据进行分组插值;
    ## 2.若未指定groupRow，则依据输入表格中列索引的第一行进行分组插值;
    ## 3.函数输入输出均为pandas.DataFrame格式，且列索引需为MultiIndex.
    '''
    # 判断输入数据框是否有多级列索引，若有多级索引，则依据选定条件分组插值
    if type(x.columns) == pd.core.indexes.multi.MultiIndex:
        if not groupRow: groupRow = x.columns.names[0]
        firstRow =  x.columns.names[0]
        x = x.swaplevel(firstRow,groupRow,axis=1)
        x_imputation = pd.DataFrame()
        for group in x.columns.levels[0]:
            x_sub = x.loc[:,[group]]
            x_sub = x_sub.transpose().fillna(x.min(axis=1)).transpose()
            x_imputation = pd.concat([x_imputation,x_sub],axis=1)
        # 由于上述插补后依旧存在缺失值（来源于同组某蛋白均为缺失值）,再对这些值进行全局最小值插补
        x_imputation = minimum_value_impute(x=x_imputation,minStrategy="global")
        x_imputation = x_imputation.swaplevel(firstRow,groupRow,axis=1)
        return x_imputation
    # 若输入数据表无多级索引，直接弹出错误，无返回值
    elif type(x.columns) == pd.core.indexes.base.Index:
        raise AttributeError("The input dataframe contains only one row of column-index.This method is not available for imputation.")
        return None

def random_number_impute(x:pd.core.frame.DataFrame, percentile=0.05):
    '''
    ## 函数功能:使用小于threshold分位数的值构建随机数进行列缺失值插补.
    ## 备注:
    ## 1.threshold=0.05是指使用最小的5%的数值计算相关随机数生成参数;
    ## 2.函数输入输出均为pandas.DataFrame格式;
    ## 3.建议本函数与log变换联用.
    '''
    import random
    # 基lambda表达式计算各列的分位数，均值和标准差
    x_quanitle = x.apply(lambda x:x.quantile(percentile))
    mean_quantile = x[x<x_quanitle].mean(skipna=True)
    std_quantile = x[x<x_quanitle].std(skipna=True,ddof=1)
    for col in x.columns:
        data = x[col]
        mask = data.isnull()
        mean_col = mean_quantile.loc[col]
        std_col = std_quantile.loc[col]
        # 计算插补用数据
        np.random.seed(seed=12345)
        impute_col = np.random.normal(loc=mean_col,scale=std_col,size=mask.sum())
        # 通过随机抽样进行缺失值插补
        samples = random.choices(impute_col, k=mask.sum())
        data[mask] = samples
    return x

def knn_impute(x:pd.core.frame.DataFrame, neighborNum=5):
    '''
    ## 函数功能:基于scikit-learn计算库中的KNN近邻算法完成缺失值插补
    ## 备注:
    ## 1.groupRow为列索引的名称，即将依据指定列索引行对数据进行分组插值;
    ## 2.若未指定groupRow，则依据输入表格中列索引的第一行进行分组插值;
    ## 3.函数输入输出均为pandas.DataFrame格式，且列索引需为MultiIndex.
    '''
    from sklearn.impute import KNNImputer
    # Link: https://scikit-learn.org/stable/modules/generated/sklearn.impute.KNNImputer.html
    x_value = x.values
    imputer = KNNImputer(n_neighbors= neighborNum)
    x_imputation = imputer.fit_transform(x_value)
    x_imputation = pd.DataFrame(x_imputation,index=x.index,columns=x.columns)
    return x_imputation

def impute(dataframe:pd.core.frame.DataFrame,
           method="minimum_value",
           minStrategy="global",# minimum_value_impute() valid
           groupRow="Status",# group_minimum_value_impute() valid
           percentile=0.05,# random_number_impute() valid
           neighborNum=5,# knn_impute() valid
           replaceZero=False):
    try:
        if replaceZero: dataframe = dataframe.replace({0:np.nan})
        if method in ("minimum_value_impute"):
            impute_dataframe = minimum_value_impute(x=dataframe,minStrategy=minStrategy) 
        elif method in ("group_minimum_value_impute"):
            impute_dataframe = group_minimum_value_impute(x=dataframe,groupRow=groupRow) 
        elif method in ("random_number_impute"):
            impute_dataframe = random_number_impute(x=dataframe,percentile=percentile)
        elif method in ("knn_impute"):
            impute_dataframe = knn_impute(x=dataframe) 
        # dictImpute = impute_dataframe.reset_index().to_dict(orient="list")
        return impute_dataframe
    except Exception as e:
        print(e)
        raise ValueError('Parameter "method" must in: "minimum_value_impute", "group_minimum_value_impute", "random_number_impute", "knn_impute".')


# if __name__ == "__main__":
#     dataframe = pd.read_csv(os.path.join(os.getcwd(),"Proteomics_Normalization_Impute_TestFile.csv"),index_col=[0],header=[0,1])
#     impute(dataframe,method="knn_impute")
