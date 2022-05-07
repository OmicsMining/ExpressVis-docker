from django.test import TestCase
from django.test import Client
import pandas as pd
import json
from fgvis.settings import DATABASE_DIR, FRONTEND_TEST_DIR


class SuccessPCAanalysis(TestCase):
  def setUp(self):
    self.c = Client()
    
  def testSuccess(self):
    exprsFrame  = pd.read_csv(DATABASE_DIR + "/datasets/GEO/GSE62nnn/GSE62208/normalizedExprs.txt", sep = "\t")
    
    exprsFrame  = exprsFrame.set_index("ID")
   
    exprsMatrix = exprsFrame.values.tolist()
    samples     = exprsFrame.columns.to_list()
    
    request = {
      "values": exprsMatrix,
      "samples": samples
    }
    response = self.c.post("/restful/exploreAnalysis/localDatasetPCA/",
                      request,
                      content_type = "application/json")
    print(response.json())