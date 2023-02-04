import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from firebase import Firebase

cred = credentials.Certificate("serviceAccountKey.json")
#firebase_admin.initialize_app(cred, {'databaseURL': 'https://bitebutler-e193b-default-rtdb.firebaseio.com/'}) https://bitebutler-e193b.firebaseapp.com/
app = firebase_admin.initialize_app(cred)
firestore_client = firestore.client()
doc_ref = firestore_client.collection('locations')
print(f"tehdcoucment id is {doc_ref.id}")
# doc = doc_ref.get()
# print(f"The docutment is {doc.to_dict()}")

# ref = db.reference("/locations")
# print(ref.get())

#ref = db.reference("path/to/data")
#data = ref.get()

# data = db.collection(u"locations")
# docs = data.stream()

# for doc in docs:
#     print(f'{doc.id} => {doc.to_dict()}')

# print(data)

# config = {
#     "apiKey":  "AIzaSyAHQhCz26Et5hv21rekZrPc2mX8HQ4rYl0",

#     "authDomain": "bitebutler-e193b.firebaseapp.com",
#     "databaseURL": "https://bitebutler-e193b.web.app",

#   "storageBucket": "bitebutler-e193b.appspot.com",

# }

# firebase = Firebase(config)
# db = firebase.database()
# locations = db.child('locations').get()
# print(locations.val())

class queryRunner:
    def __init__(self):
        self.city = None
        self.state = None
        self.yelpAPIkey = 'MikZl0KXOKRhZqwYd8AtnciOlMvglph4ySAlVIWManM985WwztK3R-7vKi-WRUxu0Bbuxqy4Ml41iHcaN1PgSyf5S59cvTTogJfeZeUnH_h9UVvWvlxZ8D9SHa_dY3Yx'
        self.yelpRestaurants = None

    def get_input(self):
        self.city = input("Enter city: ")
        self.state = input("Enter state: ")

    def run_yelp_query(self):
        from yelpFetcher import YelpRestaurantFetcher
        yelpFetcher = YelpRestaurantFetcher(self.yelpAPIkey)
        yelpRestaurants = yelpFetcher.fetch(self.city, self.state)
        return yelpRestaurants
    
    def sort_restaurants(self, restaurants, past_choices, rating_weight=0.5, choice_weight=0.5):
        # Sort the restaurants based on a combination of ratings, number of reviews, and past choices
        for restaurant in restaurants:
            restaurant["score"] = restaurant["rating"] * rating_weight + restaurant["review_count"] * (1 - rating_weight)
            if restaurant["name"] in past_choices:
                restaurant["score"] += past_choices[restaurant["name"]] * choice_weight
        sorted_restaurants = sorted(restaurants, key=lambda x: x["score"], reverse=True)
        return sorted_restaurants
        
    def main(self):
        """takes input from user, runs yelp query, sorts restaurants, and prints results
        """
        self.get_input()
        yelpRestaurants = self.run_yelp_query()
        sortedRestaurants = self.sort_restaurants(yelpRestaurants, {})
        for restaurant in sortedRestaurants:
            print(restaurant["name"], restaurant["score"])

temp = queryRunner()
temp.main()