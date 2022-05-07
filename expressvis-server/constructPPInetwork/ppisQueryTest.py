from django.test import TestCase
from constructPPInetwork.ppisQuery import queryPPIs, convertPPIs2cytoscapeJsGraph
import json


class PPIsQueryTest(TestCase):
  def testQueryHuamnMenthaPPIsBetweenProteinsBySymbol(self):
    symbols = ["IL6", "STAT3", "IL6", "STAT1", "FAM20C", "OSM"]
    subPPIs = queryPPIs(
      speciesID      = "9606", 
      database       = "Mentha",
      IDtype         = "SYMBOL",
      proteinIDs     = symbols,
      subNetworkType = "between")
    self.assertEqual(subPPIs[0][0], "FAM20C")
    self.assertEqual(subPPIs[0][1], "IL6")
    self.assertEqual(len(subPPIs), 6)
    print(subPPIs)
  def testQueryMouseMenthaPPIsBetweenProteinsBySymbol(self):
    symbols = ["Il6", "Stat3", "Stat1", "Fam20c", "Osm"]
    subPPIs = queryPPIs(
      speciesID      = "10090", 
      database       = "Mentha",
      IDtype         = "SYMBOL",
      proteinIDs     = symbols,
      subNetworkType = "between")
    self.assertEqual(len(subPPIs), 1)
  def testConvertPPIs2cytoscapeJsGraph(self):
    ppis = [
      ["a", "b", "lablea", "lableb"],
      ["c", "d", "labelc", "lablec"],
      ["e", "f", "labele", "lablef"],
    ]
    graph = convertPPIs2cytoscapeJsGraph(ppis)

