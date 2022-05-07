from django.test import TestCase
import os
from fgvis.settings import DATABASE_DIR
from keggExplore.keggExploreUtils import obtainKEGGpathwayGenesInfo, PathwayInfoParse, obtainKeggPathwayKGMLstring, \
  obtainKeggPathwayKGMLstringFromWebsite, obtainPathwaysInOneSpecies

  
class TestKeggFunctions(TestCase):
  def testObtainKEGGpathwayGenesInfo(self):
    keggID         = "hsa00061"
    entryID2Symbol = obtainKEGGpathwayGenesInfo(kegg_id = keggID)
    print(entryID2Symbol)
  def testObtainKeggPathwayKGMLstringFromWebsite(self):
    keggID     = "hsa00061"
    kgmlString = obtainKeggPathwayKGMLstringFromWebsite(keggID = keggID) 
    print(kgmlString)
  # def testObtainEntryID2Symbol(self):
    # speciesID = "9606"
    # pathwayID    = "hsa04919"
    
    # entry2symbol = obtainEntryID2Symbol(speciesID = speciesID, pathwayID = pathwayID)
    # self.assertEqual(entry2symbol["3265"], "HRAS")
    # self.assertEqual(entry2symbol["60", "ACTB"])
  # def testObtainKeggGenesClusteringInfoFromDataset(self):
  #   keggID     = "hsa00061"
  #   dataAccess = "GSE62208"
  #   groups     = [
  #     {
  #       "name": "Negative Control",
  #       "samples": ["GSM1522519","GSM1522520","GSM1522521"]
  #     },
  #     {
  #       "name": "Positive Control",
  #       "samples": ["GSM1522522", "GSM1522523", "GSM1522524"]
  #     },
  #     {
  #       "name": "B treatment",
  #       "samples": ["GSM1522525", "GSM1522526", "GSM1522527"]
  #     },
  #     {
  #       "name": "Il1 Stimulated",
  #       "samples": ["GSM1522533","GSM1522534","GSM1522535"]
  #     }
  #   ]
    
  #   clusteringInfo = obtainKeggGenesClusteringInfoFromDataset(
  #     keggID = keggID,
  #     geoSeriesAcc = dataAccess,
  #     groups = groups,
  #   )
  #   print(clusteringInfo)
  # def testObtainProbeID2EntryIDForMicroarray(self):
  #   annoPkgName = "hugene20sttranscriptcluster.db"
  #   probeID2EntryID = obtainProbeID2EntryIDForMicroarray(annoPkgName = annoPkgName, speciesID = "9606")
  #   print(len(probeID2EntryID.keys()))


class TestPathwayInfoParse(TestCase):
  def testObtainEntry2symbolsDescriptionNoTwoParagraphs(self):
    speciesID = "9606"
    pathwayID = "hsa04919"
    # pathwayID = "hsa04110"
    pathwayInfoPath = os.path.join(DATABASE_DIR, "speciesCenteredInfo", speciesID, "kegg", "pathwayInfo", pathwayID + ".txt")
    with open(pathwayInfoPath, "r") as f:
      pathwayInfoString = f.read()
    pathwayInfoParse = PathwayInfoParse(pathwayInfoString = pathwayInfoString)
    entry2symbol     = pathwayInfoParse.obtainEntryID2symbol()
    self.assertEqual(entry2symbol["5566"], "PRKACA")
    self.assertEqual(entry2symbol["25942"], "SIN3A")
    self.assertEqual(entry2symbol["60"], "ACTB")
  def testObtainEntry2symbolsDescriptionHasTwoParagraphs(self):
    speciesID = "9606"
    pathwayID = "hsa04110" # The description of cell cycle has two paragraphs
    pathwayInfoPath = os.path.join(DATABASE_DIR, "speciesCenteredInfo", speciesID, "kegg", "pathwayInfo", pathwayID + ".txt")
    with open(pathwayInfoPath, "r") as f:
      pathwayInfoString = f.read()
    pathwayInfoParse = PathwayInfoParse(pathwayInfoString = pathwayInfoString)
    entry2symbol     = pathwayInfoParse.obtainEntryID2symbol()
    self.assertEqual(entry2symbol["595"], "CCND1")
    self.assertEqual(entry2symbol["1021"], "CDK6")
    self.assertEqual(entry2symbol["4176"], "MCM7")

class TestObtainKGMLstring(TestCase):
  def testObtainKGMLstring(self):
    speciesID = "9606"
    pathwayID = "hsa04919"
    kgmlString = obtainKeggPathwayKGMLstring(speciesID = speciesID, pathwayID = pathwayID)
    print(kgmlString)

class TestObtainPathwaysInOneSpecies(TestCase):
  def testObtainPathwaysInHuman(self):
    speciesID = "9606"
    pathways = obtainPathwaysInOneSpecies(speciesID = speciesID)
    self.assertEqual(pathways[0]["name"], "Glycolysis / Gluconeogenesis - Homo sapiens (human)")
    self.assertEqual(pathways[0]["ID"],   "hsa00010")
  def testObtainPathwaysInMouse(self):
    speciesID = "10090"
    pathways = obtainPathwaysInOneSpecies(speciesID = speciesID)
    self.assertEqual(pathways[0]["name"], "Glycolysis / Gluconeogenesis - Mus musculus (mouse)")
    self.assertEqual(pathways[0]["ID"],   "mmu00010")
  def testObtainPathwaysInRat(self):
    speciesID = "10116"
    pathways = obtainPathwaysInOneSpecies(speciesID = speciesID)
    self.assertEqual(pathways[0]["name"], "Glycolysis / Gluconeogenesis - Rattus norvegicus (rat)")
    self.assertEqual(pathways[0]["ID"],   "rno00010")

