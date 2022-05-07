from django.test import TestCase
from fgvis.settings import BASE_DIR
from .functionsForArray import log2MeanTransform
import pandas as pd

class SuccessKmeans(TestCase):
  def setUp(self):
    # read test file
    fileName = "".join([BASE_DIR, "/static/examples/RNA-seq_tutorial_example.txt"])
    dataFrame = pd.read_table(fileName)
    valuesFrame = dataFrame[['Groupa_1_RPKM', 'Groupa_2_RPKM',
                        'Groupb_1_RPKM', 'Groupb_2_RPKM', 'Groupc_1_RPKM', 'Groupc_2_RPKM',
                        'Groupd_1_RPKM', 'Groupd_2_RPKM', 'Groupe_1_RPKM', 'Groupe_2_RPKM']]
    valuesMatrix = valuesFrame.values
    # transfrom matrix
    self.transformedMatrix = log2MeanTransform(valuesMatrix)
  def testKemans(self):
    print(self.transformedMatrix)

