from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from tools.restaurant_menu_search import get_likely_menu


class RestaurantMenuSearchInput(BaseModel):
    url: str = Field(description="website to scrape")


class RestaurantMenuSearchTool(BaseTool):
    name = "RestaurantMenuSearch"
    description = "retrieves information about a website that will be helpful to find the menu"
    args_schema: Type[RestaurantMenuSearchInput] = RestaurantMenuSearchInput

    def _run(
            self,
            url: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return get_likely_menu(url)

    async def _arun(
            self,
            url: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        return get_likely_menu(url)
