from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    latest_bid = models.ForeignKey('BidHistory', on_delete=models.CASCADE, related_name='+', null=True)
    image = models.URLField()
    #category = models.CharField(max_length=64)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE, related_name='+')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField()
    ended = models.BooleanField(default=False)
    ended_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.title}"

class BidHistory(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings")
    amount = models.DecimalField(decimal_places=2, max_digits=6)
    time = models.DateTimeField()
    starting = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.amount}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watching = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.watching}"

class Comments(models.Model):
    comment = models.CharField(max_length=1024)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.comment}"

class Categories(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"