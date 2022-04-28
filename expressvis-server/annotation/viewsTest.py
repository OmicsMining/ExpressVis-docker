from django.test import TestCase
from django.test import Client
import pandas as pd
from fgvis.settings import SERVER_TEST_DIR

class SuccessLoadGenesAnnotations(TestCase):
  def setUp(self):
    self.client = Client()

  def testEnsemblSuccess(self):
    species = "9606"
    IDtype  = "EnsemblGene"

    request = {
      "speciesID": species,
      "IDtype":    IDtype,
    }
    self.response = self.client.get("/restful/annotation/obtainGenesAnno/",
                           request,
                           content_type = "application/json")
    self.assertEqual(self.response.json()["genesInfoDic"]["ENSG00000142694"][0], "EVA1B")

  def testMicroarraySuccess(self):
    request = {
      "IDtype":    "hugene20sttranscriptcluster",
      "speciesID": "9606",
    }
    self.response = self.client.get("/restful/annotation/obtainGenesAnno/",
                           request,
                           content_type = "application/json")
    self.assertEqual(self.response.json()["genesInfoDic"]["17126256"][1], "SNHG3")
    self.assertEqual(self.response.json()["attributes"], ['ENTREZID', 'SYMBOL', 'GENENAME'])
  
  def testUniprotIDSuccess(self):
    request = {
      "IDtype":    "UniprotID",
      "speciesID": "9606"
    }
    self.response = self.client.get("/restful/annotation/obtainGenesAnno/",
                           request,
                           content_type = "application/json")
    self.assertEqual(self.response.json()["genesInfoDic"]["Q5T985"][1], "ITIH2")
    

class SuccessLoadIDmappingsInfoBetweenIDsInAspecies(TestCase):
  def setUp(self):
    self.client = Client()
  def testMouseMappingsBetweenEntrezidAndEnsemblgeneid(self):
    speciesID = "10090"
    idType1   = "NcbiEntrezGene"
    idType2   = "EnsemblGene"

    request = {
      "speciesID": speciesID,
      "IDtype1":   idType1,
      "IDtype2":   idType2
    }
    self.response = self.client.get("/restful/annotation/obtainSpeciesMappingInfoBetweenTwoIDtypes",
      request,
      content_type = "application/json")
    idMappintsDirectionaries = self.response.json()["idMappingDictionaries"]
    self.assertEqual(len(idMappintsDirectionaries), 2)

    self.assertEqual(idMappintsDirectionaries[0]["sourceID2targetID"]["115490466"], ["ENSMUSG00000064724"])
    self.assertEqual(idMappintsDirectionaries[1]["sourceID2targetID"]["ENSMUSG00000064724"], ["115490466"])

class SuccessLoadArrayIDsInOneSpecies(TestCase):
  def setUp(self):
    self.client = Client()
  def testLoadArrayIDsOfHuman(self):
    speciesID = "9606"
    request = {
      "speciesID": speciesID
    }
    self.response = self.client.get("/restful/annotation/arrayIDtypesInOneSpecies",
      request,
      content_type = "application/json")
    print(self.response.json()[0])
    self.assertEqual(len(self.response.json()), 68)
    
class SuccessLoadAnnotationsAndGenes(TestCase):
  def setUp(self):
    self.client = Client()
  def testRequestAnnotationTerms(self):
    speciesID = "10090"
    annotationType = "KEGG Pathway"
    request = {
      "speciesID": speciesID,
      "annotationType": annotationType
    }
    self.response = self.client.get("/restful/annotation/annotationTerms", 
      request, content_type = "application/json")
    self.assertEqual(len(self.response.json()["annotationTerms"]), 332);
  def testRequestAnnotationGenes(self):
    speciesID = "10090"
    annotationType = "KEGG Pathway"
    annotationID   = "mmu00604"
    request = {
      "speciesID":      speciesID,
      "annotationType": annotationType,
      "annotationID":   annotationID,
    }
    self.response = self.client.get("/restful/annotation/annotationGenes",
      request, content_type = "application/json")
    self.assertEqual(len(self.response.json()["genes"]), 15)


class SuccessObtainMatchedPercentageOfGenes(TestCase):
  def setUp(self):
    self.client = Client()
  def testSuccess(self):
    speciesID = "9606"
    IDtypeToBeChecked = "UniprotID"
    IDs = ["P04637", "96S44"]

    request = {
      "speciesID": speciesID,
      "IDs":       IDs,
      "IDtype":    IDtypeToBeChecked
    }
    self.response = self.client.post("/restful/annotation/obtainMatchedIDsPercentage",
      request, content_type = "application/json");
    self.assertEqual(self.response.json()["matchedPercentage"], 0.5)
