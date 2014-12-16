# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Ccola(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://ccola-dev.savoirfairelinux.net/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_ccola(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        for i in range(60):
            try:
                if "Audit Learning Network" == driver.find_element_by_css_selector("strong").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        driver.find_element_by_id("edit-name").click()
        driver.find_element_by_id("edit-name").clear()
        driver.find_element_by_id("edit-name").send_keys("sflmonitoring")
        driver.find_element_by_css_selector("#edit-pass-wrapper > label.compact-form-label").click()
        driver.find_element_by_id("edit-pass").click()
        driver.find_element_by_id("edit-pass").clear()
        driver.find_element_by_id("edit-pass").send_keys("AuKoo0ohneb2aeX4cu")
        driver.find_element_by_id("edit-submit").click()
        driver.find_element_by_css_selector("li.leaf.first > a").click()
        for i in range(60):
            try:
                if "Member for" == driver.find_element_by_css_selector("dt").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        driver.find_element_by_css_selector("li.leaf.last > a").click()
        try: self.assertEqual("Log in", driver.find_element_by_id("edit-submit").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
