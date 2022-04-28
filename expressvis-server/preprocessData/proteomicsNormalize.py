'''
These code is wri by KaiKun Xu.
'''

'''
## 函数功能:实现对于输入DataFrame的标准化，此处针对实际需求分为行（蛋白质维度）的标准化及列的标准化（样本维度），对应其中的norm_samlpe()和norm_protein()两函数.
## 备注:
## 1.函数输入输出均为pandas.DataFrame格式;
## 2.dim表示标准化的维度(注：**method为quantile_normalize时不起作用**)：
##   + dim为("col", "cols", "column", "columns")中的其中之一时，按照列为标准确定中位数、最大值、平均值，而后完成标准化；
##   + dim为("row", "rows")中的其中之一时，按照行为标准确定中位数、最大值、平均值，而后完成标准化；
##   + dim为其他值时，按照全局为标准确定中位数、最大值、平均值，而后完成标准化；
## 3.method表示标准化方式——**重新归类合并**：
##   + 如下常用于对列维度进行标准化:
##     - 若method为mean_normalize，表示进行均值标准化；
##     - 若method为median_normalize，表示进行中位数标准化；
##     - 若method为max_normalize，表示进行最大值标准化；
##     - 若method为fot_normalize，计算fot作为标准化结果；
##   + 如下常用于对行维度进行标准化：
##     - 若method为clr_normalize，表示进行CLR(Centered log-ratio)标准化(取对数并将均值校正为0)——**新增**；
##     - 若method为max_min_normalize，表示进行max_min标准化(将数据线性压缩至[0,1])；
##     - 若method为zscore_normalize，表示进行zscore标准化($\frac{x-x_mean}{x_std}$)；
##     - 若method为IQR_normalize，表示进行IQR标准化($\frac{x-x_median}{x_0.75-x_0.25}$)；
##   + quantile标准化时同时利用了行列维度的信息(https://en.wikipedia.org/wiki/Quantile_normalization)，但仍归结于列维度标准化中：
##     - 若method为quantile_normalize，表示进行quantile标准化——**重新编程后新增，目前与R preprocess函数包计算一致**；

## 注：本部分函数对所有函数均进行了行列标准化的兼容，但依旧建议按照如上分类进行标准化操作。
'''

import sys,os,re
import numpy as np
import pandas as pd
import json

# 列维度的标准化
def mean_normalize(x:pd.core.frame.DataFrame, dim="col"):
    '''
    ## 函数功能:实现对于数据表的均值标准化.
    ## 计算公式:$x_norm=\frac{x}{mean(x)}$
    ## 备注:
    ## 1.函数输入输出均为pandas.DataFrame格式;
    ## 2.本函数需要dim作为输入参数,参数定义为:
    ##    --("col", "cols", "column", "columns"):原数值除以列的均值作为最终结果，默认使用列均值;
    ##    --("row", "rows"):原数值除以行的均值作为最终结果;
    ##    --其他参数:原数值除以数据表总的均值作为最终结果.
    '''
    # {x}_{normalization}=\frac{x}{x_mean}
    if dim in ("col", "cols", "column", "columns"):
        x_norm = x / x.mean(axis=0)
    elif dim in ("row", "rows"):
        x_norm = ((x.transpose()) / x.mean(axis=1)).transpose()
    else:
        x_norm = x / x.values.reshape(-1).mean()
    return x_norm

def median_normalize(x:pd.core.frame.DataFrame, dim="col"):
    '''
    ## 函数功能:实现对于数据表的中位数标准化.
    ## 计算公式:$x_norm=\frac{x}{median(x)}$
    ## 备注:
    ## 1.函数输入输出均为pandas.DataFrame格式;
    ## 2.本函数需要dim作为输入参数,参数定义为:
    ##    --("col", "cols", "column", "columns"):原数值除以列的均值作为最终结果，默认使用列中位数;
    ##    --("row", "rows"):原数值除以行的中位数作为最终结果;
    ##    --其他参数:原数值除以数据表总的中位数作为最终结果.
    '''
    # {x}_{normalization}=\frac{x}{x_mean}
    if dim in ("col", "cols", "column", "columns"):
        x_norm = x / x.median(axis=0)
    elif dim in ("row", "rows"):
        x_norm = ((x.transpose()) / x.median(axis=1)).transpose()
    else:
        x_norm = x / x.values.reshape(-1).median()
    return x_norm

