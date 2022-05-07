from diffAnalysis.triggerDiffAnalysis import affyDiffAnalysisMultipleGroups
from fgvis.settings import FRONTEND_TEST_DIR
from fgvis.utils    import NumpyEncoder
import json

geoSeriesAcc = "GSE62208"
groups = [
  {
    "name": "Negative Control",
    "samples": ["GSM1522519","GSM1522520","GSM1522521"]
  },
  {
    "name": "Positive Control",
    "samples": ["GSM1522522", "GSM1522523", "GSM1522524"]
  },
  {
    "name": "B treatment",
    "samples": ["GSM1522525", "GSM1522526", "GSM1522527"]
  },
  {
    "name": "Il1 Stimulated",
    "samples": ["GSM1522533","GSM1522534","GSM1522535"]
  }
]

diffGroupPairs = [
  {
    "baseGroup": "Negative Control",
    "targetGroup": "Positive Control"
  },
  {
    "baseGroup": "Negative Control",
    "targetGroup": "B treatment",
  },
  {
    "baseGroup": "Negative Control",
    "targetGroup": "Il1 Stimulated"
  }
]

def obtainGroupSamples(groups, groupName):
  samples = []
  for group in groups:
    if group["name"] == groupName:
      samples = group["samples"]
      break
  return samples

diffGroupPairsList = []
for eachGroupPair in diffGroupPairs:
  groupPairDic = {
    "baseGroup":  obtainGroupSamples(groups, eachGroupPair["baseGroup"]),
    "targetGroup": obtainGroupSamples(groups, eachGroupPair["targetGroup"])
  }
  diffGroupPairsList.append(groupPairDic)

diffResults = affyDiffAnalysisMultipleGroups(
  geoSeriesAcc   = geoSeriesAcc,
  diffGroupPairs = diffGroupPairsList
)

diffResultsInList = []
for i, result in enumerate(diffResults):
  diffResultsInList.append(
    {
      "baseGroup": diffGroupPairs[i]["baseGroup"],
      "targetGroup": diffGroupPairs[i]["targetGroup"],
      "diffResults": result
    }
  )


with open(FRONTEND_TEST_DIR + "/kegg-explore/diffResults.json", "w") as fileOpen:
  json.dump(diffResultsInList, fileOpen, cls = NumpyEncoder)
