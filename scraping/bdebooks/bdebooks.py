import datetime
import os
import re
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from app_configs.common import DIR_REPORT
from app_configs.constants import DELAY_LONG
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
        id_css = '.single_book_page_read_online_area_left'
        WebDriverWait(self.driver, DELAY_LONG).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, id_css)))

        text = self.driver.find_element(By.CSS_SELECTOR, id_css).get_attribute('innerHTML')
        id  = self.get_id(text)
        self.driver.get(f'https://storage2.bdebooks.com/{id}')

        # # self.multiple_request_to_page(f'{url}')
        # download_btn_css = '.download_btn.has_sub_btns'
        # download_btn = self.driver.find_element(By.CSS_SELECTOR, f'{download_btn_css} a')
        # self.action.click_to_btn_js(self.driver, download_btn)
        # as_pdf_btn = self.driver.find_element(By.CSS_SELECTOR, f'{download_btn_css} ul.sub_btns li a')
        # self.action.click_to_btn_js(self.driver, as_pdf_btn)
        # book_download_btn_css = '#bookDwonload'
        # time.sleep(11)
        # WebDriverWait(self.driver, DELAY_LONG).until(EC.presence_of_element_located((By.CSS_SELECTOR, book_download_btn_css)))
        # book_download_btn = self.driver.find_element(By.CSS_SELECTOR, f'{book_download_btn_css}')
        # self.action.click_to_btn_js(self.driver, book_download_btn)

    def multiple_request_to_page(self, url):
        max_err = 5
        count_err = 0
        while True:
            try:
                self.driver.get(url)
                break
            except:
                print(f'Failed to enter to the {url} !')
                time.sleep(5)
                if count_err > max_err:
                    break
                count_err += 1
                continue

    def scrape(self, driver):
        print(f'first page number : {self.first_page_no} \nlast page number : {self.last_page_no}')
        self.driver = driver
        for pn in range(self.first_page_no, self.last_page_no+1):
            print(f'page number : {pn} ')
            page_url = f'{self.site}page/{pn}/'
            with open(self.report_file , 'w') as file:
                file.write(str(pn))
            try:
                # self.multiple_request_to_page(page_url)
                driver.get(f'{page_url}')
                books_url = [url.get_attribute("href") for url in driver.find_elements(By.CSS_SELECTOR, '.ep_popular_post_item.ep_books_filter_target_item > a')]
                for url in books_url:
                    max_error = 3
                    c_error = 0
                    c_try = 0
                    file_count_old = len(os.listdir(self.download_dir))
                    print(f'books downloaded : {file_count_old}')
                    print(f'Download book from {url} ')
                    while True:
                        print(f'error : {c_error}, try : {c_try}')

                        if c_try>max_error:
                            with open(self.report_file_failed, 'a') as file:
                                file.write(f'{url}\n')
                            break

                        if c_error>max_error:
                            with open(self.report_file_failed, 'a') as file:
                                file.write(f'{url}\n')
                            break

                        try:
                            self.get_book(url)
                        except Exception as e:
                            c_error += 1
                            print(f'error count :  {c_error} ')
                            self.error_logger.logger.exception(e)
                            continue

                        file_count_new = len(os.listdir(self.download_dir))
                        if file_count_new>file_count_old:
                            break
                        else:
                            c_try += 1
                            print(f'try count :  {c_error} ')

            except Exception as e:
                self.error_logger.logger.exception(e)
                with open(self.report_file_failed, 'a') as file:
                    file.write(f'{page_url}\n')


    def scrape_single(self, driver):
        print(f'first page number : {self.first_page_no} \nlast page number : {self.last_page_no}')
        self.driver = driver
        for pn in range(self.first_page_no, self.last_page_no+1):
            print(f'page number : {pn} ')
            page_url = f'{self.site}page/{pn}/'
            with open(self.report_file , 'w') as file:
                file.write(str(pn))
            try:
                # self.multiple_request_to_page(page_url)
                driver.get(f'{page_url}')
                books_url = [url.get_attribute("href") for url in driver.find_elements(By.CSS_SELECTOR, '.ep_popular_post_item.ep_books_filter_target_item > a')]
                for url in books_url:
                    max_error = 3
                    c_error = 0
                    c_try = 0
                    file_count_old = len(os.listdir(self.download_dir))
                    print(f'books downloaded : {file_count_old}')
                    print(f'Download book from {url} ')
                    while True:
                        print(f'error : {c_error}, try : {c_try}')

                        if c_try>max_error:
                            with open(self.report_file_failed, 'a') as file:
                                file.write(f'{url}\n')
                            break

                        if c_error>1:
                            with open(self.report_file_failed, 'a') as file:
                                file.write(f'{url}\n')
                            break

                        try:
                            self.get_book(url)
                        except Exception as e:
                            c_error += 1
                            print(f'error count :  {c_error} ')
                            self.error_logger.logger.exception(e)
                            continue

                        file_count_new = len(os.listdir(self.download_dir))
                        if file_count_new>file_count_old:
                            break
                        else:
                            c_try += 1
                            print(f'try count :  {c_error} ')

            except Exception as e:
                self.error_logger.logger.exception(e)
                with open(self.report_file_failed, 'a') as file:
                    file.write(f'{page_url}\n')


    def scrape_book_urls(self, driver):
        print(f'first page number : {self.first_page_no} \nlast page number : {self.last_page_no}')
        self.driver = driver
        for pn in range(self.first_page_no, self.last_page_no+1):
            print(f'page number : {pn} ')
            page_url = f'{self.site}page/{pn}/'
            driver.get(f'{page_url}')
            book_url_css = '.ep_popular_post_item.ep_books_filter_target_item > a'
            time.sleep(DELAY_LONG)
            WebDriverWait(self.driver, DELAY_LONG).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, book_url_css)))
            books_url = [url.get_attribute("href") for url in driver.find_elements(By.CSS_SELECTOR, book_url_css)]
            with open('REPORT/books_url', 'a') as file:
                file.write(' \n'.join(books_url))






    def download_book_from_page(self):
        download_btn_css = '.download_btn.has_sub_btns'
        download_btn = self.driver.find_element(By.CSS_SELECTOR, f'{download_btn_css} a')
        self.action.click_to_btn_js(self.driver, download_btn)
        as_pdf_btn = self.driver.find_element(By.CSS_SELECTOR, f'{download_btn_css} ul.sub_btns li a')
        self.action.click_to_btn_js(self.driver, as_pdf_btn)
        book_download_btn_css = '#bookDwonload'
        time.sleep(11)
        WebDriverWait(self.driver, DELAY_LONG).until(EC.presence_of_element_located((By.CSS_SELECTOR, book_download_btn_css)))
        book_download_btn = self.driver.find_element(By.CSS_SELECTOR, f'{book_download_btn_css}')
        self.action.click_to_btn_js(self.driver, book_download_btn)

    def download_book(self, driver, url):
        file_count_old = len(os.listdir(self.download_dir))
        print(f'{datetime.datetime.now()} : books downloaded : {file_count_old}')
        print(f'Download book from {url} ')
        c_try = 0
        max_try = 5
        while True:
            print(f'try : {c_try}')
            if c_try > max_try:
                break
            try:
                driver.get(f'{url}')
                driver.maximize_window()
                time.sleep(DELAY_LONG)
                self.driver = driver
                self.get_book(url)
            except Exception as e:
                self.error_logger.logger.exception(e)
                with open(self.report_file_failed_url, 'a') as file:
                    file.write(f'{url}\n')
                c_try += 1
                continue
            files_new = os.listdir(self.download_dir)
            if len(files_new) > file_count_old:
                self.wait_until_download_finished()
                with open(self.report_file_success_url, 'a') as file:
                    file.write(f'{url}\n')
                break
            else:
                c_try += 1

    def wait_until_download_finished(self):
        c = 0
        max = 10
        print('downloading')
        while True:
            print('.', end=' ')
            if c>max:
                break
            downloading = False
            files = os.listdir(self.download_dir)
            for file in files:
                if 'Unconfirmed' in file:
                    downloading = True
                    break
            if downloading:
                time.sleep(DELAY_LONG)
                c+=1
            else:
                break
