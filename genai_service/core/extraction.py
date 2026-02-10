import logging
import re
from typing import Optional, List
from utils.caching import get_cached_results, save_to_cache
from fastapi import HTTPException

from models.schemas import GeneralProfile
from utils.llm_client import platform_detection, calculate_score 
from utils.apify import search_and_extract
from utils.data_wrangling import email_generator

logger = logging.getLogger(__name__)

def link_validation(link: str) -> bool:
    pattern = r"^https?://([a-z0-9-]+\.)?linkedin\.com/"
    return bool(re.match(pattern, link, re.IGNORECASE))

class MainPipeline():
    async def run_pipeline(self, link: Optional[str] = None, keywords: Optional[str] = None, country: Optional[str] = None, page: Optional[int] = 1):
        logger.info("Running main pipeline")

        if link:
            logger.info("Validating the provided LinkedIn link")
            valid = link_validation(link)
            if not valid:
                logger.error("Invalid LinkedIn link provided.")
                raise ValueError("The provided link is not a valid LinkedIn URL.")
                
            logger.info(f"Link provided. Platform detection will be based on the link.")
            try:
                platform = await platform_detection(link=link)
            except Exception as e:
                logger.error(f"Error during platform detection: {e}")
                raise

            logger.info(f"Detected platform: {platform}")

            if platform == "linkedin":
                logger.info("Running LinkedIn extraction pipeline")
                raise NotImplementedError("LinkedIn extraction not implemented yet")  
            elif platform == "unknown":
                logger.warning("Unknown platform detected. Cannot proceed with extraction.")
                raise ValueError("The provided link does not belong to a supported platform.")
            
        elif keywords and not link:
            logger.info("No link provided. Checking cache.")
            cached_data = get_cached_results(keywords, country, page)
            if cached_data:
                #if found in cache, convert JSON back to GeneralProfile objects and return!
                logger.info("Cache hit. Returning cached results.")
                return [GeneralProfile(**p) for p in cached_data]
            #if no cache, run apify
            logger.info("cache miss. Running Apify search ...")
            try:
                search_keywords = keywords
                search_locations = [country] if country else []
                
                logger.info(f"Searching Apify for: {search_keywords} in {search_locations}")
                
                rich_profiles = await search_and_extract(keywords=search_keywords, locations=search_locations, max_items=5)
                
                if not rich_profiles:
                    logger.warning("Apify found 0 profiles.")
                    return []
                
                logger.info(f"Apify returned {len(rich_profiles)} profiles. Processing & Scoring...")

                processed_results = []
            except Exception as e:
                error_str = str(e)
                logger.error(f"Pipeline Error: {error_str}")
                if "Daily search limit reached" in error_str:
                    raise HTTPException(status_code=429, detail="Daily search limit reached, Please upgrade.")
                if "Too many requests" in error_str:
                    raise HTTPException(status_code=429, detail="Too many requests to apify,please retry after some time.")
                #default to 500 for unknown errors
                raise HTTPException(status_code=500, detail=f"Internal Server Error: {error_str}")
            
            for profile in rich_profiles:
                email = email_generator(profile)
                
                score = await calculate_score(profile, keywords.split())
                
                final_profile = GeneralProfile(
                    name=profile.get("name"),
                    linkedin_url=profile.get("linkedin_url"),
                    current_role=profile.get("current_role"),
                    company=profile.get("company"),
                    education=profile.get("education"),
                    country=profile.get("country"),
                    email=email,
                    score=score
                )
                processed_results.append(final_profile)
                # save results to cache

            logger.info(" Saving results to cache.")
            save_to_cache(keywords, country, page, processed_results)
            logger.info("Data processing complete.")
            return processed_results

        else:
            logger.warning("No valid input provided for lead sourcing.")
            raise ValueError("Either a link or keywords must be provided for lead sourcing.")