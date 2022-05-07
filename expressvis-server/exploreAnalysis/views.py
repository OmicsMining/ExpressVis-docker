
# Create your views here.
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from exploreAnalysis.pca import samplesPCAnalysis
import numpy as np

class PCA(APIView):
  permissions_classes = (AllowAny,)
  def post(self, request, *args, **kwargs):
    '''
    Notes:
      the rows of the values should be transformed first
    '''
    requestData = request.data
    valuesMatrix = requestData["values"]
    # the rows of the values should be transformed first
    transformedValues = np.array(valuesMatrix).transpose()
    
    pcaResult = samplesPCAnalysis(
      exprsMatrix = transformedValues,
      samples = requestData["samples"],
    )

    return Response({"pcaResult": pcaResult})