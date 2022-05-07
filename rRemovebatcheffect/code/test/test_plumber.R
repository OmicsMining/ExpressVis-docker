library(testthat)
library(httr)
library(SummarizedExperiment)
# 
# test_that("test remove rna-seq batch effect, genrated data", {
#   count_matrix <- matrix(rnbinom(400, size=10, prob=0.1), nrow=50, ncol=8)
#   count_matrix <- rbind(count_matrix, c(0, 0, 0, 0, 0, 0, 0, 0))
#   row.names(count_matrix) <- paste(1:51, "id", sep = "");
#   batch <- c(rep(1, 4), rep(2, 4))
#   group <- rep(c(0,1), 4)
#   print(count_matrix)
#   result <- httr::POST("http://127.0.0.1:8004/removebatcheffectrnaseq",
#                        body = list(counts = count_matrix, batch = batch),
#                        encode = "json")
# 
#   resultValue <- httr::content(result, encoding = "UTF8")
#   print(length(resultValue))
# })

# 
# test_that("test, use read data from the paper", {
#   # https://github.com/zhangyuqing/ComBat-seq
#   counts_frame <- read.table("../../testData/counts.txt", header = T)
#   phenotype_data <- read.table("../../testData/phenotypeData.txt", header = T)
#   
#   genes <- counts_frame $ genes
#   counts_matrix <- as.matrix(counts_frame[, colnames(counts_frame) != "genes"])
#   print(dim(counts_matrix))
#   print(head(counts_matrix))
#   batch <- phenotype_data $ batch
#   group <- phenotype_data $ group
#   # counts <- assays(signature_data)[[1]]
#   # batch <- phenotypeData $ batch
#   # group <- phenotypeData $ group
#   # print(length(batch))
#   # print(length(group))
#   # print(dim(counts))
#   # 
#   print(batch)
#   result <- httr::POST("http://127.0.0.1:8004/removebatcheffectrnaseq", 
#                        body = list(counts = counts_matrix, batch = batch, group = group),
#                        encode = "json")
#   resultValue <- httr::content(result, encoding = "UTF8")
#  # print(head(resultValue[[1]]))
# })


test_that("test, normalized values", {
  library(bladderbatch)
  data(bladderdata)
  dat <- bladderEset[1:50,]
  pheno = pData(dat)
  edata = exprs(dat)
  batch = pheno$batch
  group = pheno$cancer
  
  result <- httr::POST("http://127.0.0.1:8004/removebatcheffectnormalvalues",
                       body = list(values = edata, batch = batch),
                       encode = "json")
  resultValue <- httr::content(result, encoding = "UTF8")
  print(resultValue)
  
  
})