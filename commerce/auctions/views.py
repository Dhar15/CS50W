from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import *
from django import forms


class CreateListForm(forms.Form):
    owner = forms.CharField(label="",
        widget=forms.TextInput(attrs={'placeholder': ' Owner Name*', 
            'style': 'width:90%'})) 
    title = forms.CharField(label="",
        widget=forms.TextInput(attrs={'placeholder': ' Title*', 
            'style': 'width:90%'})) 
    description = forms.CharField(label="",
        widget=forms.Textarea(attrs={'placeholder': ' Description*', 
            'style': 'width:90%'}))
    starting_bid = forms.IntegerField(label="",
        widget=forms.TextInput(attrs={'placeholder': ' Starting Bid*', 
            'style': 'width:90%'}))
    url = forms.URLField(label="",required=False,
        widget=forms.TextInput(attrs={'placeholder': ' URL (Optional)', 
            'style': 'width:90%'}))
    category = forms.CharField(label="",
        widget=forms.TextInput(attrs={'placeholder': ' Category*', 
            'style': 'width:90%'}))

class BidForm(forms.Form):
    bid = forms.DecimalField(label="",max_digits=10, decimal_places=2,
        widget=forms.TextInput(attrs={'placeholder': ' Your Bid', 
            'style': 'width:90%'}))

class CommentForm(forms.Form):
    name = forms.CharField(label="",
        widget=forms.TextInput(attrs={'placeholder': ' Name', 
            'style': 'width:90%'}))
    review = forms.CharField(label="",
        widget=forms.Textarea(attrs={'placeholder': ' Feedback', 
            'style': 'width:90%'}))
    

def index(request):
    return render(request, "auctions/index.html", {
        "listings":Listing.objects.all()
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

def create(request):
    if request.method == "POST":
        form = CreateListForm(request.POST)
        if form.is_valid():
            owner = form.cleaned_data['owner']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            starting_bid = form.cleaned_data['starting_bid']
            url = form.cleaned_data['url']
            category = form.cleaned_data['category']
            instance = Listing(owner=owner,title=title, description=description, starting_bid=starting_bid, url=url, category=category)
            instance.save()
            return HttpResponseRedirect(reverse("index"))
        
    return render(request, "auctions/create.html",{
        "form": CreateListForm()
    })
    

def list(request, list_id):
    list = Listing.objects.get(pk=list_id)
    return redirect('listingpage', id=list_id)          

def watchlistpage(request,username):
    if request.user.username:
        try:
            list = Watchlist.objects.filter(user=username)
            items = []
            for i in list:
                items.append(Listing.objects.filter(id=i.listing_id))
            try:
                w = Watchlist.objects.filter(user = request.user.username)
                count = len(w)
            except:
                count = None
            return render(request,"auctions/watchlist.html",{
                "items": items,
                "count": count
            })
        except:
            try:
                w = Watchlist.objects.filter(user = request.user.username)
                count = len(w)
            except:
                count = None
            return render(request,"auctions/watchlist.html",{
                "items": None,
                "count": count
            })

def listingpage(request, id):
    try:
        item = Listing.objects.get(id=id)
    except:
        return redirect('index')
    try:
        comments = Comment.objects.filter(comment_id=id)
    except:
        comments= None
    if request.user.username:
        try:
            if Watchlist.objects.get(user=request.user.username, listing_id=id):
                added = True
            else:
                added = False
        except:
            added = False

        l = Listing.objects.get(id=id)
        if l.owner.lower() == request.user.username.lower():
            owner = True
        else:
            owner = False

    else:
        added = False
        owner = False
    
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        count=len(w)
    except:
        count=None

    return render(request, "auctions/list.html", {
        "list": item,
        "added": added,
        "owner": owner,
        "count": count,
        "bid": BidForm(),
        "comment": CommentForm(),
        "comments": comments,
        "error":request.COOKIES.get('error'),
        "errorgreen":request.COOKIES.get('errorgreen')
    })

def addtowatchlist(request, list_id):
    if request.user.username:
        w = Watchlist()
        w.user = request.user.username
        w.listing_id = list_id
        w.save()
        return redirect('listingpage', id=list_id)
    else:
        return redirect('index')

def delete_cmt(request,list_id):
    w = Comment.objects.get(comment_id = list_id)
    w.delete()
    return redirect('listingpage', id=list_id)

def removefromwatchlist(request, list_id):
    if request.user.username:
        try:
            w = Watchlist.objects.get(user=request.user.username, listing_id=list_id)
            w.delete()
            return redirect('listingpage', id=list_id)
        except:
            return redirect('listingpage', id=list_id)
    else:
        return redirect('index')

def add_comment(request, list_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            review = form.cleaned_data['review']
            instance = Comment(name=name, review=review, comment_id=list_id)
            instance.save()
            return redirect('listingpage', id=list_id)
    return HttpResponseRedirect(reverse('index'))


def categories(request):
    categories = set()
    listing = Listing.objects.all()
    for item in listing:
        categories.add(item.category)
    return render(request, "auctions/categories.html",{
        "categories":categories
    })

def jumptocategory(request, category):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.filter(category = category)
    })

def add_bid(request, list_id):
    current_bid = Listing.objects.get(id=list_id)
    current_bid = current_bid.starting_bid
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            user_bid = int(form.cleaned_data['bid'])
        if user_bid > current_bid:
            list_items = Listing.objects.get(id=list_id)
            list_items.starting_bid = user_bid
            list_items.save()
            if Bid.objects.filter(id=list_id):
                bidrow = Bid.objects.filter(id=list_id)
                bidrow.delete()
            bid = Bid()
            bid.user = request.user.username
            bid.title = list_items.title
            bid.bid_id = list_id
            bid.bid = user_bid
            bid.save()
            response = redirect('listingpage', id=list_id)
            response.set_cookie("errorgreen", "Bid Successful!",max_age=5)
            return response
        else:
            response = redirect('listingpage', id=list_id)
            response.set_cookie("error", "Bid should be greater than the current price", max_age=5)
            return response
    else:
        return redirect('index')

def close_bid(request,list_id):
    if request.user.username:
        list = Listing.objects.get(id=list_id)
        title = list.title
        closebid = CloseBid()
        closebid.owner = list.owner
        closebid.listing_id = list_id
        try:
            biditem = Bid.objects.get(bid_id=list_id, bid=list.starting_bid)
            closebid.winner = biditem.user
            closebid.win_bid = biditem.bid
            closebid.save()
            biditem.delete()
        except:
            closebid.winner = list.owner
            closebid.win_bid = list.starting_bid
            closebid.save()
        
        try:
            if Watchlist.objects.filter(listing_id=list_id):
                watchlist_item = Watchlist.objects.filter(listing_id=list_id)
                watchlist_item.delete()
        except:
            pass

        comment = Comment.objects.filter(comment_id = list_id)
        comment.delete()

        brow = Bid.objects.filter(bid_id=list_id)
        brow.delete()

        try:
            cb = CloseBid.objects.get(listing_id=list_id)
        except:
            closebid.owner = list.owner
            closebid.winner = list.owner
            closebid.listing_id = list_id
            closebid.win_bid = list.starting_bid
            closebid.save()
            cb = CloseBid.objects.get(listing_id = list_id)

        try:
            w = Watchlist.objects.filter(user=request.user.username)
            count = len(w)
        except:
            count = None

        list.active = False
        list.winner = cb.winner
        list.save()

        return redirect('listingpage', id=list_id)

    else:
        return redirect('índex')
        
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
