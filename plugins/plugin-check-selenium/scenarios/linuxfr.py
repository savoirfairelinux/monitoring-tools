# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Linuxfr(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://linuxfr.org/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_linuxfr(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        self.assertEqual("Accueil - LinuxFr.org", driver.title)
        driver.find_element_by_css_selector(u"a[title=\"Actualités, événements et autres nouveautés\"]").click()
        self.assertEqual(u"Proposer une dépêche", driver.find_element_by_css_selector("nav.toolbox > div.new_content > a").text)
        driver.find_element_by_css_selector("a[title=\"Plan du site, aide, flux Atom, etc.\"]").click()
        self.assertEqual("Plan du site", driver.find_element_by_css_selector("#contents > h1").text)
    
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
