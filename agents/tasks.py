# agents/tasks.py
from crewai import Task


# Define portfolio inquiry tasks
def create_portfolio_inquiry_task(question, agent):
    """Create a task for handling portfolio inquiries"""
    return Task(
        description=f"""
        Answer the following question about the portfolio:
        
        Question: {question}
        
        Provide a detailed, informative answer based on your knowledge.
        If the question is outside your expertise, explain why and what 
        information would be needed to answer it properly.
        """,
        expected_output="A comprehensive, accurate answer to the user's question",
        agent=agent
    )

# Define project inquiry tasks
def create_project_inquiry_task(project_name, question, agent):
    """Create a task for handling project-specific inquiries"""
    return Task(
        description=f"""
        Answer the following question about the project '{project_name}':
        
        Question: {question}
        
        Provide technical details, challenges faced, solutions implemented,
        and outcomes achieved. Include technologies used and your role in the project.
        """,
        expected_output="A detailed technical and business explanation of the project",
        agent=agent
    )

# Define initial routing task
def create_routing_task(question, agent):
    """Create a task for the interface agent to route questions"""
    return Task(
        description=f"""
        Analyze the following question and determine which specialist should handle it:
        
        Question: {question}
        
        If it's about general portfolio information, skills, education, or work history,
        route it to the Knowledge Expert.
        
        If it's about specific projects, technical implementations, or case studies,
        route it to the Project Specialist.
        
        Explain your routing decision.
        """,
        expected_output="A routing decision with explanation of why this specialist is best suited",
        agent=agent
    )