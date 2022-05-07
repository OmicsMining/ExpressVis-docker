from django.test import TestCase
import pandas as pd
#import feather
import json
from exploreAnalysis.samplesCor import obtainSamplesCorAndClusteringInfo
from fgvis.settings import DATABASE_DIR, FRONTEND_TEST_DIR
from fgvis.utils import NumpyEncoder

class SamplesCorTest(TestCase):
  def testObtainSamplesCorAndClusteringInfo(self):
    exprsFrame  = pd.read_csv(DATABASE_DIR + "/datasets/GEO/GSE62nnn/GSE62208/normalizedExprs.txt", sep = "\t")
    
    exprsFrame  = exprsFrame.set_index("ID")

    samplesCorInfo = obtainSamplesCorAndClusteringInfo(exprsFrame = exprsFrame)

    with open(FRONTEND_TEST_DIR + "/samplesCor.json", "w") as fileOpen:
      json.dump(samplesCorInfo, fileOpen, cls = NumpyEncoder)
 