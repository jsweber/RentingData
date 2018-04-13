#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'du'

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

url='https://www.liepin.com/zhaopin/'
chrome_option = Options()
chrome_option.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_option, executable_path='/home/du/apps/chromedriver')
browser.get(url)
time.sleep(3)
title = browser.find_elements_by_css_selector('title')
print(browser.page_source)
browser.quit()

