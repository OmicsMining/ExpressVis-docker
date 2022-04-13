
library(fgsea) # install in bioconductor 
library(tidyverse)



gseaAnalysis <- function(genset,# 富集所用基因集,list格式
                         rank, # Rank信息,对于相关性, 使用-logP*Sign(Corr), numeric格式
                         minSize=3, # 最小Target基因数目
                         maxSize=500, # 最大Target基因数目
                         nperm=10000# 置换检验的次数
){
  fgseaRes <- fgsea::fgsea(pathways = genset, stats = rank, minSize=minSize,
                           maxSize=maxSize,nperm=nperm)
  fgseaRes <- fgseaRes[order(NES), ]
  return (fgseaRes)
  
}

