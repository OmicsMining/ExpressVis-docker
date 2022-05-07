import pandas as pd

from preprocessData.removeBatchEffects import removeBatchEffectsNormal

def removeProteomicsBatchEffects(dataFrame: pd.DataFrame, samples2batch, samples2group = None):
  samples = list(dataFrame.columns)
  proteinIDs = dataFrame.index.values.tolist()
  if samples2group == None:
    batch = [samples2batch[sample] for sample in samples]

    values = dataFrame.to_numpy().tolist()
    adjustedValues = removeBatchEffectsNormal(values, batch, None)
    
  else:
    group = [samples2group[sample] for sample in samples]
    batch = [samples2batch[sample] for sample in samples]

    values = dataFrame.to_numpy().tolist()
  
    adjustedValues = removeBatchEffectsNormal(values, batch, group)
  adjustedFrame = pd.DataFrame(adjustedValues, columns = samples, index = proteinIDs)

  return adjustedFrame


  

  

  
 

