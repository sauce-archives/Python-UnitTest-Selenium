import os
import unittest
import sys
from selenium import webdriver
from sauceclient import SauceClient

username = os.environ.get("SAUCE_USERNAME")
access_key = os.environ.get("SAUCE_ACCESS_KEY")

class FirstSampleTest(unittest.TestCase):

    # setUp runs before each test case
    def setUp(self):
        desired_caps = {
            "name": 'Py-unittest',
            "platform": 'Windows 10',
            "browserName": 'firefox',
            "version": '47'
        }
        self.driver = webdriver.Remote(
           command_executor="http://{}:{}@ondemand.saucelabs.com:80/wd/hub".format(username, access_key),
           desired_capabilities= desired_caps)

    # verify google title
    def test_google(self):
        self.driver.get("http://www.google.com")
        assert ("Google" in self.driver.title), "Unable to load google page"

    # type 'Sauce Labs' into google search box and submit
    def test_google_search(self):
        self.driver.get("http://www.google.com")
        elem = self.driver.find_element_by_name("q")
        elem.send_keys("Sauce Labs")
        elem.submit()

    # tearDown runs after each test case
    def tearDown(self):
        self.driver.quit()
        sauce_client = SauceClient(username, access_key)
        status = (sys.exc_info() == (None, None, None))
        sauce_client.jobs.update_job(self.driver.session_id, passed=status)

