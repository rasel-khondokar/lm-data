import datetime
import os
import re
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from app_configs.common import DIR_REPORT
from app_configs.constants import DELAY_LONG, DELAY_SHORT
from scraping.common.action_element import ActionPerformer
from scraping.common.helpers import Helpers
from utils.error_handling import ErrorLogger

class BookScraper:
    def __init__(self, site, download_dir,
                 start_page, end_page):
        self.helpers = Helpers()
        self.this_filename = '_'.join(__file__.split('/')[-2:])[:-3]
        self.error_logger = ErrorLogger(self.this_filename)
        self.action = ActionPerformer(self.error_logger)
        self.site = site
        self.download_dir = download_dir
        os.makedirs(DIR_REPORT, exist_ok=True)
        self.report_file = f'{DIR_REPORT}page_scraped.txt'
        self.report_file_failed = f'{DIR_REPORT}page_scraped_failed.txt'
        self.report_file_failed_url = f'{DIR_REPORT}page_scraped_failed_url.txt'
        self.report_file_success_url = f'{DIR_REPORT}page_scraped_success_url.txt'
        # try:
        #     with open(self.report_file) as file:
        #         self.first_page_no = int(file.read().strip())
        # except FileNotFoundError:

        self.first_page_no = start_page
        self.last_page_no = end_page

    def get_id(self, text):
        pattern = r"loadBookAjax\('.*?','(.*?)'\)"
        match = re.search(pattern, text)
        if match:
            found_string = match.group(1)
            return found_string
        else:
            return None

    def get_book(self, url):
        self.driver.get(f'{url}')
        css_download_btn = '.wp-block-button__link.has-background.wp-element-button'
        WebDriverWait(self.driver, DELAY_LONG).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_download_btn)))
        download_btn = self.driver.find_element(By.CSS_SELECTOR, css_download_btn)
        with open('REPORT/download_url.txt', 'a') as file:
            file.write(f'{download_btn.get_attribute("href")}\n')
        # self.action.click_to_btn_js(self.driver, download_btn)

    def multiple_request_to_page(self, url):
        max_err = 5
        count_err = 0
        while True:
            try:
                self.driver.get(url)
                return None
            except:
                time.sleep(2)
                if count_err > max_err:
                    break
                count_err += 1
                continue

        print(f'Failed to enter to the {url} !')

    def wait_for_download(self, timeout):
        seconds = 0
        dl_wait = True
        while dl_wait and seconds < timeout:
            time.sleep(1)
            dl_wait = False
            for fname in os.listdir(self.download_dir):
                if fname.endswith('.crdownload'):
                    dl_wait = True
            seconds += 1
        return not dl_wait
    def scrape(self, driver):
        print(f'first page number : {self.first_page_no} \nlast page number : {self.last_page_no}')
        self.driver = driver
        for pn in range(self.first_page_no, self.last_page_no+1):
            print(f'page number : {pn} ')
            page_url = f'{self.site}page/{pn}/'
            with open(self.report_file , 'w') as file:
                file.write(str(pn))
            try:
                # driver.get(f'{page_url}')
                self.multiple_request_to_page(page_url)
                css_books_urls = '.blog-entry-title.entry-title a'
                WebDriverWait(self.driver, DELAY_LONG).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css_books_urls)))
                books_url = [url.get_attribute("href") for url in driver.find_elements(By.CSS_SELECTOR, css_books_urls)]


                with open('REPORT/book_url.txt', 'a') as file:
                    file.write('\n'.join(books_url))

                for url in books_url:
                    max_error = 3
                    c_error = 0
                    file_count_old = len(os.listdir(self.download_dir))
                    print(f'books downloaded : {file_count_old}')
                    print(f'Download book from {url} ')
                    while True:
                        if c_error>max_error:
                            with open(self.report_file_failed, 'a') as file:
                                file.write(f'{url}\n')
                            break
                        try:
                            self.get_book(url)
                            time.sleep(DELAY_SHORT)
                        except Exception as e:
                            c_error += 1
                            print(f'error count :  {c_error} ')
                            self.error_logger.logger.exception(e)
                            continue
                        file_count_new = len(os.listdir(self.download_dir))
                        # if file_count_new>file_count_old:
                        #     self.wait_for_download(600)
                        break
            except Exception as e:
                self.error_logger.logger.exception(e)
                with open(self.report_file_failed, 'a') as file:
                    file.write(f'{page_url}\n')

