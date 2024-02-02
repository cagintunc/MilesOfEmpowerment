from django.db import models

class Company(models.Model):
    company_name = models.CharField(max_length=200)
    company_image = models.TextField(default="")
    company_donation_cm = models.IntegerField(default=0)
    company_donation_km = models.IntegerField(default=0)
    company_donation_mil = models.IntegerField(default=0)
    last_updated_mil = models.FloatField(default=0)

    def __str__(self):
        return self.company_name
    
    
