from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from scraping.common.action_element import ActionPerformer
from scraping.common.helpers import Helpers
from utils.error_handling import ErrorLogger

class BookScraper:
    def __init__(self, site):
        self.helpers = Helpers()
        self.this_filename = '_'.join(__file__.split('/')[-2:])[:-3]
        self.error_logger = ErrorLogger(self.this_filename)
        self.action = ActionPerformer(self.error_logger)
        self.site = site
        self.last_page_no = 489

    def scrape(self, driver):
        for pn in range(1, self.last_page_no+1):
            # driver = self.helpers.multiple_request_to_page(driver,
            #                                                f'{self.site}page/{pn}/')
            driver.get(f'{self.site}page/{pn}/')
            books_url = [url.get_attribute("href") for url in driver.find_elements(By.CSS_SELECTOR, '.ep_popular_post_item.ep_books_filter_target_item > a')]
            for url in books_url:
                driver.get(f'{url}')
                # driver = self.helpers.multiple_request_to_page(driver,
                #                                                f'{url.get_attribute("href")}')
                download_btn_css = '.download_btn.has_sub_btns'
                download_btn = driver.find_element(By.CSS_SELECTOR, f'{download_btn_css} a')
                self.action.click_to_btn_js(driver, download_btn)
                as_pdf_btn = driver.find_element(By.CSS_SELECTOR, f'{download_btn_css} ul.sub_btns li a')
                self.action.click_to_btn_js(driver, as_pdf_btn)
                book_download_btn_css = '#bookDwonload'
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,book_download_btn_css)))
                book_download_btn = driver.find_element(By.CSS_SELECTOR, f'{book_download_btn_css}')
                self.action.click_to_btn_js(driver, book_download_btn)
                print(0)

