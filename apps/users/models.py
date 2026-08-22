from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER","Customer",
        SUPPORT_ADMIN = "SUPPORT_ADMIN","Support Admin",
        SUPPORT_AGENT = "SUPPORT_AGENT","Support Agent"
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER
    )    



