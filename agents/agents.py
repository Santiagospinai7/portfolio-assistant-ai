from crewai import Agent
from langchain.llms import OpenAI

# Define an LLM
llm = OpenAI(model="mistralai/mistral-7b-instruct-v0.3", temperature=0.7)

# Interface Agent
interface_agent = Agent(
    role="User Interface",
    goal="Interact with users and direct them to the right agent",
    llm=llm
)

# Knowledge Retrieval Agent
knowledge_agent = Agent(
    role="Knowledge Expert",
    goal="Answer questions about portfolio and experience",
    llm=llm
)

# Project Insights Agent
project_agent = Agent(
    role="Project Specialist",
    goal="Provide details about projects",
    llm=llm
)

agents = [interface_agent, knowledge_agent, project_agent]