from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

phone_number_validator = RegexValidator(
    regex=r'^\+?1?\d{9,25}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 25 digits allowed."
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(default="", max_length=250)
    last_name = models.CharField(default="", max_length=250)
    city = models.CharField(default="", max_length=250)
    age = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        validators=[MinValueValidator(18), MaxValueValidator(90)],
    )
    phone_number = models.CharField(
        max_length=25,
        validators=[phone_number_validator], 
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return f"{self.user}'s profile instance"
