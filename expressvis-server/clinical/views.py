from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from clinical.obtainSurvivalSplitAndForest import obtainSurvivalSplitAndForest
from clinical.surivial_KMCurve import generateKMinfoForPlot
# Create your views here.
class LocalDataSurvivalAndForestView(APIView):
  permissions_classes = (AllowAny,)
  def post(self, request, *args, **kwargs):
    '''
      clinicalDic
      expressionDic
      patientIDs
      endpointTimeCol
      endpointStatusCol
    '''
    requestData = request.data
    splitAndForest = obtainSurvivalSplitAndForest(
      clinicalDic         = requestData["clinicalDic"],
      expressionDic       = requestData["expressionDic"],
      patientIDs          = requestData["patientIDs"],
      endpointTimeCol     = requestData["endpointTimeCol"],
      endpointStatusCol   = requestData["endpointStatusCol"],
      highLowSplitSetting = requestData["highLowSplitSetting"],
    )

    return Response(splitAndForest)

class KMinfoForPlot(APIView):
  permissions_classes = (AllowAny,)
  def post(self, request, *args, **kwargs):
    '''
      eventTimes,
      eventStatus,
      highOrLows
    '''
    requestData = request.data
    survivalInfo = generateKMinfoForPlot(
      eventTimes  = requestData["eventTimes"],
      eventStatus = requestData["eventStatus"],
      highOrLows  = requestData["highOrLows"],
    )
    return Response(survivalInfo)
