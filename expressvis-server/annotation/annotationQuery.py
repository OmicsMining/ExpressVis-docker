import json
import os
import numpy as np
import pandas as pd
from fgvis.settings import DATABASE_DIR
from annotation.utils import obtainSubList
#import feather
from os import walk
import time

from pymongo import MongoClient
# from dataset.settings import GEOspeciesName2taxID

client           = MongoClient()
IDannotaionsDB   = client["geneIDannotations"]
arrayCollections = IDannotaionsDB["microarrayIDannotations"]

# query genes basic info -- start

IDtypesBesidesMicroarray = ["NcbiEntrezGene", "EnsemblGene", "UniprotID", "NcbiRefseqProtein", "SYMBOL"]

IDtypeBasicInfoSettings = {
  "NcbiEntrezGene": {
    "fileName": "NcbiEntrezGeneCenterAnnotation.json",
    "neededAttributes": ['symbol', 'description'] 
  },
  "SYMBOL": {
    "fileName": "SYMBOLCenterAnnotation.json",
    "neededAttributes": ['description'] 
  },
  "EnsemblGene": {
    "fileName": "EnsemblGeneCenterAnnotation.json",
    "neededAttributes": ['Symbol', 'Description', 'Gene Type']
  },
  "UniprotID": {
    "fileName": "UniprotIDCenterAnnotation.json", 
    "neededAttributes": ['EntryName', 'Symbol', 'ProteinName']
  },
  "NcbiRefseqProtein": {
    "fileName": "NcbiRefseqProteinCenterAnnotation.json",
    "neededAttributes": ['symbol', 'description']
  }
}


frontAnnoName2databaseAnnoName = {
  # Map GO Types from the front-end to these in the database  
  # name in the database are not the same as displayed in the front-end
  "Biological Process": "Process",
  "Molecular Function": "Function",
  "Cellular Component": "Component",
  
  "KEGG Pathway":     "KEGG",
  "REACTOME Pathway": "REACTOME",
  "WikiPathways":     "WikiPathways",
}




def obtainGeneIDannoInfor(speciesID, IDtype):
  ifIsMicroarrayID = _checkIfIdtypeIsMicroarrayID(IDtype)
  if ifIsMicroarrayID:
    return _obtainMicroarrayProbeIDannoInfoForDisplay(speciesID, IDtype)
  else:
    return _obtainGeneIDannoInfoOtherThanMicrorrays(speciesID, IDtype)


def _obtainMicroarrayProbeIDannoInfoForDisplay(speciesID, annoPkgName):
  '''
  Purpose: 
    For differential analysis, we need to display the information of the differentiall-expressed genes
    For clustering analysis, we need to display the information of the selected genes
  return: 
    {
      probeID: [ENTREZID, SYMBOL, GENENAME] 
    }
  NoteID:
    ENTREZID is used for enrichment analysis
  ''' 
  annoFile  = os.path.join(DATABASE_DIR, "speciesCenteredInfo", speciesID, "microarrayAnnotations", annoPkgName + ".db.json")
  with open(annoFile, 'r') as fp:
    probeID2anno = json.load(fp)

  return probeID2anno

def _obtainSubGenesInfo(allGenesInfo, neededAttributes):
  '''
  Only retain neededAttributes
  '''
  attributesHas = allGenesInfo["attributes"]

  neededAttributesIndex = [attributesHas.index(eachFeature) for eachFeature in neededAttributes]

  subAnnoGenesInfo = {}
  for key, values in allGenesInfo["genesInfoDic"].items():
    subAnnoGenesInfo[key] = obtainSubList(values, neededAttributesIndex)
  
  return {
    "attributes":     neededAttributes,
    "genesInfoDic": subAnnoGenesInfo
  }

def _obtainGeneIDannoInfoOtherThanMicrorrays(speciesID, IDtype):
  '''
  Note: 
    1. Only query the needed attribute values 
  return {
    attributes: ["feature1", "feature2", "feature3"],
    genesInfoDic: {
      "id1": [id1 feature1, id1 feature2, id1 feature3]
    }
  }
  '''
  neededAttributes = IDtypeBasicInfoSettings[IDtype]["neededAttributes"]
  annoFile = os.path.join(DATABASE_DIR, "speciesCenteredInfo", speciesID, "idCenteredAnnotations", IDtypeBasicInfoSettings[IDtype]["fileName"])
  with open(annoFile, 'r') as fp:
    annoGenesInfo = json.load(fp)

  return _obtainSubGenesInfo(annoGenesInfo, neededAttributes)

