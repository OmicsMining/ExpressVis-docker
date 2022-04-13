source("./obtainEnrichedAnnotations.R")
source("./obtainEnrichedAnnotations.utils.R")

library(rjson)

ANNOTATION_DATABASE_DIR = "/database/serveredByDjango/speciesCenteredInfo"

#* @param speciesID
#* @param geneIDtype
#* @param valuesForRank
#* @param genes
#* @param annotationTypes
#* @post /corenrichedannotations
function(speciesID, geneIDtype, valuesForRank, genes, annotationTypes) {
  annotationDir = paste(ANNOTATION_DATABASE_DIR, "/", speciesID, "/annotationsForEnrichment/", sep = "")
  genesets = prepareAnnotationDataForCorGSEA(annotationDir, annotationTypes, geneIDtype)
  ranks = setNames(valuesForRank, genes)
  
  fgseaRes <- gseaAnalysis(genset  = genesets,
                           rank    = ranks,
                           minSize = 3,
                           maxSize = 500,
                           nperm   = 10000)
  fgseaRes <- fgseaRes[order(pval), ]
  
  fgseaResFilter <- fgseaRes[which(fgseaRes $ pval <= 0.05), ]
  
  genesInSet <- unlist(lapply(fgseaResFilter $ pathway, function(term) {
    allGenesInset <- genesets[[term]]
    genesIntersect <- intersect(allGenesInset, genes)
    return (paste(genesIntersect, collapse = ","))
  }))
  fgseaResFilter[["GenesInAnnotation"]] <- genesInSet
  
  return (rjson::toJSON(fgseaResFilter))
}


#* @param a 
#* @param b
#* @post /sum
function(a, b) {
  sumResult = as.numeric(a) + as.numeric(b)
  return (sumResult)
}
