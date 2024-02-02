
from django.contrib import admin
from django.urls import path, include
from companyController.views import download_pdf, total_donation
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # new

urlpatterns = [
    path('', include('companyController.urls')),
    path('admin/', include('authController.urls')),
    path('download-pdf/', download_pdf),
    path('totalDonation/', total_donation),
]

urlpatterns += staticfiles_urlpatterns() # new
