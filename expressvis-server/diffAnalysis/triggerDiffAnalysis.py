# trigger differentiall analysis

import requests
import json
from fgvis.settings import DIFF_ANALYSIS_URL


def affyDiffAnalysisMultipleGroupsWithSeriesAcc(geoSeriesAcc, diffGroupPairs):
  '''
  parameters: 
    diffGroupParis:
      an example:
        [
          { "baseGroup": ["GSM1522519","GSM1522520","GSM1522521"], 
            "targetGroup": ["GSM1522522", "GSM1522523", "GSM1522524"]
          },
          { "baseGroup": ["GSM1522519","GSM1522520","GSM1522521"], 
            "targetGroup": ["GSM1522525", "GSM1522526", "GSM1522527"]},
          { "baseGroup": ["GSM1522519","GSM1522520","GSM1522521"], 
            "targetGroup": ["GSM1522533","GSM1522534","GSM1522535"]},
        ]
  return: 
  '''
  # diffanalysis is performed in the server
  requestUrl  = DIFF_ANALYSIS_URL + "arraymultiplediffanalysiswithseriesacc"
  annoLibrary = "hugene20sttranscriptcluster.db"
  requestData = {
    "geoSeriesAcc": geoSeriesAcc,
    "diffGroupPairs": diffGroupPairs,
    "annoLibrary": annoLibrary
  }
  # The result is a json string, contains result of each diffGroupPairs
  requestResult = requests.post(url  = requestUrl, 
                                json = requestData) # use json here, do not use data

  resultList = json.loads(json.loads(requestResult.text)[0])
  return resultList


def affyDiffAnalysisOneGroupPairWithSeriesAcc(geoSeriesAcc, annoLibrary, baseSamples, targetSamples):
  '''
  Parameters:
    baseSamples: an array
  return:
    a dictionary, {"logFC":, "P.Value", "PROBEID"}
  '''
  requestUrl  = DIFF_ANALYSIS_URL + "arrayonegrouppairdiffanalysiswithseriesacc"
  requestData = {
    "geoSeriesAcc":  geoSeriesAcc,
    "annoLibrary":   annoLibrary,
    "baseSamples":   baseSamples,
    "targetSamples": targetSamples
  }

  diffResult = requests.post(url  = requestUrl,
                             json = requestData)
  return json.loads(json.loads(diffResult.text)[0])

def affyDiffAnalysisOneGroupPairWithValues(valuesDic, genes, annoLibrary, baseSamples, targetSamples):
  '''
  
  '''
  requestUrl = DIFF_ANALYSIS_URL + "arrayOneDiffGroupPairWithValues"
  requestData = {
    "valuesDic":     valuesDic,
    "genes":         genes,
    "annoLibrary":   annoLibrary,
    "baseSamples":   baseSamples,
    "targetSamples": targetSamples,
  }

  results = requests.post( url  = requestUrl,
                           json = requestData)
  diffResult = json.loads(json.loads(results.text)[0])
  return diffResult

def deseq2DiffAnalysisWithCounts(countsDic, genes, baseSamples, targetSamples):
  '''
  Send request to r-server and obtain diffresults

  return:
    adictionary, {gene: , foldchange, }
  
  '''
  requestUrl  = DIFF_ANALYSIS_URL + "deseq2WithCounts"
  requestData = {
    "countsDic":     countsDic,
    "genes":         genes,
    "baseSamples":   baseSamples,
    "targetSamples": targetSamples
  }

  results = requests.post(url  = requestUrl, 
                          json = requestData)
  diffResult = json.loads(json.loads(results.text)[0])
  return diffResult

def deseq2DiffAnalysisWithCountsMultipleGroupPairs(countsDic, genes, diffGroupPairs):
  '''
  Return a list
  '''
  requestUrl  = DIFF_ANALYSIS_URL + "deseq2WithCountsMultipleGroupPairs"
  requestData = {
    "countsDic":      countsDic,
    "genes":          genes,
    "diffGroupPairs": diffGroupPairs
  }

  requestResult = requests.post(url  = requestUrl, 
                                json = requestData)
  resultList = json.loads(json.loads(requestResult.text)[0])
  return resultList
  