from django.test import TestCase
from django.test import Client
import pandas as pd
from fgvis.settings import SERVER_TEST_DIR
import json

class SuccessProteomicsDiffAnalysis(TestCase):
  def setUp(self):
    self.client = Client()
    valuesDic = {
      "sample1": [1, 2, 3, 4], 
      "sample2": [5, 6, 7, 8],
      "sample3": [1, 3, 3, 3],
      "sample4": [2, 3, 2, 4],
      "sample5": [1, 3, 4, 5],
      "sample6": [1, 3, 3, 2]
    }
    genes = ["gene1", "gene3", "gene4", "gene2"]
    baseSamples   = ["sample1", "sample3", "sample5"]
    targetSamples = ["sample2", "sample4", "sample6"]
    self.request = {
      "valuesDic":      valuesDic,
      "genes":          genes,
      "baseSamples":    baseSamples,
      "targetSamples":  targetSamples,
      "experimentType": "Protein profiling by Mass Spec",
      "diffSoftware":   "writtenByUs",
    }
  def testProteomicsOneGroupPairDiffViewMedianTbonferroni(self):
    self.request["diffAnalysisSettings"] = {
        "FCcalMethod":     "median",
        "pValuCalMethod":  "student-t",
        "pValueAdjMethod": "bonferroni",
    }
    response = self.client.post("/restful/diffAnalysis/localOneGroupPair/",
                           self.request,
                           content_type = "application/json")
    print(response.json())
  def testProteomicsOneGroupPairDiffViewMeanTbonferroni(self):
    self.request["diffAnalysisSettings"] = {
        "FCcalMethod":     "mean",
        "pValuCalMethod":  "student-t",
        "pValueAdjMethod": "bonferroni",
    }

    response = self.client.post("/restful/diffAnalysis/localOneGroupPair/",
                           self.request,
                           content_type = "application/json")
    print(response.json())
  def testProteomicsOneGroupPairDiffViewMeanWbonferroni(self):
    self.request["diffAnalysisSettings"] = {
        "FCcalMethod":     "mean",
        "pValuCalMethod":  "welch-t",
        "pValueAdjMethod": "bonferroni",
    }

    response = self.client.post("/restful/diffAnalysis/localOneGroupPair/",
                           self.request,
                           content_type = "application/json")
    print(response.json())
  def testProteomicsMultipleGroupPairs(self):
    valuesDic = {
      "sample1": [1, 2, 3, 4], 
      "sample2": [5, 6, 7, 8],
      "sample3": [1, 3, 3, 3],
      "sample4": [2, 3, 2, 4],
      "sample5": [1, 3, 4, 5],
      "sample6": [1, 3, 3, 2]
    }
    genes = ["gene1", "gene3", "gene4", "gene2"]
    groupPairs = [
      {
        "baseGroup":   "group1",
        "targetGroup": "group2",
      },
      {
        "baseGroup":   "group1",
        "targetGroup": "group3",
      },
    ]
    groups2samples = {
      "group1": ["sample1", "sample2", "sample3"],
      "group2": ["sample4", "sample5", "sample6"],
      "group3": ["sample2", "sample5", "sample6"]
    }
    request = {
      "valuesDic":      valuesDic,
      "genes":          genes,
      "groupPairs":     groupPairs,
      "groups2samples": groups2samples,
      "experimentType": "Protein profiling by Mass Spec",
      "diffSoftware":   "writtenByUs",
      "diffAnalysisSettings": {
          "FCcalMethod":     "mean",
          "pValuCalMethod":  "student-t",
          "pValueAdjMethod": "bonferroni",
      }
    };

    response = self.client.post("/restful/diffAnalysis/localMultipleGroupPairs/",
                           request,
                           content_type = "application/json")
    print(response.json())
    
