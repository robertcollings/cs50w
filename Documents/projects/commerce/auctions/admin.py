from django.contrib import admin

from .models import Listing, User, BidHistory, Watchlist, Comments, Categories

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title")

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")

class BidHistoryAdmin(admin.ModelAdmin):
    list_display = ("listing", "amount", "time", "starting", "user")

class CommentsAdmin(admin.ModelAdmin):
    list_display = ("user", "time", "listing", "comment")

admin.site.register(Listing, ListingAdmin)

admin.site.register(User, UserAdmin)

admin.site.register(BidHistory, BidHistoryAdmin)

admin.site.register(Watchlist)

admin.site.register(Comments, CommentsAdmin)

admin.site.register(Categories)