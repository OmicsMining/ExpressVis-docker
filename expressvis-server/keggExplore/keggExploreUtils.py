import urllib.request
import base64
import os
import pandas as pd
import json

from fgvis.settings import DATABASE_DIR

# from idConversion.idMapping     import obtainProbesFromEntrez
# from dataset.subsetDataset      import subsetProcessedDataByGenesFromGEO
from clustering.clusteringUtils import Matrix2clusterTree, obtainValuesArraysAcrossGroupsSamples


class PathwayInfoParse():
  def __init__(self, pathwayInfoString):
    self.pathwayInfoString = pathwayInfoString
    self.lines = pathwayInfoString.split("\n")
    self.firstWordNumList = [len(line.split(" ")[0]) for line in self.lines]
  def _obtainMaximWhiteSpaceInTheFront(self):
    maxWhiteSpaceNum = 0
    for eachLine in self.lines:
      if not eachLine.startswith(" "): # means there are terms
        whiteSpaceNum = len(eachLine.split(" ")[0]) + 1
        if whiteSpaceNum > maxWhiteSpaceNum:
          maxWhiteSpaceNum = whiteSpaceNum
      # if eachLine.startswith(" "):
      #   whiteSpaceNum = len(eachLine) - len(eachLine.lstrip(' '))
      #   if whiteSpaceNum > maxWhiteSpaceNum:
      #     maxWhiteSpaceNum = whiteSpaceNum
      #! Do not use this, some descriptions may contain multiple paragraphs. The the maxWhiteSapceNum is larger
    self.maxWhiteSpaceNum = maxWhiteSpaceNum
  def _obtainTermRange(self, term):
    ifTermExist = False # if the word exists in the firt words
    termStart = 0
    termEnd = 0

    for wordNum, line, index in zip(self.firstWordNumList, self.lines, range(len(self.lines))):
      firstWord = line.split((self.maxWhiteSpaceNum-wordNum)*" ")[0]
      if firstWord == term:
        ifTermExist = True
        termStart = index
        termSplitWhite = (self.maxWhiteSpaceNum-wordNum)*" "
        break
    if ifTermExist:
      if self.firstWordNumList[termStart+1] > 0:
        termEnd = termStart + 1
      else:
        for index, wordNum in enumerate(self.firstWordNumList[(termStart+2):]):
          if wordNum > 0:
            termEnd = termStart + index + 2
            break
      return {"start": termStart, "end": termEnd, "splitWhite": termSplitWhite}
    else:
      return None
  def obtainEntryID2symbol(self):
    self._obtainMaximWhiteSpaceInTheFront()
    termRange = self._obtainTermRange("GENE")
    
    entry2symbol = {}
    firstGeneInfoList = self.lines[termRange["start"]].strip().split(termRange["splitWhite"])[1].split("  ")
    firstGeneID     = firstGeneInfoList[0]
    firstGeneSymbol = firstGeneInfoList[1].strip().split(";")[0]
    entry2symbol[firstGeneID] = firstGeneSymbol

    for line in self.lines[(termRange["start"] + 1): termRange["end"]]:
      geneID     = line.strip().split("  ")[0]
      geneSymbol = line.strip().split("  ")[1].split(";")[0]
      entry2symbol[geneID] = geneSymbol

    return entry2symbol
   

def obtainEntryID2Symbol(speciesID, pathwayID):
  '''
  Note: 
    The files are stored in the database
  '''
  pathwayInfoPath = os.path.join(DATABASE_DIR, "speciesCenteredInfo", speciesID, "kegg", "pathwayInfo", pathwayID + ".txt")
  with open(pathwayInfoPath, "r") as fp:
    pathwayInfoString = fp.read()
  
  pathwayInfoParse = PathwayInfoParse(pathwayInfoString = pathwayInfoString)
  entry2symbol = pathwayInfoParse.obtainEntryID2symbol()
  
  return entry2symbol

