from constructPPInetwork.ppisQuery import queryPPIsBetweenProteinsBySymbol, convertPPIs2cytoscapeJsGraph
from fgvis.settings import FRONTEND_TEST_DIR
import json

# Generate test data used in PPIexp.
# Input: 
#   Two lists of genes (use symbols here)
#   two datasetIDs
# Steps:
#   1. Generate PPIs for the genes lists
#   2. Generate hierarchical clustering result across each dataset for each list of genes
#      a. Map symbols to ids used in the dataset
#      b. Obtain clustering results
#





list1Symbols = ["IL6", "STAT3", "IL6", "STAT1", "FAM20C", "OSM", "FGL1", "NFKB1", "RELA", "FGG", "STAT2"]
list2Symbols = ["IL6", "STAT3", "IL6", "STAT1", "FAM20C", "OSM", "FGL1", "NFKB1", "RELA", "FGG", "STAT2", "FGB",
                "TRP53", "STAT4", "IL6ST"]

source1      = "GEO"
accession1   = "GSE62208"
annoPkgName1 = "hugene20sttranscriptcluster.db"

source2      = "GEO"
accession2   = "GSE2240"
annoPkgName2 = "hgu133b"



subPPIs1 = queryPPIsBetweenProteinsBySymbol(
                   speciesID = "9606", 
                   database  = "mentha",
                   proteins  = list1Symbols)
subPPIs2 = queryPPIsBetweenProteinsBySymbol(
                   speciesID = "9606", 
                   database  = "mentha",
                   proteins  = list2Symbols)

graph1 = convertPPIs2cytoscapeJsGraph(ppis = subPPIs1)
graph2 = convertPPIs2cytoscapeJsGraph(ppis = subPPIs2)



dataset1Groups = [
  {
    "name": "Negative Control",
    "samples": ["GSM1522519","GSM1522520","GSM1522521"]
  },
  {
    "name": "Positive Control",
    "samples": ["GSM1522522", "GSM1522523", "GSM1522524"]
  },
  {
    "name": "B treatment",
    "samples": ["GSM1522525", "GSM1522526", "GSM1522527"]
  },
  {
    "name": "Il1 Stimulated",
    "samples": ["GSM1522533","GSM1522534","GSM1522535"]
  }
]

dataset2Groups = [
  {
    "name": "hello"
  }
]

# diffGenes = {
#   "up":   ["IL6",  "STAT3"],
#   "down": ["FGL1", "STAT1"]
# }
# diffEdges = {
#   "upEdges":   [1,2],
#   "downEdges": [3,4]
# }

# ppiInfo = {
#   "graph":     graph,
#   "diffGenes": diffGenes,
#   "diffEdges": diffEdges
# }





with open(FRONTEND_TEST_DIR + "/ppiExp/ppi.json", "w") as fileOpen:
  json.dump(ppiInfo, fileOpen)
