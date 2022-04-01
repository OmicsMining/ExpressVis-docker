from django.conf.urls import url
from . import views 
urlpatterns = [
  # url(r'parseKgml/', views.parseKgml.as_view(), name = 'parseKgml'),
  url(r'allkeggspecies/', views.QueryKeggSpecies.as_view(), name = 'allkeggspecies'),
  url(r'onespeciespathways/', views.QueryOneSpeciesPathways.as_view(), name = 'onespeciespathways'),
  url(r'kgmlentryidinfo/', views.KGMLentryIDinfo.as_view(), name = 'kgmlentryidinfo'),
]
