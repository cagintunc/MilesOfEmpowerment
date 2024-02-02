from django.urls import path
from . import views
from companyController.views import total_donation

urlpatterns = [
    path('login/', views.login_view, name="login_view"),
    path('menu/addCompany/', views.addCompanyView, name="add_company"),
    path('menu/deleteCompany/<int:pk>/', views.deleteCompanyView, name="delete_company"),
    path('menu/updateCompany/<int:pk>/', views.updateCompanyView, name="update_company"),
    path('menu/viewCompany/<int:pk>/', views.viewCompany, name="view_company"),
    path('menu/search/', views.search_get, name="search_get"),
    path('menu/totalDonation/', total_donation),
]