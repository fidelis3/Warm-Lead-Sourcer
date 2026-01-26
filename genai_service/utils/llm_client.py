from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import logging
import os
from ..config.prompts import platform_prompt, score_prompt, role_extraction_prompt

load_dotenv()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

DEFAULT_GENERAL_MODEL = "llama-3.3-70b-versatile"
DEFAULT_CORE_MODEL = "llama-3.3-70b-versatile"
DEFAULT_FALLBACK_MODEL ="llama-3.1-8b-instant"

try:
    logger.info("Setting up main Groq LLM model.")
    general_model_name = os.getenv("GENERAL_MODEL", DEFAULT_GENERAL_MODEL)
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY is not set in environment variables")
    
    general_model = ChatGroq(model=general_model_name, api_key=groq_api_key)
    logger.info(f"Successfully set up general model: {general_model_name}")
except Exception as e:
    logger.exception("Failed to set up general model. Switching to Fallback model")
    fallback_model_name = os.getenv("FALLBACK_MODEL", DEFAULT_FALLBACK_MODEL)
    general_model = ChatGroq(model=fallback_model_name, api_key=os.getenv("GROQ_API_KEY"))
    logger.info(f"Using fallback model: {fallback_model_name}")

try:
    logger.info("Setting up Groq LLM models.")
    core_model_name = os.getenv("CORE_MODEL", DEFAULT_CORE_MODEL)
    core_model = ChatGroq(model=core_model_name, api_key=os.getenv("GROQ_API_KEY"))
    logger.info(f"Successfully set up core logic model: {core_model_name}")
except Exception as e:
    logger.exception("Failed to set up core logic model. Switching to general model")
    core_model = general_model
    logger.info("Using general model as core model")


async def platform_detection(link: str) -> str:
    """Detect platform from URL"""
    try:
        platform_chain = platform_prompt | core_model | StrOutputParser()
        platform = await platform_chain.ainvoke({"link": link})
        logger.info("Detected platform: %s", platform)
        return platform.lower().strip()
    except Exception as e:
        logger.exception("Error detecting platform: %s", e)
        return "unknown"


async def calculate_score(profile: dict, criteria: list) -> int:
    """Calculate lead score (1-10) using LangChain chain"""
    try:        
        score_chain = score_prompt | core_model | StrOutputParser()
        result = await score_chain.ainvoke({
            "lead_information": str(profile),
            "keywords": criteria
        })
        return result.strip()
    except Exception as e:
        logger.exception(f"Error calculating score: {e}")
        return 5

async def profile_discovery(profile_snippets: list[dict]) -> str:
    """Extract roles and responsibilities from profile snippet"""
    try:
        role_chain = role_extraction_prompt | core_model | JsonOutputParser()
        logger.info(f"Extracting roles from {len(profile_snippets)} profile snippets...")
        result = await role_chain.ainvoke({
            "profile_snippet": profile_snippets
        })
        return result
    except Exception as e:
        logger.exception(f"Error extracting roles: {e}")
        return "Role not found"

