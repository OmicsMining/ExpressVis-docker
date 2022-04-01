from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'constructNetwork/', views.NetworkConstruction.as_view(), name = 'construct Network'),
]

