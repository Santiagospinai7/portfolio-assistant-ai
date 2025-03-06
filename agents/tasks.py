from crewai import Task

from agents.agents_list import knowledge_agent

# Define a simple task for testing
data_portfolio_task = Task(
    description="Answer the following question: {question}",
    expected_output="A detailed answer about the portfolio and experience.",
    agent=knowledge_agent  # Assign to Knowledge Agent
)