if __name__ == "__main__":
    import asyncio
    async def trial():
        raw =  [{'title': 'Prof Dr Hiram Ndiritu - Principal College of Engineering and ...', 'subtitle': 'Kenya · Principal College of Engineering and Technology · Jomo Kenyatta University of Agriculture and Technology', 'link': 'https://ke.linkedin.com/in/hiram-ndiritu-0b17b91a', 'snippet': 'Lecturer in Mechanical Engineering. Teach Engineering Thermodynamics ... Jomo Kenyatta University of Agriculture and Technology (JKUAT) Graphic. Jomo ...', 'position': 1}, {'title': 'Callistus Owaka - A graduate Marine Engineer from JKUAT ...', 'subtitle': 'Kenya · Marine Engineer · Globology Limited', 'link': 'https://ke.linkedin.com/in/callistus-owaka-7716261a2', 'snippet': 'A graduate Marine Engineer from JKUAT and a Mechanical Engineering Specialist searching for open opportunities · I am an Engineer who has the skills, ...', 'position': 2}, {'title': 'Victor Maina - Mechanical Engineering Student (JKUAT)', 'link': 'https://ke.linkedin.com/in/victor-maina-806212307', 'snippet': 'Victor Maina. Mechanical Engineering Student (JKUAT) | Aspiring Mechanical Engineer | Hands-on with Cars, Trucks, EVs & Motorcycles | Automotive ...', 'position': 3}, {'title': 'Laura Simiyu - Registered graduate mechanical engineer', 'link': 'https://ke.linkedin.com/in/laura-simiyu-a41ab658', 'snippet': '... Mechanical engineering. I have good advocacy and analytical skills with a ... Jomo Kenyatta University of Agriculture and Technology (JKUAT) Graphic ...', 'position': 4}, {'title': 'Eric Thimu - Mechanical Engineer | Mantrac Kenya', 'subtitle': 'Kenya · Service Engineer · Mantrac Kenya', 'link': 'https://ke.linkedin.com/in/eric-thimu-669aa82b1', 'snippet': 'I hold a BSc in Mechanical Engineering from JKUAT and currently serve at Mantrac Kenya, where I specialize in maintenance and diagnostics of Caterpillar ...', 'position': 5}, {'title': 'Jean Wendo - Graduate Mechanical Engineer', 'subtitle': 'Nairobi, Nairobi County, Kenya · Operations Management Intern · Centum Investment Company Plc.', 'link': 'https://ke.linkedin.com/in/jean-wendo-1b29ab2aa', 'snippet': 'Jomo Kenyatta University of Agriculture and Technology (JKUAT). BSc. Mechanical Engineering Thermo-Fluid & Energy Engineering. 2020 - 2025. Activities and ...', 'position': 6}, {'title': 'Charles Kabutu - Mechanical Engineer', 'subtitle': 'Nairobi County, Kenya · Production and Maintenance Supervisor · FM Agricultural Stores Ltd', 'link': 'https://ke.linkedin.com/in/charles-kabutu', 'snippet': 'Mechanical Engineering Workshops and Training Programs. Jomo Kenyatta University of Agriculture and Technology (JKUAT). Jul 2019 - Aug 2019 2 ...', 'position': 7}, {'title': 'Eng. Jafeth Juma - Mechanical Engineer', 'subtitle': 'Kenya · Mechanical Engineer · Spada Engineering', 'link': 'https://ke.linkedin.com/in/eng-jafeth-juma-5b37baa1', 'snippet': 'Jomo Kenyatta University of Agriculture and Technology (JKUAT) Graphic. Jomo Kenyatta University of Agriculture and Technology. BSc Mechanical Engineering ...', 'position': 8}, {'title': 'HILLARY KOROS - Master of Science in Mechanical ...', 'subtitle': 'Kenya · Part-time Mechanical Engineering Lecturer · Jomo Kenyatta University of Agriculture and Technology', 'link': 'https://ke.linkedin.com/in/hillary-koros-3990374a', 'snippet': 'Master of Science in Mechanical Engineering · I am passionate about Mechanical Engineering ... Jomo Kenyatta University of Agriculture and Technology (JKUAT) ...', 'position': 9}, {'title': 'Mr Eng Omondi Phelix - Mechanical Engineer (GE)', 'subtitle': 'Nairobi County, Kenya · Mechanical Engineering Technician · Kenya Airports Authority', 'link': 'https://ke.linkedin.com/in/omondi-phelix-5b958b9b', 'snippet': 'I am a seasoned Mechanical Engineering Professional, boasting over 14 years of experience in the field. ... Jomo Kenyatta University of Agriculture and Technology ...', 'position': 10}]
        discovered_results = await profile_discovery(profile_snippets=raw)

        return discovered_results
        

    print(asyncio.run(trial()))

    