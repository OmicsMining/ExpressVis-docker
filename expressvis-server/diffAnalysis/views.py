from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from diffAnalysis.proteomicsDiffAnalysisAdapter import proteomicsDiffAnalysis, proteomicsDiffAnalysisMultipleGroupPairs

from diffAnalysis.triggerDiffAnalysis import deseq2DiffAnalysisWithCounts, affyDiffAnalysisMultipleGroupsWithSeriesAcc, \
  affyDiffAnalysisOneGroupPairWithSeriesAcc, deseq2DiffAnalysisWithCountsMultipleGroupPairs, \
    affyDiffAnalysisOneGroupPairWithValues


# Create your views here.
class LocalDataOneGroupPairDiffView(APIView):
  def post(self, request, *args, **kwargs):
    '''
    valuesDic:      Map<string, number[]>; // for microarray, normalized values (log2);  for RNA-seq, counts; for Proteomics data, normalized values
    genes:          string[];
    baseSamples:    string[]; 
    targetSamples:  string[];
    experimentType: string;
    diffSoftware:   string;
    diffAnalysisSettings: Dictionary, keys are related with diffSoftware
    '''
    requestData  = request.data
    diffSoftware = requestData["diffSoftware"]
    if diffSoftware == "deseq2":
      diffResult = deseq2DiffAnalysisWithCounts(
        countsDic     = requestData["valuesDic"],
        genes         = requestData["genes"],
        baseSamples   = requestData["baseSamples"],
        targetSamples = requestData["targetSamples"],
      )
    elif diffSoftware == "writtenByUs":
      # change this later
      diffAnalysisSettings = requestData["diffAnalysisSettings"]
      diffResult = proteomicsDiffAnalysis(
        valuesDic = requestData["valuesDic"],
        proteins  = requestData["genes"],
        baseSamples   = requestData["baseSamples"],
        targetSamples = requestData["targetSamples"],
        foldchangeMethod = diffAnalysisSettings["FCcalMethod"], 
        statisticsMethod = diffAnalysisSettings["pValuCalMethod"], 
        multipleTestsCorrectMethod = diffAnalysisSettings["pValueAdjMethod"],
      );
    return Response({"diffResults":  diffResult, 
                     "diffSoftware": diffSoftware})

class LocalAffyDataOneGroupPairDiffView(APIView):
  '''
  Diff analysis for local affy (Microarray) data
  '''
  def post(self, request, *args, **kwargs):
    requestData = request.data
    diffSoftware = requestData["diffSoftware"]
    if diffSoftware == "limma":
      diffResult = affyDiffAnalysisOneGroupPairWithValues(
        valuesDic     = requestData["valuesDic"],
        genes         = requestData["genes"],
        annoLibrary   = requestData["annoLibrary"] + ".db",
        baseSamples   = requestData["baseSamples"],
        targetSamples = requestData["targetSamples"],
      )
    else:
      pass
    return Response({"diffResults":  diffResult, 
                     "diffSoftware": diffSoftware})


def convertClientGroupPairs2RdiffGroupPairs(clientGroupPairs, groups2samples):
  '''
  input: 
    clientGroupPairs, [
      {
        "baseGroup":  "groupName",
        "targetGroup": "groupName",
      },
    ],
    groups2samples: {
      "groupName": ["sampleName",]
    }
  '''
  diffGroupPairList = []
  for eachPair in clientGroupPairs:
    diffGroupPairList.append({
      "baseGroup":   groups2samples[eachPair["baseGroup"]],
      "targetGroup": groups2samples[eachPair["targetGroup"]]
    })
  
  return diffGroupPairList
class LocalDataMultipleGroupPairsDiffView(APIView):
  def post(self, request, *args, **kwargs):
    '''
    requestData:
      groupPairs: [ {baseGroup, targetGroup} ],
      groups2samples: {},
      valuesDic: 
      diffSoftware: string
      diffAnalysisSettings: Dictionary, keys are related with diffSoftware
    '''
    requestData  = request.data
    # transform group pairs into a list of dictionary
    if requestData["diffSoftware"] == "deseq2":
      diffGroupPairList = convertClientGroupPairs2RdiffGroupPairs(
        requestData["groupPairs"], requestData["groups2samples"])
      diffResultList = deseq2DiffAnalysisWithCountsMultipleGroupPairs(
        countsDic      = requestData["valuesDic"],
        genes          = requestData["genes"],
        diffGroupPairs = diffGroupPairList,
      )
    elif requestData["diffSoftware"] == "limma":
      pass
    elif requestData["diffSoftware"] == "writtenByUs":
      # diffAnalysisSettings = requestData["diffAnalysisSettings"]
      diffResultList = proteomicsDiffAnalysisMultipleGroupPairs(
        valuesDic  = requestData["valuesDic"],
        proteins   = requestData["genes"],
        groupPairs = requestData["groupPairs"],
        groups2samples = requestData["groups2samples"],
        # foldchangeMethod = diffAnalysisSettings["FCcalMethod"], 
        # statisticsMethod = diffAnalysisSettings["pValuCalMethod"], 
        # multipleTestsCorrectMethod = diffAnalysisSettings["pValueAdjMethod"],
      )
      # todo: add settings from the frontent later 
    return Response({"diffSoftware": requestData["diffSoftware"],
                     "diffResultList": diffResultList})
    


class RnaseqDiffUseCounts(APIView):
  def post(self, request, *args, **kwargs):
    '''
    Parameters:
      countsDic: An dictionary, keys are the samples
      genes:     list, gene IDs
      baseSamples: samples in base group
      targetSamples: samples in the target group
    '''
    requestData = request.data
    
    diffResult = deseq2DiffAnalysisWithCounts(
      countsDic     = requestData["countsDic"],
      genes         = requestData["genes"],
      baseSamples   = requestData["baseSamples"],
      targetSamples = requestData["targetSamples"]
    )

    return Response({"diffResult": diffResult})

class RemoteOneGroupPairDiffView(APIView):
  def post(self, request, *args, **kwargs):
    '''
    Parameters:
      database:  string
      datasetID: string,  
      IDtype: string,
      experimentType: string, 
      baseSamples:    string[], 
      targetSamples:  string[]
    '''
    requestData  = request.data
    diffSoftware = requestData["diffSoftware"]
    if requestData["database"] == "GEO" and requestData["experimentType"] == "Expression profiling by array":
      diffResult = affyDiffAnalysisOneGroupPairWithSeriesAcc(
                         geoSeriesAcc  = requestData["datasetID"],
                         annoLibrary   = requestData["IDtype"] + ".db", #! add .db
                         baseSamples   = requestData["baseSamples"],
                         targetSamples = requestData["targetSamples"],
                         )
      return Response({"diffResults":  diffResult, 
                       "diffSoftware": diffSoftware})

class OneGroupDiffAnalysis(APIView):
  def post(self, request, *args, **kwargs):
    '''
    Parameters:
      database:  string
      datasetID: string,  
      IDtype: string,
      experimentType: string, 
      baseSamples:    string[], 
      targetSamples:  string[]
    '''
    requestData = request.data
    if requestData["database"] == "GEO" and requestData["experimentType"] == "Expression profiling by array":
      diffResult = affyDiffAnalysisOneGroupPairWithSeriesAcc(
                         geoSeriesAcc  = requestData["datasetID"],
                         annoLibrary   = requestData["IDtype"] + ".db", # add .db !!!
                         baseSamples   = requestData["baseSamples"],
                         targetSamples = requestData["targetSamples"],
                         )
      return Response({"diffResult": diffResult})


