from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

EC.element_to_be_clickable
url = 'https://www.golfbidder.co.uk/'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(2)
cookies_accept_button = driver.find_element("xpath", '//*[@id="onetrust-accept-btn-handler"]')
cookies_accept_button.click()


delay = 30
try:
    newsletter_button =  WebDriverWait(driver, delay).until(
        EC.presence_of_element_located(("xpath", '//*[@class="leadinModal-close"]'))
    )
    newsletter_button.click()
except TimeoutException:
    print("Took too much time for newsletter to appear")
#driver.find_element(By.LINK_TEXT,"Putters")
#driver.find_elements('xpath',"//a[contains(text(),'drivers')]")
#driver.find_elements(By.PARTIAL_LINK_TEXT,"//a[contains(text(),'drivers')]")
time.sleep(1)
try:
    wood_button_tuple = ('xpath',"//a[contains(@href,'/fairway.html') and contains(@href,'clubtype/')]")
    WebDriverWait(driver,delay).until(
        EC.element_to_be_clickable(wood_button_tuple)
        ).click()
except TimeoutException:
    print('Button never becomes visible')

product_gallery = driver.find_element('xpath','//div[contains(@class,"product-gallery")]')
products = product_gallery.find_elements('xpath',"div[contains(@class,'nth-')]")

names = product_gallery.find_elements('xpath','//h3[@class="product-name product-title-reposition"]')
price_tables = product_gallery.find_elements('xpath',"//table[@class='price-table']")
handicap_tables = product_gallery.find_elements('xpath','//img[contains(@class,"state-handicap")]')

wood_dict = {}
for name,price_table,handicap_table in zip(names,price_tables,handicap_tables):
    product_info = {}
    price_info = price_table.text.split('\n')
    price_info = [price.split(':') for price in price_info]
    n = len(price_info)
    product_info = {price[0].strip():price[1].strip() for price in price_info}
    product_info['H/C'] = int(handicap_table.get_attribute('data-handicap-max'))
    wood_dict[name.text] = product_info
    
driver.find_element('id','Vector_Smart_Object').click()

try:
    driver_button_tuple = ('xpath',"//a[contains(@href,'/drivers.html') and contains(@href,'clubtype/')]")
    WebDriverWait(driver,delay).until(
        EC.element_to_be_clickable(driver_button_tuple)
        ).click()
except TimeoutException:
    print('Button never becomes visible')