import requests
import json
from fgvis.settings import GSEA_URL

annotationTypes = ["KEGG", "REACTOME", "Process", "Function", "Component",]

def corGSEAenrichedAnnotations(speciesID, valuesForRank, genes, geneIDtype):
  '''
  return a dictionary
  keys are: pathway, pval, padj,log2err, ES, NES size,leadingEdge,GenesInAnnotation
  '''
  requestUrl = GSEA_URL + "corenrichedannotations"
  requestData = {
    "speciesID":  speciesID,
    "valuesForRank": valuesForRank,
    "genes":      genes,
    "geneIDtype": geneIDtype,
    "annotationTypes": annotationTypes
  }

  requestResult = requests.post(requestUrl, json = requestData)
  
  enrichedAnnotations = json.loads(json.loads(requestResult.text)[0])

  return enrichedAnnotations
