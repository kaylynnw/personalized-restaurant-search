from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from tools.parse_menu import parse_menu_text


class ParseMenuToolInput(BaseModel):
    url: str = Field(description="link to the menu")


class ParseMenuTool(BaseTool):
    name = "ParseMenu"
    description = "learn about what the menu says"
    args_schema: Type[ParseMenuToolInput] = ParseMenuToolInput

    def _run(
            self,
            url: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return parse_menu_text(url)

    async def _arun(
            self,
            url: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        return parse_menu_text(url)
