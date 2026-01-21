from llm_client import calculate_score
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
            logger.info("Generating email for profile: %s", profile_data["name"])
            first_name, last_name = profile_data["name"].lower().split(" ", 1)  # FIX: Handle names with more than 2 parts
            if " " in last_name:  # If last_name has spaces, take the last word
                last_name = last_name.split()[-1]
            university = profile_data["education"].replace(" ", "").lower()
            email = f"{first_name}.{last_name}@{university}.edu"
            logger.info("Email generated successfully.")
            return email
        except Exception as e:
            logger.exception("Error generating email: %s", e)
            return "noemail@generated.edu"
        
    
async def filter_profiles(profiles, keywords: list[str]):
    filtered_profiles = []
    threshold = 5  
    try:
        logger.info("Starting profile filtering process.")
        for profile in profiles:
            calculated_score = await calculate_score(profile=profile, criteria=keywords)
            logger.info("Profile: %s, Score: %d", profile.get("name", ""), calculated_score)
            profile["score"] = calculated_score
            if calculated_score >= threshold:
                filtered_profiles.append(profile)
        logger.info("Profile filtering completed successfully.")
    except Exception as e:
        logger.exception("Error during profile filtering: %s", e)
        return filtered_profiles
    return filtered_profiles

def lead_presentation(profiles_with_scores):
    final_leads = []
    try:
        logger.info("Formatting generated leads for presentation.")
        for lead in profiles_with_scores:
            lead["email"] = email_generator(lead)
            final_leads.append(lead)
        logger.info("Leads formatted successfully.")
        return final_leads
    except Exception as e:
        logger.exception("Error formatting leads: %s", e)
        return final_leads

    
async def export(profile_list):
    file_name = "leads.csv"
    try:
         column_names = ["Name", "LinkedIn URL", "Current Role", "University", "Country", "Email", "Score"]
         with open(file=file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(column_names)
            for profile in profile_list:
                writer.writerow([  
                    profile.get("name", "Null"),
                    profile.get("linkedin_url", "Null"),
                    profile.get("current_role", "Null"),
                    profile.get("education", "Null"),
                    profile.get("country", "Null"),
                    profile.get("email", "Null"),
                    profile.get("score", "Null")
                ])
         logger.info("CSV file created successfully: %s", file_name)
         return file_name
    except Exception as e:
            logger.exception("Error creating CSV file: %s", e)
            return None  
