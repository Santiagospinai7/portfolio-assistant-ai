import os

from crewai import Agent
from dotenv import load_dotenv
from langchain.llms import HuggingFaceEndpoint

# Load environment variables
load_dotenv()

# Initialize the Together LLM
# llm = TogetherLLM()
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_KEY"),
    temperature=0.7
)

# Interface Agent
interface_agent = Agent(
    role="User Interface",
    goal="Interact with users and direct them to the right agent",
    backstory="This agent helps users navigate and find information.",
    llm=llm,
)

# Knowledge Retrieval Agent
knowledge_agent = Agent(
    role="Knowledge Expert",
    goal="Answer questions about portfolio and experience",
    backstory="This agent has extensive knowledge about the user's portfolio and experience.",
    llm=llm,
)

# Project Insights Agent
project_agent = Agent(
    role="Project Specialist",
    goal="Provide details about projects",
    backstory="This agent specializes in providing detailed information about various projects.",
    llm=llm,
)

agents = [interface_agent, knowledge_agent, project_agent]