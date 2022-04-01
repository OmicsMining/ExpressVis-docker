'''
These code is written by Kaikun Xu.
'''
import sys,os,re
import numpy as np
import pandas as pd
import json

def foldchange(dataframe:pd.core.frame.DataFrame,experiment:str=None,control:str=None,method:str="mean"):
    """
    ## 函数功能：用于多蛋白两组间foldchange(ratio)的计算
    ## method可选列表：["mean","median"]
    """
    if method=="mean": foldChange = dataframe.apply(
        lambda x: x[experiment].mean(skipna=True)/x[control].mean(skipna=True),axis=1)
    elif method=="median": foldChange = dataframe.apply(
        lambda x: x[experiment].median(skipna=True)/x[control].median(skipna=True),axis=1)
    foldChange = pd.Series(foldChange,index=dataframe.index,name="foldChange")
    return foldChange

def chooseStatisticsMethod(dataframe:pd.core.frame.DataFrame,experiment:str=None,control:str=None,pvalCut:float=0.05):
    """
    函数功能：自动确定各蛋白应使用的统计学检验方法:
    ## *此函数仅在differentialExpressedAnalysis()函数method="auto"时被使用*;
    ## student t-test:全组别满足正态性，组别间满足方差齐性;
    ## welch t-test:仅满足正态性;
    ## wilcoxon ranksums-test:不满足正态性
    """
    def shapiroWikiTest(dataframe:pd.core.frame.DataFrame,experiment:str=None,control:str=None,pvalCut:float=0.05):
        """
        函数功能：正态性检验
        ## 使用stats.shapiro()函数，即Shapiro-Wilk检验（W检验);
        ## 正态性检验原假设为输入数据分布满足正态性;
            ## + p-value > pvalcutoff时接受原假设满足正态性;
            ## + 该蛋白在全部组别中均满足正态性，记作True，否则为False;
            ## + 若有效值少于3例，返回空值(空值会被认定为False,即不满足正态性)
        """
        import scipy.stats as stats
        pvalue = pd.DataFrame(index=dataframe.index)
        for groupID in [experiment,control]:
            pvalue = pd.concat([pvalue,dataframe.apply(lambda x:stats.shapiro(x[groupID].dropna()).pvalue if len(x[groupID].dropna())>=3 else np.nan,axis=1)],axis=1)
        resBool = pd.cut(pvalue.max(axis=1),bins=[-np.inf,pvalCut,np.inf],right=False,labels=[False,True]).fillna(False)
        return resBool
    def leveneTest(dataframe:pd.core.frame.DataFrame,experiment:str=None,control:str=None,pvalCut:float=0.05):
        """
        函数功能：方差齐性检验
        ## 使用stats.leneve()函数，即Leneve's检验;
        ## 方差齐性检验原假设为输入两数据分布满足方差齐性；
            ## + p-value > pvalcutoff记作True,即接受原假设满足方差齐性;
            ## + p-value <= pvalcutoff及p-value==np.nan记作False
        """
        import scipy.stats as stats
        pvalue = dataframe.apply(lambda x:stats.levene(x[experiment].dropna(),x[control].dropna()).pvalue,axis=1)
        resBool = pd.cut(pvalue,bins=[-np.inf,pvalCut,np.inf],right=False,labels=[False,True]).fillna(False)
        return resBool
    def chooesMethod(x):
        """
        # 确定差异比较的统计分析方法
        """
        if x["normality"]==False: return "wilcoxon ranksums"
        elif all([x["normality"]==True,x["homoVariance"]==True]):return "student-t"
        elif all([x["normality"]==True,x["homoVariance"]==False]):return "welch-t"
        
    methodDF = pd.DataFrame(index=dataframe.index)
    methodDF["normality"] = shapiroWikiTest(dataframe=dataframe,experiment=experiment,control=control,pvalCut=pvalCut)
    methodDF["homoVariance"] = leveneTest(dataframe=dataframe.loc[methodDF[methodDF["normality"]==True].index],
                                          experiment=experiment,control=control,pvalCut=pvalCut)
    methodSeries = methodDF.apply(lambda x:chooesMethod(x),axis=1)
    return methodSeries

