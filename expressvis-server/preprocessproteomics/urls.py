from django.conf.urls import url
from . import views 
urlpatterns = [
  # url(r'parseKgml/', views.parseKgml.as_view(), name = 'parseKgml'),
  url(r'preprocessproteomics/', views.PreProcessProteomicsView.as_view(), name = "pre process proteomics data"),

]
