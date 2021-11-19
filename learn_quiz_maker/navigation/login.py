from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..helpers.parsers import parse_course_title
from ..helpers.util import click_element_of_elements, wait_until_page_fully_loaded
import os
from time import sleep
from ..helpers.parsers import parse_settings

# Is the path to the settings CSV file, please DO NOT TOUCH
MODULE_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

# Allows user to login automatically (DUO two-factor auth will still need to be done manually)
def login_user(driver):
    settings = parse_settings(MODULE_PATH, "/settings.csv")
    username = settings["Username"]

    # Initialize webdriver
    driver.maximize_window()
    driver.get("https://learn.uwaterloo.ca/")

    # Enter username automatically
    driver.find_element(By.ID, "userNameInput").click()
    driver.find_element(By.ID, "userNameInput").send_keys(username, Keys.ENTER)

    # Password and DUO must both be entered manually due to security reasons
    # Wait until user is on their LEARN homepage, quit after 2 minutes
    WebDriverWait(driver, 120).until(EC.url_matches("https://learn.uwaterloo.ca/d2l/home"))

    print("login_user: User logged in!")    

# Automatically navigates user to the "Quizzes" section of the course specified in settings.csv
# The target course must be visible at the top of the courses cards 
# (you can ensure this by pinning the course to the top)
def navigate_to_course_quizzes(shadow_driver, driver):
    settings = parse_settings(MODULE_PATH, "/settings.csv")
    csv_course_title = settings["Course"]

    wait_until_page_fully_loaded(driver, 10)

    # Wait for the courses cards widget to load in
    sleep(3)

    # Find all the courses visible on the dashboard currently
    viewable_courses = shadow_driver.find_elements("d2l-card")

    # print(f"Viewable courses: {viewable_courses}, length: {len(viewable_courses)}")

    # Find which course matches the one found in the csv file based on title and click it
    for course in viewable_courses:
        long_course_title = shadow_driver.get_attribute(course, "text")
        parsed_course_title = parse_course_title(long_course_title)
        if parsed_course_title == csv_course_title:
            course.click()
            break

    wait_until_page_fully_loaded(driver, 10)

    # Find all the navigation tab elements that contain groups of links
    course_navlink_groups = shadow_driver.find_elements(".d2l-navigation-s-group-text")
    for c in course_navlink_groups:
        print(c.text)
    click_element_of_elements(course_navlink_groups, "Submit")
    
    # Wait for sub links under "Submit" to load
    sleep(2)

    # Find the "Quizzes" sub link and click it 
    quizzes_link = shadow_driver.find_element('d2l-menu-item-link[text=\"Quizzes\"]')
    quizzes_link.click()
    
    wait_until_page_fully_loaded(driver, 10)

    # We are now at the "Quizzes" page of the course
    print("navigate_to_course_quizzes: Success!")



    