def _checkIfIdtypeIsMicroarrayID(IDtype):
  return not(IDtype in IDtypesBesidesMicroarray)
# query genes basic info -- end


## query annotation terms/genes -- start
def obtainAnnotationTerms(speciesID, annotationType):
  '''
  return: 
    [
      {
        annotationID:,
        annotationTerm:,
      }
    ]
  '''
  #todo: store the annotations in mongo and retrieve directly
  speciesAnnotationDir = os.path.join(DATABASE_DIR, "speciesCenteredInfo", speciesID,  "annotationsForEnrichment")
  annotationFile = os.path.join(speciesAnnotationDir,  "pathID2SYMBOL" + frontAnnoName2databaseAnnoName[annotationType] + ".json")

  with open(annotationFile, 'r') as fp:
    path2symbols = json.load(fp)
  annotations = []
  for key, values in path2symbols.items():
    annotations.append({"annotationID": key, "annotationTerm": values["name"]})
  
  return annotations

def obtainAnnotationGenes(speciesID, annotationType, annotationID):
  '''
  return: 
    [Symbol1, Symbol2]
  key notes:
    Use symbol as identifier
  '''
  speciesAnnotationDir = os.path.join(DATABASE_DIR, "speciesCenteredInfo", speciesID,  "annotationsForEnrichment")
  annotationFile = os.path.join(speciesAnnotationDir,  "pathID2SYMBOL" + frontAnnoName2databaseAnnoName[annotationType] + ".json")

  with open(annotationFile, 'r') as fp:
    path2symbols = json.load(fp)
  return path2symbols[annotationID]["ids"]

## query annotation terms/genes --end


def obtainMicroarrayIDtypesOfOneSpeciesFromMongo(speciesID):
  '''
  Query arrayIDtypes for one species,
  Used in importing microarray data in the front end
  '''
  microarrayQureyInfos = arrayCollections.find(
    {"speciesID": speciesID}
  )
  arrayIDtypes = []
  for eachInfo in microarrayQureyInfos:
    arrayIDtypes.append({
      "IDtype":      eachInfo["Package"],
      "description": eachInfo["Title"],
    })
  return arrayIDtypes


def obtainMicroarrayIDtypesOfOneSpecies(speciesID):
  '''
  In this version, just obtain from the directory containing microarray annotation data;
  Use mongodb in later versions

  return:
    [
      {
        name: ,
        description: ,
      }
    ]
  '''
  #TODO: use mongodb to store species related info
  arrayAnnoPath = os.path.join(DATABASE_DIR, "speciesCenteredInfo", speciesID, "microarrayAnnotations")
  arrayAnnoNames = []
  for (dirPath, dirnames, fileNames) in walk(arrayAnnoPath):
    arrayAnnoNames = fileNames
  arrayPackageNames = [eachName.split(".")[0] for eachName in arrayAnnoNames]
  arrayIDtypes = [{"name": eachIDtype, "description": eachIDtype} for eachIDtype in arrayPackageNames]
  return arrayIDtypes


# def obtainMicroarrayProbeIDsWithOneSymbol(annoPkgName):
#   '''
#   Filter out probes that have no entrez annotation and multiple entrezs annotations

#   return:
#     a series, [probe1, probe2]
#   '''
#   annoFile  = os.path.join(DATABASE_DIR, "annotations", "biocpackages", annoPkgName + ".ftr")
#   annoFrame = pd.read_feather(annoFile)
  
#   annoFilter = annoFrame.loc[annoFrame["ENTREZID"].notnull(), ]
#   annoFilter = annoFilter.drop_duplicates(subset = ["PROBEID"], keep = False)

#   return annoFilter["PROBEID"]
  
# def obtainSymbol2MicroarrayProbeIDs(annoPkgName, geneSymbols):
#   '''
#   retrun:
#     {symbol: [entrez1, entrez2]}
#   '''
#   annoFile  = os.path.join(DATABASE_DIR, "annotations", "biocpackages", annoPkgName + ".ftr")
#   annoFrame = pd.read_feather(annoFile)
  
#   annoFilter      = annoFrame.loc[annoFrame["SYMBOL"].notnull(), ]
#   annoFilter      = annoFilter.drop_duplicates(subset = ["PROBEID"], keep = "first")
#   annoWithSymbols = annoFilter.loc[annoFilter["SYMBOL"].isin(geneSymbols),]
  
