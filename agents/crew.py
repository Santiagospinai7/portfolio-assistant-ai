from crewai import Crew, Process
from dotenv import load_dotenv

from agents.agents_list import interface_agent, knowledge_agent, project_agent
from agents.llm import TogetherLLM  # Import the custom LLM
from agents.tasks import data_portfolio_task

# Load environment variables
load_dotenv()

# Define Crew with TogetherAI as the manager LLM
portfolio_ai_crew = Crew(
    agents=[interface_agent, knowledge_agent, project_agent],
    tasks=[data_portfolio_task],  
    manager_llm=TogetherLLM(),  # Use the TogetherLLM class
    process=Process.sequential,
    verbose=True,
)

# 🚀 Kickoff the Crew
response = portfolio_ai_crew.kickoff(inputs={"question": "What is your role?"})
print(response)