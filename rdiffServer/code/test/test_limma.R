library(testthat)
source("../limma.R")

# test_that("Filter using intensity", {
#   esetFilePath  <- "../../testData/rawData/GSE109186/eSet.rds"
#   eset <- readRDS(esetFilePath)
#   baseSamples   <- c("GSM2935058", "GSM2935059", "GSM2935060", "GSM2935061", "GSM2935062")
#   targetSamples <- c("GSM2935063", "GSM2935064", "GSM2935065", "GSM2935066", "GSM2935067")
#   filteredEset  <- filterByIntensity(
#                       eset            = eset,
#                       baseSamples     = baseSamples,
#                       targetSamples   = targetSamples,
#                       valueThreshold  = 0.25,
#                       numberThreshold = 1)
#   expect_equal(length(featureNames(filteredEset)), 38435)
# })

# test_that("Filter by feature data", {
#   esetFilePath  <- "../../testData/rawData/GSE109186/eSet.rds"
#   eset          <- readRDS(esetFilePath)
#   esetFilter    <- filterByFeatureData(eset        = eset, 
#                                        annoLibrary = "hugene20sttranscriptcluster.db")
#   expect_equal(length(featureNames(esetFilter)), 29421)
# })


test_that("Affy differential result", {
  esetFilePath  <- "../../testData/rawData/GSE109186/eSet.rds"
  eset          <- readRDS(esetFilePath)
  baseSamples   <- c("GSM2935058", "GSM2935059", "GSM2935060", "GSM2935061", "GSM2935062")
  targetSamples <- c("GSM2935063", "GSM2935064", "GSM2935065", "GSM2935066", "GSM2935067")
  
  esetFilter    <- filterByFeatureData(eset        = eset, 
                                       annoLibrary = "hugene20sttranscriptcluster.db")
  diffResults   <- affyLimmaDiffAnalysis(eset          = esetFilter, 
                                         baseSamples   = baseSamples,
                                         targetSamples = targetSamples)
  print(head(diffResults))
})

# test_that("affyLimmaMultipleDiffGroupPairsDiffAnalysis", {
#   esetFilePath  <- "../../testData/rawData/GSE109186/eSet.rds"
#   diffGroupPairsInfo <- list(
#     list(baseGroup   = c("GSM2935058", "GSM2935059", "GSM2935060", "GSM2935061", "GSM2935062"), 
#          targetGroup = c("GSM2935063", "GSM2935064", "GSM2935065", "GSM2935066", "GSM2935067")),

#     list(baseGroup   = c("GSM2935063", "GSM2935064", "GSM2935065", "GSM2935066", "GSM2935067"),
#          targetGroup = c("GSM2935058", "GSM2935059", "GSM2935060", "GSM2935061", "GSM2935062"))
#   )
#   diffResults <- affyLimmaMultipleDiffGroupPairsDiffAnalysis(
#     esetPath           = esetFilePath, 
#     annoLibrary        = "hugene20sttranscriptcluster.db", 
#     diffGroupPairsInfo = diffGroupPairsInfo,
#   )
#   print(str(diffResults))
# })



