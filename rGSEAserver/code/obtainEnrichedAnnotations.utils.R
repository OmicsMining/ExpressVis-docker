library(rjson)
library(purrr)
library(dplyr)

prepareOneTypeAnnotationDataForGSEA <- function(databaseDir, annotationType, IDtype) {
  # return a list
  # $`1368092_Rora_activates_gene_expression`
  # [1] "11865"  "12753"  "12894"  "18143"  "19017"  "19883"  "20787"  "217166"
  # [9] "328572"
  # 
  # $`1368110_Bmal1:Clock,Npas2_activates_circadian_gene_expression`
  # [1] "11865"  "11998"  "12753"  "12952"  "12953"  "13170"  "14068"  "18143" 
  # [9] "18626"  "18627"  "19013"  "19883"  "20893"  "59027"  "79362"  "217166"
  annotationPath = paste(databaseDir, "/pathID2", IDtype, annotationType, ".json", sep = "")
  annotationData <- rjson::fromJSON(file = annotationPath)
  
  IDsInAnnotation = map(annotationData, function(annotation) {
    #print(annotation[["ids"]])
    return (annotation[["ids"]]) # ID
  })
  annotationNames = map_chr(annotationData, function(annotation) {
    return (annotation[["name"]]) # annotation name
  })
  # change list names
  names(IDsInAnnotation) <- paste(annotationType, names(annotationData), annotationNames, sep = "#") # sep by "#"
  return (IDsInAnnotation)
}


prepareAnnotationDataForCorGSEA <- function(databaseDir, annotationTypes, IDtype) {
  annotationIDs = do.call(c,lapply(annotationTypes, function(type) {
    return (prepareOneTypeAnnotationDataForGSEA(databaseDir, type, IDtype))
  }))
  return (annotationIDs)
}
