import os
from django.test import TestCase
from fgvis.settings import SERVER_TEST_DIR
import pandas as pd
from clinical.obtainSurvivalSplitAndForest import obtainSurvivalSplitAndForest

class SurvivalSplitAndForestTest(TestCase):
  def setUp(self):
    pass
  def testSuccessMaxStatSurvivalSplitAndForest(self):
    survivalFrame = pd.read_csv(os.path.join(SERVER_TEST_DIR, "testClinical", "SH+cohort-SurvivalAnalysis-Proteomics.csv"))
    clinicalDic   = survivalFrame.loc[:,["OS", "OS Status"]].to_dict("list")
    expressionDic = survivalFrame.loc[:, ["GNL2", "BDH1", "SEPTIN1"]].to_dict("list")
    patientIDs    = survivalFrame["PatientID"].tolist()
    endpointTimeCol   = "OS"
    endpointStatusCol = "OS Status"
    highLowSplitSetting = {
      "method": "maxstatSplit",
      "settings": {
        "minProb": 0.2,
        "maxProb": 0.8
      }
    }
    result = obtainSurvivalSplitAndForest(
      clinicalDic   = clinicalDic,
      expressionDic = expressionDic,
      patientIDs    = patientIDs,
      endpointTimeCol   = endpointTimeCol,
      endpointStatusCol = endpointStatusCol,
      highLowSplitSetting = highLowSplitSetting,
    )
    print(result["survivalAnno"])

  def testSuccessPercentageSurvivalSplitAndForest(self):
    survivalFrame = pd.read_csv(os.path.join(SERVER_TEST_DIR, "testClinical", "SH+cohort-SurvivalAnalysis-Proteomics.csv"))
    clinicalDic   = survivalFrame.loc[:,["OS", "OS Status"]].to_dict("list")
    expressionDic = survivalFrame.loc[:, ["GNL2", "BDH1", "SEPTIN1"]].to_dict("list")
    patientIDs    = survivalFrame["PatientID"].tolist()
    endpointTimeCol   = "OS"
    endpointStatusCol = "OS Status"
    highLowSplitSetting = {
      "method": "percentageSplit",
      "settings": {
        "percentageThreshold": 0.5,
      }
    }
    result = obtainSurvivalSplitAndForest(
      clinicalDic   = clinicalDic,
      expressionDic = expressionDic,
      patientIDs    = patientIDs,
      endpointTimeCol   = endpointTimeCol,
      endpointStatusCol = endpointStatusCol,
      highLowSplitSetting = highLowSplitSetting,
    )
    print(result["survivalAnno"])

    


