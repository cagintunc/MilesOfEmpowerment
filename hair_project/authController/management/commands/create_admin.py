from django.core.management.base import BaseCommand
from authController.models import HairDonationUser

class Command(BaseCommand):
    help = 'Creates a HairDonationUser instance'

    def handle(self, *args, **options):
        hair_donation_user = HairDonationUser.objects.create_user(
            email='admin@hotmail.com',
            password='123'  # Replace with the actual password
        )

        # Print the created user's email
        self.stdout.write(self.style.SUCCESS(f"Created HairDonationUser: {hair_donation_user.email}"))