# api/dependencies.py
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import Header, HTTPException

from agents.analytics.usage_tracker import AnalyticsTracker
from memory.conversation_store import ConversationMemory

# Load environment variables
load_dotenv()

# API key validation
def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Verify the API key if required"""
    if os.getenv("REQUIRE_API_KEY", "false").lower() == "true":
        expected_key = os.getenv("API_KEY")
        if not x_api_key or x_api_key != expected_key:
            raise HTTPException(
                status_code=401,
                detail="Invalid or missing API key"
            )
    return x_api_key

# Memory store dependency
def get_memory_store():
    """Provides a ConversationMemory instance"""
    return ConversationMemory()

# Analytics tracker dependency
def get_analytics_tracker():
    """Provides an AnalyticsTracker instance"""
    return AnalyticsTracker()