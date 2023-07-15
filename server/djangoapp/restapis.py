import requests
import json
import os
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import NaturalLanguageUnderstandingV1, Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    print("json_result")
    print(json_result[0])
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
            print(dealer_obj)

    return results


def get_dealer_by_id(url, state):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=kwargs["id"])
    print("json_result")
    print(json_result[0])
    if json_result:
        # Get the row list in JSON as dealers
        dealer_doc = json_result[0]

        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                               id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                               short_name=dealer_doc["short_name"],
                               st=dealer_doc["st"], zip=dealer_doc["zip"])
        results.append(dealer_obj)
        print(dealer_obj)

    return results


def get_dealers_by_state(url, state):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, st=state)
    print("json_result")
    print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        print(dealers)
        # For each dealer object
        for dealer in dealers:
            print(dealer['short_name'])
            # Get its content in `doc` object
            # dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
            print(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id, api_key=None):
    results = []
    # Call get_request with a URL parameter
    if api_key:
        json_result = get_request(
            url, id=dealer_id, auth=HTTPBasicAuth('apikey', api_key))
    else:
        json_result = get_request(url, id=dealer_id)
    # print(json_result['data']['docs'])
    # print ("json_result")
    # print(json_result[0])
    reviews = json_result['data']['docs']
    # print(type(reviews))
    # print(reviews)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result['data']['docs']
        # For each dealer object
        for review in reviews:
            print(review)
            # Get its content in `doc` object
            # review_doc = review["doc"]
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=review['dealership'], name=review['name'], purchase=review['purchase'],
                                      review=review['review'], purchase_date=review['purchase_date'],
                                      car_make=review['car_make'], car_model=review['car_model'], car_year=review['car_year'],
                                      sentiment=None, id=review['id'])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
            print(review_obj)
        # review_obj = results[0]
        # sentiment = analyze_review_sentiments(review_obj.review)
        # print(sentiment)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    # - Call get_request() with specified arguments
    api_key = os.environ['API_KEY']
    print(api_key)
    url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/7c29c038-64fb-4ffc-90c5-26c180368811'

    # response = get_request(url, text=text, version='2022-08-10',
    #                        features='sentiment', headers={'Content-Type': 'application/json'},
    #                        auth=HTTPBasicAuth('apikey', api_key))

    # print("respose")
    # print(response)

    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url(url)
    # response = natural_language_understanding.analyze(
    #     url='https://en.wikipedia.org/wiki/Emmanuel_Macron',
    #     features=Features(sentiment=SentimentOptions(targets=['France']))).get_result()
    response = natural_language_understanding.analyze(text=text, language="en", features=Features(
        sentiment=SentimentOptions(targets=[text]))).get_result()
    # response = json.dumps(response, indent=2)

    label = response['sentiment']['document']['label']
    # label = response['sentiment']['targets']['label']
    # print("sentiment: {}".format(label))
    return label


# - Get the returned sentiment label such as Positive or Negative
