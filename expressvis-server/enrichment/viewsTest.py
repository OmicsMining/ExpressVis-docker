from django.test import TestCase
from django.test import Client
from fgvis.settings import SERVER_TEST_DIR


class SuccessEnrichment(TestCase):
  def setUp(self):
    self.client = Client()
  def testRequestEnrichmentAnalysis(self):
    targets    = []
    background = []
    with open(SERVER_TEST_DIR + "/enrichTest/targets.txt", "r") as fileOpen:
      for eachLine in fileOpen:
        targets.append(eachLine.strip())
    with open(SERVER_TEST_DIR + "/enrichTest/background.txt") as fileOpen:
      for eachLine in fileOpen:
        background.append(eachLine.strip())

    request = {
      "speciesID":  "10090",
      "geneIDtype": "EnsemblGene",
      "genes":      targets,
      "backgroundGenes": background,
    }
    response = self.client.post("/restful/enrichment/pathway/",
                           request,
                           content_type = "application/json")
    self.assertEqual(response.json()[0]["annotationType"], "KEGG Pathway")
    self.assertEqual(response.json()[0]["enrichedResult"]["attributes"][0], "AnnotationID")
  def testRequestEnrichmentAnalysisOfMicroarrayIDs(self):
    targets    = []
    background = []
    with open(SERVER_TEST_DIR + "/enrichTest/targetsMicroarray.txt", "r") as fileOpen:
      for eachLine in fileOpen:
        targets.append(eachLine.strip())
    with open(SERVER_TEST_DIR + "/enrichTest/backgroundMicroarray.txt") as fileOpen:
      for eachLine in fileOpen:
        background.append(eachLine.strip())
    
    request = {
      "speciesID":  "10090",
      "geneIDtype": "mogene21sttranscriptcluster",
      "genes":      targets,
      "backgroundGenes": background,
    }
    response = self.client.post("/restful/enrichment/pathway/",
                           request,
                           content_type = "application/json")
    print(response.json())