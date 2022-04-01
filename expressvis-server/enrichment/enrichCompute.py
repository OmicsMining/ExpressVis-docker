import os
import json
from scipy.stats import hypergeom
import numpy as np 
import math
from fgvis.settings import BASE_DIR, DATABASE_DIR


frontAnnoName2databaseAnnoName = {
  # Map GO Types from the front-end to these in the database  
  # name in the database are not the same as displayed in the front-end
  "Biological Process": "Process",
  "Molecular Function": "Function",
  "Cellular Component": "Component",
  
  "KEGG Pathway":     "KEGG",
  "REACTOME Pathway": "REACTOME",
  "WikiPathways":     "WikiPathways",
}

IDtypesHasEnrichAnnotations = ["EnsemblGene", "NcbiEntrezGene", "NcbiRefseqProtein", "UniprotID", "SYMBOL"]


class AnnotationEnrich():
  '''
  功能： 通路和GO富集分析。
        通路包括KEGG pathway, REACTOME pathway, Wiki Pathway。
        GO包括biological process, cellular component, molecular function。
  输入： 初始化输入：通路或GO类型，目标蛋白，背景蛋白，物种
  输出： 富集结果.
        表中的列名称为： ID， Term，Enrichment, logP, Genes in Term, Target Genes in Term,
                      Fraction of Targets in Term, Total Target genes, Total Genes,
                      Gene Symbols
  '''
  def __init__(self, annotationType, proteinIDtype, targets, background, speciesID):
    self.annotationType = annotationType
    self.proteinIDtype  = proteinIDtype
    self.targets    = set(targets)
    self.background = set(background)
    self.speciesID = speciesID
    self._ifLoadedAnnotationData = False
    self._ifPvaluesComputed = False
  def _loadAnnotationData(self):
    '''
    读取相应的蛋白注释数据. load cache data
    注释数据格式：
       {
         key(annotationID): {
           name: pathwayname,
           ids: [gene1, gene2...]
         }...
       }
    '''
    speciesAnnotationDir = os.path.join(DATABASE_DIR, "speciesCenteredInfo", self.speciesID,  "annotationsForEnrichment")
  
    annotationFile = os.path.join(speciesAnnotationDir,  "pathID2" + self.proteinIDtype + frontAnnoName2databaseAnnoName[self.annotationType] + ".json")
    with open(annotationFile, 'r') as f:
      self.annotationGenes = json.load(f)
  
    self._ifLoadedAnnotationData = True
      # annotationFile = BASE_DIR + "/database/annotationData/" + self.species + "/" \
      #                  + self.annotationType + "_pathid2" + self.IDtype + ".json"
      # with open(annotationFile, 'r') as f:
      #   self.annotationGenes = json.load(f)

  def _computePvalues(self):
    '''
    功能：计算P值
    方法：采用超几何分布
    说明： 为提高计算速度，先计算各个条目的参数，存为列表，统一计算p值。
    :return: 富集结果，一个字典， 
      {
        "attributes": []
        "enrichedResultList": tuple[]
      }
        一个列表，列表中每一个元素是为一个元组（tuple）,
        tuple格式：(注释ID， 注释名称，富集的p值，富集的p值-log10,注释条目中基因数，
                   在该注释中的目标基因数，目标基因数，背景基因数，基于的EntrezID)
    '''
    self.backgroundNum = len(self.background)
    self.targetNum     = len(self.targets)

    pathNumList     = []
    genesBothList   = []
    pathsIdList     = []
    genesEntrezList = []

    for pathId, term in self.annotationGenes.items():
      pathGenes = set(term["ids"]).intersection(self.background) # * 注释条目中的基因, 必须在背景基因中 
      genesBoth = pathGenes.intersection(self.targets) # 注释条目中的基因与目标基因的交集
      genesBothNum = len(genesBoth) # 注释条目中的基因与目标基因的交集的数目
      pathNum = len(pathGenes) # 注释条目中基因与背景基因交集数量
      pathNumList.append(pathNum)
      genesBothList.append(genesBothNum - 1)
      pathsIdList.append(pathId)
      genesEntrez = ",".join(genesBoth)
      genesEntrezList.append(genesEntrez)
    pValueList = hypergeom.sf(np.array(genesBothList), self.backgroundNum,
                              self.targetNum, np.array(pathNumList))
    self._pValueList = pValueList
    self._pathIdList = pathsIdList
    self._pathNumList = pathNumList
    self._genesBothList = genesBothList
    self._genesEntrezList = genesEntrezList
    self._ifPvaluesComputed = True

  def summaryResultsWithPvalue(self, PvalueCutoff = 0.05):
    '''
    :param PvalueCutoff:
    :return: 
      A dictionary: {
        "annotationType": string,
        "enrichedResult": {
          "attributes":    string[],
          "enrichedInfos": enrichedInfo[]
        }
        
      }
     enriched info is a tuple, which contains
     Term, pValue, and so on
    '''
    assert PvalueCutoff > 0 and PvalueCutoff <=1, "P value should be between 0 and 1"

    if not self._ifLoadedAnnotationData:
      self._loadAnnotationData()
    if not self._ifPvaluesComputed:
      self._computePvalues()

    specificEnrichInfo = []
    for i, pValue in enumerate(self._pValueList):
      pathId = self._pathIdList[i]
      pathNum = self._pathNumList[i]
      genesBothNum = self._genesBothList[i] + 1
      if pValue <= PvalueCutoff:
        # the tuple order:
        # TermId; Term; Enrichment; logP; Genes in Term; Target genes in Term;
        # Total target genes; Total genes; EntrezIDs
        genesEntrez = self._genesEntrezList[i]
        logP = 'NA'
        if pValue > 0:
          logP = -math.log(pValue, 10)
        termName = self.annotationGenes[pathId]['name']
        enrichInfo = (pathId, termName, pValue, logP, pathNum, genesBothNum,
                      self.targetNum, self.backgroundNum, genesEntrez)
        specificEnrichInfo.append(enrichInfo)
    enrichedInfoSorted = sorted(specificEnrichInfo,
                                key=lambda info: info[2])
    return {
      "annotationType": self.annotationType,
      "enrichedResult": {
        "attributes": ["AnnotationID", "Annotation Name", "Enrichment P value", "Enrichment -log10 Pvalue", 
                     "Genes Num in Annotation", "Target Genes Num in Annotation", "Target Genes Num","Background Genes Num", "Gene IDs"],
        "enrichedInfos": enrichedInfoSorted
      }
    }
    # self.enrichedResult = enrichedInfoSorted
  # @property
  # def result(self):
  #   self._loadAnnotationData()
  #   self._computePvalues()
  #   return self.enrichedResult

