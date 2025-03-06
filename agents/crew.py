import os

from crewai import Crew, Process
from dotenv import load_dotenv
from langchain.llms import HuggingFaceEndpoint

from agents.agents_list import interface_agent, knowledge_agent, project_agent
from agents.tasks import data_portfolio_task

# Load environment variables
load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_KEY"),
    temperature=0.7
)

# Define Crew with TogetherAI as the manager LLM
portfolio_ai_crew = Crew(
    agents=[interface_agent, knowledge_agent, project_agent],
    tasks=[data_portfolio_task],  
    manager_llm=llm,
    process=Process.sequential,
    verbose=True,
)

# 🚀 Kickoff the Crew
response = portfolio_ai_crew.kickoff(inputs={"question": "What is your role?"})
print(response)