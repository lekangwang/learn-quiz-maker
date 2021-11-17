from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..helpers.parsers import parse_course_title
import os
from csv import DictReader
from time import sleep

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
    driver.maximize_window()
    driver.get("https://learn.uwaterloo.ca/")

    # Enter username automatically
    driver.find_element(By.ID, "userNameInput").click()
    driver.find_element(By.ID, "userNameInput").send_keys(username, Keys.ENTER)

    # Password and DUO must both be entered manually due to security reasons
    # Wait until user is on their LEARN homepage, quit after 2 minutes
    WebDriverWait(driver, 120).until(EC.url_matches("https://learn.uwaterloo.ca/d2l/home"))

    print("login_user: User logged in!")    

def navigate_to_course_quizzes(shadow_driver, driver):
    # Retrieve full course name from settings csv file
    settings = parse_login_settings()
    csv_course_title = settings["Course"]

    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

    sleep(3)

    viewable_courses = shadow_driver.find_elements("d2l-card")

    # print(f"Viewable courses: {viewable_courses}, length: {len(viewable_courses)}")

    for course in viewable_courses:
        long_course_title = shadow_driver.get_attribute(course, "text")
        parsed_course_title = parse_course_title(long_course_title)
        if parsed_course_title == csv_course_title:
            course.click()
            break

    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

    course_navlink_groups = shadow_driver.find_elements(".d2l-navigation-s-group-text")

    for link in course_navlink_groups:
        print(link.text)
        if link.text == "Submit":
            link.click()
            break
    sleep(2)

    quizzes_link = shadow_driver.find_element('d2l-menu-item-link[text=\"Quizzes\"]')
    
    quizzes_link.click()
    
    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

    print("Success!")


    # # Retrieve "Pinned" tab
    # pinned_tab = shadow_driver.find_element("d2l-tab-internal[text='Pinned']")
    # pinned_tab.click()

    # WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

    # # Retrieve the course card elements from "Pinned"
    # pinned_courses_container = shadow_driver.find_element(".course-card-grid")
    # pinned_courses = shadow_driver.get_child_elements(pinned_courses_container)
    # print(f"Number of children: {len(pinned_courses)}")

    # for (i, course) in enumerate(pinned_courses):
    #     print(f"Course {i}: {course}")
    #     print(f"Course {i} children: {shadow_driver.get_child_elements(course)}")
    
    # print("End")

    






