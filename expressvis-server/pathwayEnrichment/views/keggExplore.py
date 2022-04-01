from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import urllib.request

class parseKgml(APIView):
  '''download kgml data and entris information from kegg database and
    send back to client side
  '''
  permission_classes = (AllowAny, )
  def __init__(self):
    '''set the success note and the error note'''
    self.kegg_success_note = "success"
    self.error_note        = ""
    self.genesIdSymbol     = []
  def set_kegg_id(self, request):
    '''obtain the kegg id from client side'''
    kegg_id = request.GET["keggId"]
    self.kegg_id = kegg_id
  def processEntriesKegg(self, request, *args, **kwargs):
    kegg_entry_url    = "http://rest.kegg.jp/get/" + self.kegg_id
    try:
      kegg_entry_open   = urllib.request.urlopen(kegg_entry_url)
      kegg_entries      = kegg_entry_open.read().decode().split("\n")
      gene_start = 0
      gene_end = 0
      for i, entry in enumerate(kegg_entries):
        entry_split = entry.split(  )
        if (len(entry_split) >0):
          if (entry_split[0] == "GENE"):
            gene_start = i
      for i, entry in enumerate(kegg_entries):
        if (i > gene_start):
          entry_split = entry.split("   ")
          if (entry_split[0]):
            gene_end = i
            break
      # obtain the genes' entrez id and symbol
      genes_id_symbol = {}
      # the first
      geneStart = kegg_entries[gene_start].strip().split("     ")
      gene_id = geneStart[1].strip().split("  ")[0]
      gene_symbol = geneStart[1].strip().split("  ")[1].split(";")[0]
      genes_id_symbol[gene_id] = gene_symbol
      for gene in kegg_entries[(gene_start + 1):gene_end]:
        gene_split  = gene.strip().split("  ")
        gene_id     = gene_split[0]
        gene_symbol = gene_split[1].split(";")[0]
        genes_id_symbol[gene_id] = gene_symbol
      self.genesIdSymbol = genes_id_symbol
      kegg_entry_open.close()
    except urllib.error.HTTPError as e:
      error_note = "The kegg server couldn\'t fulfill the request. \n" \
                         "Error code: " + str(e.code)
      self.error_note = error_note
    except urllib.error.URLError as e:
      error_note = "We failed to reach a server. \n" \
                         "Reason: " + str(e.reason)
      self.error_note = error_note

  def processEntriesTogows(self, request, *args, **kwargs):
    ''''obtain the entries information'''

    requestUrl = "http://togows.org/entry/kegg-pathway/" + self.kegg_id + "/genes"
    try:
      requestOpen    = urllib.request.urlopen(requestUrl)
      requestEntries = requestOpen.read().decode().strip("\n").split("\t")
      genesIdSymbol = {}
      for entry in requestEntries:
        geneSymbol = entry.split(";")[0].split("  ")
        genesIdSymbol[geneSymbol[0]] = geneSymbol[1]
      self.genesIdSymbol = genesIdSymbol
      requestOpen.close()
    except urllib.error.HTTPError as e:
      error_note = "The kegg server couldn\'t fulfill the request. \n" \
                         "Error code: " + str(e.code)
      self.error_note = error_note
    except urllib.error.URLError as e:
      error_note = "We failed to reach a server. \n" \
                        "Reason: " + str(e.reason)
      self.error_note = error_note

  def process_kgml(self, request, *args, **kwargs):
    '''otain the kgml file of the pathway'''
    kegg_url         = "http://rest.kegg.jp/get/" + self.kegg_id + "/kgml"
    try:
      kgml_open        = urllib.request.urlopen(kegg_url)
      kgml_string      = kgml_open.read()
      self.kgml_string = kgml_string
      kgml_open.close()
    except urllib.error.HTTPError as e:
      error_note = "The kegg server couldn\'t fulfill the request. \n" \
                         "Error code: " + str(e.code)
      self.error_note += error_note
    except urllib.error.URLError as e:
      error_note = "We failed to reach a server. \n" \
                         "Reason: " + str(e.reason)
      self.error_note += error_note

  def get(self, request, *args, **kwargs):
    self.set_kegg_id(request)
    self.processEntriesKegg(request)
    self.process_kgml(request)
    if self.genesIdSymbol:
      print(self.genesIdSymbol)
    if (self.error_note):
      return Response({"kegg_note": self.error_note})
    else:
      return Response(
        {"kgmlString":     self.kgml_string,
         "genesIdSymbol": self.genesIdSymbol,
         "keggNote":       self.kegg_success_note})

