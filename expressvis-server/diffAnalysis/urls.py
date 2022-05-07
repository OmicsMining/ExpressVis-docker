from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'rnaseqdiffusecounts/',     views.RnaseqDiffUseCounts.as_view(),                 name = 'RNA-seq diffrential analysis, counts from the front-end'),
  url(r'remoteOneGroupPair/',      views.RemoteOneGroupPairDiffView.as_view(),          name = 'Differentail analysis for one diff group pair of the dataset in the server'),
  url(r'localOneGroupPair/',       views.LocalDataOneGroupPairDiffView.as_view(),       name = 'local dataset, one grouppair'),
  url(r'localArrayOneGroupPair/',  views.LocalAffyDataOneGroupPairDiffView.as_view(),   name = "local Microarray dataset, one groupPair"),
  url(r'localMultipleGroupPairs/', views.LocalDataMultipleGroupPairsDiffView.as_view(), name = 'local dataset, multiple grouppair'),
  # url(r'uploadFile/', views.uploadFile.as_view(), name='uploadFile'),
]
