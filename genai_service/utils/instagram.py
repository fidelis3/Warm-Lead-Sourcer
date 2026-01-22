from apify_client import ApifyClient
from dotenv import load_dotenv
from typing import List
from ..models.schemas import IGPostScrape, IGComment
import logging
import os


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

load_dotenv()

apify_token = os.getenv("APIFY_CLIENT_TOKEN")
if not apify_token:
    logging.error("APIFY_CLIENT_TOKEN environment variable is not set")
    raise ValueError("APIFY_CLIENT_TOKEN environment variable is required")

try:
    client = ApifyClient(token=apify_token)
    logging.info("ApifyClient initialized successfully.")
except Exception as e:
    logging.error(f"Error initializing ApifyClient: {e}")
    raise







def instagram_output(url: List[str]) -> IGPostScrape:
    def scraper() -> dict:  
        run_input = {
        "directUrls": url,
        "resultsType": "posts",
        "resultsLimit": 200,
        "searchType": "hashtag",
        "searchLimit": 1,
        }
        run = client.actor("apify/instagram-scraper").call(run_input=run_input)
        logging.info("💾 Check your data here: https://console.apify.com/storage/datasets/" + run["defaultDatasetId"])

        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            logging.info(f'Link: {run_input["directUrls"]}\n     Comment count: {item["commentsCount"]}\n\n All content: {item}\n\n')
            return item
    raw_data = scraper()
    parsed_comments = [
        IGComment(
            username = comment["ownerUsername"],
            text = comment["text"],
            timestamp = comment["timestamp"]) for comment in raw_data.get("latestComments", []
        )
    ]
    return IGPostScrape(
        url=raw_data["url"],
        owner_username=raw_data["ownerUsername"],
        likes_count=raw_data["likesCount"],
        comments_count=raw_data["commentsCount"],
        top_comments=parsed_comments,
        image_description=raw_data["alt"]
    )
    

if __name__ == "__main__":
    result = instagram_output(["https://www.instagram.com/p/DTVsrSHDp9i/?utm_source=ig_web_copy_link"])
    if result:
        print(result)