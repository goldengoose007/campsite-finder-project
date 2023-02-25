import re
import requests
import time
from datetime import datetime, timedelta
import datetime
import operator
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage

# Text Message API
from twilio.rest import Client

account_sid = 'AC6dc17e1c24a57b10ce91ef94b57579fc'
auth_token = 'cb363de5b03fc4f4697a95fad6b68faa'
client = Client(account_sid, auth_token)


class HomePage(BasePage):
    path = '/'

    def is_on_page(self): 
        return "Reserve California" in self.driver.title 

    @property
    def book_online_button(self):
        return self.driver.find_element(By.XPATH, "//li[@id='menu-item-1603']//a[contains(text(),'Book Online')]")

    def click_book_online_button(self): 
        self.book_online_button.click()


class ReservationPage(BasePage):

    def is_on_page(self): 
        return "Check Availability for Riverside Campground" in self.driver.title 

    @property
    def check_in_field(self):
        return self.driver.find_element(By.XPATH, "//input[@id='Arrival']")

    @property
    def check_out_field(self):
        return self.driver.find_element(By.XPATH, "//input[@id='Departure']")

    @property
    def selection_box(self): 
        return self.driver.find_element(By.XPATH, "//div[@id='rs-select-dates']")

    @property
    def search_button(self): 
        return self.driver.find_element(By.XPATH, "//span[normalize-space()='Search']")

    def set_reservation_info(self, check_in_date, length_of_stay): 
        self.check_in_field.clear()
        self.check_in_field.send_keys(check_in_date)
        self.check_out_field.clear()

        # Set check_out_date date based on length_of_stay
        date_format = "%m/%d/%Y"
        date = datetime.datetime.strptime(check_in_date, date_format) # string parse time 
        offset = datetime.timedelta(days=int(length_of_stay)) # offset by length_of_stay
        new_date = date + offset 
        check_out_date = new_date.strftime(date_format) # string format time
        self.check_out_field.send_keys(check_out_date) 

        self.selection_box.click()
        self.search_button.click()
        time.sleep(2)

class CampsiteSelectionPage(BasePage):
    path = ''

    def is_on_page(self): 
        return "Select Your Accommodations" in self.driver.page_source

    def check_campsite_availability(self, check_in_date, campsite_number, length_of_stay, cell_number): 
        
        # Check if the campsite is available for the length of stay
        days = {} 
        for i in range(int(length_of_stay)):

            # Tries to find the element, if it can't it will throw an exception and move on to the next day
            try:
                days[i] = self.driver.find_element(By.XPATH, "//a[contains(text(), '" + campsite_number + "')]/../following-sibling::td["+ str(i+1) +"]//div[@class='rs-cell-content']").text 
            except:
                days[i] = None
        
        if all(value for value in days.values()): # All dates available 
            message = "The Camping trip for " + check_in_date + " with " + length_of_stay + " night stay at spot #" + campsite_number + " is available! \n\n"
            # Sends text message with Twilio
            for key, value in days.items():
                day_number = int(key) + 1
                if value:
                    message += "Night " + str(day_number) + " will cost " + value + " \n\n"
            message += "Do you want to book?"
            client.messages.create(
                body = message,
                from_ = '+18889088049', # your Twilio phone number
                to = cell_number # recipient's phone number
            )
        elif any(value for value in days.values()): # Some dates available 
            message = "Some night/s are available for " + check_in_date + " with a " + length_of_stay + " stay... Here is a list: \n\n"
            date_dt = datetime.datetime.strptime(check_in_date, "%m/%d/%Y")
            for key, value in days.items():
                day_number = int(key) + 1
                if value:
                    new_date = date_dt + timedelta(days=key)
                    formatted_date = new_date.strftime('%-m/%-d/%Y')
                    message += "Night #" + str(day_number) + " on " + str(formatted_date) + " is available and will cost " + value + " \n\n"
            message += "Do you want to book?"
            client.messages.create(
                body = message,
                from_ = '+18889088049', # your Twilio phone number
                to = cell_number # recipient's phone number
            )
        else: 
            print("No dates available for " + check_in_date + " with a " + length_of_stay + " stay...")


