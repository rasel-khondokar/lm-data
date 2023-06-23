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


class PDFDownloader:
    def __init__(self, driver_path, base_dir):
        unique_dir = str(uuid.uuid4())
        self.download_directory = os.path.join(base_dir, unique_dir)
        os.makedirs(self.download_directory, exist_ok=True)

        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": self.download_directory,
            "download.prompt_for_download": False,
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

    def get_book(self, url):
        self.driver.get(url)
        download_btn_css = '.download_btn.has_sub_btns a'
        WebDriverWait(self.driver, self.delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, download_btn_css)))
        download_btn = self.driver.find_element(By.CSS_SELECTOR, download_btn_css)
        self.click_to_btn_js(self.driver, download_btn)
        as_pdf_btn = self.driver.find_element(By.CSS_SELECTOR, '.download_btn.has_sub_btns ul.sub_btns li a')
        self.click_to_btn_js(self.driver, as_pdf_btn)
        book_download_btn_css = '#bookDwonload'
        time.sleep(self.delay)
        WebDriverWait(self.driver, self.delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, book_download_btn_css)))
        book_download_btn = self.driver.find_element(By.CSS_SELECTOR, book_download_btn_css)
        ic(book_download_btn)
        self.click_to_btn_js(self.driver, book_download_btn)
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
            urls.append(line)

    for url in urls:
        try:
            downloader.get_book(url)
            print(f'Successfully downloaded book from {url}')
        except Exception as e:
            print(f'Failed to download book from {url} due to {e}')