def max_normalize(x:pd.core.frame.DataFrame, dim="col"):
    '''
    ## 函数功能:实现对于数据表的最大值标准化.
    ## 计算公式:$x_norm=\frac{x}{max(x)}$
    ## 备注:
    ## 1.函数输入输出均为pandas.DataFrame格式;
    ## 2.本函数需要dim作为输入参数,参数定义为:
    ##    --("col", "cols", "column", "columns"):原数值除以列的最大值作为最终结果，默认使用列最大值;
    ##    --("row", "rows"):原数值除以行的最大值作为最终结果;
    ##    --其他参数:原数值除以数据表总的最大值作为最终结果.
    '''
    # {x}_{normalization}=\frac{x}{x_mean}
    if dim in ("col", "cols", "column", "columns"):
        x_norm = x / x.max(axis=0)
    elif dim in ("row", "rows"):
        x_norm = ((x.transpose()) / x.max(axis=1)).transpose()
    else:
        x_norm = x / x.values.reshape(-1).max()
    return x_norm

def fot_normalize(x:pd.core.frame.DataFrame, dim="col"):
    '''
    ## 函数功能:依据原始数据计算fraction of total(FOT)作为标准化方式.
    ## 计算公式:$x_norm=\frac{x}{sum(x)}$
    ## 备注:
    ## 1.函数输入输出均为pandas.DataFrame格式;
    ## 2.本函数需要dim作为输入参数,参数定义为:
    ##    --("col", "cols", "column", "columns"):原数值除以列的和作为最终结果;
    ##    --("row", "rows"):原数值除以行的和作为最终结果;
    ##    --其他参数:原数值除以数据表的和作为最终结果.
    '''
    # {x}_{normalization}=\frac{x}{x_mean}
    if dim in ("col", "cols", "column", "columns"):
        x_norm = x / x.sum(axis=0)
    elif dim in ("row", "rows"):
        x_norm = ((x.transpose()) / x.sum(axis=1)).transpose()
    else:
        x_norm = x / x.values.reshape(-1).sum()
    return x_norm

def max_min_normalize(x:pd.core.frame.DataFrame, dim="row"):
    '''
    ## 函数功能:实现对于数据表的max-min标准化,将原始数据线性缩放到[0,1].
    ## 计算公式:$x_norm=\frac{x-x_min}{x_max-x_min}$
    ## 备注:
    ## 1.函数输入输出均为pandas.DataFrame格式;
    ## 2.本函数需要dim作为输入参数,参数定义为:
    ##    --("col", "cols", "column", "columns"):使用列最值计算最终结果;
    ##    --("row", "rows"):使用行最值计算最终结果;
    ##    --其他参数:使用数据表的最值计算最终结果.
    '''
    # 线性函数归一化,将按照原始数据线性化的方法转换到[0,1]的范围,{x}_{normalization}=\frac{x-Min}{Max-Min}
    # axis=0表示每列取最大值最小值，axis=1表示每行取最大值最小值
    if dim in ("col", "cols", "column", "columns"):
        x_norm = (x - x.min(axis=0)) / (
            x.max(axis=0) - x.min(axis=0))
    elif dim in ("row", "rows"):
        x_norm = ((x.transpose() - x.min(axis=1).transpose()) / (
            x.max(axis=1).transpose() - x.min(axis=1).transpose())).transpose()
    else:
        x_norm = (x - np.min(np.array(x), axis=None)) / (
            np.max(np.array(x), axis=None) - np.min(np.array(x), axis=None))
    return x_norm

# 行维度的标准化
def clr_normalize(x:pd.core.frame.DataFrame,dim="row"):
    '''
    ## 函数功能:实现对于数据表的CLR标准化,是的对数后的样本均值为0.
    ## 计算公式:x_norm=ln(x)-ln(x)_mean
    '''
    x = np.log(x) # numpy.log()函数用于计算自然对数的底
    if dim in ("col", "cols", "column", "columns"):
        x_norm = x - x.mean(axis=0)
    elif dim in ("row", "rows"):
        x_norm = (x.transpose() - x.mean(axis=1)).transpose()
    else:
        x_norm = x - pd.Series(x.values.reshape(-1)).mean(skipna=True)
    return x_norm
    
def zscore_normalize(x:pd.core.frame.DataFrame, dim="row"):
    '''
    ## 函数功能:实现对于数据表的Z-Score标准化,依据均值及标准差将原始进行缩放，缩放后均值$\mu$为0，标准差$\sigma$为1.
    ## 计算公式:$x_norm=\frac{x-x_mean}{x_std}$
    ## 备注:
    ## 1.函数输入输出均为pandas.DataFrame格式;
    ## 2.本函数需要dim作为输入参数,参数定义为:
    ##    --("col", "cols", "column", "columns"):使用列相关值计算最终结果;
    ##    --("row", "rows"):使用行相关值计算最终结果;
    ##    --其他参数:使用数据表的相关值计算最终结果.
    ## **WARING**:使用本方法将产生负值，之后不能使用对数形式的数据格式转换.
    '''
    # axis=0表示每列取最大值最小值，axis=1表示每行取最大值最小值
    if dim in ("col", "cols", "column", "columns"):
        x_norm = (x - x.mean(axis=0)) / (x.std(axis=0, ddof=1))
    elif dim in ("row", "rows"):
        x_norm = ((x.transpose() - x.mean(axis=1).transpose()) /
                  (x.std(axis=1, ddof=1).transpose())).transpose()
    else:
        x_norm = (x - np.mean(np.array(x), axis=None)) / (
            np.std(np.array(x), axis=None, ddof=1))
    return x_norm

