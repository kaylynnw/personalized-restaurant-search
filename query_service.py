import ast
import json
import os

from dotenv import load_dotenv

from menu_parse_agent import MenuParseAgent
from restaurant_retrieval_agent import RestaurantRetrievalAgent

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')


def create_restaurant_retrieval_prompt(user_address: str):
    return f"""        
    ### Goal
    You are trying to find the menus of the closest restaurants nearby.
    
    # This is the process you will follow to find this information.
    1. Use google maps to search for the nearby restaurants to your current location. 
    You will find a list of restaurants with their website.
    2. You will use the restaurant website to find information about the menu.
    3. You will use the information about the menu to return the link to the restaurants' menu.
    
    ### Return your response 
    as an array with a json object with the following fields: restaurant_name, restaurant_menu, latitude, and longitude
    
    ### To use google maps
    api_key = {GOOGLE_MAPS_API_KEY}
    
    ### Current Location
    Your current location is {user_address}
    """


def create_menu_parse_prompt(restaurant_details: str, dietary_restrictions: str):
    return f"""    
    ### Goal
    You are trying to find restaurants that are compatible with your dietary restrictions.
    
    ### This is the process you will follow to find this information.
    1. Based off of the menu content, is this menu compatible with your dietary restrictions? 
    
    ### Example Answer Format
    Jitterbug Cafe: 
    - Yes, I think this place looks great! 
    - The Jitterbug Cafe offers a BLT bagel sandwich, overnight oats, and muffins. All great options for a vegetarian. 
    
    ### Example Answer Format
    Snack'ums: 
    - Not recommended. 
    - Snack'ums offers complimentary peanuts to every guest. So, I don't think this would be a good place for your severe peanut allergy.  
    
    ### Restaurant Info
    The restaurant url included in the following: {restaurant_details}
    
    ### Your dietary restrictions
    Your dietary restrictions are {dietary_restrictions}
    """


class QueryService:

    def __init__(self):
        self.restaurant_retrieval_agent = RestaurantRetrievalAgent()
        self.menu_parse_agent = MenuParseAgent()

    async def query(self, address: str, dietary_restrictions: str):
        restaurant_retrieval_prompt = create_restaurant_retrieval_prompt(address)
        try:
            restaurant_info_string = self.restaurant_retrieval_agent.run_agent(restaurant_retrieval_prompt)
            restaurant_info_dict = ast.literal_eval(restaurant_info_string)
            labelled_restaurant_info = {"restaurant_info": restaurant_info_dict}
            yield f"data: {json.dumps(labelled_restaurant_info)}\n\n"
        except Exception as e:
            print(f"**************Error:****************** \n {e}")
            yield f"data: {json.dumps({'error': 'Experienced an error while retrieving restaurants and their menus'})}\n\n"
            return

        for restaurant in restaurant_info_dict:
            print(restaurant)
            try:
                recommendations: str = self.menu_parse_agent.run_agent(
                    create_menu_parse_prompt(restaurant, dietary_restrictions))
                labelled_recommendations = {"recommendations": recommendations}
                # yield f"data: {json.dumps(labelled_recommendations)}\n\n"
            except Exception as e:
                print(f"**************Error:****************** \n {e}")
                yield f"data: {json.dumps({'error': 'Experienced an error while analyzing menu'})}\n\n"
        return
