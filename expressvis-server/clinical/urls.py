from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'localDataSurvivalAndForest/',     views.LocalDataSurvivalAndForestView.as_view(),name = 'obtain survivalSplit and forest info'),
  url(r'localDataKMinfoForPlot/', views.KMinfoForPlot.as_view(), name = "obtain km info for plot")
]
