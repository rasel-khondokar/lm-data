import time

from selenium.webdriver.remote.webelement import WebElement

from app_configs.constants import DELAY_LONG


class Helpers:

    def multiple_request_to_page(self, driver, url):
        max_err = 5
        count_err = 0
        while True:
            try:
                driver.get(url)
                break
            except:
                print(f'Failed to enter to the {url} !')
                time.sleep(10)
                if count_err > max_err:
                    break
                count_err += 1
                continue
        return driver


    def scroll_to_element_js(self, driver, el: WebElement, scroll_pause_time=2):
        driver.execute_script('arguments[0].scrollIntoView(true);', el)
        time.sleep(scroll_pause_time)

    def scroll_to_bottom_js(self, driver, scroll_pause_time=2):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(scroll_pause_time)
        return driver

    def click_to_btn_js(self, driver, element):
        driver.execute_script('arguments[0].click();', element)

    def open_url_with_new_tab(self,driver, url):
        # open new tab
        driver.execute_script(f'window.open("{url}", "new_window")')
        # Switch to the tab
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(DELAY_LONG)

    def close_opened_new_tab(self, driver):
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(DELAY_LONG)

    def set_current_window(self, driver):
        self.current_window = driver.current_window_handle

    def keep_only_one_tab(self, driver, window_before):
        windows_after = driver.window_handles

        if len(windows_after) > 1:

            for i, w in enumerate(windows_after):
                driver.switch_to.window(w)
                if i != 0:
                    driver.close()

            driver.switch_to.window(window_before)
