from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    watchlist = models.ForeignKey('Listing', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Id: {self.id}, Username: {self.username}, Email: {self.email}"

class Bid(models.Model):
    bidder = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return f"Id: {self.id}, Bidder: {self.bidder.username}, Amount: ${self.amount}"

class Comment(models.Model):
    commenter = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"Id: {self.id}, Commenter: {self.commenter.username}, Text: {self.text}"

class Listing(models.Model):
    CATEGORIES = (
        "No Category",
        "Fashion",
        "Toys",
        "Electronics",
        "Home",
        "Other"
    )

    CATEGORIES = ((category, category) for category in CATEGORIES)

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    start_bid = models.FloatField()
    image_url = models.URLField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)
    bids = models.ForeignKey(Bid, null=True, on_delete=models.CASCADE)
    comments = models.ForeignKey(Comment, null=True, on_delete=models.CASCADE)
    category = models.CharField(choices=CATEGORIES, default="No Category", max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Id: {self.id}, "
            f"Title: {self.title}, "
            f"Description: {self.description}, "
            f"Start Bid: ${self.start_bid}, "
            f"Image URL: {self.image_url}, "
            f"Is Active: {self.is_active}, "
            f"Bids: {self.bids}, "
            f"Comments: {self.comments}, "
            f"Category: {self.category}, "
            f"Owner: {self.owner.username}, "
            f"Creation Time: {self.creation_time}"
        )
