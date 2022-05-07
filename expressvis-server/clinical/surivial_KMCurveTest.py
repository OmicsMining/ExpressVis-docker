import json
import os
from django.test import TestCase
from fgvis.settings import SERVER_TEST_DIR
import pandas as pd
from clinical.surivial_KMCurve import generateKMinfoForPlot


class GenerateKMinfoForPlotTest(TestCase):
  def setUp(self):
    pass
  def testSuccessGenerateKMinfoForPlot(self):
    jsonFilePath = os.path.join(SERVER_TEST_DIR, "testClinical","Proteomics_SurvivalAnalysis_KMCurve_TestFile.json")
    with open(jsonFilePath) as file:
        dataJson = json.load(file)
    condition="SOAT1"; event="DFS"; status="DFS Status"
    eventTimes  = dataJson[event]
    eventStatus = dataJson[status]
    highOrLows  = dataJson[condition]
    KMinfo = generateKMinfoForPlot(eventTimes, eventStatus, highOrLows)
    print(KMinfo)