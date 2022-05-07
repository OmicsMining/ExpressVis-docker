from django.test import TestCase
from diffAnalysis.proteomicsDiffAnalysisAdapter import proteomicsDiffAnalysis, proteomicsDiffAnalysisMultipleGroupPairs
class ProteomicsDiffAnalysisAdapterTest(TestCase):
  def testOneGroupPairSuccess(self):
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
    
    result = proteomicsDiffAnalysis(valuesDic, genes, baseSamples, targetSamples)
    print(result)
  def testMultipleGroupPairSuccess(self):
    valuesDic = {
      "sample1": [1, 2, 3, 4], 
      "sample2": [5, 6, 7, 8],
      "sample3": [1, 3, 3, 3],
      "sample4": [2, 3, 2, 4],
      "sample5": [1, 3, 4, 5],
      "sample6": [1, 3, 3, 2]
    }
    genes = ["gene1", "gene3", "gene4", "gene2"]
    groupPairs = [
      {
        "baseGroup":   "group1",
        "targetGroup": "group2",
      },
      {
        "baseGroup":   "group1",
        "targetGroup": "group3",
      },
    ]
    groups2samples = {
      "group1": ["sample1", "sample2", "sample3"],
      "group2": ["sample4", "sample5", "sample6"],
      "group3": ["sample2", "sample5", "sample6"]
    }
    diffResultList = proteomicsDiffAnalysisMultipleGroupPairs(valuesDic, genes, groupPairs, groups2samples)
    print(diffResultList)