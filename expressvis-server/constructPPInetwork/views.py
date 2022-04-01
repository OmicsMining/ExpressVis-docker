from rest_framework.views import APIView
from rest_framework.response import Response
import urllib.request

from constructPPInetwork.ppisQuery import queryPPIs

from fgvis.settings import BASE_DIR, DATABASE_DIR


class NetworkConstruction(APIView):
  def __init__(self):
    pass
  def post(self, request, *args, **kwargs):
    requestData = request.data
    subPPIs = queryPPIs(
      speciesID      = requestData["speciesID"],
      database       = requestData["database"],
      IDtype         = requestData["IDtype"],
      proteinIDs     = requestData["proteinIDs"],
      subNetworkType = requestData["subNetworkType"],
    )
    return Response({"PPIs": subPPIs})
  


# construct network
class constructNetworkUsingPSIC(APIView):
  '''download data using PSICQUIC and reponse the data to the database
      steps:
      1. convert entrezid to uniprotAcs
      2. access the interaction data
      3. parese the interaction data and convert to interaction data with entrezids as targets or sources
  '''
  def __init__(self):
    self.storeDic = BASE_DIR + "/annoData/idConversion"
    self.psicquic_success_note = "success"
    self.errorNote = ""
    self.databaseUlrsDic = {'mentha': "http://mentha.uniroma2.it:9090/psicquic/webservices/current/search/query/"}
    self.interactionUniprot = []
    self.interactionEntrez  = []
  def setSettings(self, requestData):
    self.species  = requestData['species']
    self.database = requestData['database']
    self.databaseUrl = self.databaseUlrsDic[requestData['database']]
    self.ids = requestData['ids']
    self.interactionType = requestData['interactionType']

  def entrezToUniprotAc(self):
    dataFile = self.storeDic + "/" + self.species + "_ncbiEntrez.to.uniprotAc" + ".pickle"
    with open(dataFile, 'rb') as f:
      self.entrezToUniprot = pickle.load(f)
    allNcbiIds = self.entrezToUniprot.keys()
    idsUniprot = []
    uniprotToEntrezDic = {}
    for eachId in self.ids:
      if eachId in allNcbiIds:
        # the uniprot ids of this gene
        uniprotIds = self.entrezToUniprot[eachId]
        for eachUniprot in uniprotIds:
          uniprotToEntrezDic[eachUniprot] = eachId
          idsUniprot.append(eachUniprot)
    self.requestUniprotToEntrez = uniprotToEntrezDic
    self.allUniprotIds = set(idsUniprot)
  def parseInteraction(self):
    if (self.interactionType == "participate"):
      requestUrl  = self.databaseUrl + "id:(%20" + "%20OR%20".join(self.allUniprotIds) + "%20)" + "%20AND%20species:" + self.species
    else:
      requestUrl  = self.databaseUrl + "idA:(%20" + "%20OR%20".join(self.allUniprotIds) + "%20)" + "%20AND%20idB:(%20" + "%20OR%20".join(self.allUniprotIds) + "%20)" + "%20AND%20species:" + self.species
    interactionUniprot = []
    try:
      interactionOpen = urllib.request.urlopen(requestUrl)
      interactions =interactionOpen.read().decode().strip().split("\n")
      interactionOpen.close()
      for eachInteraction in interactions:
        intSplit = eachInteraction.split("\t")
        sourceId = intSplit[0].split(":")[1]
        targetId = intSplit[1].split(":")[1]
        if [sourceId, targetId] not in interactionUniprot:
          interactionUniprot.append([sourceId, targetId])
    except urllib.error.HTTPError as e:
      errorNote = "The kegg server couldn\'t fulfill the request. \n" \
                     "Error code: " + str(e.code)
      self.error_note = errorNote
    except urllib.error.URLError as e:
      errorNote = "We failed to reach a server. \n" \
                     "Reason: " + str(e.reason)
      self.errorNote = errorNote
    self.interactionUniprot = interactionUniprot

  def interactionUniprotToEntrez(self):
    interactionEntrez = []
    # read uniprot to entrez data
    dataFile = self.storeDic + "/" + self.species + "_uniprotAc.to.ncbiEntrez" + ".pickle"
    with open(dataFile, 'rb') as f:
      self.uniprotToentrez = pickle.load(f)
    # all uniprotIds
    dataUniprotIds = self.uniprotToentrez.keys()
    requestUniprotIds = self.requestUniprotToEntrez.keys()

    for eachPPI in self.interactionUniprot:
      # first, transform the uniprot to entrez using the requestUniprot
      # then transform using all the unprot ids in the species
      source = eachPPI[0]
      target = eachPPI[1]
      sourceEntrezs = []
      targetEntrezs = []
      if (source in requestUniprotIds ):
        sourceEntrezs.append(self.requestUniprotToEntrez[source])
      else:
        if (source in dataUniprotIds):
          sourceEntrezs = sourceEntrezs + self.uniprotToentrez[source]

      if (target in requestUniprotIds ):
        targetEntrezs.append(self.requestUniprotToEntrez[target])
      else:
        if (target in dataUniprotIds):
          targetEntrezs = targetEntrezs + self.uniprotToentrez[target]
      for eachSource in sourceEntrezs:
        for eachTarget in targetEntrezs:
          if [eachSource, eachTarget] not in interactionEntrez:
            interactionEntrez.append([eachSource, eachTarget])
      self.interactionEntrez = interactionEntrez

  def post(self, request, *args, **kwargs):
    requestData = request.data
    self.setSettings(requestData)
    self.entrezToUniprotAc()
    self.parseInteraction()
    self.interactionUniprotToEntrez()
    return Response({"PPIs": self.interactionEntrez})


































