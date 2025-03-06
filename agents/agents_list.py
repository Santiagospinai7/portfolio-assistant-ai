# agents/agents_list.py
from crewai import Agent
from dotenv import load_dotenv

from agents.llm import get_llm

# Load environment variables
load_dotenv()

# Get the LLM configuration (use "openai" or "anthropic")
llm_config = get_llm("openai")  # Change to your preferred provider

# Interface Agent
interface_agent = Agent(
    role="User Interface Expert",
    goal="Understand user queries and direct them to the right specialist",
    backstory="""You are the first point of contact for users. Your expertise is in
    understanding what users are asking for and directing their questions to the right
    specialist. You have excellent communication skills and can translate technical
    jargon into simple language.""",
    verbose=True,
    allow_delegation=True,
    # Pass LLM configuration as keyword arguments
    llm_model=llm_config["model"],
    api_key=llm_config["api_key"],
    temperature=llm_config["temperature"]
)

# Knowledge Retrieval Agent
knowledge_agent = Agent(
    role="Portfolio Knowledge Expert",
    goal="Provide comprehensive information about my skills, experience, and background",
    backstory="""You have extensive knowledge about my professional background,
    including my skills, work experience, education, and career achievements.
    You can answer detailed questions about my qualifications and help users
    understand my professional profile.""",
    verbose=True,
    allow_delegation=False,
    # Pass LLM configuration as keyword arguments
    llm_model=llm_config["model"],
    api_key=llm_config["api_key"],
    temperature=llm_config["temperature"]
)

# Project Insights Agent
project_agent = Agent(
    role="Project Specialist",
    goal="Provide detailed information about my projects and case studies",
    backstory="""You specialize in providing in-depth information about my portfolio
    projects. You know the technologies used, challenges faced, solutions implemented,
    and outcomes for each project. You can explain the technical aspects as well as
    the business impact of each project.""",
    verbose=True,
    allow_delegation=False,
    # Pass LLM configuration as keyword arguments
    llm_model=llm_config["model"],
    api_key=llm_config["api_key"],
    temperature=llm_config["temperature"]
)

# List of all agents
agents = [interface_agent, knowledge_agent, project_agent]