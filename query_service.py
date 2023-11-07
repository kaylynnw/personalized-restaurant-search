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
    as an array with the a json object with the following fields: restaurant_name and restaurant_menu
    
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
    For each restaurant in the list: 
    1. You will then learn what the menu says. 
    2. Based off of the menu content, is this menu compatible with your dietary restrictions? 
    Answer as succinctly as possible.
    
    ### Desired format of response
    an array with the a json object with the following fields: restaurant_name (string), is_compatible (boolean), details (string)
    
    ### Restaurant Info
    The restaurant url included in the following: {restaurant_details}
    
    ### Your dietary restrictions
    Your dietary restrictions are {dietary_restrictions}
    """


class QueryService:

    def __init__(self):
        self.restaurant_retrieval_agent = RestaurantRetrievalAgent()
        self.menu_parse_agent = MenuParseAgent()

    def query(self, address: str, dietary_restrictions: str):
        async def event_stream():
            restaurant_retrieval_prompt = create_restaurant_retrieval_prompt(address)
            try:
                restaurant_info = self.restaurant_retrieval_agent.run_agent(restaurant_retrieval_prompt)
                yield {"data": f"\"{{ {restaurant_info} }}\""}
                print(restaurant_info)
            except Exception as e:
                print(f"**************Error:****************** \n {e}")
                yield {"data": {"error": str(e)}}
                return
            # answer = ''
            #
            # for restaurant in restaurants:
            #     restaurant_string = f"{restaurant}"
            #     try:
            #         answer += self.menu_parse_agent.run_agent(
            #             create_menu_parse_prompt(restaurant_string, dietary_restrictions))
            #         yield {"data": {"restaurant": restaurant_string, "menu": answer}}
            #     except Exception as e:
            #         print(f"ERROR --- address:{address} --- {e} ")

        return event_stream()
