from apify_client import ApifyClientAsync
from dotenv import load_dotenv
import logging
import os
import asyncio
from typing import List, Dict, Optional
import re 

load_dotenv()

logger = logging.getLogger(__name__)

class ApifyError(Exception):
    pass

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")
if not APIFY_TOKEN:
    logger.critical("APIFY_API_TOKEN is missing from environment variables.")

async def _run_actor(run_input: dict, actor_id: str):
    apify_client = ApifyClientAsync(APIFY_TOKEN)
    
    try:
        logger.info(f"Starting Apify Actor: {actor_id}")
        
        run = await apify_client.actor(actor_id).call(run_input=run_input)
        
        if not run or "defaultDatasetId" not in run:
            logger.error(f"Apify Run Failed: No Dataset ID. Status: {run.get('status')}")
            return
        
        logger.info(f"Apify Run ID: {run.get('id')} - Status: {run.get('status')}")
        
        dataset = apify_client.dataset(run["defaultDatasetId"])
        item_count = 0
        async for item in dataset.iterate_items():
            item_count += 1
            yield item
            
        logger.info(f"Total items fetched from Apify: {item_count}")

    except Exception as e:
        error_msg = str(e).lower()
        if "quota" in error_msg:
            logger.critical("APIFY QUOTA EXCEEDED")
            raise ApifyError("Apify quota exceeded.")
        elif "rate limit" in error_msg:
            logger.warning("APIFY RATE LIMIT HIT.")
            raise ApifyError("Too many requests to Apify.")
        else: 
            logger.error(f"Apify Actor {actor_id} failed: {e}")
            raise ApifyError(f"Actor failed: {e}")


async def apify_search(keywords: str, max_items: int = 10, locations: list = None, start_page: int = 1):
    if not keywords:
        return
    
    if locations is None:
        locations = []
    
    run_input = {
        "profileScraperMode": "Full",
        "search": keywords,
        "maxItems": max_items,
        "locations": locations, 
        "startPage": start_page,
    }
    
    async for item in _run_actor(run_input, actor_id="qXMa8kADnUQdmz18G"):
        yield item


async def enrich_profiles(profile_urls: list):
    if not profile_urls:
        return

    run_input = {
        "urls": profile_urls,
        "minDelay": 1,
        "maxDelay": 5,
    }
    
    async for item in _run_actor(run_input, actor_id="harvestapi/linkedin-profile-scraper"):
        yield item


def warm_lead_extractor(profiles: List[Dict]) -> List[Dict]:
    if not profiles:
        return []
    
    cleaned_profiles = []
    
    for idx, profile in enumerate(profiles, 1):
        try:
            first = profile.get("firstName")
            last = profile.get("lastName")
            
            if first and last:
                name = f"{first} {last}"
            else:
                name = (
                    profile.get("fullName") or 
                    profile.get("name") or 
                    profile.get("title") or       
                    profile.get("author") or 
                    "Unknown"
                )

            linkedin_url = (
                profile.get("linkedinUrl") or   
                profile.get("url") or 
                profile.get("linkedinProfileUrl") or 
                profile.get("publicIdentifier") or 
                None
            )

            if name == "Unknown" and linkedin_url:
                try:
                    match = re.search(r'/in/([^/]+)', linkedin_url)
                    if match:
                        name = match.group(1).replace("-", " ").title()
                except:
                    pass

            job_title = profile.get("headline") or profile.get("jobTitle") or ""
            
            location = profile.get("location", {}) or {}
            parsed_location = location.get("parsed", {}) or {} # Handle nested if exists
            
            if isinstance(location, dict):
                 country = location.get("country") or location.get("default") or "Not available"
                 city = location.get("city") or "Not available"
            elif isinstance(location, str):
                country = location
                city = ""
            else:
                country = "Not available"
                city = ""

            education_list = profile.get("education", []) or []
            school_name = "Not available"
            degree = "Not available"
            
            if isinstance(education_list, list) and len(education_list) > 0:
                first_edu = education_list[0]
                # Check if fields are different (e.g. 'schoolName' vs 'school')
                if isinstance(first_edu, dict):
                    school_name = (
                        first_edu.get("schoolName") or 
                        first_edu.get("school") or 
                        first_edu.get("name") or 
                        "Not available"
                    )
                    degree = first_edu.get("degree") or first_edu.get("degreeName") or "Not available"
                else:
                    school_name = str(first_edu)

            company_name = ""
            experience = profile.get("experience", []) or [] # HarvestAPI uses 'experience' list
            
            if isinstance(experience, list) and len(experience) > 0:
                latest_job = experience[0]
                if isinstance(latest_job, dict):
                    company_name = (
                        latest_job.get("companyName") or 
                        latest_job.get("company") or 
                        latest_job.get("name") or 
                        ""
                    )

            if not company_name and " at " in job_title:
                parts = job_title.split(" at ")
                if len(parts) > 1:
                    company_name = parts[-1].strip()

            profile_data = {
                "name": name,
                "current_role": job_title,
                "company": company_name,
                "education": school_name,
                "degree": degree,
                "country": country,
                "city": city,
                "linkedin_url": linkedin_url,
                "summary": profile.get("about", "")[:200], 
            }
            
            cleaned_profiles.append(profile_data)
            
        except Exception as e:
            logger.warning(f"Skipping corrupt profile: {e}")
            continue
    
    return cleaned_profiles


async def search_and_extract(keywords: str, max_items: int = 10, locations: list = None) -> List[Dict]:
    try:
        profiles = []
        async for profile in apify_search(keywords, max_items, locations=locations):
            profiles.append(profile)
        return warm_lead_extractor(profiles)
    except ApifyError as e:
        logger.error(f"Apify pipeline failed: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in pipeline: {e}")
        return []

if __name__ == "__main__":
    asyncio.run(search_and_extract("test"))