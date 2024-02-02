
from django.contrib import admin
from django.urls import path, include
from companyController.views import download_pdf, total_donation
urlpatterns = [
    path('', include('companyController.urls')),
    path('admin/', include('authController.urls')),
    path('download-pdf/', download_pdf),
    path('totalDonation/', total_donation),
]
