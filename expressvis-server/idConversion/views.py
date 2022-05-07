from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

#from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from fgvis.settings import BASE_DIR
import pickle

# ID conversion
class idConversion(APIView):
  '''obtain the id conversion dictionary for front-end'''
  permission_classes = (AllowAny, )
  def __init__(self):
    self.storeDic = BASE_DIR + "/annoData/idConversion"
  def setOrganism(self, organism):
    '''
      @ set the organism; the organism name comes from the front-end
    '''
    self.organism = organism

  def setId1(self, id1):
    '''
      @ set id1, id1 were the keys of the dictionary
    '''
    self.id1 = id1

  def setId2(self, id2):
    '''
      @ set id1, id1 were the keys of the dictionary
    '''
    self.id2 = id2

  def obtainConversionDic(self, requestIds):
    '''
      @ return conversion dictionary
    '''
    dataFile = self.storeDic + "/" + self.organism + "." + self.id1 + ".to." + self.id2 + ".pickle"
    dataOpen = open(dataFile, 'rb')
    data     = pickle.load(dataOpen)
    allGenesSet = set(data.keys())
    requestSet  = set(requestIds)
    intersectSet = allGenesSet.intersection(requestSet)
    conversionDic = {}
    for gene in intersectSet:
        conversionDic[gene] = data[gene]
    self.conversionDic = conversionDic
    #self.conversionDic = {k:v for (k,v) in data.items() if k in requestIds}

  def post(self, request, *args, **kwargs):
    requestData = request.data
    species = requestData["species"]
    id1     = requestData["id1"]
    id2     = requestData['id2']
    requestIds = requestData['requestIds']
    self.setOrganism(species)
    self.setId1(id1)
    self.setId2(id2)
    self.obtainConversionDic(requestIds)
    return Response({"conversionDic": self.conversionDic})

class SpeciesIDs(APIView):
  '''
  obtain genes ids of a species for checking IDs
  '''
  permission_classes = (AllowAny, )
  def __init__(self):
    self.storeDic = BASE_DIR + "/annoData/idConversion"
  def setOrganism(self, organism):
    '''
      @ set the organism; the organism name comes from the front-end
    '''
    self.organism = organism
  def obtainIDs(self):
    dataFile = self.storeDic + "/" + self.organism + "." + "idCheck.pickle"
    with open(dataFile, 'rb') as fileOpen:
      self.speciesIDs = pickle.load(fileOpen)
  def get(self, request, *args, **kwargs):
    species = request.GET["species"]
    self.setOrganism(species)
    self.obtainIDs()
    return Response(self.speciesIDs)

class LoadEntryEntrez(APIView):
  '''
  obtain entrez2keggentry; keggentry2entrez
  '''
  permission_classes = (AllowAny, )
  def __init__(self):
    self.storeDic = BASE_DIR + "/annoData/idConversion"
  def setOrganism(self, organism):
    '''
      @ set the organism; the organism name comes from the front-end
    '''
    self.organism = organism
  def obtainEntryEntrzDic(self):
    toEntryFile = self.storeDic + "/" + self.organism + "." + "GeneID.to.KeggEntry.pickle"
    with open(toEntryFile, 'rb') as fileOpen:
      self.entrez2entry = pickle.load(fileOpen)
    toEntrezFile = self.storeDic + "/" + self.organism + "." + "KeggEntry.to.GeneID.pickle"
    with open(toEntrezFile, 'rb') as fileOpen:
      self.entry2entrez = pickle.load(fileOpen)
  def get(self, request, *args, **kwargs):
    species = request.GET["species"]
    self.setOrganism(species)
    self.obtainEntryEntrzDic()
    return Response({'entry2entrez': self.entry2entrez,
                     'entrez2entry': self.entrez2entry})