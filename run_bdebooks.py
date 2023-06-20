import os
import time
from app_configs.constants import DELAY_LONG
from scraping.bdebooks.bdebooks import BookScraper
from scraping.common.scraping_driver import ScrapingDriver

MAIN_SITE = 'https://bdebooks.com/books/'
def main():
    # Set download preferences
    download_dir = f'{os.getcwd()}/downloads'
    os.makedirs(download_dir, exist_ok=True)
    prefs = {
        'download.default_directory': download_dir,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    }
    scraping_driver = ScrapingDriver()
    scraping_driver.option.add_experimental_option('prefs', prefs)
    scraping_driver.download_driver()
    driver = scraping_driver.execute_driver()
    driver.get(f'{MAIN_SITE}')
    driver.maximize_window()
    time.sleep(DELAY_LONG)
    book_scraper = BookScraper(MAIN_SITE, download_dir)
    book_scraper.scrape(driver)

if __name__ == '__main__':
    main()