def IQR_normalize(x:pd.core.frame.DataFrame, dim="row"):
    '''
    ## 函数功能:实现对于数据表的IQR标准化,将数据的四分位距interquartile-range(IQR)缩放为1，中值缩放为0.
    ## 计算公式:$x_norm=\frac{x-median(x)}{x_0.75-x_0.25}$
    ## 备注:
    ## 1.函数输入输出均为pandas.DataFrame格式;
    ## 2.本函数需要dim作为输入参数,参数定义为:
    ##    --("col", "cols", "column", "columns"):使用列相关值计算最终结果;
    ##    --("row", "rows"):使用行相关值计算最终结果;
    ##    --其他参数:使用数据表的相关值计算最终结果.
    '''
    if dim in ("col", "cols", "column", "columns"):
        x_norm = (x - x.median(axis=0)) / (x.quantile(0.75, axis=0) -
                                               (x.quantile(0.25, axis=0)))
    elif dim in ("row", "rows"):
        x_norm = ((x.transpose() - x.transpose().median()) / (
            x.quantile(0.75, axis=1) - x.quantile(0.25, axis=1))).transpose()
    else:
        x_norm = (x - x.median(axis=None)) / (
            np.percentile(x, 75, axis=None) - np.percentile(x, 25, axis=None))
    return x_norm

def quantile_normalize(x:pd.core.frame.DataFrame):
    '''
    ## 函数功能:实现对于数据表的Quantile标准化
    ## 备注:
    ## 1.函数输入输出均为pandas.DataFrame格式;
    ## 2.本函数不需要dim作为输入参数.
    '''
    from preprocessproteomics.quantile_normalize import quantile_normalize
    x_norm = pd.DataFrame(quantile_normalize(x),index=x.index,columns=x.columns)
    return x_norm

# 汇总函数
def norm_sample(dataframe:pd.core.frame.DataFrame,
                method="quantile_normalize"):
    """
    ## 函数功能:实现对于数据表列的标准化
    """
    try:
        if method in ("mean_normalize","mean"):
            normalize_dataframe = mean_normalize(x=dataframe,dim="col")
        elif method in ("median_normalize","median"):
            normalize_dataframe = median_normalize(x=dataframe,dim="col")
        elif method in ("max_normalize","max"):
            normalize_dataframe = max_normalize(x=dataframe,dim="col") 
        elif method in ("fot_normalize","fot"):
            normalize_dataframe = fot_normalize(x=dataframe,dim="col") 
        elif method in ("quantile_normalize","quantile"):
            normalize_dataframe = quantile_normalize(x=dataframe) 
        # dictNormalize = normalize_dataframe.reset_index().to_dict(orient="list")
        return normalize_dataframe
    except Exception as e:
        print(e)
        raise ValueError('Parameter "method" must in: "mean_normalize","median_normalize","max_normalize","fot_normalize","quantile_normalize".')
        
def norm_protein(dataframe:pd.core.frame.DataFrame,
                 method="zscore_normalize"):
    """
    ## 函数功能:实现对于数据表列的标准化
    """
    try:
        if method in ("clr_normalize","clr"):
            normalize_dataframe = clr_normalize(x=dataframe,dim="row") 
        elif method in ("max_min_normalize","max-min"):
            normalize_dataframe = max_min_normalize(x=dataframe,dim="row") 
        elif method in ("zscore_normalize","zscore"):
            normalize_dataframe = zscore_normalize(x=dataframe,dim="row")
        elif method in ("IQR_normalize","IQR"):
            normalize_dataframe = IQR_normalize(x=dataframe,dim="row") 
        dictNormalize = normalize_dataframe.reset_index().to_dict(orient="list")
        return dictNormalize
    except Exception as e:
        print(e)
        raise ValueError('Parameter "method" must in: "max_min_normalize","zscore_normalize","IQR_normalize".')
        
# if __name__ == "__main__":
#     dataframe = pd.read_csv(os.path.join(os.getcwd(),"Proteomics_Normalization_Impute_TestFile.csv"),index_col=[0],header=[0,1])
#     norm_protein(dataframe,method="zscore_normalize")
