import json
import os
import time
from app_configs.constants import DELAY_LONG
from scraping.bengaliebook.bengaliebook import BookScraper
from scraping.common.scraping_driver import ScrapingDriver
from utils.common import load_arguments

MAIN_SITE = 'https://bengaliebook.com/bengali-books/'
def main():
    download_dir = f'{os.getcwd()}/downloads'
    os.makedirs(download_dir, exist_ok=True)
    scraping_driver = ScrapingDriver()
    scraping_driver.option.add_experimental_option('prefs', {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
    })
    # scraping_driver.option.add_extension(f"{os.getcwd()}/ublock_origin.crx")
    scraping_driver.download_driver()
    driver = scraping_driver.execute_driver()
    driver.get(f'{MAIN_SITE}')
    args = load_arguments()
    print(f'ARGS  : {json.dumps(args.__dict__, indent=2)}')
    book_scraper = BookScraper(MAIN_SITE, download_dir, 1, 197)
    book_scraper.scrape(driver)

if __name__ == '__main__':
    main()