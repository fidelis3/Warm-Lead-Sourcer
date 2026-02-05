from apify_client import ApifyClient
from dotenv import load_dotenv
import logging
import os
load_dotenv()

client = ApifyClient(os.getenv("APIFY_API_TOKEN"))
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)



async def apify_search(keywords: str):
    run_input = {
    "profileScraperMode": "Full",
    "search": keywords,
    "maxItems": 10,
    "locations": None,
    "startPage": 1,
    "takePages": None,
    }
    logger.info("Starting Apify actor for profile extraction with keywords: %s", keywords)
    run = client.actor("qXMa8kADnUQdmz18G").call(run_input=run_input)
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        yield item


def warm_lead_extractor(profiles):
    profiles = []
    logger.info("Processing profiles extracted from Apify.")
    for profile in profiles:
        profile_data = {
            "name": profile.get("name"),
            "role": profile.get("position"),
            "summary": profile.get("summary"),
            "linkedin_url": profile.get("linkedinProfileUrl"),
            "country": profile.get("location").get("parsed").get("country") ,
            "city": profile.get("location").get("parsed").get("city"),
            "education": profile.get("education").get("SchoolName"),
            "degree": profile.get("education")[0].get("degree"),  
        }
        logger.info("Extracted  profiles wrangled successfully: %s", profile_data)
        profiles.append(profile_data)

    return profiles