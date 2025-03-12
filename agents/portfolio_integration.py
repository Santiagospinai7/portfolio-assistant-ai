# agents/portfolio_integration.py
from knowledge.portfolio_data import PORTFOLIO_INFO


def format_portfolio_data():
    """
    Format the portfolio data into a format that's optimal for LLM context
    """
    formatted_data = ""
    
    # Personal Information
    personal = PORTFOLIO_INFO["personal"]
    formatted_data += "# PERSONAL INFORMATION\n"
    formatted_data += f"Name: {personal['name']}\n"
    formatted_data += f"Title: {personal['title']}\n"
    formatted_data += f"Location: {personal['location']}\n"
    formatted_data += f"Contact: {personal['contact']['email']} | {personal['contact']['phone']}\n"
    formatted_data += f"LinkedIn: {personal['contact']['linkedin']}\n"
    formatted_data += f"Website: {personal['contact']['website']}\n\n"
    formatted_data += f"Summary: {personal['summary']}\n\n"
    
    # Skills
    skills = PORTFOLIO_INFO["skills"]
    formatted_data += "# SKILLS\n"
    for category, skill_list in skills.items():
        formatted_category = category.replace('_', ' ').title()
        formatted_data += f"## {formatted_category}\n"
        formatted_data += f"{', '.join(skill_list)}\n\n"
    
    # Experience
    formatted_data += "# WORK EXPERIENCE\n"
    for job in PORTFOLIO_INFO["experience"]:
        formatted_data += f"## {job['role']} at {job['company']} ({job['location']})\n"
        formatted_data += f"Duration: {job['duration']}\n"
        formatted_data += "Responsibilities:\n"
        for responsibility in job['responsibilities']:
            formatted_data += f"- {responsibility}\n"
        formatted_data += f"Technologies: {', '.join(job['technologies'])}\n\n"
    
    # Education
    formatted_data += "# EDUCATION\n"
    for edu in PORTFOLIO_INFO["education"]:
        formatted_data += f"## {edu['degree']} - {edu['institution']} ({edu['location']})\n"
        formatted_data += f"Duration: {edu['duration']}\n"
        if 'details' in edu and edu['details']:
            formatted_data += f"{edu['details']}\n\n"
        else:
            formatted_data += "\n"
    
    # AI Journey
    ai_journey = PORTFOLIO_INFO["ai_journey"]
    formatted_data += "# AI EXPERTISE AND JOURNEY\n"
    
    formatted_data += "## Current Focus\n"
    for focus in ai_journey["current_focus"]:
        formatted_data += f"- {focus}\n"
    
    formatted_data += "\n## Learning Path\n"
    for path in ai_journey["learning_path"]:
        formatted_data += f"- {path}\n"
    
    formatted_data += "\n## AI Interests\n"
    for interest in ai_journey["interests"]:
        formatted_data += f"- {interest}\n"
    
    formatted_data += "\n## Next Steps in AI\n"
    for step in ai_journey["next_steps"]:
        formatted_data += f"- {step}\n\n"
    
    # Philosophy and Approach
    philosophy = PORTFOLIO_INFO["philosophy"]
    formatted_data += "# PROFESSIONAL PHILOSOPHY\n"
    
    formatted_data += "## Approach to Work\n"
    for approach in philosophy["approach"]:
        formatted_data += f"- {approach}\n"
    
    formatted_data += "\n## Professional Strengths\n"
    for strength in philosophy["strengths"]:
        formatted_data += f"- {strength}\n"
    
    formatted_data += "\n## Career Goals\n"
    for goal in philosophy["career_goals"]:
        formatted_data += f"- {goal}\n"
    
    formatted_data += "\n## Personal Passions\n"
    for passion in philosophy["passions"]:
        formatted_data += f"- {passion}\n\n"
    
    # Projects
    formatted_data += "# PROJECTS\n"
    for project in PORTFOLIO_INFO["projects"]:
        formatted_data += f"## {project['name']}\n"
        formatted_data += f"Description: {project['description']}\n"
        formatted_data += f"Technologies: {', '.join(project['technologies'])}\n"
        
        formatted_data += "Features:\n"
        for feature in project["features"]:
            formatted_data += f"- {feature}\n"
        
        if 'github' in project:
            formatted_data += f"GitHub: {project['github']}\n\n"
        else:
            formatted_data += "\n"
    
    return formatted_data

def get_portfolio_context():
    """
    Returns the formatted portfolio data as context for the AI models
    """
    return format_portfolio_data()

def get_portfolio_knowledge_prompt():
    """
    Returns a prompt with portfolio information that can be used in the agent's backstory
    """
    return f"""
      As Santiago Ospina's Portfolio AI Assistant, you have detailed knowledge about his background, 
      skills, experience, and professional philosophy.

      {format_portfolio_data()}

      When answering questions about Santiago's portfolio, use this information to provide accurate
      and detailed responses. If asked about specific projects or technical details not explicitly 
      mentioned here, you can respond based on his general technology stack and experience, but
      make it clear that you're providing a general answer based on his background.

      Always maintain Santiago's voice and philosophy in your responses:
      - Focus on business value before technology
      - Emphasize problem-solving and practical solutions
      - Highlight the connection between technology and business impact
      - Showcase his experience with AI, automation, and scalable systems

      If asked about Santiago's availability for projects, interviews, or collaborations, suggest
      contacting him directly through the provided contact information.
      """

    # Example usage in agents_list.py:
    """
    from agents.portfolio_integration import get_portfolio_knowledge_prompt

    # Knowledge Retrieval Agent
    knowledge_agent = Agent(
        role="Portfolio Knowledge Expert",
        goal="Provide comprehensive information about Santiago's skills, experience, and background",
        backstory=get_portfolio_knowledge_prompt(),
        verbose=True,
        allow_delegation=False,
        llm_model=llm_config["model"],
        api_key=llm_config["api_key"],
        temperature=llm_config["temperature"]
    )
    """