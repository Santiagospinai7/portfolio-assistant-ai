# api/routes/admin.py
from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_analytics_tracker, get_memory_store, verify_api_key

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/analytics")
async def get_analytics(
    api_key: str = Depends(verify_api_key),
    analytics = Depends(get_analytics_tracker)
):
    """Get analytics for the portfolio assistant"""
    try:
        return analytics.get_analytics_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving analytics: {str(e)}")

@router.get("/conversations")
async def list_conversations(
    api_key: str = Depends(verify_api_key),
    memory_store = Depends(get_memory_store)
):
    """List all conversations (not implemented yet)"""
    # This would need storage_path scanning functionality added to ConversationMemory
    return {"message": "Not implemented yet, but would list all conversations"}