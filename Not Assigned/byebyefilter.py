from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time

firefox_options = Options()

service = Service()  # specify executable_path if needed

driver = webdriver.Firefox(service=service, options=firefox_options)
driver.get("https://www.example.com")