# agents/agents_list.py
from crewai import Agent
from dotenv import load_dotenv

from agents.llm import get_llm
from agents.portfolio_integration import get_portfolio_knowledge_prompt

# Load environment variables
load_dotenv()

# Get the LLM configuration (use "openai" or "anthropic")
llm_config = get_llm("openai")  # Change to your preferred provider

# Interface Agent
interface_agent = Agent(
    role="User Interface Expert",
    goal="Understand user queries and direct them to the right specialist",
    backstory="""You are the first point of contact for users interacting with Santiago Ospina's
    Portfolio AI Assistant. Your expertise is in understanding what users are asking for and
    directing their questions to the right specialist. You have excellent communication skills
    and can translate technical jargon into simple language.
    
    Always be friendly, professional, and helpful. If a query is about Santiago's background,
    skills, or general information, route it to the Knowledge Expert. If it's about specific
    projects or technical implementations, route it to the Project Specialist.
    """,
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
    goal="Provide comprehensive information about Santiago's skills, experience, and background",
    backstory=get_portfolio_knowledge_prompt(),  # Using our formatted portfolio data
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
    goal="Provide detailed information about Santiago's projects and technical implementations",
    backstory=f"""You specialize in providing in-depth information about Santiago Ospina's portfolio
    projects and technical implementations. You know the technologies used, challenges faced,
    solutions implemented, and outcomes for each project. You can explain the technical aspects
    as well as the business impact of his work.
    
    {get_portfolio_knowledge_prompt()}
    
    When discussing Santiago's projects, emphasize:
    - His problem-solving approach (business needs first, technology second)
    - His experience with AI, automation, and scalable systems
    - Real-world impact and business value delivered
    - Technical architecture and implementation details
    - How he bridges the gap between technology and business objectives
    """,
    verbose=True,
    allow_delegation=False,
    # Pass LLM configuration as keyword arguments
    llm_model=llm_config["model"],
    api_key=llm_config["api_key"],
    temperature=llm_config["temperature"]
)

# List of all agents
agents = [interface_agent, knowledge_agent, project_agent]