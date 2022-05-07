from django.test import TestCase
from django.test import Client
from numpy import NAN
import pandas as pd

from fgvis.settings import SERVER_TEST_DIR

class SuccessPreprocessProteomics(TestCase):
  def setUp(self):
    self.client = Client()
  def testPreprocessProteomicsData(self):
    # 根据需求调整requestData
    requestData = {
       "proteinIDs": ["protein1", "protein2", "protein3", "protein4", "protein5", "protein6", "protein7", "protein8"],
       "samples2intensities": {
         "sample1": [1,  0, 0, 5, 3, 4, 2, 1],
         "sample2": [2,  4, 0, 7, 8, 7, 2, 1],
         "sample3": [10, 9, 0, 7, 6, 5, 0, 1] 
       },
       "groups": [
         {
           "name": "group1",
           "samples": ["sample1", "sample2"],
         },
         {
           "name": "group2",
           "samples": ["sample3"],
         }
       ],
       "preprocessSettings": {
          "filterSettings": {
            "percentage": 0.5,
            "filterType": "each"
          },
          "imputeSettings": {
            "method": "minimum_value",
            "subSetting": 0.02
          },
          "normalizationMethod": "mean_normalize"
       },
       "removeBatchSettings": {
         "ifRemoveBatch": False,
         "samples2batch": {
           "sample1": "batch1",
           "sample2": "batch2",
           "sample3": "batch2"
         },
         "ifUseGroupVariable": True
       }
    }

    response = self.client.post("/restful/preprocess/preprocessProteomics/",
                                requestData,
                                content_type = "application/json")

    expectedResult = {
      "sample1": [1.1, 3.1, 4.1],
      "sample2": [2.1, 5.1, 6.1]
    }
    print(response.json())
    # self.assertEqual(response.json()["normalizedValues"], expectedResult)
  
class SuccessRemoveBatchEffect(TestCase):
  def setUp(self):
    self.client = Client()
  def testRemoveRNAseqBatchEffects(self):
    countsFrame = pd.read_csv(SERVER_TEST_DIR + "/removeBatch/counts.txt",
                              sep = "\t")
    counts_matrix = countsFrame.iloc[:,:-1].to_numpy().tolist()

    phenotypeFrame = pd.read_csv(SERVER_TEST_DIR + "/removeBatch/phenotypeData.txt",
                                 sep = "\t")
    batch = phenotypeFrame["batch"].tolist()
    group = phenotypeFrame["group"].tolist()
    requestData = {
      "values": counts_matrix,
      "batch": batch,
      "group": group,
      "valueType": "counts"
    }

    

    response = self.client.post("/restful/preprocess/removebatcheffect/",
                                requestData,
                                content_type = "application/json")
    print(response.json()["adjustedData"][0:100])
  def testRemoveProteomicsBatchEffects(self):
    requestData = {
       "proteinIDs": ["protein1", "protein2", "protein3", "protein4", "protein5", "protein6", "protein7", "protein8"],
       "samples2intensities": {
         "sample1": [1,  0, 0, 5, 3, 4, 2, 1],
         "sample2": [2,  4, 0, 7, 8, 7, 2, 1],
         "sample3": [10, 9, 0, 7, 6, 5, 0, 1] 
       },
       "groups": [
         {
           "name": "group1",
           "samples": ["sample1", "sample2"],
         },
         {
           "name": "group2",
           "samples": ["sample3"],
         }
       ],
       "preprocessSettings": {
          "filterSettings": {
            "percentage": 0.5,
            "filterType": "each"
          },
          "imputeSettings": {
            "method": "minimum_value",
            "subSetting": 0.02
          },
          "normalizationMethod": "mean_normalize"
       },
       "removeBatchSettings": {
         "ifRemoveBatch": True,
         "samples2batch": {
           "sample1": "batch1",
           "sample2": "batch2",
           "sample3": "batch2"
         },
         "ifUseGroupVariable": True
       }
    }

    response = self.client.post("/restful/preprocess/preprocessProteomics/",
                                requestData,
                                content_type = "application/json")

    expectedResult = {
      "sample1": [1.1, 3.1, 4.1],
      "sample2": [2.1, 5.1, 6.1]
    }
    print(response.json())


    
    