from django.test import TestCase
from django.test import Client
import pandas as pd
import os
from fgvis.settings import SERVER_TEST_DIR
import json

class SuccessSurvivalSplitAndForestTest(TestCase):
  def setUp(self):
    self.client = Client()
  def testObtainSurvivalSplitAndForest(self):
    survivalFrame = pd.read_csv(os.path.join(SERVER_TEST_DIR, "testClinical", "SH+cohort-SurvivalAnalysis-Proteomics.csv"))
    clinicalDic   = survivalFrame.loc[:,["OS", "OS Status"]].to_dict("list")
    expressionDic = survivalFrame.loc[:, ["GNL2", "BDH1", "SEPTIN1"]].to_dict("list")
    patientIDs    = survivalFrame["PatientID"].tolist()
    endpointTimeCol   = "OS"
    endpointStatusCol = "OS Status"

    request = {
       "clinicalDic":    clinicalDic,
       "expressionDic":  expressionDic,
       "patientIDs":     patientIDs,
       "endpointTimeCol":   endpointTimeCol,
       "endpointStatusCol": endpointStatusCol,
    }
    response = self.client.post("/restful/clinical/localDataSurvivalAndForest/", 
                                request,
                                content_type = "application/json")
    print(response.json())
  
  def testObtainSurvivalInfoForPlot(self):
    jsonFilePath = os.path.join(SERVER_TEST_DIR, "testClinical","Proteomics_SurvivalAnalysis_KMCurve_TestFile.json")
    with open(jsonFilePath) as file:
        dataJson = json.load(file)
    condition="SOAT1"; event="DFS"; status="DFS Status"
    eventTimes  = dataJson[event]
    eventStatus = dataJson[status]
    highOrLows  = dataJson[condition]

    request = {
      "eventTimes":  eventTimes,
      "eventStatus": eventStatus,
      "highOrLows":  highOrLows
    };
    response = self.client.post("/restful/clinical/localDataKMinfoForPlot/",
                                request,
                                content_type = "application/json")
    print(response.json().keys())
