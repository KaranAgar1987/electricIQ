import enum
from enum import Enum
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Driver(enum.Enum):
    CROME = 0
    FIREFOX = 1
    SAFARI = 2

#Decorator to define driver and if the headless execution needs to happen
#This is just to demonstrate the selection of driver, havent added different versions
def select_env(*, driver: Driver, headless=False):
    def inner(cls):
        if headless:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        else:
            options = None
        if driver.CROME:
            cls.driver = webdriver.Chrome(executable_path="../drivers/chromedriver.exe", options=options)
        elif driver.FIREFOX:
            cls.driver = webdriver.Chrome(executable_path="../drivers/chromedriver.exe", options=options)
        else:
            cls.driver = webdriver.Chrome(executable_path="../drivers/chromedriver.exe", options=options)
        return cls
    return inner


