from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import tempfile
import shutil
import os
import json
import logging

from backend.utils.logging import setup_logging
from backend.utils.Pulse import Pulse

# Set up logging
setup_logging(log_level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Pulse API", description="API for running Pulse analysis")

@app.post("/api/pulse")
async def create_pulse(
    request: Dict[str, Any],
    parallel: Optional[bool] = False
):
    """
    Create and run a Pulse analysis from JSON input.
    Returns the pulse_spec.json content.
    """
    temp_dir = None
    try:
        logger.info("Starting Pulse analysis")
        temp_dir = tempfile.mkdtemp()
        
        # Create and run Pulse
        logger.debug("Loading Pulse from request")
        pulse = Pulse.load(request)
        logger.debug("Running Pulse")
        pulse.run(parallel=parallel)
        
        # Save results directly to temp directory
        logger.debug("Saving Pulse results")
        pulse.save(temp_dir)
        
        # Read pulse_spec.json
        spec_path = os.path.join(temp_dir, 'pulse_spec.json')
        return JSONResponse(content=json.load(open(spec_path, 'r')))
            
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request. Please try again later."
        )
    finally:
        # Clean up temporary directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                logger.error(f"Error cleaning up temporary directory: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)