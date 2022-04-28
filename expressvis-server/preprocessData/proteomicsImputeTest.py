import os
from django.test import TestCase
import pandas as pd
from fgvis.settings import SERVER_TEST_DIR
from preprocessData.proteomicsImpute import impute

class ProteomicsImputeTest(TestCase):
  def setUp(self):
    # testFile = os.path.join(SERVER_TEST_DIR, "proteomics", "impute_normalize_diff_xkk", "Proteomics_Normalization_Impute_TestFile.csv")
    # self.inputDataframe = pd.read_csv(testFile)
    self.inputDataframe = pd.DataFrame({
      "sample1": [1, 0, 3 ,4 ,5],
      "sample2": [2, 3, 0, 5, 7],
    })

  def testMinimumValueImpute(self):
    imputeResult = impute(self.inputDataframe, replaceZero = True)
    expectedResult = {'index': [0, 1, 2, 3, 4], 'sample1': [1.0, 1.0, 3.0, 4.0, 5.0], 'sample2': [2.0, 3.0, 1.0, 5.0, 7.0]}
    self.assertEqual(imputeResult, expectedResult)
