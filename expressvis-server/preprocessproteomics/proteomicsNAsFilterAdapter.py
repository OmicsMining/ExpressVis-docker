import pandas as pd
from preprocessproteomics.proteomicsNAsFilter import naFilter, naConvert

def addGroupsAsMultiindex(dataframe, groups):
  samples = dataframe.columns.tolist()
  samples2groups= {}
  for eachGroup in groups:
    for eachSample in eachGroup["samples"]:
      samples2groups[eachSample] = eachGroup["name"]

  groupsOfSamples = []
  for eachSample in samples:
    groupsOfSamples.append(samples2groups[eachSample])
  
  columnIndexes = pd.MultiIndex.from_arrays([groupsOfSamples, samples])
  dataframe.columns = columnIndexes

  return dataframe



def filterProteinsWithNAs(dataframe, groups, filterSettings):
  frameAfterNaConver = naConvert(dataframe = dataframe)
  if filterSettings["filterType"] == "all":
    frameAfterFilter = naFilter(
      dataframe = frameAfterNaConver,
      naThreshold = filterSettings["percentage"],
      method = filterSettings["filterType"]
    );
    return frameAfterFilter
  else:
    # other methods except 'all' requires groups as multiple indexes
    frameAfterNaConver = addGroupsAsMultiindex(frameAfterNaConver, groups)
    frameAfterFilter = naFilter(
      dataframe = frameAfterNaConver,
      naThreshold = filterSettings["percentage"],
      method = filterSettings["filterType"]
    )

    frameAfterFilter.columns = frameAfterFilter.columns.droplevel(0)
    return frameAfterFilter