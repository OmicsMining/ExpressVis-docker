import os
import json
from fgvis.settings import BASE_DIR, DATABASE_DIR

def loadPPIs(speciesID, database, IDtype):
  '''
  Load PPIs stored in json formats
  
  Return:
    list of list
    [IDA,IDB, SYMBOLA, SYMBOLB][]
  '''
  ppisFile = os.path.join(DATABASE_DIR, "speciesCenteredInfo", speciesID, "PPIs", database + "PPI" + IDtype + ".json")
  with open(ppisFile, "r") as fileOpen:
    ppis = json.load(fileOpen)
  return ppis

def queryPPIsBetweenProteinsBySymbol(speciesID, database, proteins):
  '''
  In PPIUniprotID.json, the third and forth columns are symbols

  To keep consistent, we add symbol in the third column and forth column

  notes: 
    All symbols are upper case

  return
    [sourceSymbol, targetSymbol, sourceSymbol, targetSymbol]
  '''
  SOURCE_SYMBOL_INDEX = 2
  TARGET_SYMBOL_INDEX = 3

  ppis = loadPPIs(speciesID = speciesID, database = database, IDtype = "UniprotID")
  
   # All symbols are upper case in Mentha
  proteinsUpper2RawDic = {};
  for eachPro in proteins:
    proteinsUpper2RawDic[eachPro.upper()] = eachPro
  proteinsUpper = set(proteinsUpper2RawDic.keys())

  # To 
  subPPIs = []
  for eachPPI in ppis:
    sourceSymbol = eachPPI[SOURCE_SYMBOL_INDEX]
    targteSymbol = eachPPI[TARGET_SYMBOL_INDEX]
    if sourceSymbol in proteinsUpper and targteSymbol in proteinsUpper:
      subPPIs.append([proteinsUpper2RawDic[sourceSymbol], proteinsUpper2RawDic[targteSymbol], 
                      proteinsUpper2RawDic[sourceSymbol], proteinsUpper2RawDic[targteSymbol]])
  
  return subPPIs

def queryPPIsBySymbol(speciesID, database, proteins, subNetworkType):
  '''
  interactionType is not a good name
  '''
  if subNetworkType == "between":
    return queryPPIsBetweenProteinsBySymbol(speciesID = speciesID, database = database, proteins = proteins)



def queryPPIs(speciesID, database, IDtype, proteinIDs, subNetworkType):
  '''
  Input:
    requestData
      {
        speciesID,
        database,
        IDtype,
        proteinIDs,
        subNetworkType
      }
  
  '''
  if IDtype == "SYMBOL":
    return queryPPIsBySymbol(speciesID = speciesID, database = database, 
                             proteins  = proteinIDs, subNetworkType = subNetworkType)


def convertPPIs2cytoscapeJsGraph(ppis):
  '''
  Input:
    ppis, a list of list, the list is [IDA,IDB, SYMBOLA, SYMBOLB][]
  return:
    graph data used in the front-end 
    {
      edges: [
        {
          data: {
            id:
            source: 
            target: 
          }
        }
      ],
      nodes: [
        {
          data: {
            id: 
            name: 
          }
        }
      ]
    }
  '''
  PROA_ID_INDEX   = 0
  PROB_ID_INDEX   = 1
  PROA_NAME_INDEX = 2
  PROB_NAME_INDEX = 3
  
  nodesAdded = []
  edges = []
  nodes = []
  
  for i, eachPPI in enumerate(ppis):
    edges.append({"data": {"id": i, "source": eachPPI[PROA_ID_INDEX],  "target": eachPPI[PROB_ID_INDEX]}})
    if eachPPI[PROA_ID_INDEX] not in nodesAdded:
      nodes.append({"data": {"id": eachPPI[PROA_ID_INDEX], "name": eachPPI[PROA_NAME_INDEX]}})
      nodesAdded.append(eachPPI[PROA_ID_INDEX])
    if eachPPI[PROB_ID_INDEX] not in nodesAdded:
      nodes.append({"data": {"id": eachPPI[PROB_ID_INDEX], "name": eachPPI[PROB_NAME_INDEX]}})
      nodesAdded.append(eachPPI[PROB_ID_INDEX])
  return {
    "edges": edges,
    "nodes": nodes
  }


 
  

