# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Savoirfairelinuxcom(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.savoirfairelinux.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_savoirfairelinuxcom(self):
        driver = self.driver
        driver.get(self.base_url + "/en/")
        for i in range(60):
            try:
                if "Contact Us" == driver.find_element_by_xpath("//a[contains(text(),'Contact Us')]").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        driver.find_element_by_css_selector("input[name=\"_77_keywords\"]").clear()
        driver.find_element_by_css_selector("input[name=\"_77_keywords\"]").send_keys("shinken")
        driver.find_element_by_css_selector("input[type=\"image\"]").click()
        for i in range(60):
            try:
                if "OSS117 - Supervision avec Shinken" == driver.find_element_by_css_selector("td.col-2").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        driver.find_element_by_xpath("//a[contains(text(),'Contact Us')]").click()
        for i in range(60):
            try:
                if u"Montréal Headquarters - Office / Training Center" == driver.find_element_by_css_selector("#portlet-wrapper-1_WAR_googlemapsportlet_INSTANCE_1NrV > div.portlet-head-l > div.portlet-head-r > span.portlet-title").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
    
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
