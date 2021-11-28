from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from collections import namedtuple
import pandas as pd


class Home:

    def __init__(self, driver):
        self.driver = driver
        self._filterData_txtBox_id = "filter-input"
        self._sort_dd_id = "sort-select"
        self._data_tbl_class = "table"
        self._data_tblHdr_class = "table-header"
        self._data_tblData_class = "table-content"

    def load_full_page(self):
        timeout = 5
        try:
            element_present = EC.presence_of_element_located((By.NAME, self._sort_dd_id))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")

    def get_page_elements(self):
        return [self.driver.find_element(By.ID, self._filterData_txtBox_id),
                self.driver.find_element(By.ID, self._sort_dd_id),
                self.driver.find_element(By.CLASS_NAME, self._data_tblData_class)]

    def filter_data_by_text(self, text):
        if self.driver.find_element(By.ID, self._filterData_txtBox_id):
            self.driver.find_element(By.ID, self._filterData_txtBox_id).send_keys(text)

    def sort_data_by_text(self, text=None):
        if self.driver.find_element(By.NAME, self._sort_dd_id):
            sorted_data = Select(self.driver.find_element(By.NAME, self._sort_dd_id))
        if text:
            sorted_data.select_by_visible_text(text)

    def get_table_data(self):
        table_id = self.driver.find_element(By.CLASS_NAME, self._data_tblData_class)
        table_header = self.driver.find_element(By.CLASS_NAME, self._data_tblHdr_class).find_elements(By.TAG_NAME,
                                                                                                      "div")
        table_data = self.driver.find_element(By.CLASS_NAME, self._data_tblData_class).find_elements(By.CLASS_NAME,
                                                                                                     "table-row")
        header = [item.text for item in table_header]
        if table_data:
            data = [[col.text for col in r.find_elements(By.TAG_NAME, "div")] for r in table_data]
        else:
            data = []
        return pd.DataFrame(columns=header, data=data)

    def get_page_header(self):
        if self.driver.find_element_by_id('app'):
            return self.driver.find_elements(By.XPATH, '//*[@id="app"]/h1')[0].text
