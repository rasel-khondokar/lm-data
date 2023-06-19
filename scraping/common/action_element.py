import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class ActionPerformer:

    def __init__(self, error_logger):
        self.error_logger = error_logger

    def click_to_n_th_element_js(self, driver, css,n, xpath=None):
        try:
            btn = f"document.querySelectorAll('{css}')[{n}].click();"
            driver.execute_script(btn)
        except Exception as e:
            self.error_logger.exception(e)

    def move_cursor_to_element(self, driver, element):
        action = webdriver.ActionChains(driver)
        # action.move_to_element(element).release().perform()
        # action.move_to_element(element).click_and_hold().move_by_offset(0, 100).release().perform()
        action.move_to_element(element).move_by_offset(0, 100).release().perform()
        url = driver.find_element(By.CSS_SELECTOR, element)
        action.move_to_element(url).perform()

    def click_to_btn_js(self, driver, element):
        driver.execute_script('arguments[0].click();', element)
        time.sleep(3)

    def scroll_to_element(self, driver, el: WebElement):
        driver.execute_script("arguments[0].scrollIntoView(true);", el)
        time.sleep(3)

    def scroll_to_bottom(self, driver, scroll_pause_time):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        return driver

    def multiple_scroll_bottom(self, driver, n):
        for i in range(n):
            self.scroll_to_bottom(driver, 3)
    def scroll_down(self, driver, height):
        driver.execute_script(f"window.scrollBy(0,-{height})")
        time.sleep(3)
        return driver
    def scroll_up(self, driver, height):
        driver.execute_script(f"window.scrollBy(0,{height})")
        time.sleep(3)
        return driver

