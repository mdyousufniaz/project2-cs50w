from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing',
                                    blank=True,
                                    related_name='observers')

    def __str__(self):
        return f"Id: {self.id}, Username: {self.username}, Email: {self.email}, watchlist: {self.watchlist}"
    


class Listing(models.Model):
    CATEGORIES = (
        "No Category",
        "Fashion",
        "Toys",
        "Electronics",
        "Home",
        "Other"
    )

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    start_bid = models.DecimalField(decimal_places=2, max_digits=10)
    image_url = models.URLField(max_length=400)
    is_active = models.BooleanField(default=True)
    category = models.CharField(choices=[(category, _(category)) for category in CATEGORIES],
                                default="No Category",
                                max_length=15)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Id: {self.id}, "
            f"Title: {self.title}, "
            f"Description: {self.description}, "
            f"Start Bid: ${self.start_bid}, "
            f"Image URL: {self.image_url}, "
            f"Is Active: {self.is_active}, "
            f"Category: {self.category}, "
            f"Owner: {self.owner.username}, "
            f"Creation Time: {self.creation_time}"
        )
    



class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')

    def __str__(self):
        return f"Id: {self.id}, Bidder: {self.bidder}, Amount: ${self.amount}, Listing: {self.listing}"

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Id: {self.id}, Commenter: {self.commenter}, Text: {self.text}, Listing: {self.listing}"
    