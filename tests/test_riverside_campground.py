import pytest
import random

from pages.riverside_campground import *


CAMPING_TRIPS = [
    # date, length of stay, campsite number, cell phone number
    ("6/11/2023", "2", "14", "8053045884"), 
    # ("5/26/2023", "2", "15") 
]

class TestRiversideCampground:

    @pytest.mark.parametrize("check_in_date, length_of_stay, campsite_number, cell_number", CAMPING_TRIPS)
    def test_riverside_campground(self, browser, app_config, check_in_date, length_of_stay, campsite_number, cell_number):
        """ 
            If campsite is available on check_in_date and length of stay requested, then it will send me a text...
        """
        home_page = HomePage(driver=browser)
        reservation_selection_page = ReservationPage(driver=browser)
        campsite_selection_page = CampsiteSelectionPage(driver=browser)
        
        # Go to Riverside Campground home page and click "Book Online" button
        home_page.go(app_config.base_url_riverside_campground) 
        home_page.is_on_page()
        home_page.click_book_online_button()  

        # Fill out check-in and check-out and click on the search button
        reservation_selection_page.is_on_page()
        reservation_selection_page.set_reservation_info(check_in_date, length_of_stay)

        # Check if campsite number is available
        campsite_selection_page.is_on_page()
        campsite_selection_page.check_campsite_availability(check_in_date, campsite_number, length_of_stay, cell_number) 
        time.sleep(2)
