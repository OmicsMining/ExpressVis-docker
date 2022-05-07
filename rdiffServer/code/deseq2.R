# differential analysis of RNA-seq data
# 
# To keep accordance with expressionAtlas, we use DESeq2 
# to perform differential analyse of RNA-seq data

library(purrr)
library(DESeq2)
library("BiocParallel")
register(MulticoreParam(4))

readCounts <- function(arrayID, storeDir) {
  # read counts data
  # counts data can be extracted from atlasExperimentSummary.Rdata. assay
  filePath     <- paste(storeDir, arrayID, "/", arrayID, "-raw-counts.tsv", sep = "")
  countsFrame  <- read.csv(filePath, sep = "\t")
  countsMatrix <- as.matrix(countsFrame[, 3:ncol(countsFrame)])
  rownames(countsMatrix) <- unlist(countsFrame["Gene.ID"])
  return (countsMatrix)
}

deseq2Diff <- function(countsMatrix, baseSamples, targetSamples) {
  # subset counts according to samples
  # construct DESeqDataSet
  countsMatrix <- countsMatrix[, c(baseSamples, targetSamples)] 
  samplesType  <- lapply(colnames(countsMatrix), function(sample){
    if (sample %in% baseSamples) {
      return ("Base")
    } else {
      return ("Target")
    }
  })
  samplesAnno <- data.frame(Type = factor(samplesType, levels = c("Base", "Target")))
  row.names(samplesAnno) <- colnames(countsMatrix)
  # DDS, DESeqDataSet
  DDS <- DESeqDataSetFromMatrix(countData = countsMatrix, 
                                colData   = samplesAnno, 
                                design    = ~Type)
  # filter 
  keep <- rowSums(counts(DDS)) >= 5 * length(c(baseSamples, targetSamples)) # TODO: why
  DDS  <- DDS[keep, ]
  # differential analysis
  gc()
  rm(list = c("countsMatrix", "keep", "baseSamples", "targetSamples", "samplesType", "samplesAnno"))
  

  DDS         <- DESeq(DDS)#, parallel=TRUE, BPPARAM=MulticoreParam(4))
  diffResults <- results(DDS)#, parallel=TRUE, BPPARAM=MulticoreParam(4))
  # using parallel does not speed up, why?
  resultFrame <- as.data.frame(diffResults)
  resultSub   <- resultFrame[,c("log2FoldChange","pvalue", "padj")]
  resultSub $ Gene.ID <- rownames(resultSub) # only use log2FoldChange, and padj
  resultSub <- resultSub[, c("Gene.ID", "log2FoldChange", "pvalue", "padj")]
  return (resultSub)
}

deseq2DiffMultipleGroupParis <- function(countsMatrix, diffGroupPairList) {
  diffResultList <- map(diffGroupPairList, function(groupPairInfo) {
    baseSamples   = groupPairInfo $ baseGroup
    targetSamples = groupPairInfo $ targetGroup
    diffResult <- deseq2Diff( countsMatrix  = countsMatrix, 
                              baseSamples   = baseSamples, 
                              targetSamples = targetSamples)
    return (diffResult)
  })
  return (diffResultList)
}

