import os
import time

from app_configs.constants import DELAY_LONG
from scraping.bdebooks.bdebooks import BookScraper
from scraping.common.scraping_driver import ScrapingDriver
from utils.common import load_arguments

download_dir = f'{os.getcwd()}/downloads'
os.makedirs(download_dir, exist_ok=True)
MAIN_SITE = 'https://bdebooks.com/books/'
book_scraper = BookScraper(MAIN_SITE, download_dir, 1, 489)
scraping_driver = ScrapingDriver()
prefs = {
    'download.default_directory': download_dir,
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': True
}
scraping_driver.option.add_experimental_option('prefs', prefs)
scraping_driver.download_driver()
driver = scraping_driver.execute_driver()
args = load_arguments()
# book_scraper.download_book(driver, args.book_url)
book_scraper.download_book(driver, args.book_url)



