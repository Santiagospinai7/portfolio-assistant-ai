# agents/llm.py
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define LLM options for CrewAI
def get_llm(provider="openai"):
    """
    Get an LLM configuration dictionary based on the provider
    Supported providers: openai, anthropic
    """
    if provider == "openai":
        return {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": "gpt-3.5-turbo",  # Most affordable OpenAI model
            "temperature": 0.7
        }
    elif provider == "anthropic":
        return {
            "api_key": os.getenv("ANTHROPIC_API_KEY"),
            "model": "claude-3-haiku-20240307",  # Affordable Claude model
            "temperature": 0.7
        }
    elif provider == "huggingface":
        return {
            "api_key": os.getenv("HUGGINGFACE_API_KEY"),
            "model": "mistralai/Mistral-7B-Instruct-v0.3",
            "temperature": 0.7
        }
    else:
        # Default to OpenAI if provider not recognized
        return {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": "gpt-3.5-turbo",
            "temperature": 0.7
        }

# For local testing with HuggingFace models (not for CrewAI)
def get_huggingface_llm():
    """This won't work directly with CrewAI but can be used for testing"""
    from langchain.llms import HuggingFaceEndpoint
    
    return HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.3",
        huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_KEY"),
        temperature=0.7
    )