library(fgsea)
library(data.table)
library(ggplot2)


data(examplePathways)
data(exampleRanks)
set.seed(42)


fgseaRes <- fgsea(pathways = examplePathways, 
                  stats    = exampleRanks,
                  minSize  = 15,
                  maxSize  = 500)
head(fgseaRes[order(pval), ])


plotEnrichment(examplePathways[["5990979_Cell_Cycle,_Mitotic"]],
               exampleRanks) + labs(title="Cell Cycle Mitotic")


pathwayGenes = examplePathways[["5990979_Cell_Cycle,_Mitotic"]]
rankedGenes = names(exampleRanks)

gseaGenesInfo = list( annotationGenes = pathwayGenes, 
                      rankedGenes = rankedGenes )

