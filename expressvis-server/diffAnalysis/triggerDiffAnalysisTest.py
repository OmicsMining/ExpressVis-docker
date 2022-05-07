from django.test import TestCase
import pandas as pd
from fgvis.settings import SERVER_TEST_DIR
from diffAnalysis.triggerDiffAnalysis import affyDiffAnalysisMultipleGroupsWithSeriesAcc, \
  affyDiffAnalysisOneGroupPairWithSeriesAcc, deseq2DiffAnalysisWithCounts, \
  deseq2DiffAnalysisWithCountsMultipleGroupPairs, affyDiffAnalysisOneGroupPairWithValues
import json

class DiffAnalysisTest(TestCase):
  def testAffyDiffAnalysisMultipleGroups(self):
    geoSeriesAcc   = "GSE62208"
    
    diffGroupPairs = [
      {"baseGroup": ["GSM1522519","GSM1522520","GSM1522521"], 
       "targetGroup": ["GSM1522522", "GSM1522523", "GSM1522524"]
       },
      {"baseGroup": ["GSM1522519","GSM1522520","GSM1522521"], 
       "targetGroup": ["GSM1522525", "GSM1522526", "GSM1522527"]},
      {"baseGroup": ["GSM1522519","GSM1522520","GSM1522521"], 
       "targetGroup": ["GSM1522533","GSM1522534","GSM1522535"]},
    ]

    diffResults = affyDiffAnalysisMultipleGroupsWithSeriesAcc(
                    geoSeriesAcc   = geoSeriesAcc, 
                    diffGroupPairs = diffGroupPairs)
    # test 
    # print(diffResults)
    # diffResults = json.loads(diffResults)
    # print(json.loads(diffResults[0])[0]["P.Value"][1:100])
  def testAffyDiffAnalysisOneGroupPair(self):
    geoSeriesAcc  = "GSE62208"
    annoLibrary   = "hugene20sttranscriptcluster.db"
    baseSamples   = ["GSM1522519", "GSM1522520", "GSM1522521"]
    targetSamples = ["GSM1522522", "GSM1522523", "GSM1522524"]
    
    diffResult = affyDiffAnalysisOneGroupPairWithSeriesAcc( 
                          geoSeriesAcc  = geoSeriesAcc, 
                          annoLibrary   = annoLibrary,
                          baseSamples   = baseSamples,
                          targetSamples = targetSamples)

  def testAffyDiffAnalysisOneGroupPairWithValues(self):
    valuesFrame = pd.read_csv(SERVER_TEST_DIR + "/Microarray/normalizedExprs.txt",
                              sep = "\t")
    valuesFrame = valuesFrame.set_index("ID")
    valuesDic   = valuesFrame.to_dict("list")
    genes       = valuesFrame.index.to_list()

    with open(SERVER_TEST_DIR + "/Microarray/datasetInfo.json", "r") as fileOpen:
      datasetInfo = json.load(fileOpen)
      print(datasetInfo["groups"])

    annoLibrary   = "mogene21sttranscriptcluster.db"
    baseSamples   = datasetInfo["groups"][0]["samples"]
    targetSamples = datasetInfo["groups"][1]["samples"]
    diffResult = affyDiffAnalysisOneGroupPairWithValues(
      valuesDic     = valuesDic, 
      genes         = genes,
      annoLibrary   = annoLibrary,
      baseSamples   = baseSamples,
      targetSamples = targetSamples,
    )
    print(diffResult["adj.P.Val"])
    


  def testDeseq2DiffAnalysisWithCounts(self):
    edagCountsFrame = pd.read_csv(SERVER_TEST_DIR + "/EDAG_counts.txt",
                                  sep = "\t")
    edagCountsFrame = edagCountsFrame.set_index("Gene")

    genes     = edagCountsFrame.index.to_list()
    countsDic = edagCountsFrame.to_dict("list")
    baseSamples   = ['W1_count', 'W2_count', 'W3_count']
    targetSamples = ['K1_count', 'K2_count', 'K3_count']

    diffResultDic = deseq2DiffAnalysisWithCounts(
      countsDic     = countsDic,
      genes         = genes,
      baseSamples   = baseSamples,
      targetSamples = targetSamples
    )
    print(diffResultDic)
    diffResultFrame = pd.DataFrame.from_dict(diffResultDic)
    diffResultFrame.to_csv(SERVER_TEST_DIR + "/result/EDAG_KO_VS_WT.txt",
                           sep  = "\t",
                           index = False,)
  
  def testDeseq2DiffAnalysisWithCountsMultipleGroupPairs(self):
    edagCountsFrame = pd.read_csv(SERVER_TEST_DIR + "/RNA-seq/test_counts.txt",
                                  sep = "\t")
    edagCountsFrame = edagCountsFrame.set_index("Gene")

    genes     = edagCountsFrame.index.to_list()
    countsDic = edagCountsFrame.to_dict("list")

    diffGroupPairs = [
      {
        "baseGroup":   ['W1', 'W2', 'W3'],
        "targetGroup": ['K1', 'K2', 'K3'],
      },
      {
        "baseGroup":   ['K1', 'K2', 'K3'],
        "targetGroup": ['W1', 'W2', 'W3'],
      }
    ]

    diffResults = deseq2DiffAnalysisWithCountsMultipleGroupPairs(
      countsDic      = countsDic,
      genes          = genes,
      diffGroupPairs = diffGroupPairs,
    )
    self.assertEqual(len(diffResults), 2)

    
    
# diffAnalysisTest = DiffAnalysisTest()
# diffAnalysisTest.testDeseq2DiffAnalysisWithCounts()

