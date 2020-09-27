from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import datetime

from .models import User, Listing, BidHistory, Watchlist, Comments, Categories
from .forms import CreateListingForm, CreateBidForm, CreateCommentsForm


def index(request):

    active_listings = Listing.objects.filter(ended=False)
    ended_listings = Listing.objects.filter(ended=True)

    categories = Categories.objects.all() #.values_list('category', flat=True)

    print(request.user)
    if request.user.is_authenticated:
        # Get watched items
        watcheditems = Watchlist.objects.filter(user=request.user).values_list('watching', flat=True)
    else:
        watcheditems = []

    return render(request, "auctions/index.html", {
        "listings":active_listings,
        "watching":watcheditems,
        "endedlistings":ended_listings,
        "categories":categories,
    })

@login_required
def bid(amount, listing, start, request):
    # Update database with the bid
    dbEntry = BidHistory(
        listing = listing,
        amount = amount,
        time = datetime.datetime.now(),
        starting = start,
        user = request.user
    )

    # Save the db entry
    dbEntry.save()

    # Assign the latest bid ID to the listing
    bidID = BidHistory.objects.latest('time')
    listing.latest_bid = bidID
    listing.save()


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

def create(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = CreateListingForm(request.POST)

        # check whether it's valid:
        if form.is_valid():

            # store form data in a variable called listing
            listing = form.cleaned_data

            # new variable with the specific elements in list form
            listing_data = Listing(
                title=listing["title"],
                description=listing["description"],
                image=listing["image"],
                created_date=datetime.datetime.now(),
                owner = request.user,
                category = listing["category"]
            )

            listing_data.save()

            # Record starting bid
            bid(listing["start_bid"], listing_data, True, request) 

            return HttpResponseRedirect(reverse('index'))

    else:
        form = CreateListingForm()

    return render(request, "auctions/create.html", {
        "form":form
    })

@login_required
def view_listing(request, auction_id):

    message = ""

    listingID = Listing.objects.get(pk=auction_id)

    if request.method == "POST":
        if "new-bid" in request.POST:
            # create a form instance and populate it with data from the request:
            form = CreateBidForm(request.POST)

            # check whether it's valid:
            if form.is_valid():

                # store form data in a variable called listing
                bid_data = form.cleaned_data

                # Check the bid to ensure it's valid
                if bid_data["amount"] <= listingID.latest_bid.amount:
                    message = False

                else:
                    bid(bid_data["amount"], listingID, False, request)
                    message = True
            
        elif "new-comment" in request.POST:
            # create a form instance and populate it with data from the request:
            form = CreateCommentsForm(request.POST)

            # check whether it's valid:
            if form.is_valid():

                # store form data in a variable called listing
                comment = form.cleaned_data

                dbEntry = Comments(
                    listing = listingID,
                    user = request.user,
                    time = datetime.datetime.now(),
                    comment = comment["comment"]
                )
                dbEntry.save()

    #listing = Listing.objects.get(pk=auction_id)

    # Create form for placing bid
    form = CreateBidForm()

    # Get bid history
    bid_history = BidHistory.objects.filter(listing=listingID).order_by("-amount")

    # Run comments section
    commentsform = add_comment(request)
    comments = Comments.objects.filter(listing=listingID)

    return render(request, "auctions/listing.html", {
        "listing":listingID, 
        "form":form, 
        "message":message, 
        "bids":bid_history,
        "commentsform":commentsform,
        "comments":comments,
    })



def add_comment(request):
    commentsform = CreateCommentsForm()

    return commentsform


def watchlist(request):

    user = request.user

    watching = Watchlist.objects.filter(user=user)

    return render(request, "auctions/watchlist.html", {
        "watching":watching,
        })


def watch(request, listing):

    if request.user.is_authenticated:
        dbEntry = Watchlist(
            user=request.user,
            watching=Listing.objects.get(id=listing),
        )

        dbEntry.save()
    
        return HttpResponseRedirect(reverse('watchlist'))
    else:
        return HttpResponseRedirect(reverse('login'))


def unwatch(request, listing):

    dbDelete = Watchlist.objects.filter(user=request.user).get(watching=listing)
    
    dbDelete.delete()
   
    return HttpResponseRedirect(reverse('watchlist'))

def end(request, listing):

    dbEntry = Listing.objects.get(id=listing)
    dbEntry.ended = True
    dbEntry.ended_time = datetime.datetime.now()
    dbEntry.save()

    return redirect(view_listing, listing)

def category(request, cat):

    active_listings = Listing.objects.filter(ended=False).filter(category=cat)
    ended_listings = Listing.objects.filter(ended=True).filter(category=cat)

    categories = Categories.objects.all() #.values_list('category', flat=True)

    if request.user.is_authenticated:
        # Get watched items
        watcheditems = Watchlist.objects.filter(user=request.user).values_list('watching', flat=True)
    else:
        watcheditems = []

    return render(request, "auctions/index.html", {
        "listings":active_listings,
        "watching":watcheditems,
        "endedlistings":ended_listings,
        "categories":categories,
    })