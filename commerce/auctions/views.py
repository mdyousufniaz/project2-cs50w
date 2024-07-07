from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment

from .util import ListingForm, ListingFilter, BiddingForm, CommentForm


def index(request):
    return render(request, "auctions/index.html",{
        'listing_list': Listing.objects.filter(is_active=True),
        'default_image': Listing.DEFAULT_IMAGE_URL
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def categories_view(request):
    return render(request, "auctions/categories.html", {
        'category_listings': {category: Listing.objects.filter(category=category) for category in Listing.CATEGORIES},
        'default_image': Listing.DEFAULT_IMAGE_URL
    })

def watchlist(request):
    pass

def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            Listing(**form.cleaned_data, owner=request.user).save()

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html",{
                "form": form
            })
    return render(request, "auctions/create_listing.html",{
        "form": ListingForm()
    })

def category_view(request, category):
    return render(request, "auctions/category.html",{
        'category': category.title(),
        'listing_list': Listing.objects.filter(is_active=True, category=category.title()),
        'default_image': Listing.DEFAULT_IMAGE_URL
    })

@login_required
def profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = ListingFilter(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            request.session['filter_choice'] = form.cleaned_data['filter_option']

            return HttpResponseRedirect(reverse('profile', args=[user_id]))
            
        else:
            return render(request, "auctions/profile.html", {
                            "new_user": user,
                            "listing_filter": form,
                            'listing_list': user.listings.all(),
                            'default_image': Listing.DEFAULT_IMAGE_URL
                        })
        
    filter_choice = request.session.get('filter_choice', 'all')
        
    match filter_choice:
        case 'active':
            listing_list = user.listings.filter(is_active=True)
        case 'inactive':
            listing_list = user.listings.filter(is_active=False)
        case _:
            listing_list = user.listings.all()
    
    return render(request, "auctions/profile.html", {
                    "new_user": user,
                    "listing_filter": ListingFilter(initial={'filter_option': filter_choice}),
                    'listing_list': listing_list,
                    'default_image': Listing.DEFAULT_IMAGE_URL
                })


def listing_view(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        print(request.POST)
        if 'bid' in request.POST:
            bid_form = BiddingForm(request.POST, listing=listing)
            if bid_form.is_valid():
                Bid(**bid_form.cleaned_data, user=request.user, listing=listing).save()
                return HttpResponseRedirect(reverse('listing', args=[listing_id]))
            else:
                return render(request, "auctions/listing.html", {
                        'listing' : listing,
                        'default_image': Listing.DEFAULT_IMAGE_URL,
                        'bid_form': bid_form,
                        'comment_form': CommentForm()
                    })
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                Comment(**comment_form.cleaned_data, user=request.user, listing=listing).save()
                return HttpResponseRedirect(reverse('listing', args=[listing_id]))
            else:
                return render(request, "auctions/listing.html", {
                        'listing' : listing,
                        'default_image': Listing.DEFAULT_IMAGE_URL,
                        'bid_form': BiddingForm(),
                        'comment_form': comment_form
                    })

    return render(request, "auctions/listing.html", {
        'listing' : listing,
        'default_image': Listing.DEFAULT_IMAGE_URL,
        'bid_form': BiddingForm(listing=listing),
        'comment_form': CommentForm()
    })