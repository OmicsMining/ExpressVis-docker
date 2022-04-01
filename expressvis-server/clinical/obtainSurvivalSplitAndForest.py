import requests
import json
from fgvis.settings import CLINICAL_URL


def obtainSurvivalSplitAndForest(clinicalDic, expressionDic, patientIDs, endpointTimeCol, endpointStatusCol, highLowSplitSetting):
  # Parameters
  #    highLowSplitSetting
  #       {method:, settings}
  #    when method is percentageSplit: { percentageThreshold: probability}
  #    when method is    maxstatSplit, { minProb: ,maxProb:} 
  # return from the server:
  # {
  #     survivalSplit, 
  #     survivalAnno = survivalAnno
  # }
  # split format, dataframe
  ##  headers: PatientID    OS `OS Status` GNL2  BDH1  SEPTIN1 ACTR10 HELZ2 ALAS1 HTRA3
  # ForestAnno, dataframe
  # 
  #  "Variable"              "n/N in high group"     "n/N in low group"     
  #  "favor/unfavor"         "Hazard ratio"          "Hazard ratio lower"   
  #  "Hazard ratio upper"    "HR (95% CI)"           "Wald test p-value"    
  #  "Log-rank test p-value"
  # 

  if highLowSplitSetting["method"] == "maxstatSplit":
    requestUrl    = CLINICAL_URL + "surivialSplitMaxStatAndForestAnnotation"
    requestData = {
      "clinicalDic":   clinicalDic,
      "expressionDic": expressionDic,
      "patientIDs":    patientIDs,
      "endpointTimeCol":   endpointTimeCol,
      "endpointStatusCol": endpointStatusCol,
      "minProb": highLowSplitSetting["settings"]["minProb"],
      "maxProb": highLowSplitSetting["settings"]["maxProb"]
    }
    clinicalResult = requests.post(url = requestUrl,
                                  json = requestData)
  elif highLowSplitSetting["method"] == "percentageSplit":
    requestUrl = CLINICAL_URL + "surivialSplitPercentageAndForestAnnotation"
    
    requestData = {
      "clinicalDic":   clinicalDic,
      "expressionDic": expressionDic,
      "patientIDs":    patientIDs,
      "endpointTimeCol":   endpointTimeCol,
      "endpointStatusCol": endpointStatusCol,
      "percentageThreshold": highLowSplitSetting["settings"]["percentageThreshold"]
    }
    clinicalResult = requests.post(url = requestUrl,
                                   json = requestData)
  return json.loads(json.loads(clinicalResult.text)[0])