def obtainPathwaysInOneSpecies(speciesID):
  pathwaysInfoFile = os.path.join(DATABASE_DIR, "speciesCenteredInfo", speciesID, "kegg", "pathwaysInfoInSpecies.json")
  with open(pathwaysInfoFile, "r") as fp:
    pathwaysInfo = json.load(fp)
  return pathwaysInfo


def obtainKEGGpathwayGenesInfo(kegg_id, *args, **kwargs):
  '''
  Return: a dictionary, {geneEntry: symbol}
  '''
  kegg_entry_url = "http://rest.kegg.jp/get/" + kegg_id
  try:
    kegg_entry_open = urllib.request.urlopen(kegg_entry_url)
    kegg_entries    = kegg_entry_open.read().decode().split("\n")
    gene_start = 0
    gene_end   = 0
    for i, entry in enumerate(kegg_entries):
      entry_split = entry.split(  )
      if (len(entry_split) >0):
        if (entry_split[0] == "GENE"):
          gene_start = i
    for i, entry in enumerate(kegg_entries):
      if (i > gene_start):
        entry_split = entry.split("   ")
        if (entry_split[0]):
          gene_end = i
          break
    # obtain the genes' entrez id and symbol
    genes_id_symbol = {}
    # the first
    geneStart = kegg_entries[gene_start].strip().split("     ")
    gene_id = geneStart[1].strip().split("  ")[0]
    gene_symbol = geneStart[1].strip().split("  ")[1].split(";")[0]
    genes_id_symbol[gene_id] = gene_symbol
    for gene in kegg_entries[(gene_start + 1):gene_end]:
      gene_split  = gene.strip().split("  ")
      gene_id     = gene_split[0]
      gene_symbol = gene_split[1].split(";")[0]
      genes_id_symbol[gene_id] = gene_symbol

    kegg_entry_open.close()

    return genes_id_symbol
  except urllib.error.HTTPError as e:
    error_note = "The kegg server couldn\'t fulfill the request. \n" \
                        "Error code: " + str(e.code)
    return error_note
  except urllib.error.URLError as e:
    error_note = "We failed to reach a server. \n" \
                        "Reason: " + str(e.reason)
    return error_note
  
def obtainKeggPathwayKGMLstringFromWebsite(keggID, *args, **kwargs):
  '''
  Download KGML string from the KEGG website
  '''
  kgmlUrl    = "http://rest.kegg.jp/get/" + keggID + "/kgml"

  try:
    kgmlOpen   = urllib.request.urlopen(kgmlUrl)
    kgmlString = kgmlOpen.read()
    kgmlString = base64.b64encode(kgmlString).decode("utf-8") 
    kgmlOpen.close()
    return kgmlString
  except urllib.error.HTTPError as e:
    errorNote = "The kegg server couldn\'t fulfill the request. \n" \
                         "Error code: " + str(e.code)
    errorNote += errorNote
    return errorNote
  except urllib.error.URLError as e:
    errorNote = "We failed to reach the server. \n" \
                "Reason: " + str(e.reason)
    return errorNote

def obtainKeggPathwayKGMLstringFromLocalDatabase(speciesID, pathwayID):
  pathwayKgmlPath = os.path.join(DATABASE_DIR, "speciesCenteredInfo", speciesID, "kegg", "kgmlString", pathwayID)
  with open(pathwayKgmlPath) as fp:
    kgmlString = fp.read()
    return kgmlString

def obtainKeggPathwayKGMLstring(speciesID, pathwayID):
  return obtainKeggPathwayKGMLstringFromLocalDatabase(speciesID, pathwayID)


