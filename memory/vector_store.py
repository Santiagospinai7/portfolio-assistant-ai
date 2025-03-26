# memory/vector_store.py
import os
from typing import List, Dict, Any, Optional
import json
from dotenv import load_dotenv
import numpy as np

# Optional imports - only needed if using the specific embeddings models
try:
    from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
    from langchain.vectorstores import Chroma
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.document_loaders import TextLoader
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

# Load environment variables
load_dotenv()

# Constants
VECTOR_DB_PATH = "./data/vectorstore"
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "openai")  # openai, huggingface, etc.

class VectorStore:
    """
    A class to handle vector embeddings and similarity search for portfolio data
    """
    def __init__(self, persist_directory: str = VECTOR_DB_PATH):
        self.persist_directory = persist_directory
        self.embeddings = None
        self.vector_db = None
        
        # Initialize if LangChain is available
        if LANGCHAIN_AVAILABLE:
            self._initialize_embeddings()
            os.makedirs(persist_directory, exist_ok=True)
    
    def _initialize_embeddings(self):
        """Initialize the embeddings model based on configuration"""
        if EMBEDDINGS_MODEL == "openai":
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
        elif EMBEDDINGS_MODEL == "huggingface":
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-mpnet-base-v2"
            )
        else:
            raise ValueError(f"Unsupported embeddings model: {EMBEDDINGS_MODEL}")
    
    def initialize_from_text(self, text_content: str, metadata: Optional[Dict] = None):
        """
        Initialize the vector store from text content
        
        Args:
            text_content: Text to embed
            metadata: Optional metadata to associate with the text
        """
        if not LANGCHAIN_AVAILABLE:
            print("LangChain not available. Skipping vector store initialization.")
            return False
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Create documents with text chunks
        chunks = text_splitter.