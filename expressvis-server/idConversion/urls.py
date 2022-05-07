from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'transformId/', views.idConversion.as_view(), name = 'transfromIDs between different IDs'),
    url(r'loadspeciesgenes/', views.SpeciesIDs.as_view(), name = 'load genesids in a species'),
    url(r'loadentryentrez/', views.LoadEntryEntrez.as_view(), name = 'load entry entrez conversion dictionary'),
]