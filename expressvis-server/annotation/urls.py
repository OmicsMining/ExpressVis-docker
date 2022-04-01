from django.conf.urls import url
from . import views 
urlpatterns = [
  url(r'obtainGenes/', views.pathwayGenes.as_view(), name = 'obtainGenesWithinPathway'),
  url(r'obtainTerms/', views.pathwayTerms.as_view(), name = 'obtainTerms'),
  url(r'obtainGenesAnno/', views.GenesAnnoInfo.as_view(), name = 'obtain genes annotation'),
  url(r'obtainSpeciesMappingInfoBetweenTwoIDtypes', views.MappingBetwwenIDtypesWitinOneSpecies.as_view(), 
    name = 'obtainSpeciesMappingInfoBetweenTwoTypes'),
  url(r'arrayIDtypesInOneSpecies', views.LoadArrayIDTypesInOneSpecies.as_view(), name = "LoadArrayIDTypesInOneSpecies"),
  url(r'annotationTerms', views.AnnotationTerms.as_view(), name = "load annotation terms"),
  url(r'annotationGenes', views.AnnotationGenes.as_view(), name = "load genes in an annotation term")
]
