from ..config.prompts import platform_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import logging
import os

load_dotenv()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

# We shall have multiple LLM models for different purposes
# llama-3.1 - general
# openai 120b - scoring logic/ complex tasks


# Implement extensive error handling for model initialization
try:
    logger.info("Setting up main Groq LLM model.")
    general_model = ChatGroq(model=os.getenv("GENERAL_MODEL"), api_key=os.getenv("GROQ_API_KEY"))
    logger.info("Successfully set up general model.")
except Exception as e:
    logger.exception("Failed to set up general model. Switching to Fallback model")
    general_model = ChatGroq(model=os.getenv("FALLBACK_MODEL"), api_key=os.getenv("GROQ_API_KEY"))

try:
    logger.info("Setting up Groq LLM models.")
    core_model = ChatGroq(model=os.getenv("CORE_MODEL"), api_key=os.getenv("GROQ_API_KEY"))
    logger.info("Successfully set up core logic model.")
except Exception as e:
    logger.exception("Failed to set up core logic model. Switching to general model", e)
    core_model = ChatGroq(model=os.getenv("FALLBACK_MODEL"), api_key=os.getenv("GROQ_API_KEY"))


async def platform_detection(link) -> str:
    try:
        platform_chain = platform_prompt | core_model | StrOutputParser()
        platform = await platform_chain.ainvoke({"link": link})
        logger.info("Detected platform: %s", platform)
        logger.exception("Error detecting platform")
    except Exception as e:
        logger.exception("Error detecting platform: %s", e)
        return "unknown"