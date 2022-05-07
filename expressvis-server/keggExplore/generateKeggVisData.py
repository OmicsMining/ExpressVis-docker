# generate test data for kegg visualization module
# Steps:
# 1. Obtain kgmlString
# 2. Obtain entryID2Symbol
# 
# 3. Obtain diffGenes for a dataset
# 
# 4. Obtain highlightGenes
# 
# 5. Generate speciesKeggPathways$
# 6. Generate availableKeggPathways$
# 
# 7. generate keggGenesClusteringResult
import json
import numpy as np

from keggExplore.keggExploreUtils import obtainKeggPathwayKGMLstringFromWebsite, \
  obtainKEGGpathwayGenesInfo, obtainKeggGenesClusteringInfoFromDataset, \
    obtainProbeID2EntryIDForMicroarray
from dataset.subsetDataset import obtainGenesExprsInfoForGroupsClusteringFromGEO
from diffAnalysis.triggerDiffAnalysis import affyDiffAnalysisMultipleGroups
from clustering.clusteringUtils import Matrix2clusterTree



keggIDs       = ["hsa00061", "hsa04141", "hsa04064", "hsa00620"]
geoSeriesAcc = "GSE62208"
diffGroupPairs = [
  {"baseGroup": ["GSM1522519","GSM1522520","GSM1522521"], 
    "targetGroup": ["GSM1522522", "GSM1522523", "GSM1522524"]
    },
  {"baseGroup": ["GSM1522519","GSM1522520","GSM1522521"], 
    "targetGroup": ["GSM1522525", "GSM1522526", "GSM1522527"]},
  {"baseGroup": ["GSM1522519","GSM1522520","GSM1522521"], 
    "targetGroup": ["GSM1522533","GSM1522534","GSM1522535"]},
]

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


kgmlEntrezIDInfoList = []
keggGenesClusteringResultList = []
for eachPath in keggIDs:
  kgmlString     = obtainKeggPathwayKGMLstringFromWebsite(keggID = eachPath)
  entryID2Symbol = obtainKEGGpathwayGenesInfo(kegg_id = eachPath)
  kgmlEntrezIDInfoList.append(
    {"ID": eachPath,
     "kgmlString": kgmlString, 
     "entryID2Symbol":entryID2Symbol}
    )
  clusteringInfo = obtainKeggGenesClusteringInfoFromDataset(
    keggID       = eachPath,
    geoSeriesAcc = geoSeriesAcc,
    groups       = groups
  )
  keggGenesClusteringResultList.append(clusteringInfo)


probeID2EntryID = obtainProbeID2EntryIDForMicroarray(
  annoPkgName = "hugene20sttranscriptcluster.db", 
  speciesID   = "9606")
probeID2EntryIDInfo = {
  "speciesID":       "9606",
  "probeIDtype":     "hugene20sttranscriptcluster.db",
  "probeID2EntryID": probeID2EntryID,
}
# diffResults = affyDiffAnalysisMultipleGroups(
#   geoSeriesAcc = geoSeriesAcc, 
#   diffGroupPairs = diffGroupPairs
# )
speciesKeggPathways = [
  {
    "ID": "hsa00061",
    "name": "Fatty acids biosynthesis",
    "speciesID": "9606"
  },
  {
    "ID": "hsa04141",
    "name": "Protein processing in endoplasmic reticulum",
    "speciesID": "9606"
  }
]

availableKeggPathways = [
  {
    "ID": "hsa00061",
    "name": "Fatty acids biosynthesis",
    "speciesID": "9606",
  },
  {
    "ID": "hsa04141",
    "name": "Protein processing in endoplasmic reticulum",
    "speciesID": "9606",
  },
  {
    "ID": "hsa04064",
    "name": "NFKB pathway",
    "speciesID": "9606",
  },
  {
    "ID": "hsa00620",
    "name": "Pyruvate pathway",
    "speciesID": "9606",
  }
]


keggVisInfo = {
  "speciesKeggPathways":   speciesKeggPathways,
  "availableKeggPathways": availableKeggPathways,
  "kgmlEntrezIDInfoList":  kgmlEntrezIDInfoList,
  "probeID2EntryIDInfo":   probeID2EntryIDInfo,
  "keggGenesClusteringResultList": keggGenesClusteringResultList,
  "selectedDatasetGroupNames": ["Negative Control", "Positive Control", "B treatment", "Il1 Stimulated"]
}


class NumpyEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, np.ndarray):
      return obj.tolist()
    return json.JSONEncoder.default(self, obj)

with open("/media/thudxz/Research/process/bioinformatics_tools/angular_django_time_series/client/src/assets/kegg-explore/keggMapVis.json", "w") as fileOpen:
  json.dump(keggVisInfo, fileOpen, cls = NumpyEncoder)




