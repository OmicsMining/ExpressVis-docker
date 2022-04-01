from django.test import TestCase
from idConversion.idMapping import obtainProbesFromEntrez
import time

class TestIDmappingFunctions(TestCase):
  def testObtainProbesFromEntrez(self):
    start = time.time()
    annoPkgName = "hugene20sttranscriptcluster.db"
    genes       = ["6774", "6772", "2267"]
    genesInfo   = obtainProbesFromEntrez(
      annoPkgName = annoPkgName,
      genes = genes,
    )
    print(time.time() - start)
    print(genesInfo)


testFunctions = TestIDmappingFunctions()
testFunctions.testObtainProbesFromEntrez()