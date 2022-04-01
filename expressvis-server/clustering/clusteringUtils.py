import scipy
import scipy.cluster.hierarchy as sch
from scipy import stats
import fastcluster
import numpy as np




class Matrix2clusterTree():
  # cluster a matrix, obtain the dendrogram json used in the front-end
  def __init__(self, matrix, clusterMethod = "average"):
    self.matrix = matrix
    self.clusterMethod = clusterMethod
  def _computeDistance(self):
    '''
    compute the distance using correlation method
    '''
    distMat = scipy.spatial.distance.pdist(self.matrix,
                                           metric = "correlation")
    np.clip(distMat, 0, 2, out = distMat)
    self.distMat = distMat

  def _cluster(self):
    self.clusters  = fastcluster.linkage(self.distMat, method = self.clusterMethod)
    self.leafLists = sch.leaves_list(self.clusters).tolist()
    self.leafLists.reverse()
    self.leafLength = len(self.leafLists)
    self.tree = sch.to_tree(self.clusters, rd = False)
    self.maxDist = self.tree.dist
    #sch.dendrogram(self.clusters, orientation='left', no_plot = True)

  def _obtainNodeYpos(self, node):
    ''' gain the y-coordinate of node'''
    if node.right:
      rightChildYpos = self._obtainNodeYpos(node.right)
    else:
      rightChildYpos = (self.leafLists.index(node.id) + 1/2) * 1/self.leafLength
    # + 1/2
    if node.left:
      leftChildYpos = self._obtainNodeYpos(node.left)
    else:
      leftChildYpos = (self.leafLists.index(node.id) + 1/2) * 1/self.leafLength
    # + 1/2
    nodeYpos = (rightChildYpos + leftChildYpos)/2
    self.nodeYposDic[node.id] = nodeYpos
    return nodeYpos


  def _add_node(self,node, parent, direction):
    # First create the new node and append it to its parent's children
    # xPos
    _xPos = (self.maxDist - node.dist)/self.maxDist

    _yPos = self.nodeYposDic[node.id]
    _newNode = dict( node_id=node.id, children=[], xPos = _xPos, yPos = _yPos)
    parent["children"].append( _newNode )
    # Recursively add the current node's children
    if node.left:
      self._add_node(node.left, _newNode, "left" )
    if node.right:
      self._add_node(node.right, _newNode, "right")

  def gainClusterJson(self):
    #startTime = time.time()
    self._computeDistance()
    self._cluster()
    self.nodeYposDic = {}
    self._obtainNodeYpos(self.tree)
    d3Dendro = dict(children=[], name="Root1")
    self._add_node(self.tree, d3Dendro, "other")
    return d3Dendro

def meanTransform(x):
  '''
  Input: matrix
  subscribe the mean value of each row
  '''
  return (x.transpose() - x.mean(1)).transpose()


def obtainValuesArraysAcrossGroupsSamples(processedData, groups):
  '''
  Obtain arrays across groups and samples for clustering

  note: 
    the values are zscore transformed before clustering

  return: 
   {
    "samplesExprsMatrix": number[][],
    "groupsExprsMatrix":  number[][],
    "samples":            string[],
    "groupNames":         string[],
    "genes":              string[],
   }
  '''

  allSamples = []
  for eachGroup in groups:
    allSamples.extend(eachGroup["samples"])
  allSamples = list(set(allSamples))

  dataFilterBySamples = processedData.reindex(columns = allSamples)
  dataFilterBySamples = dataFilterBySamples.dropna(how = "all", axis = 1)

  samplesExprsMatrix = stats.zscore(dataFilterBySamples.values, axis = 1, ddof = 1) # z-score values
  samples            = list(dataFilterBySamples.columns)
  genesKept          = list(dataFilterBySamples.index) # some genes may not in the dataset

  # generate mean values for each groups
  groupNames     = []
  samples2groups = {}
  for eachGroup in groups:
    groupNames.append(eachGroup["name"])
    for eachSample in eachGroup["samples"]:
      samples2groups[eachSample] = eachGroup["name"]
  
  dataAcrossGroups  = dataFilterBySamples.groupby(samples2groups, axis = 1).mean()
  dataAcrossGroups  = dataAcrossGroups.reindex(columns = groupNames)
  groupsExprsMatrix = stats.zscore(dataAcrossGroups.values, axis = 1, ddof = 1)
  groupNames        = list(dataAcrossGroups.columns)

  return {
    "samplesExprsMatrix": samplesExprsMatrix,
    "groupsExprsMatrix":  groupsExprsMatrix,
    "samples":    samples,
    "groupNames": groupNames,
    "genes": genesKept,
  }