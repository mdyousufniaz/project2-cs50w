from django.contrib import admin

from .models import User, Bid, Comment, Listing
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'start_bid', 'image_url', 'is_active', 'category', 'owner', 'creation_time')

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
