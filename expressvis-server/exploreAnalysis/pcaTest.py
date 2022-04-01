from django.test import TestCase
import pandas as pd
import feather
import json
from exploreAnalysis.pca import samplesPCAnalysis
from fgvis.settings import DATABASE_DIR, FRONTEND_TEST_DIR

class PCAtest(TestCase):
  def testPCAanalysis(self):
    exprsFrame  = pd.read_csv(DATABASE_DIR + "/datasets/GEO/GSE62nnn/GSE62208/normalizedExprs.txt", sep = "\t")
    
    exprsFrame  = exprsFrame.set_index("ID")
   
    exprsMatrix = exprsFrame.values.transpose()
    samples     = exprsFrame.columns.to_list()

    pcaResult = samplesPCAnalysis(
      exprsMatrix = exprsMatrix,
      samples     = samples
    )

    with open(FRONTEND_TEST_DIR + "/pca.json", "w") as fileOpen:
      json.dump(pcaResult, fileOpen)
  def generatePCAtestDataForTheFrontEnd(self):
    exprsFrame  = pd.read_csv(DATABASE_DIR + "/datasets/GEO/GSE62nnn/GSE62208/normalizedExprs.txt", sep = "\t")
    
    exprsFrame  = exprsFrame.set_index("ID")
   
    exprsMatrix = exprsFrame.values.transpose()
    samples     = exprsFrame.columns.to_list()

    pcaResult = samplesPCAnalysis(
      exprsMatrix = exprsMatrix,
      samples     = samples
    )

    phenotypeFrame = pd.read_csv(DATABASE_DIR + "/datasets/GEO/GSE62nnn/GSE62208/normalizedPhenotype.txt", sep = "\t")
    

