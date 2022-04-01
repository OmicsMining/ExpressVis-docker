from scipy.spatial.distance import pdist, squareform
from clustering.clusteringUtils import Matrix2clusterTree


def obtainSamplesCorAndClusteringInfo(exprsFrame):
  '''
  This function is to generate correlation between samples and 
  the result of clustering samples using correlation as distance

  input: 
    columns of exprsFrame are samples
  
  return:
    {
       samples
       corMatrix
       samplesClusteringDendgro
    }

  '''
  samples   = exprsFrame.columns.to_list()
  corMatrix = exprsFrame.corr(method = 'pearson')
  samplesClusteringDendgro = Matrix2clusterTree(matrix = exprsFrame.values.transpose()).gainClusterJson()

  return {
    "samples":   samples,
    "corMatrix": corMatrix.values,
    "samplesClusteringDendgro": samplesClusteringDendgro
  }


