from apify_client import ApifyClient

class TripAdvisorRestaurantFetcher:
    def fetchItems(location):
        # Initialize the ApifyClient with your API token
        client = ApifyClient("apify_api_fSa4LhqHzlT0OtMzhB6dnDmt6WZKHH3QeBsQ")

        #location = "Atlanta"
        
        # Prepare the actor input
        run_input = {
            "locationFullName": location,
            "maxItems": 100,
            "maxReviews": 0,
            "includeAttractions": False,
            "includeRestaurants": True,
            "includeHotels": False,
            "includeTags": False,
            "includeReviews": False,
            "language": "en",
            "currency": "USD",
            "proxyConfiguration": { "useApifyProxy": True },
        }

        # Run the actor and wait for it to finish
        run = client.actor("maxcopell/tripadvisor").call(run_input=run_input)

        # Fetch and print actor results from the run's dataset (if there are any)
        restuarants = []
        print("Results:")
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            name = item['name']
            rating = item['rating']
            number_of_reviews = item['numberOfReviews']
            restuarants.append({'name': name, 'rating': rating, 'review_count': number_of_reviews})     
        return(restuarants)
    
    if __name__=="__main__":
        fetchItems("Atanta")
        
    
