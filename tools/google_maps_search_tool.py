from tools.google_maps_search import google_maps_search
from langchain.tools import BaseTool, tool
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field


# Define input schema for better parameter understanding and validation
class GoogleMapsSearchInput(BaseModel):
    api_key: str = Field(description="API key for Google Maps")
    address: str = Field(description="Address to search restaurants at")


# Define the custom tool by subclassing the BaseTool class
class GoogleMapsSearchTool(BaseTool):
    name = "GoogleMapsSearch"
    description = "Performs a restaurant search on Google Maps using an API key and address"
    args_schema: Type[GoogleMapsSearchInput] = GoogleMapsSearchInput

    def _run(
            self,
            api_key: str,
            address: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return google_maps_search(api_key, address)

    async def _arun(
            self,
            api_key: str,
            address: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        # Asynchronous implementation of google_maps_search if desired/necessary
        # For simplicity, the sync version is used here
        return google_maps_search(api_key, address)
