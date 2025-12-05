from fastapi import FastAPI
from ..models.schemas import GeneralProfile
from ..utils.llm_client import platform_detection
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger.info("Starting GenAI Service API")
app = FastAPI(title="Warm Lead Sourcer", description="API for Generative AI based lead enrichment and scoring service", version="1.0.0")

@app.get("/")
async def health_check():
    logger.info("Health check endpoint called")
    return {"message": "GenAI Service is up and running!"}

@app.post("/leads")
async def lead_generator(post_link):
    logger.info("Starting the lead generaation process")
    platform = await platform_detection(link=post_link)
    logger.info("Platform detected: %s", platform)
    return {"platform": platform, "post_link": post_link}

