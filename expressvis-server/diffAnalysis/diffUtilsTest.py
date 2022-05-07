from django.test import TestCase
import pandas as pd
from diffAnalysis.diffUtils import constructMultilIndexDataframeForProteimicsDiffAnalysis

class DiffUtilsTest(TestCase):
  def testConstructMultilIndexDataframeForProteimicsDiffAnalysis(self):
    
    valuesDic = {
      "sample1": [1, 2, 3, 4], 
      "sample2": [5, 6, 7, 8],
      "sample3": [1, 3, 3, 3],
      "sample4": [2, 3, 2, 4],
      "sample5": [1, 3, 4, 5],
      "sample6": [1, 3, 3, 2]
    }
    genes = ["gene1", "gene3", "gene4", "gene2"]
    baseSamples   = ["sample1", "sample3", "sample5"]
    targetSamples = ["sample2", "sample4", "sample6"]

    resultFrame = constructMultilIndexDataframeForProteimicsDiffAnalysis(valuesDic, genes, baseSamples, targetSamples)
    print(resultFrame)

    