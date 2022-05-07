import requests
import json
from fgvis.settings import BATCH_URL
import numpy as np

def removeBatchEffectsRNAseq(counts, batch, group):
  '''
  counts: number[][],
  batch: string[],
  group: string[],
  '''
  requestUrl = BATCH_URL + "removebatcheffectrnaseq"
  requestData = {
    "counts": counts,
    "batch": batch,
    "group": group,
  }

  requestResult = requests.post(requestUrl, json = requestData)
  adjustedData = json.loads(json.loads(requestResult.text))
  # adjustedData is a list, the server transform matrix to the list column by column
  # we transform the adjusted data in R, convert the list to numpy and then to list of lists
  nCol = len(counts[0])
  nRow = len(counts)
  adjustedMatrix = np.array(adjustedData).reshape((nRow, nCol))
  return adjustedMatrix


def removeBatchEffectsNormal(values, batch, group):
  '''
  values: number[][], 
  batch:  string[],
  group:  string[]
  '''
  requestUrl = BATCH_URL + "removebatcheffectnormalvalues"
  requestData = {
    "values": values,
    "batch":  batch,
    "group":  group,
  }

  requestResult = requests.post(requestUrl, json = requestData)
  adjustedData = json.loads(json.loads(requestResult.text))
  
  nCol = len(values[0])
  nRow = len(values)

  adjustedValues = np.array(adjustedData).reshape((nRow, nCol))

  return adjustedValues

