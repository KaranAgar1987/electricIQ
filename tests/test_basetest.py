import unittest
from src.pages.home import *

class BaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """ setup any state specific to the execution of the given class
        """
        cls.page = Home(cls.driver)
        cls.driver.get("https://mystifying-beaver-ee03b5.netlify.app/")
        cls.driver.maximize_window()
        cls.page.load_full_page()

    @classmethod
    def tearDownClass(cls) -> None:
        """ Close driver
        """
        cls.driver.quit()