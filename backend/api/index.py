import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import and create FastAPI app
from main import app
from mangum import Mangum

# Create the ASGI handler for Vercel
handler = Mangum(app, lifespan="off")
