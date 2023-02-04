from yelpFetcher import YelpRestaurantFetcher

def sort_restaurants(restaurants, past_choices, rating_weight=0.5, choice_weight=0.5):
    # Sort the restaurants based on a combination of ratings, number of reviews, and past choices
    for restaurant in restaurants:
        restaurant["score"] = restaurant["rating"] * rating_weight + restaurant["review_count"] * (1 - rating_weight)
        if restaurant["name"] in past_choices:
            restaurant["score"] += past_choices[restaurant["name"]] * choice_weight
    sorted_restaurants = sorted(restaurants, key=lambda x: x["score"], reverse=True)
    return sorted_restaurants



yelpAPIkey = 'MikZl0KXOKRhZqwYd8AtnciOlMvglph4ySAlVIWManM985WwztK3R-7vKi-WRUxu0Bbuxqy4Ml41iHcaN1PgSyf5S59cvTTogJfeZeUnH_h9UVvWvlxZ8D9SHa_dY3Yx'
yelpFetcher = YelpRestaurantFetcher(yelpAPIkey)
yelpRestaurants = yelpFetcher.fetch('Dothan', 'AL')

tempRestaurants = sort_restaurants(yelpRestaurants, {}, 0.5, 0.5)
print(tempRestaurants)