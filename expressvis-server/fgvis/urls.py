"""fgvis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
#from fgvis.settings import STATIC_URL, STATIC_ROOT
from django.conf.urls.static import static

urlpatterns = [
  url(r'dataset/', include('dataset.urls')),
  url(r'enrichment/', include('enrichment.urls')),
  url(r'annotation/', include('annotation.urls')),
  url(r'keggExplore/', include('keggExplore.urls')),
  url(r'clustering/', include('clustering.urls')),
  url(r'diffAnalysis/', include('diffAnalysis.urls')),
  url(r'ids/', include('idConversion.urls')),
  url(r'ppinetwork/', include('constructPPInetwork.urls')),
  url(r'proteomics/', include('preprocessproteomics.urls')),
  url(r'clinical/',   include('clinical.urls')),
  url(r'^admin/', admin.site.urls),
] #+ static(STATIC_URL, document_root=STATIC_ROOT)