class EnrichMultipleAnnotations():
  def __init__(self, annotationTypes, proteinIDtype, targets, background, species):
    self.annotationTypes = annotationTypes
    self.proteinIDtype   = proteinIDtype
    self.targets         = targets
    self.background      = background
    self.species         = species
  def enrichForAllAnnotations(self):
    '''
    return: [
      {
        "annotationType": string,
        "enrichedResult": {
          "attributes":    string[],
          "enrichedInfos": enrichedInfo[]
        }
      }，
    ]
    '''
    annotationType2enrichedResult = []

    for eachAnnotationType in self.annotationTypes:
      annotationEnrich = AnnotationEnrich(eachAnnotationType, self.proteinIDtype, self.targets, self.background, self.species)
      enrichResult     = annotationEnrich.summaryResultsWithPvalue()
      annotationType2enrichedResult.append(enrichResult)
    
    return annotationType2enrichedResult


class EnrichMultipleAnnotationsAdapter():
  '''
  If proteinIDtype is in IDtypesHasEnrichAnnotations, just call EnrichMultipleAnnotations,
  else:
    1. Convert microarray IDs to entrezID,
    2. Use entrez IDs to perform enrichment
    3. Convert entrezid to microrray ID 
  '''
  def __init__(self, annotationTypes, proteinIDtype, targets, background, species):
    self.annotationTypes = annotationTypes
    self.proteinIDtype   = proteinIDtype
    self.targets         = targets
    self.background      = background
    self.species         = species
  def perpareInfoForIDmapping(self):
    '''
    
    '''
    annoFile  = os.path.join(DATABASE_DIR, "speciesCenteredInfo", self.species, "microarrayAnnotations", self.proteinIDtype + ".db.json")
    with open(annoFile, 'r') as f:
      geneID2info = json.load(f)["genesInfoDic"]
    
    backgroundEntrezs = []
    targetsEntrezs    = []
    targetEntrez2microarray = {}
    for eachGene in self.background:
      backgroundEntrezs.append(geneID2info[eachGene][0])
    for eachGene in self.targets:
      entrezID = geneID2info[eachGene][0]
      targetsEntrezs.append(entrezID)
      if entrezID in targetEntrez2microarray:
        targetEntrez2microarray[entrezID].append(eachGene)
      else:
        targetEntrez2microarray[entrezID] = [eachGene]
    self.backgroundEntrezs = backgroundEntrezs
    self.targetsEntrezs    = targetsEntrezs
    self.targetEntrez2microarray = targetEntrez2microarray

    
  def obtainEnrichedResult(self):
    if self.proteinIDtype in IDtypesHasEnrichAnnotations:
      enrichMultipleAnnotations = EnrichMultipleAnnotations(self.annotationTypes, self.proteinIDtype, self.targets, self.background, self.species)
      return enrichMultipleAnnotations.enrichForAllAnnotations()
    else:
      # use EntrezID to perform enrichment analysis
      entrezIDorder = 8
      self.perpareInfoForIDmapping()
      enrichMultipleAnnotations = EnrichMultipleAnnotations(self.annotationTypes, "NcbiEntrezGene", self.targetsEntrezs, self.backgroundEntrezs, self.species)
      enrichedResult = enrichMultipleAnnotations.enrichForAllAnnotations()
      # convert Entrez ids to microrray IDs
      for eachTyepEnrichedAnnotation in enrichedResult:
        newEnrichedInfos = []
        for eachEnrichedInfo in eachTyepEnrichedAnnotation["enrichedResult"]["enrichedInfos"]:
          entrezString = eachEnrichedInfo[entrezIDorder]
          microarrayIDs = []
          for entrezID in entrezString.split(","):
            microarrayIDs += self.targetEntrez2microarray[entrezID]
          newEnrichedInfo = list(eachEnrichedInfo)
          newEnrichedInfo[entrezIDorder] = ",".join(microarrayIDs)
          newEnrichedInfos.append(tuple(newEnrichedInfo))
        eachTyepEnrichedAnnotation["enrichedResult"]["enrichedInfos"] = newEnrichedInfos
      return enrichedResult
      
      
    
