from diffAnalysis.diffUtils import constructMultilIndexDataframeForProteimicsDiffAnalysis
from diffAnalysis.proteomicsDiffAnalysisXKK import proteomicsStatistics

def proteomicsDiffAnalysis(
         valuesDic, 
         proteins, 
         baseSamples, 
         targetSamples, 
         foldchangeMethod:str="mean",
         statisticsMethod:str="student-t",          
         multipleTestsCorrectMethod:str="fdr_bh"):
  inputFrame = constructMultilIndexDataframeForProteimicsDiffAnalysis(valuesDic, proteins, baseSamples, targetSamples)
  diffResult = proteomicsStatistics(
    dataframe  = inputFrame, 
    experiment = "experiment", 
    control    = "control", 
    foldchangeMethod = foldchangeMethod,
    statisticsMethod = statisticsMethod,          
    multipleTestsCorrectMethod = multipleTestsCorrectMethod
  )
  return diffResult


def proteomicsDiffAnalysisMultipleGroupPairs(
      valuesDic, 
      proteins, 
      groupPairs, 
      groups2samples, 
      foldchangeMethod:str = "mean",
      statisticsMethod:str = "student-t",          
      multipleTestsCorrectMethod:str = "fdr_bh"):
  diffResultList = []
  for eachGroupPair in groupPairs:
    baseSamples   = groups2samples[eachGroupPair["baseGroup"]]
    targetSamples = groups2samples[eachGroupPair["targetGroup"]]
    samplesInGroups = baseSamples + targetSamples

    subValuesDic = {}
    for eachSample in samplesInGroups:
      subValuesDic[eachSample] = valuesDic[eachSample]
    diffResult = proteomicsDiffAnalysis(subValuesDic, proteins, baseSamples, targetSamples, 
      foldchangeMethod, statisticsMethod, multipleTestsCorrectMethod)
    diffResultList.append(diffResult)
  
  return diffResultList

  