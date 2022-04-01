from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

from enrichment.enrichCompute import EnrichMultipleAnnotationsAdapter
from enrichment.settings import species2supportedEnrichAnnotations
#from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from fgvis.settings import BASE_DIR
import pickle
from scipy.stats import hypergeom
import numpy as np
import math
import time
# Create your views here.

# enrichment

class PathwayEnrichment(APIView):
  '''
    return: 
      [ 
        {
          annotationType: string,
          enrichedResult: {
            "attributes":    string[],
            "enrichedInfos": enrichedTuple[],
        }
      ]
  '''
  
  def post(self, request, *args, **kwargs):
    requestData = request.data
    speciesID       = requestData["speciesID"]
    geneIDtype      = requestData["geneIDtype"]
    backgroundGenes = requestData["backgroundGenes"]
    genes           = requestData["genes"]

    annotationTypes = species2supportedEnrichAnnotations[speciesID]

    enrichMultipleAnnotations = EnrichMultipleAnnotationsAdapter(
      annotationTypes = annotationTypes,
      proteinIDtype   = geneIDtype,
      targets         = genes,
      background      = backgroundGenes,
      species         = speciesID,
    )
    enrichedResults = enrichMultipleAnnotations.obtainEnrichedResult()

    return Response(enrichedResults)

# enrichment
class tfsEnrichment(APIView):
  def setSettings(self):
    self.storeDic = BASE_DIR + "/annoData/tfTargets/"
    self.organisms = ['human', 'mouse', 'worm', 'rat', 'fly', 'rice', 'arabidopsis',
                          'frog', 'yeast', 'zebrafish', 'pombe']
    self.tfsType = ['cellNet']
    self.tfInfo = {}
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
  def loadTfsData(self):
    '''
      @ load the pathway data from the dictionary
    '''
    for tfType in self.tfsType:
      dataFile = self.storeDic + "/" + self.organism + "." + tfType + ".tf.targets.pickle"
      with open(dataFile, 'rb') as f:
        self.tfInfo[tfType] = pickle.load(f)

  def computePvalue(self):
    '''
      @ compute the p-values and store them in dictonary
    '''
    for tfType in self.tfsType:
      # self.enrichedInfo[tfType] = {}
      specificEnrichInfo = []
      for pathId, term in self.tfInfo[tfType].items():
        pathGenes = set(term["targets"]) & self.genesBackground
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
          logP = math.log(pValue, 10)
          enrichInfo = (pathId, term["name"], pValue, logP, pathNum, genesBoth,
                      self.clusterNum, self.backgroundNum, genesEntrez)
          specificEnrichInfo.append(enrichInfo)
        specificEnrichInfoSorted = sorted(specificEnrichInfo,
                                          key = lambda info: info[2])
        self.enrichedInfo[tfType] = specificEnrichInfoSorted
  def post(self, request, *args, **kwargs):
    requestData = request.data
    self.setSettings()
    self.setOrganism(requestData["species"])
    self.setGenesInCluster(requestData["geneSet"])
    self.setGenesBackground(requestData["backgroundSet"])
    self.loadTfsData()
    self.computePvalue()
    return Response({"tfsEnrich": self.enrichedInfo})


