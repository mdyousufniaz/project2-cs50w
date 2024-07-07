from django.urls import path, re_path
from .models import Listing

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories_view, name="categories"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("profile/<int:user_id>", views.profile_view, name="profile"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    re_path(r'^category/(?P<category>(' + '|'.join((category.lower() for category in Listing.CATEGORIES)) + '))/?$', views.category_view, name="category")
]
