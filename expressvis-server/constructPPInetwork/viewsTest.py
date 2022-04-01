from django.test import TestCase
from django.test import Client

class SuccessConstructNetwork(TestCase):
  def setUp(self):
    self.client = Client()
  def testConstructNetworkUseSymbols(self):
    request = {
      "speciesID":       "9606",
      "database":        "Mentha",
      "IDtype":          "SYMBOL",
      "proteinIDs":      ["IL6", "STAT3", "IL6", "STAT1", "FAM20C", "OSM"],
      "subNetworkType": "between",
    }
    response = self.client.post("/restful/ppinetwork/constructNetwork/",
                           request,
                           content_type = "application/json")
    self.assertEqual(len(response.json()["PPIs"]), 6)
    