class SuccessDiffAnalysis(TestCase):
  def setUp(self):
    self.client = Client()
  def testRnaseqdiffusecounts(self):
    edagCountsFrame = pd.read_csv(SERVER_TEST_DIR + "/RNA-seq/test_counts.txt",
                                  sep = "\t")
    edagCountsFrame = edagCountsFrame.set_index("Gene")

    genes     = edagCountsFrame.index.to_list()
    countsDic = edagCountsFrame.to_dict("list")
    baseSamples   = ['W1_count', 'W2_count', 'W3_count']
    targetSamples = ['K1_count', 'K2_count', 'K3_count']

    request = {
      "countsDic":    countsDic,
      "genes":        genes,
      "baseSamples":  baseSamples,
      "targetSamples":targetSamples,
    }
    response = self.client.post("/restful/diffAnalysis/rnaseqdiffusecounts/",
                           request,
                           content_type = "application/json")
    print(response.json()["diffResult"])
  def testLocalDataOneGroupPairDiffView(self):
    edagCountsFrame = pd.read_csv(SERVER_TEST_DIR + "/RNA-seq/test_counts.txt",
                                  sep = "\t")
    edagCountsFrame = edagCountsFrame.set_index("Gene")

    genes     = edagCountsFrame.index.to_list()
    countsDic = edagCountsFrame.to_dict("list")
    baseSamples   = ['W1', 'W2', 'W3']
    targetSamples = ['K1', 'K2', 'K3']
    print(countsDic.keys())
    request = {
      "valuesDic":      countsDic,
      "genes":          genes,
      "baseSamples":    baseSamples,
      "targetSamples":  targetSamples,
      "experimentType": "RNA-seq of coding RNA",
      "diffSoftware":   "deseq2",
    }
    response = self.client.post("/restful/diffAnalysis/localOneGroupPair/",
                           request,
                           content_type = "application/json")
    print(len(response.json()["diffResults"]["Gene.ID"]))
  
  def testLocalAffyDataOneGroupPairDiffView(self):
    valuesFrame = pd.read_csv(SERVER_TEST_DIR + "/Microarray/normalizedExprs.txt",
                              sep = "\t")
    valuesFrame = valuesFrame.set_index("ID")
    valuesDic   = valuesFrame.to_dict("list")
    genes       = valuesFrame.index.to_list()

    with open(SERVER_TEST_DIR + "/Microarray/datasetInfo.json", "r") as fileOpen:
      datasetInfo = json.load(fileOpen)
      print(datasetInfo["groups"])

    annoLibrary   = "mogene21sttranscriptcluster"
    baseSamples   = datasetInfo["groups"][0]["samples"]
    targetSamples = datasetInfo["groups"][1]["samples"]
    request = {
      "valuesDic":     valuesDic, 
      "genes":         genes,
      "annoLibrary":   annoLibrary,
      "baseSamples":   baseSamples,
      "targetSamples": targetSamples,
      "diffSoftware":  "limma"
    }
    response = self.client.post("/restful/diffAnalysis/localArrayOneGroupPair/",
                                request,
                                content_type = "application/json")                            
    print(response.json()["diffResults"])


  def testLocalDataMultipleGroupPairsDiffView(self): 
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

    request = {
      "valuesDic":      countsDic,
      "genes":          genes,
      "groupPairs":     [
        {
          "baseGroup":   "WT",
          "targetGroup": "KO",
        },
        {
          "baseGroup":  "KO",
          "targetGroup": "WT"
        }
      ],
      "groups2samples": {
        "WT": ["W1", "W2", "W3"],
        "KO": ["K1", "K2", "K3"],
      },
      "experimentType": "rna-seq",
      "diffSoftware":   "deseq2",
    }
    response = self.client.post("/restful/diffAnalysis/localMultipleGroupPairs/",
                                request,
                                content_type = "application/json")
    self.assertEqual(response.status_code, 200)
    print(response.json()["diffResultList"][0].keys())
    
  def testProteomicsOneGroupPairDiffView(self):
    valuesDic = {
      "sample1": [1, 2, 3, 4], 
      "sample2": [5, 6, 7, 8],
      "sample3": [1, 3, 3, 3],
      "sample4": [2, 3, 2, 4],
      "sample5": [1, 3, 4, 5],
      "sample6": [1, 3, 3, 2]
    }
    genes = ["gene1", "gene3", "gene4", "gene2"]
    baseSamples   = ["sample1", "sample3", "sample5"]
    targetSamples = ["sample2", "sample4", "sample6"]

    request = {
      "valuesDic":      valuesDic,
      "genes":          genes,
      "baseSamples":    baseSamples,
      "targetSamples":  targetSamples,
      "experimentType": "Protein profiling by Mass Spec",
      "diffSoftware":   "writtenByUs",
      "diffAnalysisSettings": {
        "FCcalMethod":     "median",
        "pValuCalMethod":  "student-t",
        "pValueAdjMethod": "bonferroni",
      }
    }

    response = self.client.post("/restful/diffAnalysis/localOneGroupPair/",
                           request,
                           content_type = "application/json")
    print(response.json())



  def testRemoteOneGroupDiffAnalysis(self):
    datasetID = "GSE62208"
    IDtype    = "hugene20sttranscriptcluster"
    baseSamples   = ["GSM1522519", "GSM1522520", "GSM1522521"]
    targetSamples = ["GSM1522522", "GSM1522523", "GSM1522524"]
    
    request = {
      "database":  "GEO",
      "datasetID":  datasetID,  
      "IDtype":     IDtype,
      "experimentType": "Expression profiling by array", 
      "baseSamples":    baseSamples, 
      "targetSamples":  targetSamples,
    }

    response = self.client.post("/restful/diffAnalysis/remoteOneGroupDiffAnalysis/",
                            request,
                            content_type = "application/json")
    self.assertEqual(response.json()["diffResult"]["logFC"][0],5.03150358941771)
