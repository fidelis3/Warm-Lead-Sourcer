from langchain_core.output_parsers import StrOutputParser
from ..config.prompts import score_prompt, platform_prompt
from ..utils.llm_client import score_model, core_model
import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


async def calculate_score(profile, criteria) -> int: 
    try:
        score_chain =  score_prompt | core_model | StrOutputParser()
        score = await score_chain.ainvoke({
            "lead_information": profile,
            "keywords": criteria
        })
        logger.info("Calculated lead score: %s", score)
        return int(score)
    except Exception as e:
        logger.exception("Error calculating lead score: %s", e)
        return 0
    
async def platform_detection(link) -> str:
    try:
        platform_chain = platform_prompt | core_model | StrOutputParser()
        platform = await platform_chain.ainvoke({"link": link})
        logger.info("Detected platform: %s", platform)
        return platform.lower()
    except Exception as e:
        logger.exception("Error detecting platform: %s", e)
        return "unknown"
    


