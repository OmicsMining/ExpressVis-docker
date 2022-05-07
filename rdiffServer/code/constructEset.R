# construct eSet from expression matrix

library("Biobase")
constructEsetFromExpressionMatrix <- function(expressionMatrix) {
  newEset <- ExpressionSet(assayData = expressionMatrix)
  return (newEset)
}

