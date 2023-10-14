from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI

from config import CHAT_MODEL
from tools.restaurant_menu_search_tool import RestaurantMenuSearchTool
from tools.google_maps_search_tool import GoogleMapsSearchTool


class Agent:

    def __init__(self):
        self.llm = ChatOpenAI(temperature=0, model_name=CHAT_MODEL)
        self.agent = self.create_agent()

    def create_agent(self):
        tools = [GoogleMapsSearchTool(), RestaurantMenuSearchTool()]
        return initialize_agent(
            tools, self.llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
        )

    def run_agent(self, prompt):
        response = self.agent.run(prompt)
        print(response)
        return response
