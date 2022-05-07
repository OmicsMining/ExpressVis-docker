
convertValuesList2matrix <- function(valuesList, genes) {
  # values list is from the client, the client send a
  # dictionary, and the dic is converted to a list, names of the list 
  # is the keys of the dictionary, values is the expression values
  # 
  # The order of genes is the same of the values
  colNames = names(valuesList)
  
  valueMatrix = matrix(unlist(valuesList), ncol = length(colNames))
  
  colnames(valueMatrix) = colNames
  rownames(valueMatrix) = genes 
  
  return (valueMatrix)
}


convertDiffGroupPairs <- function(diffGroupPairs) {
  # Why:  the diff group pairs from the client can not be used directly
  # 
  # @ parameter:
  # diffGroupPairVector in the client (python)
  # [
  #   {"baseGroup":    ["GSM1522519","GSM1522520","GSM1522521"], 
  #     "targetGroup": ["GSM1522522", "GSM1522523", "GSM1522524"]
  #   },
  #   {"baseGroup": ["GSM1522519","GSM1522520","GSM1522521"], 
  #     "targetGroup": ["GSM1522525", "GSM1522526", "GSM1522527"]},
  #   {"baseGroup": ["GSM1522519","GSM1522520","GSM1522521"], 
  #     "targetGroup": ["GSM1522533","GSM1522534","GSM1522535"]},
  # ]
  # return: 
  #   a list
  # TODO: the input structure is not clear
  
  groupPairList = list()
  for (i in 1:nrow(diffGroupPairs)) {
    baseGroupVector   = diffGroupPairs[i, "baseGroup"][[1]]
    targetGroupVector = diffGroupPairs[i, "targetGroup"][[1]]
    groupPairList[[i]] = list("baseGroup" = baseGroupVector, "targetGroup" = targetGroupVector)
  }
  
  return (groupPairList)
}













