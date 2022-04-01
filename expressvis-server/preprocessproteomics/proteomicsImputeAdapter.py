from preprocessproteomics.proteomicsImpute import impute

def imputeNAs(dataframe, imputeSettings):
  if ("subSetting" in imputeSettings):
    frameAfterImpute = impute(
      dataframe = dataframe, 
      method      = imputeSettings["method"],
      percentile  = imputeSettings["subSetting"],
      replaceZero = True)
    return frameAfterImpute
  else:
    frameAfterImpute = impute(
      dataFrame  = dataframe, 
      method     = imputeSettings["method"],
      replaceZero = True
    )
    return frameAfterImpute