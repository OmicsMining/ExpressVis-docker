from django.test import TestCase
import pandas as pd
from preprocessData.proteomicsNormalize import norm_sample, norm_protein


class SampleNormalizeTest(TestCase):
  def setUp(self):
    self.inputDataframe = pd.DataFrame({
      "sample1": [1, 0, 3 ,4 ,5],
      "sample2": [2, 3, 0, 5, 7],
    })
  def testzscorenormalize(self):
    resultFrame =  norm_sample(self.inputDataframe)
    print(resultFrame)