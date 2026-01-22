import asyncio
import logging
from ..utils.llm_client import platform_detection

logger = logging.getLogger(__name__)


# Main extraction class
class FieldExtractor:
    def __init__(self, link:str):
        self.link = link
        logger.info("FieldExtractor initialized")

    async def serper_extractor(self,keywords):
        from ..utils.serper import serper_search
        serper_results = await serper_search(keywords=keywords, country="ke", pages=1)
        return serper_results
    
    def instagram_extractor(self):
        from ..utils.instagram import instagram_output
        instagram_results = instagram_output()
        return instagram_results
    
class MainPipeline():
    def __init__(self, link):
        self.link = link
        logger.info("Main Pipeline initialized")
        

    def run_pipeline(self):
        extractor = FieldExtractor(link=self.link)
        platform = asyncio.run(platform_detection(self.link))
        logger.info(f"Detected platform: {platform}")

        if platform == "linkedin":
            logger.info("Running LinkedIn extraction pipeline")
            extraction_results = asyncio.run(extractor.serper_extractor(self.link))
            return extraction_results
        elif platform == "instagram":
            extraction_results = asyncio.run(extractor.instagram_extractor())
            return extraction_results
        else:
            logger.warning("Unsupported platform for extraction")
            return None
