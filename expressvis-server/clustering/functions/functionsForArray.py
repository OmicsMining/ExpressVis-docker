'''
 functions applied to numpy array
'''
import numpy as np
import math

def log2Transform(x):
  return math.log2(x)
vLog2Transform = np.vectorize(log2Transform)

def log10Transform(x):
  return math.log10(x)
vLog10Transform = np.vectorize(log10Transform)

def log2MeanTransform(x):
  '''
  input: matrix
  first, compute log2 value of each element
  second, subscribe the mean value of each row
  :param x:
  :return:
    transformed matrix
  '''
  log2Matrix = vLog2Transform(x)
  # substract row mean
  subMatrix = (log2Matrix.transpose() - log2Matrix.mean(1)).transpose()
  return subMatrix
