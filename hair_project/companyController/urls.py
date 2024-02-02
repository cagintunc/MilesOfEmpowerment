from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_all_companies_sorted),
    path('sortAlphabetically/', views.get_alphabetically_sorted),
]