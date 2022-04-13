source("../obtainEnrichedAnnotations.utils.R")

library(testthat)

test_that("convert one annotation type", {
  print(getwd())
  databaseDir = "../../testData/annotationsData/"
  annotationType = "KEGG"
  IDtype = "SYMBOL"

  annotationIDs = prepareOneTypeAnnotationDataForGSEA(databaseDir,annotationType, IDtype )
  print("annotationIDs")
  print(annotationIDs[1:5])
})
# 
# test_that("convert multiple annotation types", {
#   databaseDir <- "../../testData/annotationsData/"
#   annotationTypes = c("Component", "KEGG")
#   annotationIDs = prepareAnnotationDataForCorGSEA(databaseDir, annotationTypes, "SYMBOL")
#   print("annotationIDs")
#   print(annotationIDs[1000:1005])
# })

