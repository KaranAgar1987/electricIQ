import unittest
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from app.pages.home import *
from pandas._testing import *
from parameterized import parameterized
from util import *


@select_env(driver=Driver.CROME,headless=False)
class TestHome(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """ setup any state specific to the execution of the given class
        """
        cls.page = Home(cls.driver)
        cls.driver.get("https://mystifying-beaver-ee03b5.netlify.app/")
        cls.driver.maximize_window()
        cls.page.load_full_page()

    def setUp(self) -> None:
        self.driver.get("https://mystifying-beaver-ee03b5.netlify.app/")
        self.page.load_full_page()

    # Tests to check if page is loaded correctly
    def test_page_load(self):
        assert self.page.get_page_header() == "Cyber attack completely fake statistics"

    # Test to validate if all the relevant page elements exists
    def test_page_all_elements_visible(self):
        try:
            for ele in self.page.get_page_elements():
                ele.text
        except NoSuchElementException:
            raise NoSuchElementException

    #Testing filtering with valid string / blank / special characters
    @parameterized.expand(["S","","%s%"])
    def test_filtering_text_string_param(self, text):
        # Get complete data
        data = self.page.get_table_data()
        # Filter table and get updated data
        self.page.filter_data_by_text(text)
        act_data = self.page.get_table_data()

        # Apply manual filter and check implementation
        mask = data[data.columns].apply(
            lambda col: col.str.contains(
                text, na=False, case=False)).any(axis=1)
        exp_data = data[mask]
        assert_frame_equal(exp_data.reset_index(drop=True), act_data.reset_index(drop=True))

    # Testing filtering with numbers - Currently doesnt filter if pattern starts with number
    # Its valid bug which is marked as failure
    @unittest.expectedFailure
    def test_filtering_text_Numbers(self):
        # Get complete data
        data = self.page.get_table_data()

        # Filter table and get updated data
        self.page.filter_data_by_text("1.2")
        act_data = self.page.get_table_data()

        # Apply manual filter and check implementation
        mask = data[data.columns].apply(
            lambda col: col.str.contains(
                "1.2", na=False, case=False)).any(axis=1)
        exp_data = data[mask]
        assert_frame_equal(act_data.reset_index(drop=True), exp_data.reset_index(drop=True))

    # testing the sorting function for column - NAME
    def test_sort_column1_NAME(self):
        # Get complete data
        data = self.page.get_table_data()

        # Sort based on column Name
        self.page.sort_data_by_text("Name")
        fil_data = self.page.get_table_data()

        #Apply manual sort to dataframe based on name column
        fil_data.loc[:, "NAME"] = fil_data["NAME"].map(lambda x: x.lower())
        data.loc[:, "NAME"] = data["NAME"].map(lambda x: x.lower())
        data = data.sort_values("NAME")
        assert_frame_equal(fil_data.reset_index(drop=True), data.reset_index(drop=True))

    # testing the sorting function for column - Complexity
    #Test is marked as failed as the same
    @unittest.expectedFailure
    def test_sort_column2_complexity(self):
        # Get complete data
        data = self.page.get_table_data()
        cols = data.columns

        # Sort based on column Complexity
        self.page.sort_data_by_text("Complexity")
        act_data = self.page.get_table_data()

        # Apply manual sort to dataframe based on name complexity
        data.loc[:, "_COMPLEXITY"] = data["COMPLEXITY"].map({"low": 0, "medium": 1, "high": 2})
        data.loc[:, "_NAME"] = data["NAME"].map(lambda x: x.lower())
        data = data.sort_values("_COMPLEXITY")
        exp_data = data[cols]
        assert_frame_equal(exp_data.reset_index(drop=True), act_data.reset_index(drop=True))

    def test_filter_and_sort_column_Name(self):
        # Get complete data
        data = self.page.get_table_data()
        cols = data.columns

        # Filter and then Sort based on column Name
        self.page.filter_data_by_text("S")
        self.page.sort_data_by_text("Name")
        act_data = self.page.get_table_data()
        act_data.loc[:, "NAME"] = act_data["NAME"].map(lambda x: x.lower())

        mask = data[data.columns].apply(
            lambda col: col.str.contains(
                "S", na=False, case=False)).any(axis=1)
        fil_data = data[mask]

        fil_data.loc[:, "NAME"] = fil_data["NAME"].map(lambda x: x.lower())
        exp_data = fil_data.sort_values("NAME")
        assert_frame_equal(act_data.reset_index(drop=True), exp_data.reset_index(drop=True))

    @classmethod
    def tearDownClass(cls) -> None:
        """ Close driver
        """
        cls.driver.quit()