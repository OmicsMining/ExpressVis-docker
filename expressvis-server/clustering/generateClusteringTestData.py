import json
from clustering.obtainClusteringInfo import obtainDatasetHierarchicalClusteringInfo
from fgvis.utils import NumpyEncoder

source      = "GEO"
accession   = "GSE62208"
annoPkgName = "hugene20sttranscriptcluster.db"
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
clusteringInfo = obtainDatasetHierarchicalClusteringInfo(
  source      = source,
  accession   = accession,
  annoPkgName = annoPkgName,
  groups      = groups,
)

datasetInfoForCluster = {
  "datasetID": accession,
  "valuesArrayAcrossSamples": clusteringInfo["valuesArrayAcrossSamples"],
  "valuesArrayAcrossGroups": clusteringInfo["valuesArrayAcrossGroups"],
  "samples":    clusteringInfo["samples"],
  "groupNames": clusteringInfo["groupNames"],
  "genes":      clusteringInfo["genes"], 
}

datasetHierarchicalClusResult = {
  "datasetID":     accession,
  "clusterMethod": "average",
  "acrossGroups": {
    "topDendgrogramInfor":  clusteringInfo["acrossGroupsTopDendgro"],
    "leftDendgrogramInfor": clusteringInfo["acrossGroupsLeftDendgro"],
  },
  "acrossSamples": {
    "topDendgrogramInfor":  clusteringInfo["acrossSamplesTopDendgro"],
    "leftDendgrogramInfor": clusteringInfo["acrossSamplesLeftDendgro"],
  },
}

datasetHierarchicalClusteringInfo = {
  "datasetInfoForCluster":         datasetInfoForCluster,
  "datasetHierarchicalClusResult": datasetHierarchicalClusResult
}


with open("/media/thudxz/Research/process/bioinformatics_tools/angular_django_time_series/client/src/assets/clustering/datasetHierarchicalClusteringInfo.json", "w") as fileOpen:
  json.dump(datasetHierarchicalClusteringInfo, fileOpen, cls = NumpyEncoder)
  