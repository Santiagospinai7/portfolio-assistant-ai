# api/routes/query.py
import time
import uuid
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from agents.crew import get_portfolio_crew, get_project_crew

from ..dependencies import get_analytics_tracker, get_memory_store, verify_api_key
from ..models import QueryRequest, QueryResponse

router = APIRouter(prefix="/api", tags=["queries"])

@router.post("/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest, 
    background_tasks: BackgroundTasks,
    memory_store = Depends(get_memory_store),
    analytics = Depends(get_analytics_tracker),
    api_key: Optional[str] = Depends(verify_api_key)
):
    """Process a query to Santiago's portfolio assistant"""
    start_time = time.time()
    
    # Generate or use existing conversation ID
    conversation_id = request.conversation_id or str(uuid.uuid4())
    
    try:
        # Get conversation history
        conversation_history = memory_store.get_conversation(conversation_id)
        
        # Add user message to history
        memory_store.add_message(conversation_id, "user", request.query)
        
        # Determine which crew to use
        if request.project_specific and request.project_name:
            crew = get_project_crew(request.project_name, request.query, conversation_history)
            agent_used = "Project Specialist"
        else:
            crew = get_portfolio_crew(request.query, conversation_history)
            agent_used = "Portfolio Knowledge Expert"
        
        # Process the query
        response = crew.kickoff()
        
        # Record response in history
        memory_store.add_message(conversation_id, "assistant", response)
        
        # Track query in analytics (background)
        background_tasks.add_task(
            analytics.track_query,
            query=request.query,
            user_id=request.user_id,
            conversation_id=conversation_id,
            response_time=time.time() - start_time
        )
        
        # Return the response
        return QueryResponse(
            conversation_id=conversation_id,
            response=response,
            agent_used=agent_used,
            confidence=0.95,  # You can implement proper confidence scoring later
            processing_time=time.time() - start_time,
            metadata={
                "conversation_length": len(conversation_history) + 2  # +2 for current exchange
            }
        )
    
    except Exception as e:
        # Log the error (implementation depends on your logging setup)
        print(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing your request")