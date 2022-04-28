from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

import pandas as pd

from preprocessData.proteomicsNAsFilterAdapter import filterProteinsWithNAs
from preprocessData.proteomicsImputeAdapter import imputeNAs
from preprocessData.proteomicsImpute import impute
from preprocessData.proteomicsNormalize import norm_sample
from preprocessData.removeBatchEffects import removeBatchEffectsRNAseq, removeBatchEffectsNormal
from preprocessData.removeBatchEffectsAdapter import removeProteomicsBatchEffects


# Create your views here.
class PreProcessProteomicsView(APIView):
  permissions_classes = (AllowAny,)
  def post(self, request, *args, **kwargs):
    '''
    Request Data:
     
     {
       samples2intensities: {
         sampleName: number[] 
       },
       groups: [
         {
           name: string,
           samples: string[],
         }
       ],
       imputeSettings: {
         method: ,
         settings {},
       },
       normalizationSettings: {
         method: ,
         settings: {},
       }
     } 
    
    '''
    # TODO: impute settings and normalization settings
    # TODO: add other impute and normalization methods
    requestData = request.data
    intensityValues    = requestData['samples2intensities']
    proteinIDs         = requestData['proteinIDs']
    preprocessSettings = requestData["preprocessSettings"]
    intensityFrame = pd.DataFrame(intensityValues)
    intensityFrame["proteinIDs"] = proteinIDs
    intensityFrame = intensityFrame.set_index("proteinIDs")
    # removeBatchSettings = requestData["removeBatchSettings"]

    groups = requestData["groups"]
    frameAfterFilter = filterProteinsWithNAs(intensityFrame, groups, preprocessSettings["filterSettings"])
    
    # knn method has no subSetting 
    frameAfterImpute = imputeNAs(frameAfterFilter, preprocessSettings["imputeSettings"])

    frameAfterNormalization = norm_sample(
      dataframe = frameAfterImpute,
      method    = preprocessSettings["normalizationMethod"],
    )

    # remove batch
    # if removeBatchSettings["ifRemoveBatch"]:
    #   samples2group = {}
    #   if removeBatchSettings["ifUseGroupVariable"]:
    #     for group in groups:
    #       for sample in group["samples"]:
    #         samples2group[sample] = group["name"]
    #   else:
    #     samples2group = None

    #   adjustedFrame = removeProteomicsBatchEffects(
    #     frameAfterNormalization, 
    #     samples2batch = removeBatchSettings["samples2batch"],
    #     samples2group = samples2group)
    #   valuesDic  = adjustedFrame.to_dict(orient="list")
    #   proteinIDs = adjustedFrame.index.tolist()
    # else:
    valuesDic = frameAfterNormalization.to_dict(orient="list")
    proteinIDs = frameAfterNormalization.index.tolist()
    
    return Response({
      "normalizedValues": valuesDic,
      "proteinIDs": proteinIDs
    })


class RemoveBatchView(APIView):
  permissions_classes = (AllowAny,)
  def post(self, request, *args, **kwargs):
    '''
    values: number[],
    batch:  string[],
    group:  string[]
    '''
    requestData = request.data
    valueType   = requestData["valueType"]
    if valueType == "counts":
      adjustedData = removeBatchEffectsRNAseq(
        counts = requestData["values"],
        batch  = requestData["batch"],
        group  = requestData["group"]
      )
    else: 
      adjustedData = removeBatchEffectsNormal(
        values = requestData["values"],
        batch  = requestData["batch"],
        group  = requestData["group"]
      )
    return Response({
      "adjustedData": adjustedData,
    })