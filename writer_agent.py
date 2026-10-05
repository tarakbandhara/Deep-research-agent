# Report-writing agent

from pydantic import BaseModel, Field
from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI
import os
from dotenv import load_dotenv
load_dotenv(override=True)

gemini_base_url = os.getenv('gemini_base_url')
gemini_api_key = os.getenv('GOOGLE_API_KEY')
Model_Name = "gemini-2.5-flash-lite"

or_client = AsyncOpenAI(base_url=gemini_base_url, api_key=gemini_api_key)
or_model = OpenAIChatCompletionsModel(model = Model_Name, openai_client=or_client)

INSTRUCTIONS = """
You are a senior researcher tasked with writing a cohesive report for a research query.

You will be provided with the original query and research results.

Generate a comprehensive report based on the research and query.

IMPORTANT:
- Return ONLY the Markdown report.
- Do NOT wrap the report inside ```markdown or ``` code fences.
- Use normal Markdown headings such as #, ##, and ###.
- Use bullet points, numbered lists, bold text, tables, and links where appropriate.
- Do not explain that you are generating Markdown.
- Do not add any text before or after the report.
- Make final report look perfect, dont give full report in h1 only give it in proper fonts and format.

The final output should be lengthy and detailed.
Aim for 5-6 pages of content, at least 1000 words.

"""

class ReportData(BaseModel):
    short_summary: str = Field(description="A short 2-3 lines of summry of the findings.")
    markdown_report: str = Field(description="The Final Report")
    Follow_up_question: list[str] = Field(description="Suggested topics to research further")


writer_agent = Agent(name = "Writer Agent", instructions=INSTRUCTIONS, model = or_model, output_type=ReportData)

# You are a senior researcher tasked with writing a cohesive report for a research query.
# You will be provided with the original query, and some research.
# Generate a comprehensive report based on the research and the query.
# The final output should be an markdown format, and it should be lengthy and detailed. Aim for 5-6 pages of content, at least 1000 words.