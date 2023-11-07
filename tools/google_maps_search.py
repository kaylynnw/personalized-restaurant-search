import requests


def get_lat_lng_from_address(api_key, address):
    endpoint_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {'address': address, 'key': api_key}
    response = requests.get(endpoint_url, params=params)
    result = response.json()
    if result['status'] != 'OK':
        raise Exception(f"ERROR: {result['status']} - Could not retrieve the latitude and/or longitude from given "
                        f"address {address}")
    location = result['results'][0]['geometry']['location']
    return location['lat'], location['lng']


def get_place_details(api_key, place_id):
    """
    Fetch detailed information for a place using Google's Place Details API.

    Parameters:
    - api_key (str): Your Google API key.
    - place_id (str): The Place ID of the desired place.

    Returns:
    - dict: Detailed place information.
    """
    endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {'place_id': place_id, 'key': api_key}
    response = requests.get(endpoint_url, params=params)
    result = response.json()
    if result['status'] != 'OK':
        raise Exception(f"ERROR: {result['status']} - Could not retrieve the place details")
    return result['result']


def find_nearby_restaurants(api_key, latitude, longitude, radius=500):
    """
    Fetch nearby restaurants using Google Places API and get additional
    details using Google's Place Details API.

    Parameters:
    - api_key (str): Your Google API key.
    - latitude (float): Latitude of the user's location.
    - longitude (float): Longitude of the user's location.
    - radius (int, optional): Search within a 'radius' from the user location. Default is 500 meters.

    Returns:
    - list: List of nearby restaurants and their website.
    """
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f"{latitude},{longitude}",
        'radius': radius,
        'type': 'restaurant',
        'key': api_key
    }
    response = requests.get(endpoint_url, params=params)
    results = response.json()
    if results['status'] != 'OK':
        raise Exception(f"ERROR: {results['status']} - Could not retrieve the nearby restaurants")

    restaurants = []
    for place in results['results']:
        name = place.get('name', 'Unknown Name')
        place_id = place.get('place_id', '')

        details = get_place_details(api_key, place_id)
        website = details.get('website', 'Website not available') if details else 'Website not available'

        restaurants.append({
            'name': name,
            'website': website
        })
    return restaurants


def google_maps_search(api_key, address, radius=500):
    """
    Unified function to retrieve nearby restaurants for a given address using Google Maps APIs.

    Parameters:
    - api_key (str): Your Google API key.
    - address (str): The address to search nearby restaurants.
    - radius (int, optional): Search within a 'radius' from the address. Default is 500 meters.

    Returns:
    - list: List of nearby restaurants and their website.
    """
    latitude, longitude = get_lat_lng_from_address(api_key, address)

    restaurants = find_nearby_restaurants(api_key, latitude, longitude, radius)
    if not restaurants:
        return "Unable to find nearby restaurants."

    # Formulate a single string with search results
    search_results_str = "Nearby Restaurants:\n"
    for i, restaurant in enumerate(restaurants, 1):
        search_results_str += (
            f"{i}. Name: {restaurant['name']}\n"
            f"   Website: {restaurant['website']}\n"
            "---------------------\n"
        )

    return search_results_str.rstrip('-')
