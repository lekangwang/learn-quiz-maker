from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from csv import DictReader

# Parse CSV login settings file to extract username, password, course
def parse_login_settings():
    csv_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + "/settings.csv"

    # print(csv_path)

    with open(csv_path) as s:
        settings = list(DictReader(s))[0]
        # print(settings)
        return settings

# Allows user to login automatically (DUO two-factor auth will still need to be done manually)
def login_user(driver):
    settings = parse_login_settings()
    username = settings["Username"]

    # # Initialize webdriver
    # driver = create_driver()
    driver.maximize_window()
    driver.get("https://learn.uwaterloo.ca/")

    # Enter username
    driver.find_element(By.ID, "userNameInput").click()
    driver.find_element(By.ID, "userNameInput").send_keys(username, Keys.ENTER)

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "passwordInput")))

    WebDriverWait(driver, 120).until(EC.url_matches("https://learn.uwaterloo.ca/d2l/home"))

    print("login_user: User logged in!")

def navigate_to_course_quizzes():
    parse_login_settings()