# def obtainKeggGenesClusteringInfoFromDataset(keggID, geoSeriesAcc, groups, *args, **kwargs):
#   '''
#   Steps:
#     1. obtain genes in the pathway
#     2. cluster genes across samples
#     3. cluster genes across groups
#   return: 
#     {
#       pathwayID: string,
#       acrossGroups:  ClusteringResult, 
#       acrossSamples: ClusteringResult
#     },
#     ClusteringResult: 
#       {
#         xDendgrogramInfor: any;
#         yDendgrogramInfor: any;
#         dataArray: number[][];
#         xTerms: string[];
#         yTerms: string[];
#       }
#   '''
#   pathwayGenes2Symbols = obtainKEGGpathwayGenesInfo(kegg_id = keggID)
#   pathwayGenes = list(pathwayGenes2Symbols.keys())
#   # obtain probe ids
#   genesInfoInArray = obtainProbesFromEntrez(
#     annoPkgName = "hugene20sttranscriptcluster.db", # obtain annoPkgName first
#     genes       = pathwayGenes)
#   genesProbes = genesInfoInArray["PROBEID"].to_list()
#   # obtain expression info for clustering
#   processedData = subsetProcessedDataByGenesFromGEO(
#                    accession = geoSeriesAcc,
#                    genes     = genesProbes )
#   genesExprs = obtainValuesArraysAcrossGroupsSamples(
#                   processedData = processedData,
#                   groups = groups )
#   exprsAcrossSamples = genesExprs["samplesExprsMatrix"] 
#   exprsAcrossGroups  = genesExprs["groupsExprsMatrix"]
#   samples    = genesExprs["samples"]
#   groupNames = genesExprs["groupNames"]
#   genes      = genesExprs["genes"]
#   # obtain genes symbols
#   genesInfoInArrayReIndex = genesInfoInArray.set_index("PROBEID")
#   genesInfoInArrayReIndex = genesInfoInArrayReIndex.reindex(genes, fill_value = "")
#   genesSymbols = genesInfoInArrayReIndex["SYMBOL"].to_list()

#   assert len(genes) == len(genesSymbols)
#   # obtain dendrogram
#   acrossSamplesLeftDendgro = Matrix2clusterTree(matrix = exprsAcrossSamples).gainClusterJson()
#   acrossSamplesTopDendgro  = Matrix2clusterTree(matrix = exprsAcrossSamples.transpose()).gainClusterJson()

#   acrossGroupsLeftDendgro = Matrix2clusterTree(matrix = exprsAcrossGroups).gainClusterJson()
#   acrossGroupsTopDendgro  = Matrix2clusterTree(matrix = exprsAcrossGroups.transpose()).gainClusterJson()
  
#   # return result
#   keggPathClusterInfo = {
#     "pathwayID": keggID,
#     "dataID": geoSeriesAcc,
#     "acrossGroups": {
#       "leftDendgrogramInfor": acrossGroupsLeftDendgro,
#       "topDendgrogramInfor": acrossGroupsTopDendgro,
#       "dataArray": exprsAcrossGroups,
#       "leftUniqueTerms": genes, 
#       "leftDisplayTerms": genesSymbols,
#       "topUniqueTerms": groupNames
#     },
#     "acrossSamples": {
#       "leftDendgrogramInfor": acrossSamplesLeftDendgro,
#       "topDendgrogramInfor": acrossSamplesTopDendgro,
#       "dataArray": exprsAcrossSamples,
#       "leftUniqueTerms": genes,
#       "leftDisplayTerms": genesSymbols,
#       "topUniqueTerms": samples,
#     }
#   }
#   return keggPathClusterInfo

# def obtainProbeID2EntryIDForMicroarray(annoPkgName, speciesID):
#   '''
#   return： {
#     probeID: entryID
#   }
#   '''
#   entryIDtype = "ENTREZID" # obtain entryIDtype for a species
  
#   annoFile  = os.path.join(DATABASE_DIR, "annotations", "biocpackages", annoPkgName + ".ftr")
#   annoFrame = pd.read_feather(annoFile)
  
#   annoFilter = annoFrame.loc[annoFrame[entryIDtype].notnull(), ]
#   # delete probes that have multiple genes annotations
#   annoFilter = annoFilter.drop_duplicates(subset = ["PROBEID"], keep = "first")
#   # change frame to a dictionary, key 
#   probeID2EntryID = {}
#   for probeID, entryID in zip(annoFilter["PROBEID"], annoFilter[entryIDtype]):
#     probeID2EntryID[probeID] = entryID
#   return probeID2EntryID


