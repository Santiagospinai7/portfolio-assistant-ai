# api/main.py
import uuid
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from memory.conversation_store import ConversationMemory
from memory.vector_store import initialize_vector_store
from pydantic import BaseModel

# Import your agent system
from agents.crew import get_portfolio_crew, get_project_crew

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Santiago Ospina Portfolio AI API",
    description="API for interacting with Santiago's portfolio AI assistant",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize conversation memory
conversation_memory = ConversationMemory()

# Initialize vector store on startup
@app.on_event("startup")
async def startup_event():
    # Initialize vector database with portfolio information
    initialize_vector_store()

# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None
    project_specific: bool = False
    project_name: Optional[str] = None

class QueryResponse(BaseModel):
    conversation_id: str
    response: str
    agent_used: str
    confidence: float
    metadata: Optional[Dict[str, Any]] = None

# Define API endpoints
@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest, background_tasks: BackgroundTasks):
    """Process a query about Santiago's portfolio"""
    try:
        # Generate or use existing conversation ID
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Retrieve conversation history if available
        conversation_history = conversation_memory.get_conversation(conversation_id)
        
        # Add the new query to the conversation history
        conversation_memory.add_message(conversation_id, "user", request.query)
        
        # Determine if we need to use project-specific crew
        if request.project_specific and request.project_name:
            crew = get_project_crew(request.project_name, request.query, conversation_history)
            agent_used = "Project Specialist"
        else:
            crew = get_portfolio_crew(request.query, conversation_history)
            agent_used = "Portfolio Knowledge Expert"
        
        # Process the query using the appropriate crew
        response = crew.kickoff()
        
        # Store the response in conversation history
        conversation_memory.add_message(conversation_id, "assistant", response)
        
        # In the background, update the vector store with new conversation data
        background_tasks.add_task(
            update_vector_store_with_conversation,
            conversation_id,
            request.query,
            response
        )
        
        # Return the response
        return QueryResponse(
            conversation_id=conversation_id,
            response=response,
            agent_used=agent_used,
            confidence=0.95,  # You can implement confidence scoring later
            metadata={
                "history_length": len(conversation_memory.get_conversation(conversation_id))
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Retrieve the conversation history for a given ID"""
    try:
        history = conversation_memory.get_conversation(conversation_id)
        if not history:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return {"conversation_id": conversation_id, "messages": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation: {str(e)}")

@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation by ID"""
    try:
        success = conversation_memory.delete_conversation(conversation_id)
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return {"status": "success", "message": "Conversation deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting conversation: {str(e)}")

# Background task to update vector store
async def update_vector_store_with_conversation(conversation_id, query, response):
    """Background task to update the vector store with new conversation data"""
    # This will help with future semantic search capabilities
    pass

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)