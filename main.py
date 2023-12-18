from src.scraper import Crunchbase

crunchbase = Crunchbase()

crunchbase.initialize_driver()
crunchbase.get_funding_rounds()