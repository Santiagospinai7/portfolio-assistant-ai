# agents/crew.py
from crewai import Crew, Process
from dotenv import load_dotenv

from agents.agents_list import interface_agent, knowledge_agent, project_agent
from agents.llm import get_llm
from agents.tasks import (
    create_portfolio_inquiry_task,
    create_project_inquiry_task,
    create_routing_task,
)

# Load environment variables
load_dotenv()

# Get LLM configuration for the crew manager
manager_llm_config = get_llm("openai")  # Use OpenAI for manager (more reliable)

def get_portfolio_crew(question):
    """Create and configure a crew to handle portfolio inquiries"""
    
    # Create a routing task
    routing_task = create_routing_task(question, interface_agent)
    
    # Create a knowledge task
    knowledge_task = create_portfolio_inquiry_task(question, knowledge_agent)
    
    # Create the crew
    portfolio_crew = Crew(
        agents=[interface_agent, knowledge_agent, project_agent],
        tasks=[routing_task, knowledge_task],
        process=Process.sequential,
        verbose=True,
    )
    
    return portfolio_crew

def get_project_crew(project_name, question):
    """Create and configure a crew to handle project-specific inquiries"""
    
    # Create a project task
    project_task = create_project_inquiry_task(project_name, question, project_agent)
    
    # Create the crew
    project_crew = Crew(
        agents=[project_agent, knowledge_agent],
        tasks=[project_task],
        process=Process.sequential,
        verbose=True,
    )
    
    return project_crew

# Example usage
if __name__ == "__main__":
    # Test with a simple question
    crew = get_portfolio_crew("What skills do you have in AI development?")
    response = crew.kickoff()
    print(response)