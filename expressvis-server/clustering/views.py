from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
#from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import sys
import scipy
import scipy.cluster.hierarchy as sch
import scipy.spatial
import numpy as np
import fastcluster
import json
from sklearn.cluster import KMeans
import time

sys.setrecursionlimit(10000)

class hirarchicalCluster(APIView):
  # permission_classes = (IsAuthenticated, )
  # authentication_classes = (JSONWebTokenAuthentication, )
  # authentication_classes = (JSONWebTokenAuthentication, BaseJSONWebTokenAuthentication)
  def setMatrix(self, expArray):
    self.matrix = np.array(expArray)
    #self.matrix = pd.DataFrame(expArray).transpose();
  def setClusterMethod(self, method):
    self.clusterMethod = method
  def computeDistance(self):
    '''
    compute the distance using correlation method
    '''
    distMat = scipy.spatial.distance.pdist(self.matrix,
                                           metric = "correlation")
    # distMat = self.matrix.corr();
    np.clip(distMat, 0, 2, out = distMat)
    self.distMat = distMat

  def cluster(self):
    self.clusters  = fastcluster.linkage(self.distMat, method = self.clusterMethod)
    self.leafLists = sch.leaves_list(self.clusters).tolist()
    self.leafLists.reverse()
    self.leafLength = len(self.leafLists)
    self.tree = sch.to_tree(self.clusters, rd = False)
    self.maxDist = self.tree.dist
    sch.dendrogram(self.clusters, orientation='left', no_plot = True)

  def obtainNodeYpos(self, node):
    ''' gain the y-coordinate of node'''
    if node.right:
      rightChildYpos = self.obtainNodeYpos(node.right)
    else:
      rightChildYpos = (self.leafLists.index(node.id) + 1/2) * 1/self.leafLength
    # + 1/2
    if node.left:
      leftChildYpos = self.obtainNodeYpos(node.left)
    else:
      leftChildYpos = (self.leafLists.index(node.id) + 1/2) * 1/self.leafLength
    # + 1/2
    nodeYpos = (rightChildYpos + leftChildYpos)/2
    self.nodeYposDic[node.id] = nodeYpos
    return nodeYpos


  def add_node(self,node, parent, direction):
    # First create the new node and append it to its parent's children
    # xPos
    _xPos = (self.maxDist - node.dist)/self.maxDist

    _yPos = self.nodeYposDic[node.id]
    _newNode = dict( node_id=node.id, children=[], xPos = _xPos, yPos = _yPos)
    parent["children"].append( _newNode )
    # Recursively add the current node's children
    if node.left:
      self.add_node(node.left, _newNode, "left" )
    if node.right:
      self.add_node(node.right, _newNode, "right")

  def gainClusterJson(self):
    #startTime = time.time()
    self.computeDistance()
    self.cluster()
    self.nodeYposDic = {}
    self.obtainNodeYpos(self.tree)
    d3Dendro = dict(children=[], name="Root1")
    self.add_node(self.tree, d3Dendro, "other")
    # self.treeJson = json.dumps(d3Dendro)
    self.treeJson = d3Dendro
  def post(self, request, *args, **kwargs):
    requestData = request.data
    expArray = requestData["expArray"]
    clusterMethod = requestData["clusterMethod"]
    self.setMatrix(expArray)
    self.setClusterMethod(clusterMethod)
    self.gainClusterJson()
    return Response({"dendgrogram": self.treeJson})

class kmeansCluster(APIView):
  def __init__(self):
    pass
  def setMatrix(self, expArray):
    '''
    :param expArray:
      the data should be first log2 transformed and then z-score transformed
    :return:
    '''
    self.matrix = np.array(expArray)
  def setClusterNumber(self, n):
    self.clusterNumber = n
  def cluster(self):
    '''
    :return:
    '''
    kmeans = KMeans(n_clusters = self.clusterNumber, random_state=0).fit_predict(self.matrix)
    # kmeans is a list of number, which indicate the cluster this gene belongs to
    self.kmeansList = kmeans
  def post(self, request, *args, **kwargs):
    requestData = request.data
    clusterNumber = int(requestData["clusterNumber"])
    expArray = requestData["expArray"]
    self.setMatrix(expArray)
    self.setClusterNumber(clusterNumber)
    self.cluster()
    return Response({'clusterNumber': clusterNumber, "kmeansList": self.kmeansList})



class LocalDatasetHierarchicalCluster(APIView):
  def __init__(self):
    pass

class RemoteDatasetHierarchicalClusterWithGenes(APIView):
  def __init__(self):
    '''
    Parameters from the front-end:
      genes, 
    '''
    pass

class RemoteDatasetHierarchicalClusterWithThresholds(APIView):
  def __init__(self):
    '''
    RemoteDatasetGenesHierarchicalCluster receives genes from the front-end,
    while RemoteDatasetThresholdsHierarchicalCluster recieves thresholds that are 
    used to filter genes for clustering
    '''
    pass 