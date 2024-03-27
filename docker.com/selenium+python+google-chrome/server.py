from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


# instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

# download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads and put it in the
# current directory

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
