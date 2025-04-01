# memory/vector_store.py
import json
import os
from typing import Dict, List, Optional

from dotenv import load_dotenv

# Optional imports - only needed if using the specific embeddings models
try:
    from langchain.document_loaders import TextLoader
    from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.vectorstores import Chroma
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
        chunks = text_splitter.split_text(text_content)
        
        # Create documents with metadata
        documents = []
        for i, chunk in enumerate(chunks):
            doc_metadata = metadata.copy() if metadata else {}
            doc_metadata.update({"chunk": i})
            documents.append({"page_content": chunk, "metadata": doc_metadata})
        
        # Create or update vector store
        self.vector_db = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        # Persist to disk
        self.vector_db.persist()
        
        return True
    
    def similarity_search(self, query: str, k: int = 3) -> List[Dict]:
        """
        Search for documents similar to the query
        
        Args:
            query: The search query
            k: Number of results to return
            
        Returns:
            List of document dictionaries with content and metadata
        """
        if not LANGCHAIN_AVAILABLE or not self.vector_db:
            print("Vector store not initialized or LangChain not available.")
            return []
        
        # Perform similarity search
        results = self.vector_db.similarity_search(query, k=k)
        
        # Format results
        formatted_results = []
        for doc in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })
        
        return formatted_results
    
# Simple interface function for the API to use
def initialize_vector_store():
    """Initialize the vector store with portfolio data"""
    if not LANGCHAIN_AVAILABLE:
        print("LangChain not available. Skipping vector store initialization.")
        return False
    
    # Import portfolio data
    from knowledge.portfolio_data import PORTFOLIO_INFO
    
    # Format portfolio data as text
    portfolio_text = json.dumps(PORTFOLIO_INFO, indent=2)
    
    # Initialize vector store
    vector_store = VectorStore()
    vector_store.initialize_from_text(
        portfolio_text, 
        metadata={"source": "portfolio_info"}
    )
    
    print("Vector store initialized successfully.")
    return True