from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'pathway', views.PathwayEnrichment.as_view(), name='pathwayEnrichment'),
  url(r'gseaAllAnnotations/',  views.GSEAallAnnotations.as_view(),  name = "GSEA all types of annotations"),
  url(r'tfs', views.tfsEnrichment.as_view(), name='tfsEnrichment'),
]

