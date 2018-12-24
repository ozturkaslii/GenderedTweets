from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('barchart', views.IndexView.get_data, name='barchart'),
    path('analysis', views.analysis, name='analysis')
]

