from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from keggExplore import keggExploreUtils

class KGMLentryIDinfo(APIView):
  '''download kgml data and entris information from kegg database and
    send back to client side
  '''
  permission_classes = (AllowAny, )
  def __init__(self):
    '''set the success note and the error note'''
    pass
  def get(self, request, *args, **kwargs):
    speciesID = request.GET["speciesID"]
    pathwayID = request.GET["pathwayID"]

    kgmlString     = keggExploreUtils.obtainKeggPathwayKGMLstring(speciesID = speciesID, pathwayID = pathwayID)
    entryID2Symbol = keggExploreUtils.obtainEntryID2Symbol(speciesID = speciesID, pathwayID = pathwayID)
    
    return Response(
      {
        "KEGGkgmlEntryIDInfo": {
          "ID":             pathwayID,
          "kgmlString":     kgmlString,
          "entryID2Symbol": entryID2Symbol,
        }
      }
    )
    #  TODO: add keggNote later

class QueryKeggSpecies(APIView):
  def get(self, request, *args, **kwargs):
    # TODO: the following code are only for test, implement this later
    return Response(
      {
        "allKeggSpecies": [
          {
            "taxID": "9606",
            "name":  "Homo sapiens",
          },
          {
            "taxID": "10090",
            "name":  "Mus musculus",
          },
          {
            "taxID": "10116",
            "name":  "Rattus norvegicus"
          }
        ]
      }
    )

class QueryOneSpeciesPathways(APIView):
  def get(self, request, *args, **kwargs):
    speciesID = request.GET["speciesID"]
    pathwaysInfoList = keggExploreUtils.obtainPathwaysInOneSpecies(speciesID = speciesID)
    return Response({
      "pathways": pathwaysInfoList
    })


