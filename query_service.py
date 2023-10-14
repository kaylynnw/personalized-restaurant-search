import os

from dotenv import load_dotenv

from menu_parse_agent import MenuParseAgent
from models.question import Question
from restaurant_retrieval_agent import RestaurantRetrievalAgent
from image_menu_search import image_menu_search

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')


def create_restaurant_retrieval_prompt(user_address: str):
    return f"""
    # Goal
    You are trying to find the menus of the closest restaurants nearby.
    
    # This is the process you will follow to find this information.
    1. Use google maps to search for the nearby restaurants to your current location. 
    You will find a list of restaurants with their website.
    2. You will use the restaurant website to find information about the menu.
    3. You will use the information about the menu to return the link to the restaurants' menu.
    
    # To use google maps
    api_key = {GOOGLE_MAPS_API_KEY}
    
    # Current Location
    Your current location is {user_address}
    """


def create_menu_parse_prompt(restaurant_details: str, dietary_restrictions: str):
    return f"""
    # Goal
    You are trying to find restaurants that are compatible with your dietary restrictions.
    
    # This is the process you will follow to find this information.
    For each restaurant in the list: 
    1. You will then learn what the menu says. 
    2. Based off of the menu content, is this menu compatible with your dietary restrictions? 
    Answer as succinctly as possible, but make sure to include the restaurant name. 
    
    # Restaurant Info
    The restaurant url included in the following: {restaurant_details}
    
    # Your dietary restrictions
    Your dietary restrictions are {dietary_restrictions}
    """

def create_menu_image_parse_prompt(restaurant_details: str, dietary_restrictions: str):
    return f"""
    # Goal
    You are trying given a restaurant menu, you are trying to find out if the menu is compatible with your dietary restrictions.

    # This is the process you will follow to find this information.
    For each restaurant in the list:
    1. You will then learn what the menu says.
    2. Based off of the menu content, is this menu compatible with your dietary restrictions?
    Answer as succinctly as possible, but make sure to include the restaurant name.

    # Restaurant Info
    The restaurant menu included in the following: {restaurant_details}

    # Your dietary restrictions
    Your dietary restrictions are {dietary_restrictions}
    """

class QueryService:

    def __init__(self):
        self.restaurant_retrieval_agent = RestaurantRetrievalAgent()
        self.menu_parse_agent = MenuParseAgent()

    def query(self, question: Question):
        restaurant_retrieval_prompt = create_restaurant_retrieval_prompt(question.address)
        try:
            restaurant_info = self.restaurant_retrieval_agent.run_agent(restaurant_retrieval_prompt)
            restaurants = restaurant_info.strip().split('\n')
            answer = ''

            for restaurant in restaurants:
                restaurant_string = f"{restaurant}"
                try:
                    answer += self.menu_parse_agent.run_agent(
                        create_menu_parse_prompt(restaurant_string, question.dietaryRestrictions))
                except Exception as e:
                    print(f"ERROR --- address:{question.address} --- {e} ")
        except Exception as e:
            print(f"ERROR --- address:{question.address} --- {e} ")
            raise e
        return answer


class ImageQueryService:

    def __init__(self):
        self.restaurant_retrieval_agent = RestaurantRetrievalAgent()
        self.menu_parse_agent = MenuParseAgent()

    def query(self, image_path, question: Question):
        try:
            restaurant_info = image_menu_search(image_data=image_path)
            restaurants = restaurant_info.strip().split('\n')
            answer = ''

            for restaurant in restaurants:
                restaurant_string = f"{restaurant}"
                try:
                    answer += self.menu_parse_agent.run_agent(
                        create_menu_image_parse_prompt(restaurant_string, question.dietaryRestrictions))
                except Exception as e:
                    print(f"ERROR --- address:{question.address} --- {e} ")
        except Exception as e:
            print(f"ERROR --- address:{question.address} --- {e} ")
            raise e
        return answer
