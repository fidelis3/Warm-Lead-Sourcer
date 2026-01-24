from ..models.schemas import SerperSearchResult
from dotenv import load_dotenv
import http.client
import json
import logging
import os

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

load_dotenv()


def serper_search(keywords: str = "latest technology trends", country: str = "ke", pages: int = 1) -> list[dict]:
    params = SerperSearchResult(keywords=keywords, country=country, pages=pages)
    def linkedin_query_builder() -> str:
        logger.info("Building LinkedIn-specific query for Serper search.")
        keyword_list = keywords.split()
        formatted_keywords = " AND ".join([f'"{k}"' for k in keyword_list])
        return f'site:linkedin.com/in/ {formatted_keywords} {country}'
    try:
        logger.info("Building combined payload query.")
        queries = [
            # General query
            {
            "q": params.keywords, 
            "gl": params.country, 
            "page": params.pages
            },
            # 2. The LinkedIn Targeted Search (People)
            {
                "q": linkedin_query_builder(), 
                "gl": params.country,
                "page": params.pages
            }
        ]
        logger.info("Combined payload query built successfully.")
    except Exception as e:
        logger.error("Error building combined payload query: %s", e)
        raise Exception(f"Failed to build combined payload query: {e}")

    try:
        logger.debug("Creating connection object for google.serper.dev.")
        google = http.client.HTTPSConnection("google.serper.dev", timeout=10)
    except Exception as e:
        logger.error("Error creating connection object: %s", e)
        raise  Exception(f"Failed to connect to Serper API: {e}") 
    
    try:
        logger.info("Preparing Serper search payload.")
        payload = json.dumps(queries)
        logger.info("Serper search payload prepared: %s", payload)
    except Exception as e:
        logger.error("Error preparing Serper search payload: %s", e)
        raise Exception(f"Failed to prepare Serper search payload: {e}")
    
    try:
        logger.info("Getting Serper API key from environment variables.")
        SERPER_API_KEY = os.getenv("SERPER_API_KEY")

        if not SERPER_API_KEY:
            raise ValueError("SERPER_API_KEY environment variable is not set")
        logger.info("Making Serper search request.")
    except Exception as e:
        logger.error("Error retrieving Serper API key: %s", e)
        raise Exception(f"Failed to retrieve Serper API key: {e}")
    try:
        logger.info("Executing Serper search request")
        headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
        }
        google.request("POST", "/search", payload, headers)
        res = google.getresponse()
        raw_data = res.read().decode("utf-8")
        if res.status >= 400:
            logger.error("Serper API error %d: %s", res.status, raw_data)
            raise Exception(f"Serper API returned {res.status}: {raw_data}")

        logger.info("Serper search request executed successfully.")
        json_data = json.loads(raw_data)
        warm_data = json_data[1].get("organic", [])
        return serper_formatter(warm_data)
        # return warm_data
    except Exception as e:
        logger.error("Error executing Serper search request: %s", e)
        raise Exception(f"Failed to execute Serper search request: {e}")
    finally:
        google.close()

def serper_formatter(raw_data):
    formatted_results = []
    def name_formatter(complex_str):
        complex_str = complex_str.replace("-", "*", 1)
        name = complex_str.split("*")[0].strip()
        role = complex_str.split("*")[1].strip() if "*" in complex_str else "Not specified"
        return {"name": name, "role": role}

    for profile in raw_data:
        try:
            name_role = name_formatter(profile.get("title", ""))
            formatted_profile = {
                "name": name_role["name"],
                "current_role": name_role["role"],
                "linkedin_url": profile.get("link", ""),
                "snippet": profile.get("snippet", ""),
            }
            formatted_results.append(formatted_profile)
        except Exception as e:
            logger.error("Error formatting profile data: %s", e)
            continue
    return formatted_results

    

if __name__ == "__main__":
    print(serper_search(keywords="Jkuat Mechanical Engineering", country="ke", pages=2))