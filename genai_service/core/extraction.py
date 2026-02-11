import logging
import re
from typing import Optional, List

from models.schemas import GeneralProfile
from utils.llm_client import platform_detection, calculate_score 
from utils.apify import apify_search, apify_lead_presentation, enrich_profiles
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
                
                raw_profiles = await apify_search(keywords=search_query, max_items=5)
                
                if not raw_profiles:
                    logger.warning("Apify found 0 profiles.")
                    save_to_cache(keywords, country, page, [])
                    return []
                
                logger.info(f"Apify returned {len(raw_profiles)} profiles. Cleaning data...")
                
                cleaned_profiles = apify_lead_presentation(raw_profiles)
                
                logger.info(f"Processing & Scoring {len(cleaned_profiles)} cleaned profiles...")

                processed_results = []
                
                for profile in cleaned_profiles:
                    current_role = profile.get("current_role", "")
                    if "|" in current_role:
                        parts = current_role.split("|")
                        company = parts[1].strip() if len(parts) > 1 else "Not available"
                    else:
                        company = "Not available"
                    
                    education_list = profile.get("education", [])
                    if education_list and isinstance(education_list, list) and len(education_list) > 0:
                        education = education_list[0].get("school", "Not available")
                    else:
                        education = "Not available"
                    
                    profile_for_email = {
                        "name": profile.get("name"),
                        "company": company,
                        "education": education
                    }
                    
                    email = email_generator(profile_for_email)
                    
                    kw_list = keywords.split() if isinstance(keywords, str) else keywords
                    score = await calculate_score(profile, kw_list)
                    
                    final_profile = GeneralProfile(
                        name=profile.get("name"),
                        linkedin_url=profile.get("linkedin_url"),
                        current_role=current_role,
                        company=company,
                        education=education,
                        country=profile.get("country"),
                        email=email,
                        score=score
                    )
                    processed_results.append(final_profile)

                logger.info("Data processing completed")
                
                save_to_cache(keywords, country, page, [p.model_dump() for p in processed_results])
                
                return processed_results

            except Exception as e:
                logger.error(f"Error during Apify extraction/processing: {e}")
                raise

        else:
            logger.warning("No valid input provided for lead sourcing.")
            raise ValueError("Either a link or keywords must be provided for lead sourcing.")

    async def run_enrichment(self, links: List[str]):
        """
        Takes specific LinkedIn URLs, scrapes details, adds emails.
        """
        logger.info(f"Starting Enrichment Pipeline for {len(links)} links")
        
        try:
            raw_profiles = []
            async for profile in enrich_profiles(links):
                raw_profiles.append(profile)
            
            if not raw_profiles:
                logger.warning("No profiles extracted from enrichment")
                return {"error": "Could not scrape details."}
            
            logger.info(f"Fetched {len(raw_profiles)} raw profiles. Cleaning data...")
            
            cleaned_profiles = apify_lead_presentation(raw_profiles)
            
            if not cleaned_profiles:
                logger.warning("No profiles after cleaning")
                return {"error": "Could not process profile data."}

            processed_results = []
            for profile in cleaned_profiles:
                current_role = profile.get("current_role", "")
                if "|" in current_role:
                    parts = current_role.split("|")
                    company = parts[1].strip() if len(parts) > 1 else "Not available"
                else:
                    company = "Not available"
                
                education_list = profile.get("education", [])
                if education_list and isinstance(education_list, list) and len(education_list) > 0:
                    education = education_list[0].get("school", "Not available")
                else:
                    education = "Not available"
                
                profile_for_email = {
                    "name": profile.get("name"),
                    "company": company,
                    "education": education
                }
                
                email = email_generator(profile_for_email)
                
                final_profile = GeneralProfile(
                    name=profile.get("name"),
                    linkedin_url=profile.get("linkedin_url"),
                    current_role=current_role,
                    company=company,
                    education=education,
                    country=profile.get("country"),
                    email=email,
                    score=10  
                )
                processed_results.append(final_profile)

            
            csv_file = await export([p.model_dump() for p in processed_results])
            
            logger.info(f"Enrichment completed: {len(processed_results)} profiles processed")
            
            return {
                "count": len(processed_results),
                "data": processed_results,
                "csv_file": csv_file
            }
            
        except Exception as e:
            logger.error(f"Error during enrichment pipeline: {e}")
            raise