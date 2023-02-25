import datetime
import operator
from random import randint
import re
import requests
import time
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

class BasePage(object):

    url = None

    def __init__(self, driver):
        self.driver = driver

    def go(self, base_url):
        if(self, base_url):
            url = base_url + self.path
            self.driver.get(url)
            self.wait_for_page_loaded()
        else: 
            time.sleep(10)
            url = base_url + self.path
            self.driver.get(url)
            self.wait_for_page_loaded()

    def wait_for_page_loaded(self):
        """
        Ionic Pages only: This should wait until the click block on the page isn't active
        """
        page_loaded = False
        while not page_loaded:
            try:
                WebDriverWait(self.driver, .5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.click-block-active")))
                page_loaded = False
            except TimeoutException:
                page_loaded = True

    # def riverside_campground_checkout_submit_order(self, test_env, checkout_page):

    #     PAY_BY ="cc"

    #     if test_env == 'prod':
    #         FNAME = "Scott"
    #         LNAME = "Langdon"
    #         PHONE = '8055551212'
    #         EMAIL = "brianscottlangdon@gmail.com"
    #         ADDRESS = "4325 Avenida Simi"
    #         ADDRESS2 = ""
    #         ZIP = "93063"
    #         CITY = "Simi Valley"
    #         STATE = "California"
    #         COUNTRY = "United States"

    #         # Credit Card Info
    #         NAME_ON_CARD = "Craig Clemens"
    #         CARD_TYPE = "Amex"
    #         CARD_NUM = ""
    #         EXP_MONTH = "11"  # mm
    #         EXP_YEAR = "2021"  # yyyy
    #         CVV2 = ""
            
    #         checkout_page.fill_in_form(PAY_BY, FNAME, LNAME, PHONE, EMAIL, ADDRESS, ADDRESS2, CITY, ZIP, STATE, COUNTRY, NAME_ON_CARD, CARD_TYPE, CARD_NUM, EXP_MONTH, EXP_YEAR, CVV2)
    #         checkout_page.submit_order()
        