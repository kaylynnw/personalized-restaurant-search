import os

from dotenv import load_dotenv

from agent import Agent
from models.question import Question

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')


def create_prompt(user_address: str):
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


class QueryService:

    def __init__(self):
        self.agent = Agent()

    def query(self, question: Question):
        prompt = create_prompt(question.address)
        try:
            answer = self.agent.run_agent(prompt)
        except Exception as e:
            print(f"ERROR --- address:{question.address} --- {e} ")
            raise e
        return answer
