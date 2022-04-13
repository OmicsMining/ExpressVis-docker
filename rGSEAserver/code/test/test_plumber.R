library(testthat)
library(httr)

test_that("test enriched annotations", {
  load(file=file.path(here::here(),"/testData/examplePathways.rda"))
  load(file=file.path(here::here(),"/testData/exampleRanks.rda"))
  
  #* @param speciesID
  #* @param signedlogP
  #* @param genes
  #* 
  
  genes = names(exampleRanks)
  signedlogP = unname(exampleRanks)
  annotationTypes = c("REACTOME", "Process", "Function", "Component")
  gseaEnrichedAnnotations <- httr::POST("http://127.0.0.1:8003/corenrichedannotations", 
                                        body = list(speciesID = "10090", valuesForRank = signedlogP, 
                                                    genes = genes, geneIDtype = 'NcbiEntrezGene', 
                                                    annotationTypes = annotationTypes), 
                                        encode = "json")
  resultValue <- httr::content(gseaEnrichedAnnotations, encoding = "UTF8")[[1]]
  #print(resultValue)
})
