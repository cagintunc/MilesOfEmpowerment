from .models import Company
from .serializer import CompanySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
import os
from django.conf import settings
import base64
 
@api_view(['GET'])
def get_all_companies_sorted(request, *args, **kwargs):
    company_objects = Company.objects.all()
    companies_serializer = CompanySerializer(company_objects, many=True)
    companies = companies_serializer.data
    
    n = len(companies)
    swapped = False
    for i in range(n-1):
        for j in range(0, n-i-1):
            if (companies[j]["company_donation_cm"] < 
                companies[j + 1]["company_donation_cm"]):
                swapped = True
                companies[j], companies[j + 1] = companies[j + 1], companies[j]
        
        if not swapped:
            break
    for i in range(n):
        km = companies[i]["company_donation_cm"] * 0.00001
        mil = companies[i]["company_donation_cm"] * 0.0000062137
        companies[i]["company_donation_km"] = round(km, 2)
        companies[i]["company_donation_mil"] = round(mil, 2)
        companies[i]["last_updated_cm"] = companies[i]["last_updated_mil"] / 0.0000062137
        companies[i]["last_updated_mil"] = round(companies[i]["last_updated_mil"], 2)
    
    return Response(companies)

@api_view(["GET"])
def get_alphabetically_sorted(request, *args, **kwargs):
    sorted_companies = None
    parameter = int(request.data["reverse"])
    companies = Company.objects.all()
    if parameter == 0:
        sorted_companies = sorted(companies, 
                                  key=lambda company: company.company_name.lower())
    else:
        sorted_companies = sorted(companies, 
                                  key=lambda company: company.company_name.lower(), reverse=True)

    company_seri = CompanySerializer(sorted_companies, many=True)

    companiesS = company_seri.data
    n = len(companiesS)
    for i in range(n):
        km = companiesS[i]["company_donation_cm"] * 0.00001
        mil = companiesS[i]["company_donation_cm"] * 0.0000062137
        companiesS[i]["company_donation_km"] = round(km, 2)
        companiesS[i]["company_donation_mil"] = round(mil, 2)
        companiesS[i]["last_updated_cm"] = companiesS[i]["last_updated_mil"] / 0.0000062137
        companiesS[i]["last_updated_mil"] = round(companiesS[i]["last_updated_mil"], 2)
    return Response(companiesS)
    


@api_view(["GET"])
def download_pdf(request):
    file_path = os.path.join(settings.STATIC_ROOT, 'pdfs', 'DonationForm.pdf')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
            pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
            return Response({'pdf_base64': pdf_base64})
    else:
        return Response({'error': 'PDF not found'}, status=404)
    
@api_view(["GET"])
def total_donation(request):
    companyObject = Company.objects.all()
    companySeri = CompanySerializer(companyObject, many=True)
    companies = companySeri.data
    total_mil = 0.0
    for company in companies:
        total_mil += round(company["company_donation_cm"] * 0.0000062137, 5)
    return Response({"totalDonation": total_mil})