def differentialExpressedAnalysis(dataframe,experiment=None,control=None,method:str="ranksums"):
    """
    ## 本函数用于蛋白质组学的差异分析：
    ## + 总体均数的检验——参数检验tTest()/非参数检验ranksumTest();
    ## + method参数可选列表:["student-t","welch-t","ranksums","auto"]
    ## + method=="auto"时，将调用chooseStatisticsMethod()函数为各个蛋白质选取合适的分析方法
    """
    def tTest(dataframe:pd.core.frame.DataFrame,
              experiment:str=None,control:str=None, # 指定实验组与对照组
              equalVar:bool=False # 两组别是否满足方差齐性，默认为False,即执行Welch t-test，若为True,执行Student t-test
             ):
        """
        函数功能：用于多蛋白两组间的welch-t/student-t test检验，返回对应的pd.Series格式的p-value;
        """
        import scipy.stats as stats

        pvalue = stats.ttest_ind(dataframe[experiment].transpose(),dataframe[control].transpose(),
                                 nan_policy="omit",equal_var=equalVar).pvalue#.data, deleted by Liuxian
        pvalue = pd.Series(pvalue,index=dataframe.index,name="p-value")
        return pvalue
    def ranksumTest(dataframe:pd.core.frame.DataFrame,experiment:str=None,control:str=None):
        """
        ## 函数功能：用于多蛋白两组间的rank-sum test检验，返回对应的pd.Series格式的p-value;
        """
        import scipy.stats as stats
        pvalue = pd.Series(dataframe.apply(
            lambda x: stats.ranksums(x[experiment].dropna(),x[control].dropna()).pvalue,axis=1),name="p-value")
        return pvalue
    if method in ("ranksums","wilcoxon ranksums"): 
        pvalueSeries = ranksumTest(dataframe=dataframe,experiment=experiment,control=control)
    elif method in ("student-t"): 
        pvalueSeries = tTest(dataframe=dataframe,experiment=experiment,control=control,equalVar=True)
    elif method in ("welch-t"): 
        pvalueSeries = tTest(dataframe=dataframe,experiment=experiment,control=control,equalVar=False)
    elif method in ("auto","Auto"):
        methodSeries = chooseStatisticsMethod(dataframe=dataframe,experiment=experiment,control=control,pvalCut=0.05)
        # TODO: 选择一系列方法的目的是什么？
        indexSorter = methodSeries.index
        pvalueSeries = pd.Series([],index=pd.MultiIndex(levels=len(dataframe.index.names)*[[]],codes=len(dataframe.index.names)*[[]],names=dataframe.index.names))
        for analysisMethod in methodSeries.unique():
            pvalSub = differentialExpressedAnalysis(dataframe=dataframe.loc[methodSeries[methodSeries==analysisMethod].index].copy(),
                                                    experiment=experiment,control=control,method=analysisMethod)
            pvalueSeries = pd.concat([pvalueSeries,pvalSub],axis=0)
        pvalueSeries = pvalueSeries.loc[indexSorter]
    return pvalueSeries

def multipleTestsCorrect(series:pd.core.series.Series,method:str="fdr_bh"):
    """
    ## 函数功能：用于p-value的多重假设检验校正，本函数在计算时将忽视缺失值，类似于scipy策略(nan_policy="omit")
    ## method可选列表：["holm-sidak","fdr_bh","bonferroni"]
    """    
    assert (method in ("holm-sidak","fdr_bh","bonferroni")),"Parameter 'method' shoule be in: holm-sidak, fdr_bh, bonferroni"
    from statsmodels.sandbox.stats.multicomp import multipletests
    # nan_policy Link: https://docs.scipy.org/doc/scipy/reference/dev/api-dev/nan_policy.html
    nan_mask = np.isnan(series)
    pvalue = np.empty(series.shape, dtype=np.float64)
    pvalue[~nan_mask] = multipletests(series[~nan_mask],method=method,is_sorted=False,returnsorted=False)[1]
    pvalue[nan_mask] = np.nan
    pvalue = pd.Series(pvalue,index=series.index,name="p-value")
    return pvalue    
    
def proteomicsStatistics(dataframe:pd.core.frame.DataFrame,
                         experiment:str,control:str,
                         foldchangeMethod:str="mean",#计算FoldChange的方法
                         statisticsMethod:str="auto",#统计学检验的方法选择          
                         multipleTestsCorrectMethod:str="fdr_bh"#多重假设检验校正的方法
                        ):
    """
    ## 蛋白质组统计学检验的主函数,返回数据包括如下列：
        ## + FC:Exp/Ctrl两组别的信号强度比值;
        ## + p-value:校正后的差异表达分析的p-value;   
    ## 参数可选列表:
        ## + statisticsMethod: ["student-t","welch-t","ranksums","auto"];
        ## + foldchangeMethod: ["mean","median"];
        ## + multipleTestsCorrectMethod: ["holm-sidak","fdr_bh","bonferroni",None];

    ## LX changed in 211213
      1. 计算log2 fold change
      2. 计算adjusted p value
    """ 
    result = pd.DataFrame(index=dataframe.index)
    result["FoldChange"]     = foldchange(dataframe=dataframe,experiment=experiment,control=control,method=foldchangeMethod)
    result["log2FoldChange"] = np.log2(result["FoldChange"])
    result["P-value"]       = differentialExpressedAnalysis(dataframe=dataframe,experiment=experiment,control=control,method=statisticsMethod)
    result["adjusted P-Value"]  = multipleTestsCorrect(series=result["P-value"],method=multipleTestsCorrectMethod)
    # if multipleTestsCorrectMethod:
    #     result["P-value"] = multipleTestsCorrect(series=result["P-value"],method=multipleTestsCorrectMethod)
    result = result.reset_index().to_dict(orient="list")    
    return result
                         
                         
# if "__name__"=="__main__":                      
#     dataframe = pd.read_csv(os.path.join(os.getcwd(),"Proteomics_Normalization_Impute_TestFile.csv"),header=[0,1],index_col=[0,1])
#     experiment="Tumor";control="Paracancer";foldchangeMethod="mean";statisticsMethod="auto";multipleTestsCorrectMethod="fdr_bh"
#     result = proteomicsStatistics(dataframe=dataframe,experiment=experiment,control=control,
#                                   foldchangeMethod="mean",statisticsMethod="auto",multipleTestsCorrectMethod="fdr_bh")
#     result