from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarMake, CarDealer
from .restapis import get_dealers_from_cf, get_dealer_by_id, get_dealers_by_state, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from random import randint
import os

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def add_review(request, dealer_id):
    print("Veio add review")
    context = {}
    context['dealer_id'] = dealer_id
    if request.method == "GET":
        url_get_dealers = os.environ['URL_GET_DEALERS']
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        dealer = get_dealer_by_id(url=url_get_dealers, id=dealer_id)
        # print(dealer)
        context['dealer_name'] = dealer.full_name
        context['cars_list'] = list(cars)
        if request.user.is_authenticated:
            return render(request, 'djangoapp/add_review.html', context)
        else:
            print("user not auth")
            return redirect('djangoapp:login')
    elif request.method == "POST":
        print(request.POST)
        car = CarModel.objects.get(pk=request.POST['car'])
        print(car.make.description)
        review = {}
        review['review'] = request.POST['review_text']
        review['name'] = request.user.first_name + " " + request.user.last_name
        review['dealership'] = dealer_id
        review['purchase'] = False
        if 'purchasecheck' in request.POST.keys():
            review['purchase'] = True
        review['car_model'] = car.name
        review['car_make'] = car.make.name
        review['purchase_date'] = request.POST['purchasedate']
        review['car_year'] = car.year
        json_payload = {}
        json_payload['review'] = review
        # print(json_review)
        url_post_review = os.environ['URL_POST_REVIEW']
        response = post_request(url_post_review, json_payload, dealer_id=dealer_id)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)


# Create an `about` view to render a static about page
def about(request):
    ''' renders the about '''
    context = {}
    return render(request, 'djangoapp/about.html', context)
# ...


# Create a `contact` view to return a static contact page
def contact(request):
    ''' Renders the contact '''
    context = {}
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request


def login_request(request):
    print("Entrou login request")
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships


def get_dealerships(request):
    context = {}
    if request.method == "GET":
        #url = "https://us-south.functions.appdomain.cloud/api/v1/web/3359b9cf-db9c-4cef-8e9b-c4855d4a5213/dealership-package/get-dealership"
        url = os.environ['URL_GET_DEALERS']
        # Get dealers from the URL
        # dealerships = get_dealers_from_cf(url)
        dealerships = get_dealers_from_cf(url)
        print(len(dealerships))
        # Concat all dealer's short name
        context['dealership_list'] = dealerships
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        # return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    url_get_dealers = os.environ['URL_GET_DEALERS']
    dealer = get_dealer_by_id(url=url_get_dealers, id=dealer_id)
    # print(dealer)
    context['dealer_name'] = dealer.full_name
    context['dealer_id'] = dealer_id
    # url = "https://us-south.functions.appdomain.cloud/api/v1/web/3359b9cf-db9c-4cef-8e9b-c4855d4a5213/dealership-package/get-reviews"
    url = os.environ['URL_GET_REVIEWS']
    reviews = get_dealer_reviews_from_cf(url, dealer_id)
    context['reviews_list'] = reviews
    # reviewers_names = '; '.join([str(review) for review in reviews])
    # return HttpResponse(reviewers_names)
    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
