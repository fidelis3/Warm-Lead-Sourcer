import asyncio
import logging
from typing import Optional
from ..utils.llm_client import platform_detection
from ..utils.serper import serper_search
from ..utils.data_wrangling import data_pipeline

logger = logging.getLogger(__name__)


    
class MainPipeline():
    def run_pipeline(self, link : Optional[str], keywords: Optional[str], country: Optional[str], pages: Optional[int]):
        logger.info("Running main pipeline")

        if link:
            logger.info(f"Link provided. Platform detection will be based on the link.")
            platform = asyncio.run(platform_detection())
            logger.info(f"Detected platform: {platform}")

            if platform == "linkedin":
                logger.info("Running LinkedIn extraction pipeline")
                try:
                    logger.info(f"Extracting data from LinkedIn link: {link}")
                    extraction_results = asyncio.run(serper_search(keywords=link, country=country, pages=pages))
                    logger.info("LinkedIn data extraction completed")
                except Exception as e:
                    logger.error(f"Error during LinkedIn data extraction: {e}")
                    raise

                try:
                    logger.info("Processing extracted LinkedIn data through data pipeline")
                    processed_results = data_pipeline(extraction_results)
                    logger.info("Data processing completed")
                    return processed_results
                except Exception as e:
                    logger.error(f"Error during data processing: {e}")
                    raise
                return processed_results
                
            elif platform == "instagram":
                extraction_results = asyncio.run(serper_search(keywords=keywords, country=country, pages=pages))
                processed_results = data_pipeline(extraction_results)
                return processed_results
        elif keywords and not link:
            logger.info(f"No link provided. Using keywords for extraction.")
            extraction_results = asyncio.run(serper_search(keywords=keywords, country=country, pages=pages))
            processed_results = data_pipeline(extraction_results)
            return processed_results
        else:
            logger.info("No valid link or keywords provided.")
            return None
