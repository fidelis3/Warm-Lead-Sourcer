from .extraction import MainPipeline
from ..models.schemas import GeneralProfile
from fastapi import FastAPI, HTTPException
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

try:
    app = FastAPI(title="Warm Lead Sourcer", version="2.0", description="A service for sourcing warm leads.")
    logger.info("FastAPI application initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize FastAPI application: {e}")
    raise



@app.get("/")
async def check_service():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "Service is running"}

@app.get("/source_leads", response_model=List[GeneralProfile])
async def source_leads(link: str) -> List[Dict]:
    try:
        logger.info("Setting up MainPipeline for lead sourcing.")
        lead_pipeline = MainPipeline(link=link)
        logger.info("MainPipeline set up successfully.")
    except Exception as e:
        # Log full exception internally, but raise a sanitized HTTP error to callers
        logger.exception("Failed to set up MainPipeline")
        raise HTTPException(status_code=500, detail="Internal error setting up pipeline.")

    try:
        logger.info("Running lead sourcing pipeline.")
        leads = lead_pipeline.run_pipeline()
        if leads is None:
            logger.warning("Pipeline returned no leads for link=%s", link)
            return []
        # Expecting `leads` to be a list of dict-like profiles that match GeneralProfile shape
        return leads
    except HTTPException:
        # Re-raise HTTPExceptions unchanged
        raise
    except Exception as e:
        logger.exception("Failed to run pipeline")
        raise HTTPException(status_code=500, detail="Error processing the lead sourcing pipeline.")