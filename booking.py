import argparse
from _datetime import datetime, timedelta
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import sys
import os

# argparse working only with default args, because of different structure booking.com
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--rooms', type=str)
parser.add_argument('-a', '--adults', type=str)
parser.add_argument('-c', '--children', type=str)
options = parser.parse_args()

if options.rooms is None:
    options.rooms = '1'
if options.adults is None:
    options.adults = '2'
if options.children is None:
    options.children = '0'

DESTINATION = 'Самара, Самарская область, Россия'
ROOM_NUM = options.rooms
ADULT_NUM = options.adults
CHILDREN_NUM = options.children
MAX_PRICE = 6800


def init_chrome_driver():
    directory = os.path.abspath(os.path.dirname(__file__))
    if os.name == 'nt':
        chrome_driver = '\chromedriver.exe'
    else:
        sys.exit('Program works on windows only.')
    driver = webdriver.Chrome(directory + chrome_driver)
    driver.maximize_window()
    return driver


class WebPage:
    def __init__(self, url):
        self.url = url
        self.driver = init_chrome_driver()

        self.now = datetime.now()
        self.day = self.now.strftime('%d')
        self.month = self.now.strftime('%m')
        self.year = self.now.strftime('%Y')

        self.after_four_days = datetime.now() + timedelta(days=4)
        self.day_after = self.after_four_days.strftime('%d')
        self.month_after = self.after_four_days.strftime('%m')
        self.year_after = self.after_four_days.strftime('%Y')

        try:
            self.driver.get(self.url)

        except:
            self.driver.quit()
            sys.exit('Invalid URL address.')

    def quit_driver(self):
        self.driver.quit()

    def take_screenshot(self):
        self.driver.save_screenshot('screenshot.png')

    def search_hotels(self):
        self.driver.find_element_by_name('ss').send_keys(DESTINATION)

        self.driver.find_element_by_name('checkin_month').send_keys(self.month)
        self.driver.find_element_by_name('checkin_monthday').send_keys(self.day)
        self.driver.find_element_by_name('checkin_year').send_keys(self.year)

        self.driver.find_element_by_name('checkout_month').send_keys(self.month_after)
        self.driver.find_element_by_name('checkout_monthday').send_keys(self.day_after)
        self.driver.find_element_by_name('checkout_year').send_keys(self.year_after)

        Select(self.driver.find_element_by_name('no_rooms')).select_by_value(ROOM_NUM)
        Select(self.driver.find_element_by_name('group_adults')).select_by_value(ADULT_NUM)
        Select(self.driver.find_element_by_name('group_children')).select_by_value(CHILDREN_NUM)

        self.driver.find_element_by_class_name('sb-searchbox__button').click()

        self.driver.find_element_by_xpath("//a[@data-title='{}']".format(DESTINATION)).click()
        self.driver.find_element_by_xpath("//a[@data-id='pri-2']").click()
        # self.driver.find_element_by_xpath("//a[@data-id='oos-1']").click()

    def get_hotels_from_page(self, existing_hotels={}):
        time.sleep(5)
        new_hotels = {}

        # With different site structure
        # or hotel_el.find_element_by_class_name('site_price').text

        for hotel_el in self.driver.find_elements_by_css_selector("div[data-hotelid]"):
            try:
                while hotel_el.find_element_by_class_name('price').text == '':
                    ActionChains(self.driver).move_to_element(hotel_el).perform()
                    time.sleep(0.2)
            except:
                continue

            hotel_id = hotel_el.get_attribute('data-hotelid')
            hotel_name = hotel_el.find_element_by_class_name('sr-hotel__name').text
            hotel_price = int(''.join(filter(str.isdigit, hotel_el.find_element_by_class_name('price').text)))
            hotel_link = hotel_el.find_element_by_class_name('hotel_name_link').get_attribute('href')

            if (hotel_price/4) > MAX_PRICE:
                continue

            try:
                hotel_score = float(hotel_el.get_attribute('data-score'))
            except:
                continue

            new_hotels[hotel_id] = [hotel_name, hotel_price, hotel_score, hotel_link]

        existing_hotels.update(new_hotels)

        try:
            pagination = self.driver.find_element_by_class_name('results-paging')
            next_el = pagination.find_element_by_class_name('paging-next')
            if next_el:
                next_el.click()
                self.get_hotels_from_page(existing_hotels)
        except:
            pass

        return existing_hotels

    def get_result_page(self, hotel_url):
        try:
            self.driver.get(hotel_url)
        except:
            self.driver.quit()
            sys.exit('Invalid URL address.')
        self.take_screenshot()

    def get_most_popular(self, hotels):
        best_hotel = {}
        try:
            best_choice = next(iter(hotels.items()))
        except StopIteration:
            self.quit_driver()
            sys.exit('No available hotels.')
        for hotel_id, hotel_description in hotels.items():
            if best_choice[1][2] < hotel_description[2]:
                best_choice = [hotel_id, hotel_description]

        best_hotel[best_choice[0]] = best_choice[1]

        return best_hotel

    def get_hotel_url(self, best_hotel):
        for hotel_id, hotel_description in best_hotel.items():
            return hotel_description[3]


if __name__ == '__main__':
    try:
        wp = WebPage('http://www.booking.com')
        wp.search_hotels()
        hotels = wp.get_hotels_from_page()
        best_hotel = wp.get_most_popular(hotels)
        hotel_url = wp.get_hotel_url(best_hotel)
        wp.get_result_page(hotel_url)
        wp.quit_driver()
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(1)