import pandas as pd

def constructMultilIndexDataframeForProteimicsDiffAnalysis(valuesDic, proteins, baseSamples, targetSamples):
  '''
  The data from the client can not be directly used in proteins diff analyses, 
  They need to be tranformed 
  '''
  samples = list(valuesDic.keys())
  groupsOfSamples = []
  for eachSample in samples:
    if eachSample in baseSamples:
      groupsOfSamples.append("control")
    elif eachSample in targetSamples:
      groupsOfSamples.append("experiment")
  
  valuesDic["Protein IDs"] = proteins
  dataframe = pd.DataFrame.from_dict(valuesDic)
  dataframe = dataframe.set_index("Protein IDs")
  # set multiIndexes
  columnIndexes = pd.MultiIndex.from_arrays([groupsOfSamples, samples])
  dataframe.columns = columnIndexes

  return dataframe