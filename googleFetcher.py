import requests
import json

class googleRestaurantFetcher:

    def __init__(self, api_key):
        self.api_key = api_key
    # Specify the city and state

    def fetch(self, city, state):
        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants+in+{city},+{state}&key={self.api_key}"

        # Send the API request and get the response
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = json.loads(response.text)

            # Initialize the list of restaurants
            restaurants = []
            
            #print(data)
            #print("HERE$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

            # Loop through the list of restaurants
            for result in data["results"]:
                # Get the restaurant information
                name = result["name"]
                rating = result.get("rating", 0)
                review_count = result.get("user_ratings_total", 0)
                image_url = result.get("icon", "")

                # Store the restaurant information in a dictionary
                restaurant_info = {
                    "name": name,
                    "rating": rating,
                    "review_count": review_count,
                    "image_url": image_url
                }

                # Add the dictionary to the list of restaurants
                restaurants.append(restaurant_info)

            # Return the list of restaurants
            return restaurants
        else:
            # Raise an error
            raise Exception(f"Request failed with status code: {response.status_code}")
