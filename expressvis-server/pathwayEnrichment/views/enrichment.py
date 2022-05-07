from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from fgvis.settings import BASE_DIR
import pickle
from scipy.stats import hypergeom
import math
# obtain terms in the pathways
class pathwayTerms(APIView):
  '''obtain the pathway terms to show in the front-end'''
  permission_classes = (AllowAny, )
  def setSettings(self):
    self.storeDic = BASE_DIR + "/static/pathways/"
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
    self.storeDic = BASE_DIR + "/static/pathways/"
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


# enrichment
class pathwayEnrichment(APIView):
  #permission_classes = (IsAuthenticated, )
  #authentication_classes = (JSONWebTokenAuthentication, )
  #authentication_classes = (JSONWebTokenAuthentication, BaseJSONWebTokenAuthentication)
  def setSettings(self):
    self.storeDic = BASE_DIR + "/static/pathways/"
    self.organisms = ['human', 'mouse', 'worm', 'rat', 'fly', 'rice', 'arabidopsis',
                        'frog', 'yeast', 'zebrafish', 'pombe']
    self.pathwaysType = ['KEGG.biosystems', 'REACTOME.biosystems', 'WikiPathways.biosystems',
                           'biological_process','cellular_component', 'molecular_function']

    self.pathwayInfo = {}
    self.enrichedInfo = {}
  def setGenesInCluster(self, geneList):
    '''
      @ set genes in cluster; the genelist comes from the front-end
    '''
    self.genesInCluster = set(geneList)
    self.clusterNum = len(geneList)
  def setGenesBackground(self, backgroundList):
    '''
      @ set background genes; the background genes comes from the front-end
    '''
    self.genesBackground = set(backgroundList)
    self.backgroundNum = len(backgroundList)
  def setOrganism(self, organism):
    '''
      @ set the organism; the organism name comes from the front-end
    '''
    self.organism = organism
  def loadPathwayData(self):
    '''
      @ load the pathway data from the dictionary
    '''
    for pathwayType in self.pathwaysType:
      dataFile = self.storeDic + "/" + self.organism + "." + pathwayType + ".genes.pickle"
      with open(dataFile, 'rb') as f:
        self.pathwayInfo[pathwayType] = pickle.load(f)

  def computePvalue(self):
    '''
      @ compute the p-values and store them in dictonary
    '''
    for pathwayType in self.pathwaysType:
        # self.enrichedInfo[pathwayType] = {}
      specificEnrichInfo = []
      for pathId, term in self.pathwayInfo[pathwayType].items():
        pathGenes = set(term["genes"]) & self.genesBackground
        genesBoth = len(pathGenes & self.genesInCluster)
        pathNum = len(pathGenes)
        pValue = hypergeom.sf(genesBoth-1, self.backgroundNum,
                                    self.clusterNum, pathNum)
        genesEntrez = ",".join(pathGenes & self.genesInCluster)
        if pValue <= 0.05:
              # the tuble order:
          # infor return to client:
          # TermId; Term; Enrichment; logP; Genes in Term; Target genes in Term;
          # Total target genes; Total genes; EntrezIDs
          logP = "na"
          if pValue > 0:
            logP = math.log(pValue, 10)
          enrichInfo = (pathId, term["name"], pValue, logP, pathNum, genesBoth,
                        self.clusterNum, self.backgroundNum, genesEntrez)
          specificEnrichInfo.append(enrichInfo)
        specificEnrichInfoSorted = sorted(specificEnrichInfo,
                                            key = lambda info: info[2])
        self.enrichedInfo[pathwayType] = specificEnrichInfoSorted
  def post(self, request, *args, **kwargs):
    requestData = request.data
    self.setSettings()
    self.setOrganism(requestData["species"])
    self.setGenesInCluster(requestData["geneSet"])
    self.setGenesBackground(requestData["backgroundSet"])
    self.loadPathwayData()
    self.computePvalue()
    return Response({"pathwayEnrich": self.enrichedInfo})




