import sys,os,re
import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter
import json
from itertools import combinations
from lifelines import CoxPHFitter
from lifelines.statistics import pairwise_logrank_test

'''
## Writen by Kaikun Xu
## 功能:本节主要用于实现JavaScript-D3前端KM曲线的数据准备.
## 注释:
## 1. 输入值为json文件的url，返回值为json;
## 2. 输入数据表至少需要包含两类数据：
##    + 临床信息列：
##       - 终点状态列--死亡/未死亡，复发/未复发等，需使用0/1表示；
##       - 随访时间列--时间信息，应为float类型；
##    + 分组列：
##      - 可使用Proteomis_Surivial_Split.py程序对蛋白质组数据的高低表达分组后进行分析；
##      - 可基于临床指标(类别)进行分析；
'''        

# def generateKMCurveTable(dataJson:dict,
#                          event:str="OS",
#                          status:str="OS Status",
#                          condition:str="SOAT1"):
#     """
#     ## 本函数用于生成JavaScript-D3绘制前端KM曲线的数据表
#     ## 注释：
#     ##   + event及status为用于进行生存分析的临床终点信息；
#     ##   + condition为用于分组的数据列，应为0/1离散型变量；
#     """
#     dataJson = pd.DataFrame.from_dict(dataJson)
#     assert (condition in dataJson.columns), "The protein used for KM curve drawing should be a column of the submitted table"
#     kmDF = pd.DataFrame()
#     for subgroup in dataJson[condition].unique():
#         KMSub = dataJson[dataJson[condition]==subgroup].dropna(subset=[event,status,condition],how="any")
#         kmf = KaplanMeierFitter()
#         label = "{0} (n={1})".format(subgroup,KMSub.shape[0])
#         kmf.fit(KMSub[event], KMSub[status], label=label)
#         kmSub = pd.concat([kmf.survival_function_,kmf.event_table.drop(columns=["entrance","removed"])],axis=1).rename_axis(
#             index=["TimeLine"]).rename(
#             columns={label:"Probability","at_risk":"Number at Risk","observed":"Obversed","censored":"Censored"}).reset_index()
#         kmSub.insert(loc=0,column="Label",value=label)
#         kmDF = pd.concat([kmDF,kmSub],axis=0)
#     KMdict = kmDF.reset_index(drop=True).to_dict(orient="list") 
#     return KMdict

def generateKMinfoForPlot(eventTimes, eventStatus, highOrLows):
  '''
  # Modified from generateKMCurveTable written by Kaikun Xu
  # Input: 
  #   A dictionary
  #     + event, a list, 临床终点的时间 
  #     + status, a list, 临床终点的状态
  #     + highOrLow, a list, 蛋白在高表达组还是低表达组
  '''
  kmDF = pd.DataFrame()
  for subgroup in set(highOrLows):
    subEventTimes  = []
    subEventStatus = [] 
    for highOrLow, eventTime, eventStatu in zip(highOrLows,eventTimes, eventStatus):
      if highOrLow == subgroup:
        subEventTimes.append(eventTime)
        subEventStatus.append(eventStatu)

    kmf = KaplanMeierFitter()
    labels = "{0} (n={1})".format(subgroup, len(subEventStatus))
    kmf.fit(subEventTimes, subEventStatus, label = labels)
    kmSub = pd.concat([kmf.survival_function_,kmf.event_table.drop(columns=["entrance","removed"])],axis=1).rename_axis(
            index=["TimeLine"]).rename(
            columns={labels:"Probability","at_risk":"Number at Risk","observed":"Obversed","censored":"Censored"}).reset_index()
    kmSub.insert(loc=0,column="Label",value=labels)
    kmDF = pd.concat([kmDF,kmSub],axis=0)
  return kmDF.reset_index(drop=True).to_dict(orient="list") 



# def generateKMCurveTable(eventTimes, eventStatus, categories, categoryOrder):
#   '''
#   Input:
#     eventTimes: a list
#     status: a list,
#     categories: categories for each patient
#     categoryOrder: a list
#   '''

# def generateKMCurveText(eventTimes, eventStatus, categories, categoryOrder):




# if __name__=="main":
#     condition="SOAT1"; event="DFS"; status="DFS Status"
#     jsonFilePath = os.path.join(os.getcwd(),"Proteomics_SurvivalAnalysis_KMCurve_TestFile.json")
#     with open(jsonFilePath) as file:
#         dataJson = json.load(file)
#     jsonKM = generateKMCurveTable(dataJson,event=event,status=status,condition=condition)
#     jsonKM