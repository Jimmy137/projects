from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Category, Comment, WatchList


def index(request):
    listings = Listing.objects.all()
    bids = Bid.objects.all()
    categories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings" : listings,
        "bids" : bids,
        "ctgs" : categories,

        
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
        if not username or not email or not password or not confirmation:
             return render(request, "auctions/register.html", {
                "message": "All fields must be filled."
            }) 
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

def crl (request):
    if request.method== "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        img= request.POST["img"]
        initialbid = request.POST["initialbid"]
        ctg = request.POST.get('ctg')
        cs = Category.objects.values_list('name', flat=True)

        if ctg not in cs :
             create = Category(name=ctg)
             create.save()
             category = Category.objects.get(name=ctg)
        else :
             category = Category.objects.get(name=ctg)


        if not title or not initialbid or not content :
             categories = Category.objects.all()      
             return render(request, "auctions/crl.html",{
                   "message" : "You haven't filled required field/fields!",
                   "cs" : categories
               })  
        user = request.user
        nlisting = Listing(owner= user, created= datetime.datetime.now(), initialbid= initialbid,
                    discription= content, title= title, photo = img,
                     category = category, active= True)
        
        nlisting.save()
        lid = nlisting.id
        
        return HttpResponseRedirect(reverse("index"))
        
        

    else:  
         categories = Category.objects.all()      
         return render(request, "auctions/crl.html",{
             "cs" : categories,
            

         })


def lst (request, lid):
    listing = Listing.objects.get(pk=lid)
    comments = listing.comments.all()
    m = listing.initialbid + 0.1
    bids = Bid.objects.all()
    
    try:
         bid = Bid.objects.get(listing= listing)
         mm = bid.value + 0.1
    except Bid.DoesNotExist:
         mm = None
    
    try:
        w = WatchList.objects.get(user= request.user)
        ww = w.listings.all()
    except WatchList.DoesNotExist:
        ww = []
    except TypeError:
        ww = []


    
    return render (request, "auctions/listing.html",{
        "list" : listing,
        "comments" : comments,
        "m" : m,
        "mm" : mm,
        "ww" : ww
       
    })

def category (request, cid):
    category = Category.objects.get(pk=cid)
    listings = category.listings.all()
    bids = Bid.objects.all()
    return render (request, "auctions/category.html",{
        "listings" : listings,
        "bids" : bids
    })

def comment (request, lid):
    if request.method== "POST":
        comment = request.POST["content"]
        user = request.user
        created = datetime.datetime.now()
        listing = Listing.objects.get(pk=lid)

        
        if comment :
            c = Comment(commenter= user, listing= listing, created= created,
              content= comment)

            c.save()

            return HttpResponseRedirect(reverse("list", args=[listing.id]))

        else:
            return HttpResponseRedirect(reverse("list", args=[listing.id]))


def categories (request):
    ctgs = Category.objects.exclude(name="").all()
    return render (request, "auctions/categories.html",{
        "categories" : ctgs
    })

def bid (request, lid):
    if request.method== "POST":
        bid = float(request.POST["bid"])
        user = request.user
        listing = Listing.objects.get(pk=lid)

        if bid > listing.initialbid :
            if Bid.objects.filter(listing = listing).exists():
                 Bid.objects.filter(listing = listing).update_or_create(
            
                 defaults={'value': bid, 'bidder': user}
                 )
            else:
                Bid.objects.create(bidder= user, listing= listing, value=bid)
        
           
           
            comments = listing.comments.all()
            m = listing.initialbid + 0.1
            bids = Bid.objects.all()
            try:
                 bid = Bid.objects.get(listing= listing)
                 mm = bid.value + 0.1
            except Bid.DoesNotExist:
                 mm = None
            try:
                 w = WatchList.objects.get(user= request.user)
                 ww = w.listings.all()
            except WatchList.DoesNotExist:
                 ww = []
            except TypeError:
                 ww = []
    
    
            return render (request, "auctions/listing.html",{
                 "list" : listing,
                 "comments" : comments,
                 "m" : m,
                 "mm" : mm,
                 "message" : "Your bid has been submitted successfully.",
                 "ww" : ww
       
            })
        else:
            return HttpResponseRedirect(reverse("list", args=[listing.id]))

