import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from firebase import Firebase

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://bitebutler-e193b-default-rtdb.firebaseio.com/'})


class queryRunner:
    def __init__(self):
        self.city = None
        self.state = None
        self.yelpAPIkey = 'MikZl0KXOKRhZqwYd8AtnciOlMvglph4ySAlVIWManM985WwztK3R-7vKi-WRUxu0Bbuxqy4Ml41iHcaN1PgSyf5S59cvTTogJfeZeUnH_h9UVvWvlxZ8D9SHa_dY3Yx'
        self.yelpRestaurants = None

    def get_input(self):
        ref = db.reference("/locations")
        self.city = ref.get()['city']
        self.state = ref.get()['state']

    def run_yelp_query(self):
        from yelpFetcher import YelpRestaurantFetcher
        yelpFetcher = YelpRestaurantFetcher(self.yelpAPIkey)
        yelpRestaurants = yelpFetcher.fetch(self.city, self.state)
        return yelpRestaurants
    
    def run_google_query(self):
        from googleFetcher import googleRestaurantFetcher
        googleFetcher = googleRestaurantFetcher(self.googleAPIkey)
        googleRestaurants = googleFetcher.fetch(self.city, self.state)
        return googleRestaurants

    def sort_restaurants(self, restaurants, past_choices, rating_weight=0.5, choice_weight=0.5):
        # Sort the restaurants based on a combination of ratings, number of reviews, and past choices
        for restaurant in restaurants:
            restaurant["score"] = restaurant["rating"] * rating_weight + restaurant["review_count"] * (1 - rating_weight)
            if restaurant["name"] in past_choices:
                restaurant["score"] += past_choices[restaurant["name"]] * choice_weight
        sorted_restaurants = sorted(restaurants, key=lambda x: x["score"], reverse=True)
        return sorted_restaurants
    
    def write_restaurants(self, restaurants):
        ref = db.reference("/restaurants")
        ref.set(restaurants)
        
    def main(self):
        """takes input from user, runs yelp query, sorts restaurants, and prints results
        """
        self.get_input()
        yelpRestaurants = self.run_yelp_query()
        sortedRestaurants = self.sort_restaurants(yelpRestaurants, {})
        for restaurant in sortedRestaurants:
            print(restaurant["name"], restaurant["score"])
        self.write_restaurants(sortedRestaurants)
        print("done")

temp = queryRunner()
temp.main()