from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from tools.beautiful_soup_loader import get_likely_menu


class BeautifulSoupLoaderInput(BaseModel):
    url: str = Field(description="website to scrape")


# Define the custom tool by subclassing the BaseTool class
class BeautifulSoupLoaderTool(BaseTool):
    name = "BeautifulSoupLoader"
    description = "retrieves information about a website that will be helpful to find the menu"
    args_schema: Type[BeautifulSoupLoaderInput] = BeautifulSoupLoaderInput

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
        # Asynchronous implementation of google_maps_search if desired/necessary
        # For simplicity, the sync version is used here
        return get_likely_menu(url)
