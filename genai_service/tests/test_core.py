import os
import pytest
from utils.data_wrangling import email_generator, clean_company_name, export

# --- TEST 1: Company Name Cleaning ---
def test_clean_company_name():
    """
    Does it correctly strip legal jargon?
    """
    assert clean_company_name("Tesla Motors, Inc.") == "teslamotors"
    assert clean_company_name("Microsoft Corporation") == "microsoft"
    assert clean_company_name("  Google LLC  ") == "google"
    assert clean_company_name("Unknown") == "" 

def test_email_generator_company():
    """
    Priority 1: Company Email
    """
    profile = {
        "name": "Elon Musk",
        "company": "Tesla Inc"
    }
    assert email_generator(profile) == "elon.musk@tesla.com"

def test_email_generator_university():
    """
    Priority 2: University Email (when company is missing)
    """
    profile = {
        "name": "Mark Z",
        "company": "", 
        "education": "Harvard University"
    }
    assert email_generator(profile) == "mark.z@harvard.edu"

def test_email_generator_fallback():
    """
    Priority 3: Fallback to Gmail
    """
    profile = {
        "name": "John Doe",
        "company": "Self-Employed",
        "education": ""
    }
    assert email_generator(profile) == "john.doe@gmail.com"

@pytest.mark.asyncio
async def test_export_creates_file():
    """
    Does the export function actually create a file?
    """
    data = [
        {"name": "Test User", "email": "test@test.com", "score": 10}
    ]
    
    filename = await export(data)
    
    assert filename == "leads.csv"
    assert os.path.exists("leads.csv")
    
    if os.path.exists("leads.csv"):
        os.remove("leads.csv")