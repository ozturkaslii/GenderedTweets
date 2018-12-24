from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('barchart', views.IndexView.get_data, name='barchart'),
    path('analysis', views.AnalysisView.as_view(), name='analysis'),
    path('piechart', views.AnalysisView.get_data, name='piechart'),
]

