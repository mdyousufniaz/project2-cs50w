from django import forms
from .models import Listing, User

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ["bids", "comments", "creation_time", "is_active", "owner"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "start_bid": forms.NumberInput(attrs={"class": "form-control"}),
            "image_url": forms.URLInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].label = self.fields["title"].label + f" (max {self.fields['title'].max_length} words)"
        self.fields["description"].label = self.fields["description"].label + f" (max {self.fields['description'].max_length} words)"
        self.fields["start_bid"].label = self.fields["start_bid"].label + " (in $)"
        self.fields["image_url"].label = self.fields["image_url"].label + f" (provide a valid image for the lisiting)"

        required_fields = ["title", "description", "start_bid", "category"]
        for field_name in required_fields:
            self.fields[field_name].required = True

        for field_name, field in self.fields.items():
            field.label_suffix = "*" if field.required else ""
            field.widget.attrs['label_class'] = 'form-label'

class ListingFilter(forms.Form):
    CHOICES = [
        ('all', 'All'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    filter_option = forms.ChoiceField(choices=CHOICES, initial='all', widget=forms.Select)
