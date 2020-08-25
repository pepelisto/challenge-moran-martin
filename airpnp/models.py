from django.db import models
from django.contrib.auth.models import User, Permission
from django.core.validators import MinValueValidator, MaxValueValidator

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)
    description = models.TextField(max_length=300)
    adults = models.PositiveIntegerField()
    children = models.PositiveIntegerField()
    is_pets_allowed = models.BooleanField()
    base_price = models.DecimalField(decimal_places=2, max_digits=5)
    cleaning_fee = models.DecimalField(decimal_places=2, max_digits=5)
    image_url = models.TextField(max_length=300)
    weekly_discount = models.DecimalField(decimal_places=2, max_digits=5, default=1, validators=[MinValueValidator(0), MaxValueValidator(1)])
    monthly_discount = models.DecimalField(decimal_places=2, max_digits=5, default=1, validators=[MinValueValidator(0), MaxValueValidator(1)])
    def __str__(self):
        return self.name

class Special_price(models.Model):
    listing = models.ForeignKey(Listing, related_name='special_prices', on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(decimal_places=2, max_digits=5)
    class Meta:
        unique_together = ['listing', 'date']
    def __str__(self):
        return 'date: ' + str(self.date) + ', ' + 'base_price: ' + str(self.price)

