from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import HairDonationUser
from companyController.serializer import CompanySerializer
from companyController.models import Company
from rest_framework import generics
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import hair_project.settings
import os

class addCompanyAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

addCompanyView = addCompanyAPIView.as_view()

class viewCompanyView(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'pk'

viewCompany = viewCompanyView.as_view()

class deleteCompanyAPIView(generics.DestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'pk'

deleteCompanyView = deleteCompanyAPIView.as_view()


@api_view(["POST"])
def updateCompanyView(request, pk):
    mail = request.data["email"]
    name = request.data["name"]
    surname = request.data["surname"]

    try:
        company = Company.objects.get(pk=pk)
    except Company.DoesNotExist:
        return Response({'error': 'Company not found'}, status=404)

    try:
        new_donation = int(request.data.get('new_donation'))
    except (ValueError, TypeError):
        return Response({'error': 'Invalid number of new donation as a CM'}, status=400)

    send_email_to(mail, name, surname, new_donation)

    tmp = new_donation * 0.0000062137
    company.last_updated_mil = tmp
    company.company_donation_cm += new_donation
    company.save()

    return Response({'message': new_donation,
                     "last_updated_cm": new_donation})    


@api_view(["GET"])
def login_view(request, *args, **kwargs):
    email = request.data["email"]
    password = request.data["password"]

    users = HairDonationUser.objects.filter(email=email)

    if users.exists():
        user = users.first()
        if password == user.password:
            response = {
                "email": user.email,
            }
            return Response(data=response)
        else:
            return Response({"message": "Password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def search_get(request, *args, **kwargs):
    pure_field = request.data["search"]
    name = pure_field.rstrip().strip().lower()
    result = []
    company_objects = Company.objects.all()
    companies_serializer = CompanySerializer(company_objects, many=True)
    companies = companies_serializer.data
    n = len(companies)
    for i in range(n):
        km = companies[i]["company_donation_cm"] * 0.00001
        mil = companies[i]["company_donation_cm"] * 0.0000062137
        companies[i]["company_donation_km"] = round(km, 5)
        companies[i]["company_donation_mil"] = round(mil,2)
        companies[i]["last_updated_cm"] = companies[i]["last_updated_mil"] / 0.0000062137
        companies[i]["last_updated_cm"] = round(companies[i]["last_updated_cm"], 6)
    if name == "":
        return Response(companies)
    else:
        for comp in companies:
            if ((name in comp["company_name"].lower()) or 
                (name == comp["company_name"].lower())):
                result.append(comp)

        return Response(result)

def send_email_to(email, name, surname, new_donation):
    subject = '🌟 Your Hair Donation - Received & Making a Difference! 🌟'
    message_head = f'Dear {name.title()} {surname.title()},'

    context = {'message_head': message_head}
    html_path = 'authController/htmls/email.html' 
    html_content = render_to_string(html_path, context)

    from_email = 'milesofempowerment.hair@gmail.com'
    recipient_list = [email] 
    
    email = EmailMessage(subject, html_content, from_email, recipient_list)  # Attach HTML content to the email message
    email.content_subtype = 'html'  # Set the content subtype to HTML
    email.send()

    #from_email = 'milesofempowerment.hair@gmail.com'
    #recipient_list = [email] 

    #send_mail(subject, message, from_email, recipient_list)
    
    return Response('Email sent successfully!')