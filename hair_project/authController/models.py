from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone


class HairDonationUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have a valid email")
        user = self.model(
            email=self.normalize_email(email),
        )

        if password:
            user.password = password

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )

        user.is_admin = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length = 255,
        unique= True
    )
    role = models.CharField(max_length=255, default= "Normal")

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)


    objects = HairDonationUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email
    
    def has_perm(self, perm, obj = None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin

class HairDonationUser(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)

    objects = HairDonationUserManager()

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        self.password = raw_password

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
class HairDonationValidationCode(models.Model):
    code = models.CharField(max_length=8)
    user = models.ForeignKey(HairDonationUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.code