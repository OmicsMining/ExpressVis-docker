source("./client2server.utils.R")
source("./constructEset.R")
source("./diffAnalysis.utils.R")
source("./limma.R")
source("./deseq2.R")
library(rjson)


DATABASE_DIR = "/media/thudxz/Research/process/bioinformatics_tools/angular_django_time_series/database/"
#* @param geoSeriesAcc
#* @param baseSamples
#* @param targetSamples
#* @post /arrayonegrouppairdiffanalysiswithseriesacc
function(geoSeriesAcc, annoLibrary, baseSamples, targetSamples) {
  geoSubDir  <- formatGEOfilePath(geoSeriesAcc = geoSeriesAcc)
  geoEdsPath <- paste(DATABASE_DIR, "datasets/", "GEO/", geoSubDir, 
                      "/", geoSeriesAcc, "/eSet.rds",
                      sep = "")
  expressSet <- readRDS(geoEdsPath)

  diffResults <- affyLimmaOneDiffGroupPairDiffAnalysis( 
    expressSet    = expressSet, 
    annoLibrary   = annoLibrary, 
    baseSamples   = baseSamples, 
    targetSamples = targetSamples
  )
  
  return (rjson::toJSON(diffResults))
}


#* @param geoSeriesAcc
#* @param annoLibrary
#* @param diffGroupPairs
#* @post /arraymultiplediffanalysiswithseriesacc
function(geoSeriesAcc, annoLibrary, diffGroupPairs) {
  geoSubDir  <- formatGEOfilePath(geoSeriesAcc = geoSeriesAcc)
  geoEdsPath <- paste(DATABASE_DIR, "datasets/", "GEO/", geoSubDir, 
                      "/", geoSeriesAcc, "/eSet.rds",
                      sep = "")
  expressSet <- readRDS(geoEdsPath)
  
  groupPairList <- convertDiffGroupPairs(diffGroupPairs)
  
  diffResults <- affyLimmaMultipleDiffGroupPairsDiffAnalysis(
    expressSet        = expressSet, 
    annoLibrary       = annoLibrary, 
    diffGroupPairList = groupPairList
  )
  return (rjson::toJSON(diffResults)) # use toJSON here
}


#* @param valuesDic
#* @param genes
#* @param annoLibrary
#* @param diffGroupPairs
#* @post /arrayMultipleDiffAnalysisWithValues
function(valuesDic, genes, annoLibrary, diffGroupPairs) {
  valuesMatrix  <- convertValuesList2matrix(valuesDic, genes)
  groupPairList <- convertDiffGroupPairs(diffGroupPairs)
  
  expressSet <- constructEsetFromExpressionMatrix(valuesMatrix)
  diffResults <- affyLimmaMultipleDiffGroupPairsDiffAnalysis(
    expressSet  = expressSet,
    annoLibrary = annoLibrary,
    diffGroupPairList = groupPairList,
  )
  
  return (rjson::toJSON(diffResults))
}

#* @param valuesDic
#* @param genes
#* @param annoLibrary
#* @param baseSamples
#* @param targetSamples
#* @post /arrayOneDiffGroupPairWithValues
function(valuesDic, genes, annoLibrary, baseSamples, targetSamples) {
  valuesMatrix <- convertValuesList2matrix(valuesDic, genes)
  expressSet <- constructEsetFromExpressionMatrix(valuesMatrix)
  
  diffResults <- affyLimmaOneDiffGroupPairDiffAnalysisFromClient(
    expressSet    = expressSet, 
    annoLibrary   = annoLibrary, 
    baseSamples   = baseSamples, 
    targetSamples = targetSamples,
  )
  
  return (rjson::toJSON(diffResults))
}

#* @param countsDic
#* @param genes
#* @param baseSamples
#* @param targetSamples
#* @post /deseq2WithCounts
function(countsDic, genes, baseSamples, targetSamples) {
  countsMatrix = convertValuesList2matrix(countsDic, genes)
  
  diffResults = deseq2Diff(
    countsMatrix  = countsMatrix,
    baseSamples   = baseSamples,
    targetSamples = targetSamples
  )
  return (rjson::toJSON(diffResults)) 
}

#* @param countsDic
#* @param genes
#* @param diffGroupPairs
#* @post /deseq2WithCountsMultipleGroupPairs
function(countsDic, genes, diffGroupPairs) {
  countsMatrix  <- convertValuesList2matrix(countsDic, genes)
  groupPairList <- convertDiffGroupPairs(diffGroupPairs)

  diffResults <- deseq2DiffMultipleGroupParis(
    countsMatrix      = countsMatrix,
    diffGroupPairList = groupPairList
  )
  return (rjson::toJSON(diffResults))
}



#* @param a 
#* @param b
#* @post /sum
function(a, b) {
  sumResult = as.numeric(a) + as.numeric(b)
  return (sumResult)
}


#* @post /test
# function(baseSamples, targetSamples) {
#   # baseSamples is a string seperated with ,
#   baseSamples   = unlist(strsplit(baseSamples, ","))
#   targetSamples = unlist(strsplit(targetSamples, ","))
#   frame <- data.frame(a = c(1,3,4), b = c("h", "l", "h"))
#   return (list(frame, frame))
# }