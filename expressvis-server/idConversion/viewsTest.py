from django.test import TestCase
from django.test import Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

class obtainIdentifiers(TestCase):
  def setUp(self):
    self.client = APIClient()
  def testSuccess(self):
    self.responseGenes = self.client.get("/restful/ids/loadspeciesgenes/?species=arabidopsis")
    print("CTF2A" in self.responseGenes.json()['Symbol'])
