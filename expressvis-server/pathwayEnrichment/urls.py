from django.conf.urls import url
from . import views
# from djangoServer.pathwayEnrichment.views.enrichment import pathwayEnrichment

urlpatterns = [
  url(r'^keggVis/', views.parseKgml.as_view(), name = "keggPathwayVisualization"),
  url(r'^pathway/', views.pathwayEnrichment.as_view(), name = "pathwayEnrichment"),
  url(r'^pathwayTerms/', views.pathwayTerms.as_view(), name = "pathwayTerms"),
  url(r'^pathwayGenes/', views.pathwayGenes.as_view(), name = "pathwayGenes"),
  url(r'^hirarchicalCluster/', views.hirarchicalCluster.as_view(), name = "pathwayEnrichment"),
  url(r'^auth/', views.obtainToken, name = "obtainToken")
]