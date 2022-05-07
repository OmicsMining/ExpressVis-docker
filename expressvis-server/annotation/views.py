from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
import json
from annotation.annotationQuery import checkMatchedPercentageOfgenesUnderSpecificIDtype, \
  obtainGeneIDannoInfor,\
   obtainIDmappingsInfoWithinSpecies, \
   obtainMicroarrayIDtypesOfOneSpecies, \
   obtainAnnotationTerms, obtainAnnotationGenes
#from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from fgvis.settings import BASE_DIR
import pickle

# obtain terms in the pathways
class pathwayTerms(APIView):
  '''obtain the pathway terms to show in the front-end'''
  permission_classes = (AllowAny, )
  def setSettings(self):
    self.storeDic = BASE_DIR + "/annoData/pathways"
    self.organisms = ['human', 'mouse', 'worm', 'rat', 'fly', 'rice', 'arabidopsis',
                      'frog', 'yeast', 'zebrafish', 'pombe']
    self.pathwaysType = ['KEGG.biosystems', 'REACTOME.biosystems', 'WikiPathways.biosystems',
                         'biological_process','cellular_component', 'molecular_function']

    self.pathwayTerms = []
  def setOrganism(self, organism):
    '''
      @ set the organism; the organism name comes from the front-end
    '''
    self.organism = organism

  def setPathwayType(self, pathwayType):
    '''
      @ set the pathway Type; the pathway name comes from the front-end
    '''
    self.pathwayType = pathwayType

  def obtainPathwayTerms(self):
    '''
      @ return pathway Terms
    '''
    dataFile = self.storeDic + "/" + self.organism + "." + self.pathwayType + ".genes.pickle"
    dataOpen = open(dataFile, 'rb')
    data     = pickle.load(dataOpen)
    for pathId, term in data.items():
      termName = term["name"]
      pathwayTerm = {"id": pathId,
                     "term": termName}
      self.pathwayTerms.append(pathwayTerm)

  def get(self, request, *args, **kwargs):
    species     = request.GET["species"]
    pathwayType = request.GET["pathwayType"]
    self.setSettings()
    self.setOrganism(species)
    self.setPathwayType(pathwayType)
    self.obtainPathwayTerms()
    return Response({"pathwayTerms": self.pathwayTerms})

# obtain genes in a term

class pathwayGenes(APIView):
  '''obtain the genes in an annotation term to show in the front-end'''
  permission_classes = (AllowAny, )
  def setSettings(self):
    self.storeDic = BASE_DIR + "/annoData/pathways"
    self.organisms = ['human', 'mouse', 'worm', 'rat', 'fly', 'rice', 'arabidopsis',
                      'frog', 'yeast', 'zebrafish', 'pombe']
    self.pathwaysType = ['KEGG.biosystems', 'REACTOME.biosystems', 'WikiPathways.biosystems',
                         'biological_process','cellular_component', 'molecular_function']

    self.pathwayTerms = []
  def setOrganism(self, organism):
    '''
      @ set the organism; the organism name comes from the front-end
    '''
    self.organism = organism

  def setPathwayType(self, pathwayType):
    '''
      @ set the pathway Type; the pathway name comes from the front-end
    '''
    self.pathwayType = pathwayType

  def setPathwayId(self, pathwayId):
    '''
      @ set the pathway id; the pathway name comes from the front-end
    '''
    self.pathwayId = pathwayId

  def obtainGenes(self):
    '''
      @ return pathway Terms
    '''
    dataFile = self.storeDic + "/" + self.organism + "." + self.pathwayType + ".genes.pickle"
    dataOpen = open(dataFile, 'rb')
    data     = pickle.load(dataOpen)
    pathwayGenes = data[self.pathwayId]["genes"]
    self.pathwayGenes = pathwayGenes

  def get(self, request, *args, **kwargs):
    species     = request.GET["species"]
    pathwayType = request.GET["pathwayType"]
    pathwayId   = request.GET["pathwayId"]
    self.setSettings()
    self.setOrganism(species)
    self.setPathwayType(pathwayType)
    self.setPathwayId(pathwayId)
    self.obtainGenes()
    return Response({"genes": self.pathwayGenes})



class AnnotationTerms(APIView):
  '''
  Obtain annotation terms
  return: {
    speciesID: ,
    annotationType:, 
    annotationTerms: [
      {
        annotationID:,
        annotationTerm:,
      }
    ],
  }
  '''
  def get(self, request, *args, **kwargs):
    speciesID = request.GET['speciesID']
    annotationType = request.GET['annotationType']
    annotationTerms = obtainAnnotationTerms(speciesID = speciesID, annotationType = annotationType)
    return Response({
      "speciesID":       speciesID,
      "annotationType":  annotationType,
      "annotationTerms": annotationTerms,
    })

class AnnotationGenes(APIView):
  '''
  return
    {
      speciesID:,
      annotationType:,
      annotationID: ,
      genes: []
    }
  '''
  def get(self, request, *args, **kwargs):
    speciesID = request.GET['speciesID']
    annotationType = request.GET['annotationType']
    annotationID   = request.GET['annotationID']
    genes = obtainAnnotationGenes(
      speciesID = speciesID,
      annotationType = annotationType,
      annotationID   = annotationID
    )
    return Response({
      "speciesID":      speciesID,
      "annotationType": annotationType,
      "annotationID":   annotationID,
      "genes":          genes,
    })

class GenesAnnoInfo(APIView):
  '''
  Obtain genes annotation infor for displaying in the front-end (diff analysis, and clustering analysis)

  return {
    "features": string[],
    "genesInfoDic": {
      "geneID": string[]
    }
  }
  '''
  def get(self, request, *args, **kwargs):
    speciesID = request.GET['speciesID']
    IDtype    = request.GET["IDtype"]
    genesBasicInfo = obtainGeneIDannoInfor(speciesID = speciesID, IDtype = IDtype)
    return Response(genesBasicInfo)

class MappingBetwwenIDtypesWitinOneSpecies(APIView):
  '''
  Obtain gene mapping info for two types of ids within a species
  '''
  def get(self, request, *args, **kwargs):
    speciesID = request.GET["speciesID"]
    IDtype1   = request.GET["IDtype1"]
    IDtype2   = request.GET["IDtype2"]

    idMappingDictionaries = obtainIDmappingsInfoWithinSpecies(speciesID, IDtype1, IDtype2)
  
    return Response({"idMappingDictionaries": idMappingDictionaries})

class LoadArrayIDTypesInOneSpecies(APIView):
  '''
  Obtain arrayIDtypes in one species
  '''
  def get(self, request, *args, **kwargs):
    speciesID = request.GET["speciesID"]
    idTypes = obtainMicroarrayIDtypesOfOneSpecies(speciesID = speciesID)
    return Response(idTypes)

class IDmatchedPercentage(APIView):
  '''
  obtain the percentage of the genes that match the given ID type
  '''
  def post(self, request, *args, **kwargs):
    requestData  = request.data

    speciesID = requestData["speciesID"]
    IDs       = requestData["IDs"]
    IDtype    = requestData["IDtype"]
    
    matchedPercentage = checkMatchedPercentageOfgenesUnderSpecificIDtype(speciesID, IDs, IDtype)

    return Response({
      "speciesID":         speciesID,
      "IDtype":            IDtype,
      "matchedPercentage": matchedPercentage
    })
