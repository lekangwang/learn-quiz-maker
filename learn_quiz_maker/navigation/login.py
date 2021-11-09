from typing import Dict
from ..helpers.driver import create_driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from csv import DictReader

# Parse CSV settings file to extract username, password, course
def parse_settings():
    with open("settings.csv") as s:
        settings = dict(DictReader(s))
        print(settings)


# Allows user to login automatically (DUO two-factor auth will still need to be done manually)
def login_user(username=None, password=None):
    # Initialize webdriver
    driver = create_driver()
    driver.get("https://learn.uwaterloo.ca/")

    # Enter username
    driver.find_element(By.ID, "userNameInput").click()
    driver.find_element(By.ID, "userNameInput").send_keys(username, Keys.ENTER)

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "passwordInput")))

    # Enter password
    driver.find_element(By.ID, "passwordInput").click()
    driver.find_element(By.ID, "passwordInput").send_keys(password, Keys.ENTER)

    WebDriverWait(driver, 120).until(EC.url_matches("https://learn.uwaterloo.ca/d2l/home"))

    print("Done")
