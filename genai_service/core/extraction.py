import logging
import re
from typing import Optional, List

from models.schemas import GeneralProfile
from utils.llm_client import platform_detection, calculate_score 
from utils.apify import search_and_extract, enrich_profiles, warm_lead_extractor
from utils.data_wrangling import email_generator, export
from utils.caching import get_cached_results, save_to_cache

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
            logger.info("No link provided. Running Apify search based on keywords.")
            
            logger.info("Checking cache for existing results...")
            cached_data = get_cached_results(keywords, country, page)
            
            if cached_data is not None:
                logger.info(f"Cache HIT! Found {len(cached_data)} cached profiles.")
                return [GeneralProfile(**p) for p in cached_data]
            
            logger.info("Cache MISS. Fetching fresh data from Apify...")
            
            try:
                search_query = f"{keywords} {country}" if country else keywords
                logger.info(f"Searching Apify for: {search_query}")
                
                rich_profiles = await search_and_extract(keywords=search_query, max_items=5)
                
                if not rich_profiles:
                    logger.warning("Apify found 0 profiles.")
                    return []
                
                logger.info(f"Apify returned {len(rich_profiles)} profiles. Processing & Scoring...")

                processed_results = []
                
                for profile in rich_profiles:
                    email = email_generator(profile)
                    
                    # Ensure keywords is a list
                    kw_list = keywords.split() if isinstance(keywords, str) else keywords
                    score = await calculate_score(profile, kw_list)
                    
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

                logger.info("Data processing completed")
                
                # Cache the results before returning
                save_to_cache(keywords, country, page, [p.model_dump() for p in processed_results])
                
                return processed_results

            except Exception as e:
                logger.error(f"Error during Apify extraction/processing: {e}")
                raise

        else:
            logger.warning("No valid input provided for lead sourcing.")
            raise ValueError("Either a link or keywords must be provided for lead sourcing.")

    # --- NEW METHOD FOR INTEGRATION ---
    async def run_enrichment(self, links: List[str]):
        """
        Takes specific LinkedIn URLs (from Partner), scrapes details, adds emails.
        """
        logger.info(f"Starting Enrichment Pipeline for {len(links)} links")
        
        # 1. Fetch Raw Data
        raw_profiles_generator = []
        async for profile in enrich_profiles(links):
            raw_profiles_generator.append(profile)
            
        # 2. Clean Data using existing extractor
        cleaned_profiles = warm_lead_extractor(raw_profiles_generator)
        
        if not cleaned_profiles:
            return {"error": "Could not scrape details."}

        # 3. Add Value (Email & CSV)
        processed_results = []
        for profile in cleaned_profiles:
            email = email_generator(profile)
            
            final_profile = GeneralProfile(
                name=profile.get("name"),
                linkedin_url=profile.get("linkedin_url"),
                current_role=profile.get("current_role"),
                company=profile.get("company"),
                education=profile.get("education"),
                country=profile.get("country"),
                email=email,
                score=10 # Default score for warm leads
            )
            processed_results.append(final_profile)

        # 4. Generate CSV
        # Assuming export() is async and returns a filename or buffer
        # You might need to adjust based on your utils/data_wrangling.py
        csv_file = await export([p.model_dump() for p in processed_results])
        
        return {
            "count": len(processed_results),
            "data": processed_results,
            "csv_file": csv_file
        }