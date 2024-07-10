from django import forms
from .models import Listing, Bid, Comment
from django.utils.translation import gettext_lazy as _
from django.db.models import Max
from decimal import Decimal
from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ["creation_time", "is_active", "owner"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows'] = 4
        self.fields['image_url'].required = False
        self.fields['image_url'].label += _(" (optional)")
        self.fields['start_bid'].label += _(" (in $)")
        for i, field in self.fields.items():
            if field.widget.attrs.get('class', None):
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs.update({'class': 'form-control'})

class BiddingForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ['user', 'listing']

        labels = {
            'amount': 'Place Your Bid'
        }

    def __init__(self, *args, **kwargs):
        listing = kwargs.pop('listing', None)
        super().__init__(*args, **kwargs)

        self.fields['amount'].widget.attrs.update({
            'placeholder': 'Enter your bid amount',
            'class': 'form-control'
        })
        

        if listing:
            min_value = listing.bids.all().aggregate(Max('amount'))['amount__max'] + Decimal(0.01) if listing.bids.exists() else listing.start_bid
            self.fields['amount'].widget.attrs.update({
                'min': min_value
            })

class ListingFilter(forms.Form):
    CHOICES = [
        ('all', 'All'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    filter_option = forms.ChoiceField(choices=CHOICES, initial='all', widget=forms.Select, label='Filter')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
                'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter your comment here...'
            })
        }

def custom_login_required(next='index'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
            else:
                next_url = request.GET.get('next', '')
                if not next_url:
                    next_url = reverse(next)
                return redirect(f'{reverse("login")}?next={next_url}')
        return _wrapped_view
    return decorator
