from django.conf.urls import url
from . import views 
urlpatterns = [
  # url(r'parseKgml/', views.parseKgml.as_view(), name = 'parseKgml'),
  url(r'preprocessProteomics/', views.PreProcessProteomicsView.as_view(), name = "pre process proteomics data"),
  url(r'removebatcheffect/', views.RemoveBatchView.as_view(), name = "remove batcheffect")
]
