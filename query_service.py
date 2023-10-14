import os

from dotenv import load_dotenv

from agent import Agent
from models.question import Question

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')


def create_prompt(user_address: str):
    return f"Find restaurants near {user_address} using Google Maps. " \
           f"The api_key is {GOOGLE_MAPS_API_KEY}"


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
