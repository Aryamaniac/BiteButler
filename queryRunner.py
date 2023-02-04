import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
#from firebase import Firebase

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
    
    def combine_restaurants(self, yelp_table, google_table, trip_table):
        # Combine the restaurants based on a combination of ratings, number of reviews, and past choices
        combined_restaurants = []
        for yelp_record in yelp_table:
            found = False
            for google_record in google_table:
                for trip_record in trip_table:
                    if yelp_record['name'] == google_record['name'] and yelp_record['name'] == trip_record['name']:
                        combined_record = {
                            'name': yelp_record['name'],
                            'yelp_review_count': yelp_record['review_count'],
                            'google_review_count': google_record['review_count'],
                            'trip_review_count': trip_record['review_count'],
                            'image_url': yelp_record['image_url'],
                            'yelp_rating': yelp_record['rating'],
                            'google_rating': google_record['rating'],
                            'trip_rating': trip_record['rating'],
                        }
                        combined_restaurants.append(combined_record)
                        found = True
                        break
            if not found:
                combined_restaurants.append(yelp_record)
        return combined_restaurants
        
    def main(self):
        """takes input from user, runs yelp query, sorts restaurants, and prints results
        """
        self.get_input()
        yelpRestaurants = self.run_yelp_query()
        googleRestaurants = self.run_google_query()
        tripRestaurants = self.run_trip_query()
        print(tripRestaurants)
        #combined = self.combine_restaurants(yelpRestaurants, googleRestaurants)
        print("###############################################################################################################")
        #print(combined)
        print("###############################################################################################################")

        ##sortedRestaurants = self.sort_restaurants(combined, {})
        ##for restaurant in sortedRestaurants:
          ##  print(restaurant["name"], restaurant["score"])
        #self.write_restaurants(sortedRestaurants)
        print("done")

temp = queryRunner()
temp.main()