from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import the FastAPI app from main
from main import app

# Export handler for Vercel
handler = Mangum(app)

# Also export as app for direct access
__all__ = ["app", "handler"]
