from apify_client import ApifyClient
from dotenv import load_dotenv
from logs import logger

import os

load_dotenv()

client = ApifyClient(os.getenv("APIFY_TOKEN"))
instagram_actor = client.actor("apify/instagram-scraper")

def instagram_input(link):
    run_input = { 
    "directUrls": [link],
    "resultsType": "posts",
    "resultsLimit": 200,
    "searchType": "hashtag",
    "searchLimit": 1, 
    }
    return run_input

def get_instagram_results():
    raw_results = instagram_actor.call(run_input=instagram_input(link="https://www.instagram.com/reel/DRwZDbKjZaD/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ=="))

    for item in client.dataset(raw_results["defaultDatasetId"]).iterate_items():
        print(item)
