from django.test import TestCase
from django.test import Client
import json

from fgvis.settings import BASE_DIR

class SuccessKmeansCluster(TestCase):
  def setUp(self):
    c = Client()
    expFile = BASE_DIR + "/static/testData/kmeansArray.json"
    with open(expFile, 'r') as json_data:
      expMatrix = json.load(json_data)
    print(type(expMatrix))
    request = {"expArray": expMatrix,
               "clusterNumber": 10 }
    request = json.dumps(request)
    self.response = c.post("/restful/clustering/kmeansCluster/",
                           request,
                           content_type = "application/json")
  def testSuccess(self):
    print("test")
    print(self.response.json())

