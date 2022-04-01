from django.test import TestCase
from clustering.obtainClusteringInfo import obtainDatasetHierarchicalClusteringInfo

class TestObtainClusteringInfo(TestCase):
  def testObtainDatasetHierarchicalClusteringInfo(self):
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

testObtainClusteringInfo = TestObtainClusteringInfo()
testObtainClusteringInfo.testObtainDatasetHierarchicalClusteringInfo()