from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

import pandas as pd

from preprocessproteomics.proteomicsNAsFilterAdapter import filterProteinsWithNAs
from preprocessproteomics.proteomicsImputeAdapter import imputeNAs
from preprocessproteomics.proteomicsImpute import impute
from preprocessproteomics.proteomicsNormalize import norm_sample


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

    groups = requestData["groups"]
    frameAfterFilter = filterProteinsWithNAs(intensityFrame, groups, preprocessSettings["filterSettings"])
    
    # knn method has no subSetting 
    frameAfterImpute = imputeNAs(frameAfterFilter, preprocessSettings["imputeSettings"])

    frameAfterNormalization = norm_sample(
      dataframe = frameAfterImpute,
      method    = preprocessSettings["normalizationMethod"],)

    valuesDic = frameAfterNormalization.to_dict(orient="list")
    proteinIDs = frameAfterNormalization.index.tolist()
    
    return Response({
      "normalizedValues": valuesDic,
      "proteinIDs": proteinIDs
    })
