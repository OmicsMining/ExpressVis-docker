from django.test import TestCase

from annotation.annotationQuery import obtainAnnotationGenes, obtainAnnotationTerms, obtainGeneIDannoInfor, obtainIDmappingsInfoWithinSpecies, \
  obtainSymbol2MicroarrayProbeIDs, \
  obtainMicroarrayIDtypesOfOneSpecies, \
  checkMatchedPercentageOfgenesUnderSpecificIDtype

class TestQueryGenesBasicInfoFunctions(TestCase):
  def testObtainMicroarrayProbeIDanno(self):
    speciesID = "9606"
    annoPkgName = "hugene20sttranscriptcluster"

    probesInfo  = obtainGeneIDannoInfor(speciesID = speciesID, IDtype = annoPkgName)
    self.assertEqual(probesInfo["genesInfoDic"]["17126256"][1], "SNHG3")

  def testObtainEnsembleGeneIDannoInfoForDisplay(self):
    speciesID = "9606"
    ensemblInfo = obtainGeneIDannoInfor(speciesID = speciesID, IDtype = "EnsemblGene")
    self.assertEqual(ensemblInfo["genesInfoDic"]["ENSG00000142694"][0], "EVA1B")
  
  def testObtainNcbiEntrezGeneIDannoInfoForDisplay(self):
    speciesID  = "9606"
    entrezInfo = obtainGeneIDannoInfor(speciesID = speciesID, IDtype = "NcbiEntrezGene")
    self.assertEqual(entrezInfo["genesInfoDic"]["1"][0], "A1BG")
  
  def testObtainUniprotIDannoInfoForDisplay(self):
    speciesID   = "9606"
    uniprotInfo = obtainGeneIDannoInfor(speciesID = speciesID, IDtype = "UniprotID")
    self.assertEqual(uniprotInfo["genesInfoDic"]["Q5T985"][1], "ITIH2")

  def testObtainNcbiRefseqIDannoInfoForDisplay(self):
    speciesID = "9606"
    refseqInfo  = obtainGeneIDannoInfor(speciesID = speciesID, IDtype = "NcbiRefseqProtein")
    self.assertEqual(refseqInfo["genesInfoDic"]["NP_001356145"][0], "SMIM41")
class TestQueryIDmappingsBetweenTwoIdtypes(TestCase):
  def testObtainIDmappingsBetweenNcbiEntrezGeneAndEnsesmblGene(self):
    speciesID = "10090"
    idType1   = "NcbiEntrezGene"
    idType2   = "EnsemblGene"
    idMappintsDirectionaries = obtainIDmappingsInfoWithinSpecies(speciesID = speciesID, IDtype1 = idType1, IDtype2 = idType2)
    self.assertEqual(len(idMappintsDirectionaries), 2)
    self.assertEqual(idMappintsDirectionaries[0]["sourceIDtype"], idType1)
    self.assertEqual(idMappintsDirectionaries[0]["targetIDtype"], idType2)
    self.assertEqual(idMappintsDirectionaries[1]["sourceIDtype"], idType2)
    self.assertEqual(idMappintsDirectionaries[1]["targetIDtype"], idType1)

    self.assertEqual(idMappintsDirectionaries[0]["sourceID2targetID"]["115490466"], ["ENSMUSG00000064724"])
    self.assertEqual(idMappintsDirectionaries[1]["sourceID2targetID"]["ENSMUSG00000064724"], ["115490466"])

  def testObtainIDmappingsBetweenMicroarrayIDandNcbiEntrezGene(self):
    speciesID   = "9606"
    annoPkgName = "hugene20sttranscriptcluster"
    idMappintsDirectionaries = obtainIDmappingsInfoWithinSpecies(speciesID = speciesID, IDtype1 = annoPkgName, IDtype2 = "NcbiEntrezGene")
    self.assertEqual(idMappintsDirectionaries[0]["sourceID2targetID"]["338382"],   ['17126286', '17126288'])
    self.assertEqual(idMappintsDirectionaries[1]["sourceID2targetID"]["17126288"], ["338382"])
    # print(idMappintsDirectionaries["probe2entrez"])



  # def obtainMicroarrayIDTypesOfAspecies(self):
  #   speciesID = "9606"
  #   arrayIDtypes = obtainMicroarrayIDtypesOfOneSpecies(speciesID)
  #   print(arrayIDtypes)

  # def testObtainSymbol2MicroarrayProbeIDs(self):
  #   annoPkgName = "hugene20sttranscriptcluster.db"
  #   symbols     = ["IL6", "STAT3"]
    
  #   symbols2probeIDs = obtainSymbol2MicroarrayProbeIDs(annoPkgName = annoPkgName, geneSymbols = symbols)
  #   self.assertEqual(symbols2probeIDs, {'STAT3': ['16845126'], 'IL6': ['17044177']})
  

class TestObtainMicroarrayIDtypesOfOneSpecies(TestCase):
  def testObtainMicroarrayIDtypesOfHuman(self):
    speciesID = "9606"
    arrayIDtypes = obtainMicroarrayIDtypesOfOneSpecies(speciesID = speciesID)
    self.assertEqual(len(arrayIDtypes),69)
  
class TestObtainAnnotationTermsGenes(TestCase):
  def testObtainAnnotationTerms(self):
    speciesID = "10090"
    annotationType = "KEGG Pathway"
    annotations = obtainAnnotationTerms(speciesID = speciesID, annotationType = annotationType)
    self.assertEqual(len(annotations), 332)
  def testObtainAnnotationGenes(self):
    speciesID = "10090"
    annotationType = "KEGG Pathway"
    annotationID   = "mmu00604"
    annotationGenes = obtainAnnotationGenes(
      speciesID      = speciesID, 
      annotationType = annotationType,
      annotationID   = annotationID)
    self.assertEqual(len(annotationGenes), 15)
    self.assertEqual(annotationGenes[0], "St8sia1")
    
class TestIDtypeCheck(TestCase):
  def testHumanUniprotIDright(self):
    speciesID = "9606"
    IDtypeToBeChecked = "UniprotID"
    IDs = ["P04637", "Q96S44"]
    matchedPercentage = checkMatchedPercentageOfgenesUnderSpecificIDtype(speciesID, IDs, IDtypeToBeChecked)
    self.assertEqual(matchedPercentage, 1);
  def testHumanUniprotIDwrong(self):
    speciesID = "10090"
    IDtypeToBeChecked = "UniprotID"
    IDs = ["P04637", "Q96S44"]
    matchedPercentage = checkMatchedPercentageOfgenesUnderSpecificIDtype(speciesID, IDs, IDtypeToBeChecked)
    self.assertEqual(matchedPercentage, 0);
  def testHumanUniprotIDhalfRight(self):
    speciesID = "9606"
    IDtypeToBeChecked = "UniprotID"
    IDs = ["P04637", "96S44"]
    matchedPercentage = checkMatchedPercentageOfgenesUnderSpecificIDtype(speciesID, IDs, IDtypeToBeChecked)
    self.assertEqual(matchedPercentage, 0.5);
  def testHuamnMicroarrayIDright(self):
    speciesID = "9606"
    annoPkgName = "hugene20sttranscriptcluster"
    IDs = ["17126256"]
    matchedPercentage = checkMatchedPercentageOfgenesUnderSpecificIDtype(speciesID, IDs, annoPkgName)
    self.assertEqual(matchedPercentage, 1)

# testFunctions = TestAnnotationQueryFunctions()
# testFunctions.testObtainEnsembleIDannoInfoForDisplay()


