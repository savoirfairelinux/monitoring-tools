# -*- coding: utf-8 -*-
from selenium import selenium
import unittest, time, re

class test(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://linuxfr.org/")
        self.selenium.start()
    
    def test_test(self):
        sel = self.selenium
        sel.open("/")
        self.assertEqual("Accueil - LinuxFr.org", sel.get_title())
        sel.click(u"css=a[title=\"Actualités, événements et autres nouveautés\"]")
        sel.wait_for_page_to_load("30000")
        self.assertEqual(u"Proposer une dépêche", sel.get_text("css=nav.toolbox > div.new_content > a"))
        sel.click("css=a[title=\"Plan du site, aide, flux Atom, etc.\"]")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Plan du site", sel.get_text("css=#contents > h1"))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
