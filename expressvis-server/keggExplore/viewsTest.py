from django.test import TestCase
from django.test import Client

class SuccessKeggExplore(TestCase):
  def setUp(self):
    self.client = Client()
  def testObtainKgmlEntryID2symbol(self):
    response = self.client.get("/result/keggExplore/kgmlentryidinfo/?speciesID=9606&pathwayID=hsa04919")
    responseDic = response.json()
    self.assertEqual(responseDic["KEGGkgmlEntryIDInfo"]["ID"], "hsa04919")
    
    entry2symbol = responseDic["KEGGkgmlEntryIDInfo"]["entryID2Symbol"]
    self.assertEqual(entry2symbol["5566"], "PRKACA")
    self.assertEqual(entry2symbol["25942"], "SIN3A")
    self.assertEqual(entry2symbol["60"],    "ACTB")

  def testRequestKeggSpecies(self):
    response = self.client.get("/restful/keggExplore/allkeggspecies/")
    self.assertEqual(
      response.json()["allKeggSpecies"],
      [
         {
          "taxID": "9606",
          "name":  "Homo sapiens",
        },
        {
          "taxID": "10090",
          "name":  "Mus musculus",
        },
        {
          "taxID": "10116",
          "name":  "Rattus norvegicus"
        }
      ]
    )
  
  def testRequestPathwaysOfOneSpecies(self):
    response = self.client.get("/restful/keggExplore/onespeciespathways/?speciesID=10090")
    self.assertEqual(len(response.json()["pathways"]), 341)
    self.assertEqual(response.json()["pathways"][0]["name"], "Glycolysis / Gluconeogenesis - Mus musculus (mouse)")