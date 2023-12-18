from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from itertools import repeat

class Crunchbase:

    def __init__(self):
        self.__loggedIn = False
        self.__driver = None
        self.__useragentarray = [ 
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", 
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", 
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1"
        ] 
        self.__curAgentIdx = 2

    def initialize_driver(self):
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False)
        self.__driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)
        self.__driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": self.__useragentarray[self.__curAgentIdx]})
    
    def change_agent(self):
        self.__curAgentIdx = (self.__curAgentIdx + 1) % 6
        self.__driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": self.__useragentarray[self.__curAgentIdx]})

    def next_page(self):
        next_button = self.__driver.find_element(By.CLASS_NAME, "page-button-next")
        if next_button.is_enabled():
            next_button.click()
            return True
        return False
        
    def get_page_funding_rounds(self):

        def get_transaction(row):
            a_element = row.find_element(By.XPATH, "grid-cell[2]/div/field-formatter/identifier-formatter/a")
            link = a_element.get_attribute('href')
            transaction_name = link.split('/')[-1]
            return transaction_name
        
        def get_organization(row):
            a_element = row.find_element(By.XPATH, "grid-cell[3]/div/field-formatter/identifier-formatter/a")
            link = a_element.get_attribute('href')
            organization_name = link.split('/')[-1]
            return organization_name
        
        def get_funding_type(row):
            element = row.find_element(By.XPATH, "grid-cell[4]/div/field-formatter/span")
            funding_type = element.text
            return funding_type
        
        def get_announced_date(row):
            element = row.find_element(By.XPATH, "grid-cell[5]/div/field-formatter/span")
            announced_date = element.text
            return announced_date
        
        def get_money_raised(row):
            element = row.find_element(By.XPATH, "grid-cell[6]/div/field-formatter/span")
            money_raised = element.text
            return money_raised
        
        def get_investor_names(row):
            element = row.find_element(By.XPATH, "grid-cell[7]/div/field-formatter/identifier-multi-formatter/span")
            a_elements = element.find_elements(By.TAG_NAME, 'a')
            investors = ""
            if not a_elements:
                return investors
            for a in a_elements:
                link = a.get_attribute('href')
                investors = investors + ", " + link.split('/')[-1]
            return investors

        def get_funding_stage(row):
            element = row.find_element(By.XPATH, "grid-cell[8]/div/field-formatter/span")
            funding_stage = element.text
            return funding_stage
        
        def get_total_funding_amount(row):
            element = row.find_element(By.XPATH, "grid-cell[9]/div/field-formatter/span")
            funding_amount = element.text
            return funding_amount
        
        def get_organization_industries(row):
            element = row.find_element(By.XPATH, "grid-cell[10]/div/field-formatter/identifier-multi-formatter/span")
            a_elements = element.find_elements(By.TAG_NAME, 'a')
            categories = ""
            if not a_elements:
                return categories
            for a in a_elements:
                link = a.get_attribute('href')
                categories = categories + ", " + link.split('/')[-1]
            return categories

        rows = self.__driver.find_elements(By.TAG_NAME, "grid-row")
        transactions, organizations, funding_types, announced_dates, money_raised, investor_names, funding_stage, total_funding_amount, organization_industries = map(lambda x: list(x), repeat([], 9))
        
        for row in rows:
            transactions.append(get_transaction(row))
            organizations.append(get_organization(row)) 
            funding_types.append(get_funding_type(row)) 
            announced_dates.append(get_announced_date(row)) 
            money_raised.append(get_money_raised(row)) 
            investor_names.append(get_investor_names(row)) 
            funding_stage.append(get_funding_stage(row)) 
            total_funding_amount.append(get_total_funding_amount(row))
            organization_industries.append(get_organization_industries(row))

        data = pd.DataFrame({
                "transaction_name": transactions,
                "organization_name": organizations, 
                "funding_type": funding_types, 
                "announced_date": announced_dates, 
                "money_raised": money_raised, 
                "investor_names": investor_names, 
                "funding_stage": funding_stage, 
                "total_funding_amount": total_funding_amount,
                "organization_industries": organization_industries
            })
        return data
        
    def get_funding_rounds(self):
        start_page = 1
        end_page = 100 # Change to how many pages you want to collect
        url = f"https://www.crunchbase.com/discover/funding_rounds"
        
        self.__driver.get(url=url)

        time.sleep(5.3)

        while start_page <= end_page:

            time.sleep(5.1)

            self.__funding_data = pd.read_csv("./data/funding_rounds.csv")

            data = self.get_page_funding_rounds()

            self.__funding_data = pd.concat([self.__funding_data, data], ignore_index=True)
            self.__funding_data.to_csv('./data/funding_rounds.csv', index=False)

            print(f"Page {start_page} collected.")
            start_page += 1

            time.sleep(3.1)

            got_next_page = self.next_page()
            
            if got_next_page is False:
                print("Error: couldn't get next page.")
                break
            
        self.__driver.quit()