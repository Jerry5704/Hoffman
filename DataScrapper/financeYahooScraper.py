# ToDo: 
# 1) Change all time.sleep to something more civilized like WebDriverWait

import requests
import time
import configparser

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from DataHandler.configParser import configParser

class financeYahooScraper():

    def get_url(self, index, start, finish):
        return f"https://finance.yahoo.com/quote/%5E{index}/history?period1={start}&period2={finish}&interval=<frequency>&filter=history&frequency=1d&includeAdjustedClose=true&guccounter=1"

    def get_configParser(self):
        configParser = configparser.RawConfigParser()   
        configFilePath = r'config.cfg'
        configParser.read(configFilePath)
        return configParser

    def get_driver(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        return driver

    def get_past_popups(self):
        # click consent button
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//button[@type='submit' and @value='agree']").click()

        # click redirect button
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'here').click()

        # click close button
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//button[@aria-label='Close']").click()

    def is_page_end(self):
        if "Loading more data..." in self.get_raw_data().text:
            return False
        return True

    def scroll_down(self):
        while(not self.is_page_end()):
            self.driver.execute_script("window.scrollTo(0, 50000)")

    def get_raw_data(self):
        time.sleep(1)
        return self.driver.find_element(By.ID, "Col1-1-HistoricalDataTable-Proxy")

    def __init__(self, index, start, finish):
        # Setup for finance.yahoo.com scraping
        self.configParser = self.get_configParser()
        self.url = self.get_url(index, start, finish)
        self.driver = self.get_driver()
        self.get_past_popups()
        self.scroll_down()

        # Data parse
        self.raw_data = self.get_raw_data().text

        self.driver.quit()
