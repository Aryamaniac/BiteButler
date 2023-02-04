import requests
import json

class YelpRestaurantFetcher:
    """This class will serve to fetch information from Yelp's Fusion API
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'Authorization': 'Bearer ' + api_key,
        }

    def fetch(self, city, state):
        """Fetches restaurants from Yelp API

        Args:
            city (string): city to search
            state (string): state the city is in

        Returns:
            list: resturant names, ratings, review counts, and image urls
        """
        parameters = {
            'location': f"{city}, {state}",
            'term': 'restaurants',
        }

        #call the Yelp API
        response = requests.get('https://api.yelp.com/v3/businesses/search', headers=self.headers, params=parameters)

        #if the response is good, return the data
        if response.status_code == 200:
            data = json.loads(response.text)
            return [{
                'name': restaurant['name'],
                'rating': restaurant['rating'],
                'review_count': restaurant['review_count'],
                'image_url': restaurant['image_url']
            } for restaurant in data['businesses']]
        else:
            return None
