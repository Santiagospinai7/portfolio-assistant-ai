# api/main.py
import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from memory.vector_store import initialize_vector_store

from .routes import admin, query

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("portfolio-api")

# Initialize FastAPI app
app = FastAPI(
    title="Santiago Ospina Portfolio AI API",
    description="API for interacting with Santiago's portfolio AI assistant",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(query.router)
app.include_router(admin.router)

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting portfolio AI API")
    
    # Initialize vector store
    try:
        initialize_vector_store()
        logger.info("Vector store initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing vector store: {str(e)}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down portfolio AI API")

# For direct execution
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app", 
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=bool(os.getenv("DEBUG", "False").lower() == "true")
    )