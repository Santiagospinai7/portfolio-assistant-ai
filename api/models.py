# api/models.py
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request model for agent queries"""
    query: str = Field(..., description="The user's question")
    conversation_id: Optional[str] = Field(None, description="Existing conversation ID")
    user_id: Optional[str] = Field(None, description="User identifier for analytics")
    project_specific: bool = Field(False, description="Whether the query is about a specific project")
    project_name: Optional[str] = Field(None, description="The name of the project if project_specific=True")

class Message(BaseModel):
    """Model for a conversation message"""
    role: str = Field(..., description="Either 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now)

class ConversationResponse(BaseModel):
    """Response model for conversation history"""
    conversation_id: str
    messages: List[Message]
    
class QueryResponse(BaseModel):
    """Response model for agent queries"""
    conversation_id: str
    response: str
    agent_used: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    processing_time: float = Field(..., description="Time taken to process query in seconds")
    metadata: Optional[Dict[str, Any]] = None