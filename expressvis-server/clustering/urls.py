from django.conf.urls import url
from . import views 
urlpatterns = [
  url(r'localDatasetHierarchicalCluster/', views.LocalDatasetHierarchicalCluster.as_view(), name = 'hirarchicalCluster'),
  url(r'remoateDatasetHierarchicalClusterWithGenes', views.RemoteDatasetHierarchicalClusterWithGenes.as_view()),
  url(r'remoateDatasetHierarchicalClusterWithThresholds', views.RemoteDatasetHierarchicalClusterWithThresholds.as_view()),
  url(r'kmeansCluster/', views.kmeansCluster.as_view(), name = 'kmeansClustering'),
]
