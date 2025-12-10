import asyncio
import logging
from typing import List, Dict

from genai_service.utils.scrapers import ScraperUtils
from genai_service.core.extraction import FieldExtractor, enrich_from_linkedin
from genai_service.core.enrichment_service import filter_profiles, lead_presentation, export

logger = logging.getLogger(__name__)

class LeadPipeline:
    """Main pipeline: Scrape → Extract → Enrich → Filter → Export"""
    
    def __init__(self):
        try:
            logger.info("Initializing ScraperUtils...")
            self.scraper = ScraperUtils()
            logger.info(" ScraperUtils initialized")
            
            logger.info("Initializing FieldExtractor...")
            self.extractor = FieldExtractor()
            logger.info("FieldExtractor initialized")
            
            logger.info(" Pipeline fully initialized")
        except Exception as e:
            logger.exception(f"Failed to initialize pipeline: {e}")
            raise
    
    async def process_linkedin_post(
        self, 
        profile_urls: List[str], 
        keywords: List[str] = None
    ) -> Dict:
        """
        Full pipeline for LinkedIn profiles
        
        Args:
            profile_urls: List of LinkedIn profile URLs
            keywords: Optional keywords for filtering
        
        Returns:
            {
                "success": bool,
                "leads": List[dict],
                "csv_file": str,
                "stats": {...}
            }
        """
        try:
            logger.info(f" Scraping {len(profile_urls)} LinkedIn profiles...")
            
            if not hasattr(self, 'scraper'):
                raise AttributeError("Scraper not initialized! Check __init__ method")
            
            scrape_result = self.scraper.linkedin_scraper(profile_urls)
            
            if not scrape_result.get("success"):
                logger.error(f"Scraping failed: {scrape_result.get('error')}")
                return {"success": False, "error": scrape_result.get("error")}
            
            raw_profiles = scrape_result.get("profiles", [])
            logger.info(f"✓ Scraped {len(raw_profiles)} profiles successfully")
            
            if len(raw_profiles) == 0:
                return {
                    "success": False, 
                    "error": "No profiles scraped. Check if URLs are valid."
                }
            
            logger.info("Extracting and enriching profile data...")
            enriched_profiles = []
            
            for i, raw_profile in enumerate(raw_profiles, 1):
                logger.info(f"  Processing profile {i}/{len(raw_profiles)}")
                try:
                    enriched = await enrich_from_linkedin(raw_profile)
                    if enriched.get('name'):  # Only keep valid profiles
                        enriched_profiles.append(enriched)
                        logger.info(f"    ✓ Enriched: {enriched.get('name')}")
                    else:
                        logger.warning(f"    ⚠ Skipped profile (no name found)")
                except Exception as e:
                    logger.warning(f"    ✗ Failed to enrich profile: {e}")
            
            logger.info(f"✓ Successfully enriched {len(enriched_profiles)}/{len(raw_profiles)} profiles")
            
            if len(enriched_profiles) == 0:
                return {
                    "success": False,
                    "error": "No profiles could be enriched. Check extraction logic."
                }
            
            if keywords:
                logger.info(f" Scoring profiles with keywords: {keywords}")
                filtered = await filter_profiles(enriched_profiles, keywords)
                logger.info(f"✓ {len(filtered)}/{len(enriched_profiles)} profiles passed threshold")
            else:
                logger.info(" No keywords provided, skipping filtering")
                filtered = enriched_profiles
            
            # Step 4: Format leads
            logger.info("Formatting final leads...")
            final_leads = lead_presentation(filtered)
            logger.info(f"✓ Formatted {len(final_leads)} leads")
            
            logger.info(" Exporting to CSV...")
            csv_file = await export(final_leads)
            logger.info(f"✓ Exported to: {csv_file}")
            
            return {
                "success": True,
                "leads": final_leads,
                "csv_file": csv_file,
                "stats": {
                    "scraped": len(raw_profiles),
                    "enriched": len(enriched_profiles),
                    "filtered": len(filtered),
                    "exported": len(final_leads)
                }
            }
            
        except Exception as e:
            logger.exception(f"❌ Pipeline error: {e}")
            return {"success": False, "error": str(e)}


async def main():
    """Test the pipeline"""
    print("\n" + "="*70)
    print("TESTING LEAD PIPELINE")
    print("="*70 + "\n")
    
    try:
        print("Initializing pipeline...")
        pipeline = LeadPipeline()
        print("✓ Pipeline initialized\n")
        
        test_urls = [
            "https://www.linkedin.com/in/cindy-otieno-bb2b9a195/",
            "https://www.linkedin.com/in/brendah-patrick/"
        ]
        
        print(f"Testing with {len(test_urls)} URLs:")
        for url in test_urls:
            print(f"  • {url}")
        print()
        
        keywords = ["software", "engineer", "data"]
        print(f"Keywords for scoring: {keywords}\n")
        
        print("-"*70)
        print("RUNNING PIPELINE...")
        print("-"*70 + "\n")
        
        result = await pipeline.process_linkedin_post(test_urls, keywords)
        
        print("\n" + "-"*70)
        print("RESULTS")
        print("-"*70 + "\n")
        
        if result["success"]:
            print("✅ PIPELINE COMPLETED SUCCESSFULLY!\n")
            
            stats = result['stats']
            print(f"📊 Statistics:")
            print(f"   Profiles scraped:  {stats['scraped']}")
            print(f"   Profiles enriched: {stats['enriched']}")
            print(f"   Profiles filtered: {stats['filtered']}")
            print(f"   Leads exported:    {stats['exported']}")
            print(f"\n📄 CSV file: {result['csv_file']}\n")
            
            if result['leads']:
                print(f"📋 Sample Leads (showing first 3):\n")
                for i, lead in enumerate(result['leads'][:3], 1):
                    print(f"  Lead #{i}:")
                    print(f"    Name:       {lead.get('name', 'N/A')}")
                    print(f"    Role:       {lead.get('current_role', 'N/A')}")
                    print(f"    University: {lead.get('education', 'N/A')}")
                    print(f"    Country:    {lead.get('country', 'N/A')}")
                    print(f"    Email:      {lead.get('email', 'N/A')}")
                    print(f"    Score:      {lead.get('score', 0)}/10")
                    print()
        else:
            print("❌ PIPELINE FAILED\n")
            print(f"Error: {result.get('error', 'Unknown error')}\n")
        
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}\n")
        logger.exception("Fatal error in main()")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    asyncio.run(main())