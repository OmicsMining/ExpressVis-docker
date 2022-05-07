from django.conf.urls import url
from . import views 

urlpatterns = [
  url(r"localDatasetPCA/", views.PCA.as_view(), name = "local dataset PCA analysi")
]
