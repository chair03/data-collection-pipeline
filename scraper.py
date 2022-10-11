from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from typing import List


class golf_bidder_scraper:
    def __init__(self,url:str = 'https://www.golfbidder.co.uk/',clubs :List[str]=['drivers','iron_sets','fairway','putters','wedges','hybrids']) -> None:
        self.url = url
        self.clubs = clubs
        self.delay = 30
        self.driver = webdriver.Chrome()
        self.product_dicts = {}
        self.have_opened_website = False
        
    def open_website(self,cookies_accept_id:str = "'onetrust-accept-btn-handler'",newspaper_close_class:str = "'leadinModal-close'",delay:int = 30)->None:
        self.driver.get(self.url)
        cookies_accept_button = self.driver.find_element("xpath", "//button[@id="+cookies_accept_id+"]")
        cookies_accept_button.click()
        time.sleep(1)
        try:
            newsletter_button =  WebDriverWait(self.driver, delay).until(
            EC.presence_of_element_located(("xpath", '//*[@class="leadinModal-close"]'))
            )
            newsletter_button.click()
        except TimeoutException:
            print("Took too much time for newsletter to appear")
        self.have_open_website = True
        
    
    def get_club_products(self,club:str = 'Drivers'):
        if club not in self.clubs:
            raise ValueError(f'You must search a valid club, one of {self.clubs}')
        
        try:
            wood_button_tuple = ('xpath',f"//a[contains(@href,'/{club}.html') and contains(@href,'clubtype/')]")
            WebDriverWait(self.driver,self.delay).until(
                EC.element_to_be_clickable(wood_button_tuple)
                ).click()
        except TimeoutException:
            print('Button never becomes visible')

        product_gallery = self.driver.find_element('xpath','//div[contains(@class,"product-gallery")]')
        names = product_gallery.find_elements('xpath','//h3[@class="product-name product-title-reposition"]')
        price_tables = product_gallery.find_elements('xpath',"//table[@class='price-table']")
        club_dict = {}
        if club in ['Drivers','Woods','Irons','Hybrids']:
            handicap_tables = product_gallery.find_elements('xpath','//img[contains(@class,"state-handicap")]')
            for name,price_table,handicap_table in zip(names,price_tables,handicap_tables):
                product_info = {}
                price_info = price_table.text.split('\n')
                price_info = [price.split(':') for price in price_info]

                product_info = {price[0].strip():price[1].strip() for price in price_info}
                
                product_info['H/C'] = int(handicap_table.get_attribute('data-handicap-max'))
                club_dict[name.text] = product_info
            
            self.product_dicts[club] = club_dict
        else:
            
            for name,price_table in zip(names,price_tables):
                product_info = {}
                price_info = price_table.text.split('\n')
                price_info = [price.split(':') for price in price_info]

                product_info = {price[0].strip():price[1].strip() for price in price_info}

                club_dict[name.text] = product_info

        self.driver.find_element('id','Vector_Smart_Object').click()

    def scrape(self) -> None:
        if self.have_opened_website == False:
            self.open_website()
        for club in self.clubs:
            self.get_club_products(club)

if __name__ == '__main__':
    scraper = golf_bidder_scraper()
    scraper.scrape()

        
        
        