@login_required
def watch (request, uid):
    user = User.objects.get(pk = uid)
    try:
         watch = WatchList.objects.get(user= user)
         listings = Listing.objects.filter(watchlist = watch)
    except WatchList.DoesNotExist :
        watch = None
        listings = None

    bids = Bid.objects.all()
    categories = Category.objects.all()
    
    
    return render (request, "auctions/watchlist.html",{
        "user" : user,
        "listings" : listings,
        "bids" : bids,
        "ctgs" : categories,
    })

@login_required
def addwatch (request, lid):
    if request.method== "POST":
        user = request.user
        listing = Listing.objects.get(pk=lid)
        
        if WatchList.objects.filter(user= user).exists():
             watch = WatchList.objects.get(user= user)
             watch.listings.add(listing)
        else:
             w = WatchList(user= user)
             w.save()
             watch = WatchList.objects.get(user= user)
             watch.listings.add(listing)
        
        comments = listing.comments.all()
        m = listing.initialbid + 0.1
        bids = Bid.objects.all()
        try:
             bid = Bid.objects.get(listing= listing)
             mm = bid.value + 0.1
        except Bid.DoesNotExist:
             mm = None
        
        try:
             w = WatchList.objects.get(user= request.user)
             ww = w.listings.all()
        except WatchList.DoesNotExist:
             ww = []
        except TypeError:
             ww = []
    
    
        return render (request, "auctions/listing.html",{
             "list" : listing,
             "comments" : comments,
             "m" : m,
             "mm" : mm,
             "pm" : "The listing has been added to your Watchlist.",
             "ww" : ww
       
            })

def close (request, lid):
    
    user = request.user
    listing = Listing.objects.get(pk=lid)

    if request.method== "POST":

        if listing.owner == user :
            try:
                b = Bid.objects.get(listing= listing)
                winner = b.bidder
                Listing.objects.filter(id= lid).update(winner= winner)
                Listing.objects.filter(id= lid).update(active=False)
                comments = listing.comments.all()
                m = listing.initialbid + 0.1
                bids = Bid.objects.all()
                try:
                     bid = Bid.objects.get(listing= listing)
                     mm = bid.value + 0.1
                except Bid.DoesNotExist:
                     mm = None
    
                return render (request, "auctions/listing.html",{
                     "list" : listing,
                     "comments" : comments,
                     "m" : m,
                     "mm" : mm,
                     "sold" : "Your listing has been sold successfully"
       
                })
            
            except Bid.DoesNotExist:
                winner = None
                Listing.objects.filter(id= lid).update(active=False)
                comments = listing.comments.all()
                m = listing.initialbid + 0.1
                bids = Bid.objects.all()
                try:
                     bid = Bid.objects.get(listing= listing)
                     mm = bid.value + 0.1
                except Bid.DoesNotExist:
                     mm = None

            try:
                w = WatchList.objects.get(user= request.user)
                ww = w.listings.all()
            except WatchList.DoesNotExist:
                ww = []
            except TypeError:
                ww = []
    
                return render (request, "auctions/listing.html",{
                     "list" : listing,
                     "comments" : comments,
                     "m" : m,
                     "mm" : mm,
                     "closed" : "Your listing has been closed successfully.",
                     "ww" : ww
       
                })

@login_required
def remove (request, lid):
    if request.method== "POST":
        user = request.user
        listing = Listing.objects.get(pk=lid)
        watch = WatchList.objects.get(user= user)
        watch.listings.remove(listing)
            
        
        comments = listing.comments.all()
        m = listing.initialbid + 0.1
        bids = Bid.objects.all()
        try:
             bid = Bid.objects.get(listing= listing)
             mm = bid.value + 0.1
        except Bid.DoesNotExist:
             mm = None
        
        try:
             w = WatchList.objects.get(user= request.user)
             ww = w.listings.all()
        except WatchList.DoesNotExist:
             ww = []
        except TypeError:
             ww = []
    
    
        return render (request, "auctions/listing.html",{
             "list" : listing,
             "comments" : comments,
             "m" : m,
             "mm" : mm,
             "rm" : "The listing has been removed from your Watchlist.",
             "ww" : ww
       
            })

        
        

        