#   symbol2probeIDs = {}
#   for probeID, symbol in zip(annoWithSymbols["PROBEID"], annoWithSymbols["SYMBOL"]):
#     if symbol in symbol2probeIDs:
#       symbol2probeIDs[symbol] = symbol2probeIDs[symbol].append(probeID)
#     else:
#       symbol2probeIDs[symbol] = [str(probeID)]
  
#   return symbol2probeIDs


# obtain ID mapping between two ID types -- start
def _obtainIDmappintsBetweenProbeAndNcbiEntrezID(speciesID, annoPkgName):
  annoFile  = os.path.join(DATABASE_DIR, "speciesCenteredInfo", speciesID, "microarrayAnnotations", annoPkgName + ".db.json")
  with open(annoFile, 'r') as fp:
    probeID2anno = json.load(fp)
  
  probe2entrez = {}
  entrez2probe = {}
  ENTREZ_ORDER  = 0
  for key, values in probeID2anno["genesInfoDic"].items():
    entrez = values[ENTREZ_ORDER]
    if (entrez != "NA"):
      probe2entrez[key] = [entrez] # one probeid only maps to one entrez
      if entrez in entrez2probe:
        entrez2probe[entrez].append(key)
      else:
        entrez2probe[entrez] = [key]
  return [
    {
      "speciesID":     speciesID,
      "sourceIDtype": "NcbiEntrezGene",
      "targetIDtype":  annoPkgName,
      "sourceID2targetID": entrez2probe
    },
    {
      "speciesID":    speciesID,
      "sourceIDtype": annoPkgName,
      "targetIDtype": "NcbiEntrezGene",
      "sourceID2targetID": probe2entrez
    }
  ]

def _obtainIDmappingsInfoWithinSpeciesOtherThanMicroarrayIDs(speciesID, IDtype1, IDtype2):
  '''
  return, a list of IDmappingInfo dictionaries
  
  IDmappingInfo dictonary:
    speciesID:    string;
    sourceIDtype: string;
    targetIDtype: string;
    sourceID2targetID: dictionary;
  '''
  idMppingDir = os.path.join(DATABASE_DIR, "speciesCenteredInfo", speciesID, "idMappingBetweenTwoIDtypes")

  def formatIDmappinFilePath(rootPath, sourceIDtype, targetIDtype):
    return rootPath + "/" + sourceIDtype + "2" + targetIDtype + ".json"


  idType12idType2File = formatIDmappinFilePath(idMppingDir, IDtype1, IDtype2)
  with open(idType12idType2File, "r") as fileOpen:
    idType12idType2 = json.load(fileOpen)

  idType22idType1File = formatIDmappinFilePath(idMppingDir, IDtype2, IDtype1)
  with open(idType22idType1File, "r") as fileOpen:
    idType22idType1 = json.load(fileOpen)

  return [
    {
      "speciesID":    speciesID,
      "sourceIDtype": IDtype1,
      "targetIDtype": IDtype2,
      "sourceID2targetID": idType12idType2
    },
    {
      "speciesID":    speciesID,
      "sourceIDtype": IDtype2,
      "targetIDtype": IDtype1,
      "sourceID2targetID": idType22idType1
    }
  ]

def obtainIDmappingsInfoWithinSpecies(speciesID, IDtype1, IDtype2):
  if _checkIfIdtypeIsMicroarrayID(IDtype1) and IDtype2 == "NcbiEntrezGene":
    return _obtainIDmappintsBetweenProbeAndNcbiEntrezID(speciesID, annoPkgName = IDtype1)
  else:
    return _obtainIDmappingsInfoWithinSpeciesOtherThanMicroarrayIDs(speciesID, IDtype1, IDtype2)

# obtain ID mapping between two ID types -- end


# Check ID type -- start
# Check ID type of the IDs from the client is correct


def checkMatchedPercentageOfgenesUnderSpecificIDtype(speciesID, IDs, IDtype):
  #TODO: use mongo to store genes of one IDtype. Loading genes from directory takes too much time, 1s.
  annoGenesInfo = obtainGeneIDannoInfor(speciesID, IDtype)

  allGenesSet = set(list(annoGenesInfo["genesInfoDic"].keys()))
  inputGenesSet = set(IDs)
  intersectGenes = allGenesSet.intersection(inputGenesSet)
  return len(intersectGenes)/len(inputGenesSet)

# Check ID type -- end






  