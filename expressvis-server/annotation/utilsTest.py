import unittest
from annotation.utils import obtainSubList


class UtilTest(unittest.TestCase):
  def testObtainSubList(self):
    inputList = ["a", "b", "d", "c"]
    requiredIndex = [0, 2]
    subList = obtainSubList(inputList, requiredIndex)
    self.assertEqual(subList, ["a","d"])