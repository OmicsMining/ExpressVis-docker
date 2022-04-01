from dataset.filterDataset      import affyDatasetFilterForClustering
from clustering.clusteringUtils import obtainValuesArraysAcrossGroupsSamples, Matrix2clusterTree

def obtainGenesClusteringInfo():
  pass

def obtainDatasetHierarchicalClusteringInfo(source, accession, annoPkgName, groups, valueThreshold = 0.25, 
      numberThreshold = 0.5, stdThreshold = 0.8, clusterMethod = "average"):
  # obtain processed data after filtering
  processedData = affyDatasetFilterForClustering(
                        source          = source, 
                        accession       = accession, 
                        annoPkgName     = annoPkgName,
                        valueThreshold  = valueThreshold,
                        numberThreshold = numberThreshold,
                        stdThreshold    = stdThreshold )
  # obtain datamatrix across groups and samples for clustering
  genesExprs = obtainValuesArraysAcrossGroupsSamples(
                  processedData = processedData,
                  groups        = groups )
  exprsAcrossSamples = genesExprs["samplesExprsMatrix"] 
  exprsAcrossGroups  = genesExprs["groupsExprsMatrix"]
  samples    = genesExprs["samples"]
  groupNames = genesExprs["groupNames"]
  genes      = genesExprs["genes"] 
  # obtain dendrogram
  acrossSamplesLeftDendgro = Matrix2clusterTree(matrix        = exprsAcrossSamples, 
                                                clusterMethod = clusterMethod, ).gainClusterJson()
  acrossSamplesTopDendgro  = Matrix2clusterTree(matrix = exprsAcrossSamples.transpose()).gainClusterJson()

  acrossGroupsLeftDendgro = Matrix2clusterTree(matrix        = exprsAcrossGroups, 
                                               clusterMethod = clusterMethod ).gainClusterJson()
  acrossGroupsTopDendgro  = Matrix2clusterTree(matrix = exprsAcrossGroups.transpose()).gainClusterJson()

  return {
    "samples":    samples,
    "groupNames": groupNames,
    "genes":      genes,
    "valuesArrayAcrossGroups":  exprsAcrossGroups,
    "valuesArrayAcrossSamples": exprsAcrossSamples,
   
    "clusterMethod":  clusterMethod,
    "acrossSamplesLeftDendgro": acrossSamplesLeftDendgro,
    "acrossSamplesTopDendgro":  acrossSamplesTopDendgro,
    "acrossGroupsLeftDendgro":  acrossGroupsLeftDendgro,
    "acrossGroupsTopDendgro":   acrossGroupsTopDendgro
  }
  
  
  
  
