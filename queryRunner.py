import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
import pandas as pd

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
        googleFetcher = googleRestaurantFetcher("AIzaSyDuO8eQwp5dFa3Ju__y9XsZE7Kw0wrqGNg")
        googleRestaurants = googleFetcher.fetch(self.city, self.state)
        return googleRestaurants
    
    def run_trip_query(self):
        from tripFetcher import TripAdvisorRestaurantFetcher
        tripFetcher = TripAdvisorRestaurantFetcher()
        tripRestaurants = tripFetcher.fetch(self.city)
        return tripRestaurants
    
    def sort_restaurants(self, restaurants):
        # Sort the restaurants based on a combination of ratings, number of reviews, and past choices
        for restaurant in restaurants:
            print(restaurant)
            total_reviews = restaurant["yelp_review_count"] + restaurant["google_review_count"] + restaurant["trip_review_count"]
            restaurant["score"] = restaurant["rating"] * restaurant["review_count"] / total_reviews
        sorted_restaurants = sorted(restaurants, key=lambda x: x["score"], reverse=True)
        return sorted_restaurants
    
    def write_restaurants(self, restaurants):
        ref = db.reference("/restaurants")
        ref.set(restaurants)
    
    #take in 3 lists and turn them into dataframes
    def listToDataframeAndMerge(self, yelp_list, tripadvisor_list, google_list):
        #print(yelp_list)
        yframe = pd.DataFrame(yelp_list)
        tframe = pd.DataFrame(tripadvisor_list)
        gframe = pd.DataFrame(google_list)
        cframe = yframe.merge(tframe, on = "name", how = "outer")
        fframe = cframe.merge(gframe, on = "name", how = "outer")
        #fframe = fframe.dropna()
        for col in fframe.columns:
            print(col)
        print(fframe.head)
        
    def combine_restaurant_lists(self, yelp_list, tripadvisor_list, google_list):
        combined_list = []
        for yelp_item in yelp_list:
            for tripadvisor_item in tripadvisor_list:
                for google_item in google_list:
                    if yelp_item["name"] == tripadvisor_item["name"] == google_item["name"]:
                        combined_item = {"name": yelp_item["name"],
                                        "yelp_rating": yelp_item["rating"],
                                        "tripadvisor_rating": tripadvisor_item["rating"],
                                        "google_rating": google_item["rating"],
                                        "yelp_review_count": yelp_item["review_count"],
                                        "tripadvisor_review_count": tripadvisor_item["review_count"],
                                        "google_review_count": google_item["review_count"],
                                        "image_url": yelp_item.get("image_url", google_item.get("image_url", None))}
                        combined_list.append(combined_item)
        return combined_list
        
    def main(self):
        """takes input from user, runs yelp query, sorts restaurants, and prints results
        """
        self.get_input()
        yelpRestaurants = self.run_yelp_query()
        googleRestaurants = self.run_google_query()
        tripRestaurants = self.run_trip_query()
        self.listToDataframeAndMerge(yelpRestaurants, tripRestaurants, googleRestaurants)
        #combined = self.combine_restaurant_lists(yelpRestaurants, tripRestaurants, googleRestaurants)
        print(combined)
        for elem in combined:
            print(elem)
        sortedRestaurants = self.sort_restaurants(combined)
        for restaurant in sortedRestaurants:
            print(restaurant["name"], restaurant["score"])
        #self.write_restaurants(sortedRestaurants)
        print("done")

temp = queryRunner()
temp.main()
