import asyncio
import logging
from typing import Optional
from ..utils.llm_client import platform_detection
from ..utils.serper import serper_search
from ..utils.data_wrangling import data_pipeline

logger = logging.getLogger(__name__)


    
class MainPipeline():
    async def run_pipeline(self, link : Optional[str], keywords: Optional[str], country: Optional[str], pages: Optional[int]):
        logger.info("Running main pipeline")

        if link:
            logger.info(f"Link provided. Platform detection will be based on the link.")
            platform =  await platform_detection(link=link)
            logger.info(f"Detected platform: {platform}")

            if platform == "linkedin":
                logger.info("Running LinkedIn extraction pipeline")
                try:
                    logger.info(f"Extracting data from LinkedIn link: {link}")
                    extraction_results =  serper_search(keywords=link, country=country, pages=pages)
                    logger.info("LinkedIn data extraction completed")
                except Exception as e:
                    logger.error(f"Error during LinkedIn data extraction: {e}")
                    raise

                try:
                    logger.info("Processing extracted LinkedIn data through data pipeline")
                    processed_results = await data_pipeline(extraction_results)
                    logger.info("Data processing completed")
                    return processed_results
                except Exception as e:
                    logger.error(f"Error during data processing: {e}")
                    raise                
            elif platform == "instagram":
                logger.warning("Instagram extraction is not yet implemented")
                raise NotImplementedError("Instagram extraction feature is under development")
            
        elif keywords and not link:
            logger.info("No link provided. Running general search based on keywords.")
            try:
                logger.info(f"Searching for profiles with keywords: {keywords}")
                extraction_results =  serper_search(keywords=keywords, country=country, pages=pages)
                logger.info("General profile extraction completed")
            except Exception as e:
                logger.error(f"Error during general profile extraction: {e}")
                raise

            try:
                logger.info("Processing extracted profiles through data pipeline")
                processed_results = await data_pipeline(extraction_results, keywords=keywords.split())
                logger.info("Data processing completed")
                return processed_results
            except Exception as e:
                logger.error(f"Error during data processing: {e}")
                raise

        else:
            logger.warning("No valid input provided for lead sourcing.")
            raise ValueError("Either a link or keywords must be provided for lead sourcing.")
