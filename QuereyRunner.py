from yelpFetcher import YelpRestaurantFetcher

def sort_restaurants(restaurants, past_choices, rating_weight=0.5, choice_weight=0.5):
    # Sort the restaurants based on a combination of ratings, number of reviews, and past choices
    for restaurant in restaurants:
        restaurant["score"] = restaurant["rating"] * rating_weight + restaurant["review_count"] * (1 - rating_weight)
        if restaurant["name"] in past_choices:
            restaurant["score"] += past_choices[restaurant["name"]] * choice_weight
    sorted_restaurants = sorted(restaurants, key=lambda x: x["score"], reverse=True)
    return sorted_restaurants

def combine_restaurants(yelp_table, google_table):
    # Combine the restaurants based on a combination of ratings, number of reviews, and past choices
    combined_restaurants = []
    for yelp_record in yelp_table:
        found = False
        for google_record in google_table:
            if yelp_record['name'] == google_record['name']:
                combined_record = {
                    'name': yelp_record['name'],
                    'review_count': yelp_record['review_count'] + google_record['review_count'],
                    'image_url': yelp_record['image_url'],
                    'yelp_rating': yelp_record['rating'],
                    'google_rating': google_record['rating'],
                }
                combined_restaurants.append(combined_record)
                found = True
                break
        if not found:
            combined_restaurants.append(yelp_record)
    return combined_restaurants


yelpAPIkey = 'MikZl0KXOKRhZqwYd8AtnciOlMvglph4ySAlVIWManM985WwztK3R-7vKi-WRUxu0Bbuxqy4Ml41iHcaN1PgSyf5S59cvTTogJfeZeUnH_h9UVvWvlxZ8D9SHa_dY3Yx'
yelpFetcher = YelpRestaurantFetcher(yelpAPIkey)

yelp_restaurants = yelpFetcher.fetch("Atlanta", "GA")
google_restaurants = yelpFetcher.fetch("Atlanta", "GA")


yelp_restaurants = sort_restaurants(yelp_restaurants, {}, 0.5, 0.5)
google_restaurants = sort_restaurants(google_restaurants, {}, 0.5, 0.5)

combined_restaurants = combine_restaurants(yelp_restaurants, google_restaurants)
print(combined_restaurants)