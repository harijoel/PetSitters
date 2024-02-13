from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User, PetSitter, Review
from django.db.models import Q
from django.db.models import Avg
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse


def index(request):
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse("login"))
    return render(request, "petsitters/index.html")

def search(request):
    return HttpResponse("search page")
    if request.method == "GET":
        query = request.GET["q"]
        results = PetSitter.objects.filter(Q(name__icontains=query) | Q(lastname__icontains=query) | Q(city__icontains=query))
        numres = len(results)
        return render(request, "petsitters/search.html", {"results": results, "numres": numres})
def petsitter(request, petsitter_id):
    return HttpResponse("petsitter page")
    # Fetch petsitter profile
    try:
        petsitter = PetSitter.objects.get(petsitter_id=petsitter_id)
    except ObjectDoesNotExist:
        return render(request, "petsitters/error.html")
    user = request.user
    
    ## Before adding a new review,
    ## make sure to delete the previous one (if any)
    
    # Fetch user's  review (if any)
    try:
        userrev = user.reviews.get(petsitter=petsitter)
    except:
        userrev = None
        
    if request.method == "POST":
        # Collect form data (rating & comment)
        try:
            rating = int(request.POST["rating"])
        except:
            return render(request, "petsitters/error.html", {"message": "invalid rating"})
        comment = request.POST["comment"]
        if len(comment) < 3 or len(comment) > 250:
            return render(request, "petsitters/error.html", {"message": "invalid comment length"})
        
        # Delete previous review (if any)
        if userrev:
            userrev.delete()
            
        ## Insert review
        review = Review(user=user, petsitter=petsitter, comment=comment, rating=rating)
        review.save()
        return HttpResponseRedirect(reverse("petsitter", args=(petsitter.pk, )))
        
    # GET request handle
    # Fetch reviews form database for display
    reviews = petsitter.reviews.all()
    rating_cnt = petsitter.reviews.all().count()
    rating_avg = petsitter.reviews.aggregate(average=Avg('rating'))["average"]
    bwstat = {"count": rating_cnt, "avg": rating_avg}
    rrange = [5, 4, 3, 2, 1]
    
    return render(request, "petsitters/petsitter.html", {
        "petsitter": petsitter, 
        "reviews": reviews, 
        "userrev": userrev, 
        "rrange": rrange,
        "bwstat": bwstat})

def userProfile(request, username):
    # User exists
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        message = "User not found"
        return render(request, "petsitters/error.html", {"message": message})
    
    # Fetch books where user commented
    userReviews = user.reviews.all()
    return render(request, "petsitters/user.html", {"userReviews": userReviews, "username": username})
    
    
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "petsitters/login.html", {
                "message": "Invalid Credentials"
            })
    # GET request handler
    return render(request, "petsitters/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["username"]
        confirmation = request.POST["confirmation"]
        terms = True #request.POST["terms"]
        failed = False
        # Username was submitted
        if not username:
            message = "You must provide a username"
            failed = True
        # Only letters and numbers
        if not username.isalnum():
            message = "Username must only contain letters or numbers"
            failed = True
        # Username length fits
        if not (3 <= len(username) <= 12):
            message = "Username must be between 3 and 12 characters in length"
            failed = True
        # Password was submitted
        if not password:
            message = "You must provide a password"
            failed = True
        # Ensure password matches confirmation
        if password != confirmation:
            message = "Passwords do not match"
            failed = True
        # Password length fits
        if not (3 <= len(password) <= 12) or not (3 <= len(confirmation) <= 12):
            message = "Password must be between 3 and 12 characters in length"
            failed = True
        
        #Terms were accepted
        if not terms:
            message = "You must accept the terms"
            failed = True
        if failed:
            return render(request, "petsitters/register.html", {"message": message})
        # Attempt to create new user / #Username is not taken
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except IntegrityError:
            message = "Username already taken."
            failed = True
        if failed:
            return render(request, "petsitters/register.html", {"message": message})
        
        # Login if passed all filters
        login(request, user)
        # Redirect to login
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "petsitters/register.html")