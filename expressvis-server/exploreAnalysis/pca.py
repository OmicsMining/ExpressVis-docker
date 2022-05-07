'''
  PCA analysis on the samples
'''

from sklearn.decomposition import PCA

def samplesPCAnalysis(exprsMatrix, samples):
  '''
  Note:
    The result is only used for visualizing in the front-end

  Input: 
    exprsMatrix: number[][], rows are the samples, so the exprsMatrix should be transformed
    samples:     string[],

  Return:
    a list of dictionary
    The keys are sampleName, firstCompValue, secondCompValue 
  '''
  COMPONENTS_NUM = 2
  
  pca = PCA(n_components = COMPONENTS_NUM)
  projected = pca.fit_transform(exprsMatrix)

  pcaInfo = []
  for sample, compValue1, compValue2 in zip(samples, projected[:, 0], projected[:, 1]):
    pcaInfo.append({
      "sampleName": sample,
      "firstCompValue":  compValue1,
      "secondCompValue": compValue2
    })

  return pcaInfo

