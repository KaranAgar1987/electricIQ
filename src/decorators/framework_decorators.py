# Decorator to define driver and if the headless execution needs to happen
# This is just to demonstrate the selection of driver, havent added different versions
import webdriver_manager
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from src.FrameworkConstants.frameworkConstants import frameworkConstants
from tests.util import Driver


def select_env(*, driver: Driver, headless=False):
    def inner(cls):
        if headless:
            # TODO: "Add for headless execution"
            pass
        elif driver == driver.CROME:
            cls.driver = webdriver.Chrome(ChromeDriverManager(path=frameworkConstants.DRIVERPATH).install())
        elif driver == driver.FIREFOX:
            cls.driver = webdriver.Firefox(GeckoDriverManager(path=frameworkConstants.DRIVERPATH).install())
        else:
            cls.driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        return cls

    return inner
