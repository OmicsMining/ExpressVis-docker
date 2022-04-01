import numpy as np
from django.test import TestCase
from clustering.clusteringUtils import Matrix2clusterTree

class TestClusteringUtils(TestCase):
  def testMatrix2clusterTree(self):
    testMatrix = np.array([[1,3,4,5], [5,4,3,1], [1,4,3,5], [5,3,4,1]])
    matrix2clusterTree = Matrix2clusterTree(matrix = testMatrix)
    treeJson = matrix2clusterTree.gainClusterJson()
    print(treeJson)

testFunction = TestClusteringUtils()
testFunction.testMatrix2clusterTree()


