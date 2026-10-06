# Search planning agent

from pydantic import BaseModel, Field
from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI
import os
from dotenv import load_dotenv
load_dotenv(override=True)

or_base_url = os.getenv('open_router_base_url')
or_api_key = os.getenv('openrouter_api_key')
Model_Name = "nvidia/nemotron-3.5-lightning:free"

or_client = AsyncOpenAI(base_url=or_base_url, api_key=or_api_key)
or_model = OpenAIChatCompletionsModel(model = Model_Name, openai_client=or_client)

HOW_MANY_SEARCHES:int = 1

INSTRUCTIONS = f"""
You are a research assistant. Given a user query, come up with the web search to perform to best answer the query. Output {HOW_MANY_SEARCHES} term to query for.
"""

class WebSearchItem(BaseModel):
    reason : str = Field(description = "Your reasoning for why this search is important to the query.")
    query : str = Field(description = "The search term to use for the web search.")

class WebSearchPlan(BaseModel):
    searches : list[WebSearchItem] = Field(description="List of web searches to perform to best answer the query")

planner_agent = Agent(name= "Planner agent", instructions = INSTRUCTIONS, model = or_model, output_type=WebSearchPlan)