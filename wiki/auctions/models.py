from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    owner = models.CharField(max_length=34)
    title = models.CharField(max_length=24)
    description = models.CharField(max_length=64)
    starting_bid = models.IntegerField()
    url = models.URLField(blank=True)
    category = models.CharField(max_length=24)
    active = models.BooleanField(default=True)
    winner = models.CharField(max_length=34, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} {self.description} {self.starting_bid} {self.url} {self.category}"

class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listing_id = models.IntegerField()

    def __str__(self):
        return f"{self.user} {self.listing_id}"

class Bid(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    bid_id = models.IntegerField()
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.user} bid {self.bid} on {self.title} ({self.bid_id})"

class Comment(models.Model):
    name = models.CharField(max_length=24)
    review = models.CharField(max_length=128)
    comment_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} commented {self.review} ({self.comment_id})"

class CloseBid(models.Model):
    owner = models.CharField(max_length=64)
    winner = models.CharField(max_length=64)
    listing_id = models.IntegerField()
    win_bid = models.IntegerField() 

    def __str__(self):
        return f"{self.owner} closed the bid and the winner is {self.winner} with price {self.win_bid}"