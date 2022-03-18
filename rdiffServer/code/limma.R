# use limma for differentially analysis
# @para dataID
# @groups {groupName1: [sample, ...], groupName2: [sample1, ...]}
library(limma)
library(dplyr)
library(purrr)
library(rjson)

filterByIntensity <- function(eset, baseSamples, targetSamples, valueThreshold, numberThreshold) {
  # compute median log-expression for each probes
  # obtain the value of the lowest 25%(threshold)
  # all baseSamples should up the 25%(threshold) value or all the targetSamples up the 25% value
  esetMedians <- rowMedians(Biobase::exprs(eset))
  valueCutoff <- sort(esetMedians)[length(esetMedians) * valueThreshold]
  
  allSamples       <- sampleNames(eset)
  baseIndexes      <- match(baseSamples, allSamples)
  targetIndexes    <- match(targetSamples, allSamples)
  baseSamplesLen   <- length(baseSamples)
  targetSamplesLen <- length(targetSamples)

  selectedIndexes <- apply(Biobase::exprs(eset), 1, function(x) {
    ifBaseDetected <- sum(x[baseIndexes] >= valueCutoff) >= baseSamplesLen * numberThreshold
    ifTargetDected <- sum(x[targetIndexes] >= valueCutoff) >= targetSamplesLen * numberThreshold
    return (ifBaseDetected || ifTargetDected)
  })
  esetFilterd <- subset(eset, selectedIndexes)
  
  return (esetFilterd)
}

filterByFeatureData <- function(eset, annoLibrary) {
  # select probes that have symbol annotaion and have only one symbol annotation
  library(annoLibrary,character.only=TRUE)
  anno <- AnnotationDbi::select(eval(parse(text= annoLibrary)), 
                                keys    = featureNames(eset), 
                                columns = c("SYMBOL", "GENENAME"),
                                keytype = "PROBEID")
  # select probes that have symbol 
  annoWithSymbol <- dplyr::filter(anno, !is.na(SYMBOL))
  ifHasSymbol    <- (featureNames(eset) %in% annoWithSymbol $ PROBEID)
  esetWithSymbol <- subset(eset, ifHasSymbol)
  # filter out the probes that have multiple symbols
  annoFiltered <- annoWithSymbol %>%
    dplyr::group_by(PROBEID) %>%
    dplyr::summarise(no_of_matches = n_distinct(SYMBOL)) %>%
    dplyr::filter(no_of_matches >= 2)

  idsToExclude  <- (featureNames(esetWithSymbol) %in% annoFiltered $ PROBEID)
  esetFinal     <- subset(esetWithSymbol, !idsToExclude)

  return (esetFinal)
}

affyLimmaDiffAnalysis <- function(eset, baseSamples, targetSamples, valueThreshold = 0.25, numberThreshold = 1) {
  # use eset filtered by features
  # filter probes using intensity here
  subExpressSet <- eset[, c(baseSamples, targetSamples)]
  filteredEset  <- filterByIntensity(eset            = subExpressSet, 
                                     baseSamples     = baseSamples,
                                     targetSamples   = targetSamples,
                                     valueThreshold  = valueThreshold,
                                     numberThreshold = numberThreshold) 

  allSamples    <- sampleNames(filteredEset)
  samplesOrder  <- unlist(lapply(allSamples, function(sample) {
    if (sample %in% baseSamples) {
      return(1)
    } else {
      return(2)
    }
  }))
  design           <- model.matrix(~ 0 + factor(samplesOrder))
  colnames(design) <- c("base", "target")
  contrast.matrix  <- makeContrasts(target-base, levels = design)
  
  fit  <- lmFit(filteredEset, design)
  fit2 <- contrasts.fit(fit, contrast.matrix)
  fit2 <- eBayes(fit2)
  
  results    <- decideTests(fit2)
  #print(summary(results))
  diffResult <- topTable(fit2, coef = 1, adjust = "BH", number = Inf, p.value = 1)
  diffResult["PROBEID"] <- row.names(diffResult)
  #return (rjson::toJSON(diffResult)) # not use toJSON here
  return (diffResult)
}

affyLimmaOneDiffGroupPairDiffAnalysis <- function(esetPath, annoLibrary, baseSamples, targetSamples,
  valueThreshold = 0.25, numberThreshold = 1) {
  expressSet <- readRDS(esetPath)
  esetFilteredByFeature <- filterByFeatureData(eset        = expressSet, 
                                               annoLibrary = annoLibrary)

  diffResult <- affyLimmaDiffAnalysis( eset            = esetFilteredByFeature,
                                       baseSamples     = baseSamples, 
                                       targetSamples   = targetSamples,
                                       valueThreshold  = valueThreshold, 
                                       numberThreshold = numberThreshold)
  return (diffResult)
}

affyLimmaOneDiffGroupPairDiffAnalysisFromClient <- function(expressSet, annoLibrary, baseSamples, targetSamples, 
                                                            valueThreshold = 0.25, numberThreshold = 1) {
  esetFilteredByFeature <- filterByFeatureData(eset        = expressSet, 
                                               annoLibrary = annoLibrary)
  
  diffResult <- affyLimmaDiffAnalysis( eset            = esetFilteredByFeature,
                                       baseSamples     = baseSamples, 
                                       targetSamples   = targetSamples,
                                       valueThreshold  = valueThreshold, 
                                       numberThreshold = numberThreshold)
  return (diffResult)
}

affyLimmaMultipleDiffGroupPairsDiffAnalysis <- function(esetPath, annoLibrary, 
  diffGroupPairList, valueThreshold = 0.25, numberThreshold = 1) {
  # @param groupParirsIno
  # example: list(list(baseGroup = c("sample1", "sample2"), targetGroup = c("sample3", "sample4")), 
  #               list(baseGroup = c("sample5", "sample2"), targetGroup = c("sample4", "sample6")))
  # retrun: 
  #   a list, list(baseGroup, targetGroup, diffResult: )

  # Steps
  ## 1. filter eset using feature info (select probes with symbol and filter out probes that have multiple symbols)
  ## 2. for each diffGroupPair, filter using intensity
  ## 3. differential analysis
  expressSet            <- readRDS(esetPath)
  esetFilteredByFeature <- filterByFeatureData(eset        = expressSet, 
                                               annoLibrary = annoLibrary)
  diffResultList <- map(diffGroupPairList, function(groupPairInfo) {
    baseSamples   = groupPairInfo $ baseGroup
    targetSamples = groupPairInfo $ targetGroup
    diffResults <- affyLimmaDiffAnalysis( eset            = esetFilteredByFeature, 
                                          baseSamples     = baseSamples, 
                                          targetSamples   = targetSamples, 
                                          valueThreshold  = valueThreshold, 
                                          numberThreshold = numberThreshold
    )
    return (diffResults)
  })
  return (diffResultList)
}

rnaSeqLimmaMultipleDiffGroupPairsDiffAanalysis <- function(countsPath, diffGroupPairsInfo) {
  
}