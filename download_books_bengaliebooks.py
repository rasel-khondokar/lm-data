import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from icecream import ic
import os
import sys
import uuid

from app_configs.common import DIR_REPORT


class PDFDownloader:
    def __init__(self, driver_path, base_dir):
        unique_dir = str(uuid.uuid4())
        self.download_directory = os.path.join(base_dir, unique_dir)
        os.makedirs(self.download_directory, exist_ok=True)

        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": self.download_directory,
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True
        })
        chrome_options.add_extension(f"{os.getcwd()}/ublock_origin.crx")
        self.driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
        self.delay = 11

    def click_to_btn_js(self, driver, btn):
        driver.execute_script("arguments[0].click();", btn)

    def wait_for_download(self, timeout):
        seconds = 0
        dl_wait = True
        while dl_wait and seconds < timeout:
            time.sleep(1)
            dl_wait = False
            for fname in os.listdir(self.download_directory):
                if fname.endswith('.crdownload'):
                    dl_wait = True
            seconds += 1
        return not dl_wait

    def download_from_opened(self, file_count_old):
        file_count = len(os.listdir(self.download_directory))
        if file_count > file_count_old:
            return False
        else:
            css_download_btn = '#download'
            WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_download_btn)))
            download_btn = self.driver.find_element(By.CSS_SELECTOR, css_download_btn)
            self.click_to_btn_js(self.driver, download_btn)
            return True

    def get_book(self, url):
        file_count = len(os.listdir(self.download_directory))
        self.driver.get(url)
        css_download_btn = '.wp-block-button__link.has-background'
        WebDriverWait(self.driver, self.delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_download_btn)))
        download_btn = self.driver.find_element(By.CSS_SELECTOR, css_download_btn)
        with open('REPORT/download_url.txt', 'a') as file:
            file.write(f'{download_btn.get_attribute("href")}\n')
        self.click_to_btn_js(self.driver, download_btn)
        self.wait_for_download(300)

    def close_driver(self):
        self.driver.quit()


if __name__ == "__main__":
    # replace these with your chromedriver path and output directory
    path_to_chromedriver = f'{os.getcwd()}/chromedriver_linux64/chromedriver'
    output_directory = f'{os.getcwd()}/output'
    os.makedirs(output_directory, exist_ok=True)

    downloader = PDFDownloader(path_to_chromedriver, output_directory)

    urls = []
    with open(sys.argv[1]) as f:
        for line in f:
            if line != '\n':
                urls.append(line)

    report_file_failed_url = f'{DIR_REPORT}page_scraped_failed_url.txt'
    report_file_success_url = f'{DIR_REPORT}page_scraped_success_url.txt'
    urls = set(urls)
    for url in urls:
        try:
            downloader.get_book(url)
            print(f'{datetime.datetime.now()} : Successfully downloaded book from {url}')
            with open(report_file_success_url, 'a') as file:
                file.write(f'{url}\n')
        except Exception as e:
            print(f'{datetime.datetime.now()} : Failed to download book from {url} due to {e}')
            with open(report_file_failed_url, 'a') as file:
                file.write(f'{url}\n')
