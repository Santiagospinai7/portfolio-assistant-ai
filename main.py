# main.py
from dotenv import load_dotenv

from agents.crew import get_portfolio_crew, get_project_crew

# Load environment variables
load_dotenv()

def main():
    """Main application entry point"""
    print("Portfolio Assistant AI")
    print("----------------------")
    print("Type 'exit' to quit\n")
    
    while True:
        # Get user input
        user_input = input("Ask me anything about my portfolio: ")
        
        # Check for exit command
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        # Determine if this is a project-specific question
        if "project" in user_input.lower():
            # Extract project name (this is a simplistic approach)
            project_name = "Default Project"  # In a real app, you'd parse this
            crew = get_project_crew(project_name, user_input)
        else:
            # General portfolio question
            crew = get_portfolio_crew(user_input)
        
        # Process the question
        try:
            print("\nProcessing your question...\n")
            response = crew.kickoff()
            print(f"\nResponse: {response}\n")
        except Exception as e:
            print(f"\nError: {str(e)}\n")
            print("Try rephrasing your question or check your API keys")

if __name__ == "__main__":
    main()