import unittest
from enrichment.enrichCompute import AnnotationEnrich, EnrichMultipleAnnotations,EnrichMultipleAnnotationsAdapter
from fgvis.settings import SERVER_TEST_DIR

class AnnotationEnrichTest(unittest.TestCase):
  def testAnnotationEnrich(self):
    targets    = []
    background = []
    with open(SERVER_TEST_DIR + "/enrichTest/targets.txt", "r") as fileOpen:
      for eachLine in fileOpen:
        targets.append(eachLine.strip())
    with open(SERVER_TEST_DIR + "/enrichTest/background.txt") as fileOpen:
      for eachLine in fileOpen:
        background.append(eachLine.strip())
    annotationEnrich = AnnotationEnrich(
      annotationType = "KEGG Pathway", 
      proteinIDtype  = "EnsemblGene", 
      targets        = targets, 
      background     = background, 
      speciesID      = "10090")
    result = annotationEnrich.summaryResultsWithPvalue()
    self.assertEqual(result["enrichedResult"]["attributes"][0], "AnnotationID")
    self.assertEqual(result["enrichedResult"]["enrichedInfos"][0][0], "mmu05168")
  def testEnrichMultipleAnnotations(self):
    targets    = []
    background = []
    with open(SERVER_TEST_DIR + "/enrichTest/targets.txt", "r") as fileOpen:
      for eachLine in fileOpen:
        targets.append(eachLine.strip())
    with open(SERVER_TEST_DIR + "/enrichTest/background.txt") as fileOpen:
      for eachLine in fileOpen:
        background.append(eachLine.strip())
    annotationTypes = ["KEGG Pathway", "Molecular Function"]
    enrichMultipleAnnotations = EnrichMultipleAnnotations(
      annotationTypes = annotationTypes,
      proteinIDtype   = "EnsemblGene",
      targets         = targets,
      background      = background,
      species         = "10090"
    )
    results = enrichMultipleAnnotations.enrichForAllAnnotations()
    self.assertEqual(results[0]["enrichedResult"]["attributes"][0], "AnnotationID")
    self.assertEqual(results[0]["enrichedResult"]["enrichedInfos"][0][0], "mmu05168")

class EnrichMultipleAnnotationsAdapterTest(unittest.TestCase):
  def testIDsOtherThanMicroarrayIDs(self):
    targets    = []
    background = []
    with open(SERVER_TEST_DIR + "/enrichTest/targets.txt", "r") as fileOpen:
      for eachLine in fileOpen:
        targets.append(eachLine.strip())
    with open(SERVER_TEST_DIR + "/enrichTest/background.txt") as fileOpen:
      for eachLine in fileOpen:
        background.append(eachLine.strip())
    annotationTypes = ["KEGG Pathway", "Molecular Function"]
    enrichMultipleAnnotationsAdapter = EnrichMultipleAnnotationsAdapter(
      annotationTypes = annotationTypes,
      proteinIDtype   = "EnsemblGene",
      targets         = targets,
      background      = background,
      species         = "10090"
    )
    results = enrichMultipleAnnotationsAdapter.obtainEnrichedResult()
    self.assertEqual(results[0]["enrichedResult"]["attributes"][0], "AnnotationID")
    self.assertEqual(results[0]["enrichedResult"]["enrichedInfos"][0][0], "mmu05168")
  def testMicroarrayIDs(self):
    targets    = []
    background = []
    with open(SERVER_TEST_DIR + "/enrichTest/targetsMicroarray.txt", "r") as fileOpen:
      for eachLine in fileOpen:
        targets.append(eachLine.strip())
    with open(SERVER_TEST_DIR + "/enrichTest/backgroundMicroarray.txt") as fileOpen:
      for eachLine in fileOpen:
        background.append(eachLine.strip())
    annotationTypes = ["KEGG Pathway", "Molecular Function"]
    enrichMultipleAnnotationsAdapter = EnrichMultipleAnnotationsAdapter(
      annotationTypes = annotationTypes,
      proteinIDtype   = "mogene21sttranscriptcluster",
      targets         = targets,
      background      = background,
      species         = "10090"
    )
    results = enrichMultipleAnnotationsAdapter.obtainEnrichedResult()
    
    print(results[0])
