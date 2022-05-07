import os
from django.test import TestCase
import pandas as pd
from fgvis.settings import SERVER_TEST_DIR

from diffAnalysis.proteomicsDiffAnalysisXKK import proteomicsStatistics

class ProteomicsDiffTest(TestCase):
  def testSuccess(self):
    filePath = os.path.join(SERVER_TEST_DIR, "proteomics", "Proteomics_Normalization_Impute_TestFile.csv")
    dataframe = pd.read_csv(filePath, header = [0,1], index_col = [0,1])
    experiment="Tumor";control="Paracancer";foldchangeMethod="mean";statisticsMethod="auto";multipleTestsCorrectMethod="fdr_bh"
    result = proteomicsStatistics(dataframe=dataframe,experiment=experiment,control=control,
                                  foldchangeMethod="mean",statisticsMethod="student-t",multipleTestsCorrectMethod="fdr_bh")
    print(result.keys())
    # print(inputFrame.keys())
    # print(inputFrame["Tumor"].head())


