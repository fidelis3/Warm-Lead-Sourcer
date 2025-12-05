from langchain_core.output_parsers import StrOutputParser
from ..config.prompts import score_prompt
from ..utils.llm_client import core_model
import logging
import csv 

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

def email_generator(profile_data):
        try:
            logger.info("Generating email for profile: %s", profile_data)
            first_name, last_name = profile_data["name"][0].split(" ")
            university = profile_data["education"][0].lower()
            logger.info("Email generated successfully.")
            return f"{first_name}.{last_name}@{university}.edu"
        except Exception as e:
            logger.exception("Error generating email: %s", e)
            return ""
        

def calculate_score(profile, criteria) -> int: 
    try:
        score_chain =  score_prompt | core_model | StrOutputParser()
        score =  score_chain.ainvoke({
            "lead_information": profile,
            "keywords": criteria
        })
        logger.info("Calculated lead score: %s", score)
        return int(score)
    except Exception as e:
        logger.exception("Error calculating lead score: %s", e)
        return 0
    
async def export(profile_list):
    file_name = "leads.csv"
    try:
         column_names = ["Name", "LinkedIn URL", "Current Role", "University", "Country", "Email", "Score"]
         with open(file=file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(column_names)
            # Write profile data to csv
            for profile in profile_list:
                writer.writerow([
                    profile.get("name", ""),
                    profile.get("linkedin_url", ""),
                    profile.get("current_role", ""),
                    profile.get("education", ""),
                    profile.get("country", ""),
                    profile.get("email", ""),
                    profile.get("score", "")
                ])
         logger.info("CSV file created successfully: %s", file_name)
         return file_name
    except Exception as e:
        logger.exception("Error creating CSV file: %s", e)
        return
    


