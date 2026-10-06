# Web research/search agent

from agents import Agent, ModelSettings,AsyncOpenAI, OpenAIChatCompletionsModel

from dotenv import load_dotenv
import os
from serpapi_search_tools import web_search

load_dotenv(override = True)
or_base_url = os.getenv('open_router_base_url')
or_api_key = os.getenv('openrouter_api_key')
Model_Name = "nvidia/nemotron-3.5-lightning:free"

or_client = AsyncOpenAI(base_url=or_base_url, api_key=or_api_key)
or_model = OpenAIChatCompletionsModel(model = Model_Name, openai_client=or_client)

serpapi_key = os.getenv("serpapi_api_key")
serp_websearch = web_search()

INSTRUCTIONS = """
You are a research assistant. Given a search term, you search the web for that term and produce a concise summary of the results. The summary must be 2-3 paragraphs and less than 300 words.
Capture the main points and be clear about it. Reply only with the summary.
"""

settings = ModelSettings(tool_choice="required")
tools = [serp_websearch]

search_agent = Agent(name="search agent", instructions=INSTRUCTIONS, tools=tools, model = or_model, model_settings=settings)