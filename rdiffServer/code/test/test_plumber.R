library(testthat)
library(httr)

test_that("test_sum", {
  # resultSum <- httr::POST("http://127.0.0.1:8001/sum", body = "{'a':'1','b':'3'}", encode = "raw")
  resultSum <- httr::POST("http://127.0.0.1:8001/sum", body = list(a = 1, b = 3), encode = "json")
  resultValue <- httr::content(resultSum, encoding = "UTF8")[[1]]
  expect_equal(resultValue, 4)
})


