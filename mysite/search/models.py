from django.db import models

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    # split lat_long into 2 fields
    latitude = models.FloatField()
    longitude = models.FloatField()

    # additional fields from full_details
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    cuisines = models.CharField(max_length=255, blank=True, null=True)
    price_range = models.IntegerField(blank=True, null=True)
    average_cost_for_two = models.IntegerField(blank=True, null=True)
    user_rating = models.FloatField(blank=True, null=True)
    user_rating_votes = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.city})"


class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items') # many to one relationship (1-->M)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.name} - ₹{self.price}'