from rest_framework import serializers
from .models import HairDonationUser

class HairDonationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HairDonationUser
        fields = [
            'email',
            'password'
        ]
    
    def __str__(self):
        return self.email
    
    