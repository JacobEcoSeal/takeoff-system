import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    # Import and create FastAPI app
    from main import app
    from mangum import Mangum
    
    # Create the ASGI handler for Vercel
    handler = Mangum(app, lifespan="off")
except Exception as e:
    # If import fails, create a simple error handler
    import json
    from datetime import datetime
    
    async def error_handler(scope, receive, send):
        await send({
            'type': 'http.response.start',
            'status': 500,
            'headers': [[b'content-type', b'application/json']],
        })
        error_msg = json.dumps({
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'EcoSeal Takeoff API'
        }).encode()
        await send({
            'type': 'http.response.body',
            'body': error_msg,
        })
    
    handler = error_handler
